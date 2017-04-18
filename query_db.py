# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 17:16:26 2017

@author: Sugu
"""

#import nltk
from nltk import load_parser
from nltk.sem import chat80
import string

cp = load_parser('SealsGrammar/musicgrammar4.fcfg', trace=3)
#nltk.data.show_cfg('SealsGrammar/s4.fcfg')
query = 'What albums did Beyonce sing'

query = query.translate(string.maketrans("",""), string.punctuation)
query_list = [i for i in query.lower().split()]
trees = list(cp.parse(query_list))
answer = trees[0].label()['SEM']
answer = [s for s in answer if s]
q = ' '.join(answer)
print(q)

#
#rows = chat80.sql_query('SealsDB/music.db', q)
#for r in rows:
#    print r[0]