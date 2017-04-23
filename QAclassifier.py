# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 12:38:31 2017

@author: Suganya
"""

from feature_extraction import feature_extraction
from SealsPreprocess import SealsPreprocess
import nltk
from nltk import load_parser
from nltk.sem import chat80
import string

def execute_query(query, yes_no_grammar, wh_grammar, database):
    query = query.translate(string.maketrans("",""), string.punctuation)
    query_list = [i for i in query.lower().split()]
    yes_no = set(["was","did", "is", "does", "were", "could", "do", "are", "have", "had", "should"])
    if(query_list[0] in yes_no):
        cp = load_parser(yes_no_grammar, trace=3)
    else:
        cp = load_parser(wh_grammar)#, trace=3)
    trees = list(cp.parse(query_list))
    answer = trees[0].label()['SEM']
    answer = [s for s in answer if s]
    q = ' '.join(answer)
    print(q)
    
    results = []
    rows = chat80.sql_query(database, q)
    for r in rows:
        results.append(r[0])
        print(r[0])
    
    if(len(results) == 0 and query_list[0] in yes_no):
        print "No"
    #trees[0].draw()   

process = SealsPreprocess() 
#process.xls_to_txt('QADatabase.xlsx','QADatabase.txt')
#print("Text file saved")           
#process.clean_text_files('QADatabase_cleaned.txt','QADatabase.txt')
#print("Cleaned Text file saved") 
analysis = feature_extraction("QADatabase_cleaned.txt",1)
training_set = nltk.classify.apply_features(analysis.extract_features, analysis.tweets)
print("Starting...")
classifier = nltk.NaiveBayesClassifier.train(training_set)

query = input('Enter a query within double quotes: ')
db = classifier.classify(analysis.extract_features(analysis.generate_input_tokens(1, process.cleanup(query)))) 
print db
    
#nltk.data.show_cfg('SealsGrammar/s4.fcfg')

if(db == "music\n"):
    execute_query(query, 'SealsGrammar/music_yes_no_grammar.fcfg', 'SealsGrammar/music_wh_grammar.fcfg', 'SealsDB/music.db')
elif(db == "WorldGeography\n"):
    execute_query(query, '', '', 'SealsDB/WorldGeography.db')
elif(db == "oscar-movie_imdb\n"):
    execute_query(query, '', '', 'SealsDB/oscar-movie_imdb.db')