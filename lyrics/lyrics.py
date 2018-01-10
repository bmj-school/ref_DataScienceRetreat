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



def parse_song_links(file_name):
    """Extract all <a> tags. Return as a list of element nodes. 
    """
    
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
#TODO: asdfasdfasdf

def my_download(location_url):
    """Given a url, get the web page. Write the file as text. 
    No return value. 
    """
    
    logging.debug("Downloading {}".format(location_url))
    
    # Mimic a browser
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    
    # Get the html page
    page = requests.get(location_url, headers=headers)
    
    # Write to disk
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(page.text)
    
    logging.debug("Wrote {}".format(fname))

if __name__ == "__main__":
    
    # Get HTML
    this_url = r"https://www.azlyrics.com/j/jamestaylor.html"
    fname = "downloaded.html"
    #dl = my_download(this_url,fname)
    
    # Reload the HTML and parse for links
    path_html_file = r"downloaded.html"
    urls = parse_song_links(path_html_file)
    
    # Filter the actual lyric links, discard others
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
    
    # Display results
    for elem in lyric_urls:
        print(html.tostring(elem))
        try: 
            this_link = elem.attrib['href']
            #FIXME: The link is broken
        except:
            raise
        song_title = elem.text
        logging.debug("Song {} at {}".format(song_title,this_link))
    
    #TODO: Save each file into a band directory 
    
        