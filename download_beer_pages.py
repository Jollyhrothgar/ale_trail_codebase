#! /usr/bin/env python

import os
import re 
import sys
import urllib2
import pandas
import csv
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from bs4 import BeautifulSoup

def scrape_brewery(url,dump_directory = '.'):
    '''
    takes a beer-advocate URL formatted like so: www.beeradvocate.com/pages/<numeric_id>/" 
    and dumps the page to a utf-8 text file. Uses <numeric_id> to uniquely identify the file.
    stores these html dumps in directory argument (defualt is '.') as: 
    '<dump_directory>/index_<numeric_id>.html'
    '''
    
    # Check if data has been downloaded
    re_check = re.search('profile/(\d+)',url)
    print re_check.group(1)
    if os.path.isdir(dump_directory+'/'+re_check.group(1)):
        print "data exists"
        return 1
    else:
        sleep(0.25)
    print "Scraping URL: ",url
    headers = { 'User-Agent' : 'Mozilla/5.0'  }
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html,'lxml')
    
    if re.search('No beer listings.',soup.text):
        print "No beer listings."
        return

    # Get an appropriate output name from the url
    m = re.search(r'http://www.beeradvocate.com/beer/profile/(\d+)/',url)
    page_id = 0
    if not m:
        print 'Bad match for url:',url,'\nBailing out!'
        return
    else:
        page_id = m.group(1)
    brewery_page = soup.encode('utf-8')
    matches = re.findall('/\d+/\d+',brewery_page)
    brew_dict = {}
    for match in matches:
        id_match = re.search('/(\d+)/(\d+)',match)
        if id_match.group(1) not in brew_dict:
            brew_dict[id_match.group(1)] = []
            brew_dict[id_match.group(1)].append(id_match.group(2))
        else:
            brew_dict[id_match.group(1)].append(id_match.group(2))
    # okay, now we have a list of beer pages from which to scrape reviews, but we only
    # want the 'real' beers, not suggestions from beer-advocate, so we keep the 'larger list' of beers.
    best_key = -1
    key_length = -1
    for key in brew_dict:
        if len(brew_dict[key]) > key_length:
            best_key = key
            key_length = len(brew_dict[key])
    
    # "http://www.beeradvocate.com/beer/profile/<brewery_id>/<beer_id>/view=beer&sort=topr&start=<page_num>"
    beer_url_dict = {}
    for beer_id in brew_dict[best_key]:
        beer_url = (
            "http://www.beeradvocate.com/beer/profile/"
            +str(best_key)
            +"/"
            +str(beer_id)
            )
        if beer_url not in beer_url_dict:
            beer_url_dict[beer_url] = brew_dict[best_key]
    # Create beer review list whether or not reviews exist. If they exist, we get the top 50
    beer_review_list = []
    
    for k,v in beer_url_dict.iteritems():
        sleep(0.25)
        beer_req = urllib2.Request(k, None, headers)
        beer_html = urllib2.urlopen(beer_req).read()
        beer_soup = BeautifulSoup(beer_html,'lxml')
        reviews_search = re.search('Reviews: (\d+)',beer_soup.text)
        if reviews_search:
            print "Reviews: ",reviews_search.group(1)

            ratings_counter = 0
            while ratings_counter < int(reviews_search.group(1))+25: 
                str_counter = str(ratings_counter)
                beer_review_list.append(k + '/view=beer&sort=top&start='+str_counter)
                ratings_counter += 25
    print dump_directory+'/'+str(best_key)
    try:
        os.mkdir(dump_directory+'/'+str(best_key))
    except OSError:
        print "data exists for brewery, skipping.\n"
        return
    # dump the file
    out_file = open(dump_directory+'/'+str(best_key)+'/brewery_'+str(page_id)+'.html','w')
    out_file.write(brewery_page)
    out_file.close()
    
    beer_counter = 0
    for beer_url in beer_review_list:
        print "Scraping beer: ",beer_url
        matches = re.search('(\d+)/(\d+)',beer_url)
        out_beer_file = open(dump_directory+'/'+str(best_key)+'/beer_'+matches.group(2)+"_"+str(beer_counter)+'.html','w')
        sleep(0.25)
        beer_req = urllib2.Request(beer_url,None,headers)
        beer_html = urllib2.urlopen(beer_req).read()
        beer_soup = BeautifulSoup(beer_html,'lxml')
        out_beer_file.write(beer_soup.encode('utf-8'))
        out_beer_file.close()
        beer_counter += 1
    print "Done scraping",best_key,"!"
    return

def load_url_list(filename):
    '''
    takes the url list in filename, loads into an array, and then returns the array of URLS
    '''
    in_file = open(filename,'rU')
    brewery_list = in_file.read().splitlines()
    print 'Loaded',len(brewery_list),"breweries."
    return brewery_list

def main():
    urls = load_url_list('./lists/brewery_urls.txt')
    master_list = []
    for url in urls:
        scrape_brewery(url,'./rescrape_data')
    print "Finished scraping!"

if __name__ == '__main__':
    main()
