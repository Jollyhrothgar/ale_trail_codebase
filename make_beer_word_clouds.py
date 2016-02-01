from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2
import csv
import numpy as np
import operator
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
import nltk

from os import path
from PIL import Image
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

## For word clouds
from sklearn.feature_extraction.text import TfidfVectorizer

dbname = 'beer_final'
username = 'postgres'
mypassword = 'simple'

engine = create_engine('postgres://%s:%s@localhost/%s'%(username,mypassword,dbname))
con = psycopg2.connect(database = dbname, user = username,host='/var/run/postgresql',password=mypassword)
print "Connecting to",engine.url

beer_bins = {
    0:(0.0,0.4), 
    1:(0.4,0.6), 
    2:(0.6,1.0), 
}

review_words_per_bin = {
    0:[],
    1:[],
    2:[],
}

review_corpus_per_bin = {
    0:[],
    1:[],
    2:[],
}

beer_key_word_bags = {}

query = """
SELECT
    distinct beer_name_key,hop_mean
FROM
    breweries
"""

query_hop_mean = """
SELECT 
    breweries.hop_mean,reviews.review_text,reviews.beer_key
FROM 
    breweries,reviews 
WHERE 
    breweries.beer_name_key = reviews.beer_key 
AND 
    breweries.hop_mean > %s and breweries.hop_mean < %s;
"""

cur = con.cursor()

# Create structures for making word-clouds.
beer_key_hop_value = {}
for i in range(0,3):
    cur.execute(query_hop_mean,(beer_bins[i][0],beer_bins[i][1]))
    review_list = cur.fetchall()
    for review in review_list:
        try:
            words = review[1].split()
            beer_key = review[2]
            review_corpus_per_bin[i].append(words)
            beer_key_hop_value[beer_key] = review[0]
        except:
            continue
        for word in words:
            #print word
            review_words_per_bin[i].append(word)
            if beer_key not in beer_key_word_bags:
                beer_key_word_bags[beer_key] = []
                beer_key_word_bags[beer_key].append(word)
            else:
                beer_key_word_bags[beer_key].append(word)
                
                
    print "words reviwing bin",i,":",len(review_words_per_bin[i]),"reviews:",len(review_corpus_per_bin[i])

for key,val in beer_key_word_bags.iteritems():
    print key,len(val)

STOPWORDS.add("malt")
STOPWORDS.add("taste")
STOPWORDS.add("flavor")
STOPWORDS.add("carbonation")
STOPWORDS.add("had")
STOPWORDS.add("hop")
STOPWORDS.add("head")
STOPWORDS.add("good")
STOPWORDS.add("nice")
STOPWORDS.add("light")
STOPWORDS.add("dark")
STOPWORDS.add("hops")
STOPWORDS.add("white")

# Create global beer-clouds
for i in range(0,3):
    pint_mask = np.array(Image.open("/home/mjbeaumier/Programming/brewery_project/ale_trail_codebase/pint_spectrum/ale_mask_"+str(i)+".png"))
    out_file_name = "beer_hoppiness_"+str(i)+".png"
    wc = WordCloud(background_color="black", max_words=2000, mask=pint_mask,
                   stopwords=STOPWORDS, random_state=42)
    # generate word cloud
    wc.generate(' '.join(review_words_per_bin[i]))
    # store to file
    image_colors = ImageColorGenerator(pint_mask)
    
    # show
    plt.imshow(wc.recolor(color_func=image_colors))
    plt.axis("off")
    plt.figure()
    wc.to_file(path.join(out_file_name))

# Create wordclouds for single beers
for beer_key,word_bag in beer_key_word_bags.iteritems():
    if len(word_bag) == 0:
        continue
        
    hop_value = beer_key_hop_value[beer_key]
    pint_mask = None
    if hop_value > beer_bins[0][0] and hop_value < beer_bins[0][1]:
        pint_mask = np.array(Image.open("/home/mjbeaumier/Programming/brewery_project/ale_trail_codebase/pint_spectrum/ale_mask_0.png"))
    if hop_value > beer_bins[1][0] and hop_value < beer_bins[1][1]:
        pint_mask = np.array(Image.open("/home/mjbeaumier/Programming/brewery_project/ale_trail_codebase/pint_spectrum/ale_mask_1.png"))
    if hop_value > beer_bins[2][0] and hop_value < beer_bins[2][1]:
        pint_mask = np.array(Image.open("/home/mjbeaumier/Programming/brewery_project/ale_trail_codebase/pint_spectrum/ale_mask_2.png"))

    out_file_name = "beer_img/"+str(beer_key)+"_description.png"
    wc = WordCloud(background_color="black", max_words=2000,mask=pint_mask,
                  stopwords=STOPWORDS)
    wc.generate(' '.join(word_bag))
       
    image_colors = ImageColorGenerator(pint_mask)
    
    # show
    plt.imshow(wc.recolor(color_func=image_colors))
    plt.axis("off")
    plt.figure()
    wc.to_file(path.join(out_file_name))
