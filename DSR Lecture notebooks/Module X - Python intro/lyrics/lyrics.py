# Code modified from:
#https://www.scrapehero.com/how-to-scrape-job-listings-from-glassdoor-using-python-and-lxml/

#===============================================================================
#--- SETUP Config
#===============================================================================
from config.config import *
import unittest

#===============================================================================
#--- SETUP Logging
#===============================================================================
import logging.config
print(ABSOLUTE_LOGGING_PATH)
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

#===============================================================================
#--- SETUP Add parent module
#===============================================================================
# from os import sys, path
# # Add parent to path
# if __name__ == '__main__' and __package__ is None:
#     this_path = path.dirname(path.dirname(path.abspath(__file__)))
#     sys.path.append(this_path)
#     logging.debug("ADDED TO PATH: ".format(this_path))


#===============================================================================
#--- SETUP Standard modules
#===============================================================================
import requests
import re
#import os
#import sys
import unicodecsv as csv
#import argparse
#import json
#from exceptions import ValueError

#===============================================================================
#--- SETUP external modules
#===============================================================================
from lxml import html, etree
#from StringIO import StringIO
import io as io
import re
#io module and use io.StringIO or io.BytesIO for text and data respectively.
#print(etree)
#raise
#import lxml as lxml
#from lxml
#from lxml import html
#from xml import etree
#print(lxml.etree) 
#TODO: resolve etree import error!

#===============================================================================
#--- SETUP Custom modules
#===============================================================================
from ExergyUtilities.util_inspect import get_self

#===============================================================================
#--- Directories and files
#===============================================================================
#curr_dir = path.dirname(path.abspath(__file__))
#DIR_SAMPLE_IDF = path.abspath(curr_dir + "\..\.." + "\SampleIDFs")
#print(DIR_SAMPLE_IDF)

#===============================================================================
#--- MAIN CODE
#===============================================================================

MAIN_URL = r"https://www.azlyrics.com/j/jamestaylor.html"

def parse(keyword, place):
    logging.debug("Running on {} {}".format(keyword,place))

    headers = {    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, sdch, br',
                'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
                'referer': 'https://www.glassdoor.com/',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive'
    }

    location_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.01',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
        'referer': 'https://www.glassdoor.com/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
    }
    data = {"term": place,
            "maxLocationsToReturn": 10}

    location_url = "https://www.glassdoor.co.in/findPopularLocationAjax.htm?"

    
    # Getting location id for search location
    logging.debug("Fetching location details")
    
    location_response = requests.post(location_url, headers=location_headers, data=data).json()
    place_id = location_response[0]['locationId']
    logging.debug("place_id:{}".format(place_id))
    
    job_litsting_url = 'https://www.glassdoor.com/Job/jobs.htm'
    # Form data to get job results
    data = {
        'clickSource': 'searchBtn',
        'sc.keyword': keyword,
        'locT': 'C',
        'locId': place_id,
        'jobType': ''
    }

    job_listings = []
    
    if place_id:
        
        response = requests.post(job_litsting_url, headers=headers, data=data)
        # extracting data from
        # https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=true&clickSource=searchBtn&typedKeyword=andr&sc.keyword=android+developer&locT=C&locId=1146821&jobType=
        #print(response)
        #raise
        
        parser = html.fromstring(response.text)
        # Making absolute url 
        base_url = "https://www.glassdoor.com"
        parser.make_links_absolute(base_url)
        
        XPATH_ALL_JOB = '//li[@class="jl"]'
        XPATH_NAME = './/a/text()'
        XPATH_JOB_URL = './/a/@href'
        XPATH_LOC = './/span[@class="subtle loc"]/text()'
        XPATH_COMPANY = './/div[@class="flexbox empLoc"]/div/text()'
        XPATH_SALARY = './/span[@class="green small"]/text()'

        listings = parser.xpath(XPATH_ALL_JOB)
        for job in listings:
            raw_job_name = job.xpath(XPATH_NAME)
            raw_job_url = job.xpath(XPATH_JOB_URL)
            raw_lob_loc = job.xpath(XPATH_LOC)
            raw_company = job.xpath(XPATH_COMPANY)
            raw_salary = job.xpath(XPATH_SALARY)

            # Cleaning data
            job_name = ''.join(raw_job_name).encode("ascii","ignore") if raw_job_name else None
            job_location = ''.join(raw_lob_loc) if raw_lob_loc else None
            raw_state = re.findall(",\s?(.*)\s?", job_location)
            state = ''.join(raw_state).strip()
            raw_city = job_location.replace(state, '')
            city = raw_city.replace(',', '').strip()
            company = ''.join(raw_company).encode("ascii","ignore").strip()
            salary = ''.join(raw_salary).strip()
            job_url = raw_job_url[0] if raw_job_url else None

            jobs = {
                "Name": job_name,
                "Company": company,
                "State": state,
                "City": city,
                "Salary": salary,
                "Location": job_location,
                "Url": job_url
            }
            job_listings.append(jobs)

        return job_listings
    else:
        print("location id not available")

def get_response_TEST():
    
    logging.debug("Fetching location details")
    
    
    headers = {    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, sdch, br',
                'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
                'referer': 'https://www.glassdoor.com/',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive'
    }

    location_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.01',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'en-GB,en-US;q=0.8,en;q=0.6',
        'referer': 'https://www.glassdoor.com/',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive'
    }
    data = {"term": 'test',
            "maxLocationsToReturn": 10}

    try: 
        location_response = requests.post(location_url, headers=location_headers)
        print(location_response)
    except:
        pass


def parse_song_links_iter(file_name):
    logging.debug("NEW ATTEMPT in getting links".format())
    logging.debug("Opening {}".format(file_name))
    
    with open(file_name, 'r', encoding='utf-8') as f:
        parser = etree.HTMLParser()
        tree   = etree.parse(io.StringIO(f.read()), parser)
    logging.debug("Successfully loaded {} into tree {}".format(file_name,tree))
        
    root = tree.getroot()
    logging.debug("Root node: {}, type {}".format(file_name,root,type(root)))

    #for link in root.iterlinks():
    #    print(link)
    print(html.iterlinks(tree))
    #print(new)
    raise




def parse_song_links2(file_name):
    logging.debug("Opening {}".format(file_name))
    
    with open(file_name, 'r', encoding='utf-8') as f:
        parser = etree.HTMLParser()
        tree   = etree.parse(io.StringIO(f.read()), parser)
        
    logging.debug("Successfully loaded {} into tree {}".format(file_name,tree))
    
    # Get links
    urls = tree.xpath('//a')
    #raise
    logging.debug("Returning {} links".format(len(urls)))

    return urls


def parse_song_links(file_name):
    logging.debug("Opening {}".format(file_name))
    
    with open(file_name, 'r', encoding='utf-8') as f:
        parser = etree.HTMLParser()
        tree   = etree.parse(io.StringIO(f.read()), parser)
        
    logging.debug("Successfully loaded {} into tree {}".format(file_name,tree))
    
    # Get links
    urls = tree.xpath('//a/@href')
    #urls = tree.xpath('//a')
    #raise
    logging.debug("Returning {} links".format(len(urls)))
    
    return urls

def my_download(location_url):
    logging.debug("Downloading {}".format(location_url))
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    page = requests.get(location_url, headers=headers)
    
    fname = "downloaded.html"
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(page.text)
    
    logging.debug("Wrote {}".format(fname))
    return 0

if __name__ == "__main__":
    # Get HTML
    #dl = my_download(MAIN_URL)
    
    # Reload the HTML and parse for links
    path_html_file = r"downloaded.html"
    urls = parse_song_links2(path_html_file)
    
    # Filter the actual lyric links
    pattern = re.compile("^\.\./lyrics/")
    lyric_urls = list()
    for u in urls:
        try: 
            this_match = pattern.match(str(u.attrib['href']))
            print(html.tostring(u),"\t\t\t\t\t\t\t",this_match)
        except:
            this_path = False
            pass
        if this_match:
            lyric_urls.append(u)
     
    logging.debug("Filtered out {} lyric links (as etree nodes)".format(len(lyric_urls)))
    
    for elem in lyric_urls:
        print(html.tostring(elem))
        try: 
            this_link = elem.attrib['href']
        except:
            raise
        song_title = elem.text
        logging.debug("Song {} at {}".format(song_title,this_link))
    raise
    
    
    ##this_match = pattern.match(r"../lyrics/jamestaylor/ourtown.html")
    #if this_match:
    #    print("YES")
    #print(this_match)
    #print()
    
    
    #print(lyric_urls)

    #print(html.tostring(urls[0]))
    #print(urls[0].text_content())
    #for child in urls[0]:
    #    print(child)
    #raise
    #print(tostring(img) urls[0].tostring)
    
#     for url in urls:
#         #print(url)
#         pattern = re.compile("^\.\./lyrics/")
#         if pattern.match(url):
#             print("YES")

    
    #print(str(urls[0]))
    

    raise
    #print(lyric_urls[0],type(lyric_urls[0]))
    
    for song in lyric_urls:
        print(song)
        print(type(song))
        #for child in song:
        #    print(child)
        print(etree.iselement(song))
        raise
        text = song.child()
        print(text)
        raise
        print(song.find())
        for it in dir(song):
            print(it)
            
            
        print(etree.tostring(song, encoding='iso-8859-1'))
    raise
# 
