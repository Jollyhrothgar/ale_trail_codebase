#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import pandas as pd
import csv
import numpy as np
import operator

def create_postgres_db():
    dbname = 'beer_final'
    username = 'postgres'
    mypassword = 'simple'
    
    ## Here, we're using postgres, but sqlalchemy can connect to other things too.
    engine = create_engine('postgres://%s:%s@localhost/%s'%(username,mypassword,dbname))
    print "Connecting to",engine.url
    
    if not database_exists(engine.url):
        create_database(engine.url)
    print "Does database exist?",(database_exists(engine.url))
    
    # load a database from CSV
    brewery_data = pd.DataFrame.from_csv('clean_data_csv/merged_final_beers.csv')
    
    ## insert data into database from Python (proof of concept - this won't be useful for big data, of course)
    ## df is any pandas dataframe 
    brewery_data.to_sql('breweries', engine, if_exists='replace')

    #dbname = 'beer_review_db'
    # load a database from CSV
    beer_data = pd.DataFrame.from_csv('clean_data_csv/beer_review_information_rescrape.csv')
    #engine_2 = create_engine('postgres://%s:%s@localhost/%s'%(username,mypassword,dbname))
    #print "connecting to",engine.url
    
    #if not database_exists(engine_2.url):
    #    create_database(engine_2.url)
        
    #print "Does database exist?",(database_exists(engine_2.url))
    beer_data.to_sql('reviews',engine,if_exists='replace')
    print "database",dbname,"has been created"
    return

def main():
    print 'creating database!'
    create_postgres_db()
    print 'done!'
    return

if __name__=="__main__":
    main()

