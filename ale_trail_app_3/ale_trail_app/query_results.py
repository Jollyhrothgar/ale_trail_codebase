## Python packages - you may have to pip install sqlalchemy, sqlalchemy_utils, and psycopg2.
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import matplotlib.pyplot as plt
from nltk.stem import PorterStemmer
ps = PorterStemmer()

def query_results(hop_range_min,hop_range_max,key_word_1,key_word_2):
    """
    given a range of hop-values, returns a dict of the form:
    dict[status_id]{beer_dictionary} where beer_dictionary populates an
    html table with suggested beers + images.

    the status is either 1, 2 or 3.

    1-> found a review with key_word_1 and key_word_2
    2-> found a review with key_word_1 or key_word_2
    3-> default, could not find any key-words requested.

    Status can be used to dynamically generate a message for the user 
    to perhaps rephrase their query.
    """
    dbname = 'beer_final'
    username = 'postgres'
    mypassword = 'simple'

    status = 1

    ## Here, we're using postgres, but sqlalchemy can connect to other things too.
    engine = create_engine('postgres://%s:%s@localhost/%s'%(username,mypassword,dbname))
    con = psycopg2.connect(database = dbname, user = username,host='/var/run/postgresql',password=mypassword)
    print "Connecting to",engine.url

    stem1 = ps.stem(key_word_1)
    stem2 = ps.stem(key_word_2)

    cur = con.cursor()
    beer_query_both = """
    SELECT 
        breweries.beer_name_key,
        breweries.brewery_name,
        breweries.style_name,
        breweries.beer_name,
        breweries.city,
        breweries.latittude,
        breweries.longitude
    FROM 
        breweries
    WHERE
        breweries.hop_mean > %s and breweries.hop_mean < %s
    AND
        (breweries.review_stems like %s AND breweries.review_stems like %s)
    ORDER BY
        breweries.avg_score desc
    limit 5;
    """
    cur.execute(beer_query_both,(hop_range_min,hop_range_max,'%'+stem1+'%','%'+stem2+'%'))
    results = []
    results = cur.fetchall()
    # Try a different query
    if len(results) != 5:
        status = 2
        print "using 'or' query"
        beer_query_or = """
        SELECT 
            breweries.beer_name_key,
            breweries.brewery_name,
            breweries.style_name,
            breweries.beer_name,
            breweries.city,
            breweries.latittude,
            breweries.longitude
        FROM 
            breweries
        WHERE
            breweries.hop_mean > %s and breweries.hop_mean < %s
        AND
            (breweries.review_stems like %s OR breweries.review_stems like %s)
        ORDER BY
            breweries.avg_score desc
        limit 5;
        """
        cur.execute(beer_query_or,(hop_range_min,hop_range_max,'%'+stem1+'%','%'+stem2+'%'))
        results = cur.fetchall()
            
        # Try a different query, guaranteed to work
        if len(results) != 5:
            status = 3
            print  "using default query"
            standard_query = """
            SELECT 
                breweries.beer_name_key,
                breweries.brewery_name,
                breweries.style_name,
                breweries.beer_name,
                breweries.city,
                breweries.latittude,
                breweries.longitude
            FROM 
                breweries
            WHERE
                breweries.hop_mean > %s and breweries.hop_mean < %s
            ORDER BY
                breweries.avg_score desc
            limit 5;
            """
            cur.execute(standard_query,(hop_range_min,hop_range_max))
            results = cur.fetchall()
    # results has been filled with something by now
    print len(results)

    # construct beer image url
    beer_list = []
    for result in results:
        results_dict = {}
        beer_dict = {}
        beer_dict['beer_key'] = str(result[0])
        beer_dict['brewery_name'] = str(result[1])
        beer_dict['beer_style'] = str(result[2])
        beer_dict['beer_name'] = str(result[3])
        beer_dict['city'] = str(result[4])
        beer_dict['loc'] = str(result[5])+", "+str(result[6])
        beer_dict['img'] =  "../static/img/beer/"+beer_dict['beer_key']+"_description.png"
        beer_list.append(beer_dict)
    results_dict['status'] = status
    results_dict['beer_list'] = beer_list
    cur.close()
    return results_dict
