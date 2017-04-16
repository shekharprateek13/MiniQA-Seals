# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 12:33:13 2017

@author: Suganya
"""

import os
import nltk
from random import shuffle


class feature_extraction:
    def get_words_in_tweets(self, text):
        all_words = []
        for (words, sentiment) in text:
          all_words.extend(words)
        return all_words
    
    def get_word_features(self, wordlist):
        wordlist = nltk.FreqDist(wordlist)
        features_short= [word for word in wordlist]
        return features_short
        
    def extract_features(self, document):
        document_words = set(document)
        features = {}
        for word in self.word_features:
            features[word] = (word in document_words)
        return features
        
    def generate_ngrams(self, num, tweet):
        tweet_tokens = nltk.word_tokenize(tweet)
        ngram = []
        for i, word in enumerate(tweet_tokens):
            for n in range(1, num + 1):
                if i + n <= len(tweet_tokens):
                    ngram_list = [tweet_tokens[j] for j in xrange(i, i + n)]   
                    if(len(ngram_list) == num):
                        ngram.append(' '.join(ngram_list).lower())
        return ngram
        
    def generate_input_tokens(self, num, tweet):
        tweet_tokens = nltk.word_tokenize(tweet)
        ngram = []
        for i,q in enumerate(tweet_tokens):
            for n in range(1, num + 1):
                if i + n <= len(tweet_tokens):
                    ngram_list = [tweet_tokens[j] for j in xrange(i, i + n)]   
                    ngram.append(' '.join(ngram_list).lower())
        return ngram
        
    def read_file(self, filename,num_gram):
        rel_path = filename
        script_dir= os.path.dirname(os.path.abspath(__file__))
        abs_file_path = os.path.join(script_dir, rel_path)
        f = open ( abs_file_path )
        tweets=[]
   
        for line in f.readlines():
            cols = line.split("\t")
            if(num_gram==1):          
                words_filtered=[] 
                words_filtered =[e.lower() for e in cols[0].split() if len(e)>2] 
                tweets.append((words_filtered,cols[1]))
#            elif(num_gram==2): 
#               bigrams_list = self.generate_ngrams(2, cols[0])
#               if(len(bigrams_list) > 0):
#                   tweets.append((bigrams_list,cols[1]))
#            elif(num_gram==3):  
#               trigrams_list = self.generate_ngrams(3, cols[0])
#               if(len(trigrams_list) > 0):
#                   tweets.append((trigrams_list,cols[1]))
#            elif(num_gram==4):
#               quadgrams_list = self.generate_ngrams(4, cols[0])
#               if(len(quadgrams_list) > 0):
#                    tweets.append((quadgrams_list,cols[1]))
        f.close()
        shuffle(tweets)
        return tweets
        
    def __init__(self,filename,gram):
        self.tweets = self.read_file(filename,gram)
        self.word_features = self.get_word_features(self.get_words_in_tweets(self.tweets))   
