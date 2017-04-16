# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 12:19:50 2017

@author: Suganya
"""

import os
import re
import xlrd
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class SealsPreprocess:
    def xls_to_txt(self, filename,output_file):
            x =  xlrd.open_workbook(filename)
            x1 = x.sheet_by_index(0)        
            
            f = open(output_file, 'wb')
            for rownum in xrange(0,x1.nrows):
                f.write(u'\t'.join([re.sub(r'\s+', r' ', i) if isinstance(i, basestring) else str(float(i)) for i in x1.row_values(rownum, 0, 2)]).encode('utf-8').strip()+ '\n')
            f.close()
            
    def cleanup(self, data):
            cleantext = data.replace(",","")        #remove commas
            cleaner = re.compile('<.*?>')           #remove tags
            cleantext= re.sub(cleaner,'', cleantext)        
            ascii = set(string.printable) 
            cleantext=filter(lambda x: x in ascii , cleantext)  
            cleantext= re.sub(r'https?:\/\/.*[\r\n]*', '', cleantext)   
            cleantext = cleantext.translate(string.maketrans("",""), string.punctuation)
            lemmatizer = WordNetLemmatizer()
            cleantextlist = [lemmatizer.lemmatize(i) for i in cleantext.lower().split()]
            cleantext = ' '.join(cleantextlist)
            stop = set(stopwords.words('english')) 
            cleantextlist = [i for i in cleantext.lower().split() if i not in stop]      #remove stopwords except few exceptions  
            cleantext = ' '.join(cleantextlist)
            return cleantext
    
    def clean_text_files(self,write_filename,read_filename):
        romney_file = open(write_filename, 'w')
        rel_path = read_filename
        script_dir= os.path.dirname(os.path.abspath(__file__))
        abs_file_path = os.path.join(script_dir, rel_path)
        f = open ( abs_file_path )
        for line in f.readlines():
            cols = line.split("\t")
            cols[0] = self.cleanup(cols[0]) 
            romney_file.write(cols[0])
            romney_file.write("\t")
            romney_file.write(cols[1])
        romney_file.close()
        f.close()