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
from docutils.nodes import line
print(ABSOLUTE_LOGGING_PATH)
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

#===============================================================================
#--- SETUP Standard modules
#===============================================================================
import requests
import re
import os
#import sys
import unicodecsv as csv
#import argparse
#import json
#from exceptions import ValueError
import io as io
import re
from html.parser import HTMLParser
import pickle
import itertools


#===============================================================================
#--- SETUP external modules
#===============================================================================
from nltk.tokenize import word_tokenize
import nltk
from lxml import html
from lxml import etree
import lxml
from sklearn.feature_extraction.text import TfidfVectorizer

#===============================================================================
#--- SETUP Custom modules
#===============================================================================
from ExergyUtilities.util_inspect import get_self

#===============================================================================
#--- MAIN CODE
#===============================================================================


def extract_lyrics_lxml(file_name):
    logging.debug("Processing {}".format(file_name))
    
    with open(file_name, 'r', encoding='utf-8') as f:
        parser = etree.HTMLParser()
        tree   = etree.parse(io.StringIO(f.read()), parser)
    
    print(tree)
#     urls = tree.xpath('<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->
# ')
# 
#     raise





class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def clean_lyrics(lyric_list):
    #print("BEFORE")
    #for line in lyric_list:
    #    print(line)

    logging.debug("Cleaning {} lines".format(len(lyric_list)))

    #print("\n\nAFTER")
    clean_line_list = list()
    for line in lyric_list:
        clean_line = strip_tags(line)
        clean_line_list.append(clean_line)
        
    logging.debug("Done cleaning into {} lines".format(len(clean_line_list)))
        
    return clean_line_list

def extract_lyrics_basic(file_name):
    logging.debug("Processing {}".format(file_name))
    
    
    pattern_start = re.compile(r"<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->")
    pattern_empty = re.compile('^\s*$')
    pattern_end =   re.compile(r"<!-- MxM banner -->")
    
    flg_lyrics = False
    lyric_text = list()
    with open(file_name, 'r', encoding='utf-8') as f:
        for i,line in enumerate(f):
            line = line.rstrip()
            match_start = pattern_start.match(line)
            match_empty = pattern_empty.match(line)
            match_end   = pattern_end.match(line)
            
            if match_empty:
                continue
                
            if match_start:
                flg_lyrics = True
            if match_end:
                flg_lyrics = False
                                
            #print(i, len(line), repr(line[0:50]), "  ", end='')

            if flg_lyrics:
                lyric_text.append(line)

    logging.debug("Found {} lines between markers".format(len(lyric_text)))

    return(lyric_text)

def analyze(lyrics):
    logging.debug("Analyzing {} lines of lyrics".format(len(lyrics)))

    default_stopwords = set(nltk.corpus.stopwords.words('english'))

    all_stopwords = default_stopwords 
    
    lyrics = " ".join(lyrics)
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    
    
    #tokenizer.tokenize('Eighty-seven miles to go, yet.  Onward!')
    #tokenized = [word_tokenize(i) for i in lyrics]
    words = tokenizer.tokenize(lyrics)
    #for word in words:
    #    print(word)
    len_words = len(words)
    logging.debug("Tokenized to {} words".format(len(words)))

    # Remove single-character tokens (mostly punctuation)
    words = [word for word in words if len(word) > 1]
    
    # Remove numbers
    words = [word for word in words if not word.isnumeric()]
    
    # Lowercase all words (default_stopwords are lowercase too)
    words = [word.lower() for word in words]
    
    # Stemming words seems to make matters worse, disabled
    stemmer = nltk.stem.snowball.SnowballStemmer('english')
    words = [stemmer.stem(word) for word in words]
    
    # Remove stopwords
    words = [word for word in words if word not in all_stopwords]

    logging.debug("Removed {} words (stop words, numbers, single characters, etc,.), {} words remain".format(len_words - len(words), len(words)))
    
    # Calculate frequency distribution
    fdist = nltk.FreqDist(words)
    
    # Output top 50 words
    #for word, frequency in fdist.most_common(5):
    #    print(u'{};{}'.format(word, frequency))
    
    return(words)

def get_words_by_band(directory):
    #cumulative_words = list()
    words_song = dict()
    for filename in os.listdir(directory):
        
        if filename.endswith(".html"):
            song_name = filename.split('.')[0]
            
            raw_lyrics = extract_lyrics_basic(directory+filename)
            cleaned_lyrics = clean_lyrics(raw_lyrics)
            words_song[song_name] = analyze(cleaned_lyrics)
            #cumulative_words = cumulative_words+words
        else:
            logging.debug("Skipping {}".format(filename))
        
        logging.debug("Finished with {}".format(filename))
        
    logging.debug("Finished processing {} songs".format(len(words_song)))
    
    #logging.debug("Found {} words by this band".format(len(cumulative_words)))
    
    return words_song
    
    #fdist = nltk.FreqDist(cumulative_words)
    
    # Output top 50 words
    #for word, frequency in fdist.most_common(20):
    #    print(u'{};{}'.format(word, frequency))
    #return cumulative_words

def load_all_bands():
    """Process each band directory to retrieve lyrics. Save the results to pickle. 
    """
    
    root_dir = r"C:\Users\jon\git\ref_DataScienceRetreat\lyrcis\songs"
    
    main_words_dict = dict()
    
    this_dir = root_dir+r"\\beatles\\"
    main_words_dict['beatles'] = get_words_by_band(this_dir)
    
    this_dir = root_dir+r"\\direstraits\\"
    main_words_dict['words_dire'] = get_words_by_band(this_dir)
    
    this_dir = root_dir+r"\\eminem\\"
    main_words_dict['eminem'] = get_words_by_band(this_dir)

    this_dir = root_dir+r"\\madonna\\"
    main_words_dict['madonna'] = get_words_by_band(this_dir)
    
    out_file = "all_lyrics.pickle"
    pickle_out = open(out_file,"wb")
    pickle.dump(main_words_dict, pickle_out, protocol=pickle.HIGHEST_PROTOCOL)
    pickle_out.close()
      
    logging.debug("Wrote to pickle {}".format(out_file))

def read_all_bands(in_file):
    pickle_in = open(in_file,"rb")
    loaded_dict = pickle.load(pickle_in)
    
    for band in loaded_dict:
        print("Band: {} with {} songs".format(band, len(loaded_dict[band])))
        
    return loaded_dict

def print_freqs(words_songs,size):
    
    all_words = [words_songs[song] for song in words_songs]
    all_words = itertools.chain(*all_words)
    all_words = list(all_words)
    #print(all_words)
    fdist = nltk.FreqDist(all_words)
    
    # Output top 50 words
    for word, frequency in fdist.most_common(size):
        print(u'{};{}'.format(word, frequency))

def this_method(band_songs):
    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    tfs = tfidf.fit_transform(token_dict.values())

if __name__ == "__main__":

    #load_all_bands()
    in_file = "all_lyrics.pickle"

    band_words = read_all_bands(in_file)
    
    band_freqs = dict()
    for band in band_words:
        print("***")
        print("Frequency for {}".format(band))
        these_words = band_words[band]
        print_freqs(these_words,10)

    this_method(band_words['beatles'])
        