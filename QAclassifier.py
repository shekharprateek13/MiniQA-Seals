# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 12:38:31 2017

@author: Suganya
"""

from feature_extraction import feature_extraction
from SealsPreprocess import SealsPreprocess
import nltk
#import pickle

   
process = SealsPreprocess() 
process.xls_to_txt('QADatabase.xlsx','QADatabase.txt')
print("Text file saved")           
process.clean_text_files('QADatabase_cleaned.txt','QADatabase.txt')
print("Cleaned Text file saved") 
analysis = feature_extraction("QADatabase_cleaned.txt",1)
training_set = nltk.classify.apply_features(analysis.extract_features, analysis.tweets)
print("Starting...")
classifier = nltk.NaiveBayesClassifier.train(training_set)
#f = open('QA_classifier.pickle', 'wb')
#pickle.dump(classifier,f)
#f.close()

question = 'which movie did Richard Linklater direct?'
print classifier.classify(analysis.extract_features(analysis.generate_input_tokens(1, process.cleanup(question)))) 
