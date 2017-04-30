# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 21:05:03 2017

@author: Sugu
"""

from feature_extraction import feature_extraction
from SealsPreprocess import SealsPreprocess
import nltk
import re
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
import urllib2


class QAclassifierSolr:
    def execute_query(self, query, questions_csv_file, db, yes_no_type):
        df = pd.read_csv(questions_csv_file)
        questionsDF = df['Questions']
        answersDF = df['AnswerType']
        
        df['AnswerType'] = df['AnswerType'].astype('category')
        answersDFCodes = df['AnswerType'].cat.codes
#        print answersDFCodes.value_counts()
#        print answersDF.value_counts()
        
        questions_list = [];
        for row in questionsDF.iteritems():
            tempQuestion = row[1];
            cleanedQuestion = self.cleanText(tempQuestion);
            questions_list.append(cleanedQuestion);


#        print questions_list
        # Create feature vectors
        vectorizer = TfidfVectorizer(min_df=0.00125,
                                     max_df = 1.0,
                                     sublinear_tf=True,
                                     use_idf=True,
                                     stop_words=u'english',
                                     analyzer='word',
                                     ngram_range=(1,3),lowercase=True)
        
        totalVectors = vectorizer.fit_transform(questions_list);
#        print totalVectors.shape
#        
#        print totalVectors.shape
        
        svmLinearKernelClassifier = svm.LinearSVC();
        svmLinearKernelClassifier.fit(totalVectors, answersDFCodes)
#        testQuestion = "What is the name of Avatar's director?"
        cleanedTestQuestion = self.cleanText(query)
        print cleanedTestQuestion
#        print self.removeStopWords(cleanedTestQuestion)
        
        cleanedQuestionList = [];
        cleanedQuestionList.append(cleanedTestQuestion);
        print cleanedQuestionList;
            
        testVector = vectorizer.transform(cleanedQuestionList);
#        print testVector.shape;
        
        predictedLabel = svmLinearKernelClassifier.predict(testVector)
        
        print str(predictedLabel[0])
        columnToLabelMappingDict = dict();
        if(db == "movies"):
            columnToLabelMappingDict["0"] = "actor_name_space"
            columnToLabelMappingDict["1"] = "director_name_space"
            columnToLabelMappingDict["2"] = "movie_name_space"
            columnToLabelMappingDict["3"] = "oscar_name_space"
#        elif(db == "WorldGeography\n"):
#            print ""
        elif(db == "music\n"):
            print ""        
#        print columnToLabelMappingDict
        print columnToLabelMappingDict[str(predictedLabel[0])]
        queryURL = self.createSolrQuery(query,columnToLabelMappingDict[str(predictedLabel[0])])
        print queryURL
        connection = urllib2.urlopen(queryURL)
        response = eval(connection.read())
#        print type(response);
        if((response["response"])["numFound"] == 0 and yes_no_type):
            answer = "No"
        elif((response["response"])["numFound"] != 0 and yes_no_type):
            answer = "Yes"
        elif((response["response"])["numFound"] != 0 and yes_no_type == False):
            solrDoc = (response["response"])["docs"][0]
            answer = solrDoc[columnToLabelMappingDict[str(predictedLabel[0])]][0]
        else:
            answer = "No results found"                                    
        print answer
        return answer
        
    def cleanText(self, inputText):
        tempText = inputText;
        tempText = re.sub('<[^<]+?>', ' ', tempText);
        tempText = re.sub(r'&amp[;]?', r' ', tempText);
        tempText = re.sub(r'\'s', ' ', tempText);
        tempText = re.sub(r'[\w\.-]+@[\w\.-]+', ' ', tempText);
        tempText = re.sub(r'[<>!#\[\]@/$:.,;%\()*?-]+', r' ', tempText);
        tempText = re.sub(r'\s+', r' ', tempText);
        words_filtered =[word.lower() for word in tempText.split()]
        #cleanWordsList = [word for word in words_filtered if word not in stopwords_set]      #remove stopwords except few exceptions  
        cleanfeature = ' '.join(words_filtered)
        return cleanfeature
    
    def removeStopWords(self, inputText):
        stopwords_set = set(stopwords.words('english'));
        tempText = inputText;
        words_tokens =[word.lower() for word in tempText.split()]
        cleanWordsList = [word for word in words_tokens if word not in stopwords_set]   
        cleanedText = ' '.join(cleanWordsList)
        return cleanedText
        
    def createSolrQuery(self, testQuestion,predictedClassLabel):
        baseURL = "http://localhost:8080/solr/movies/select?";
        cleanedTestQuestion = self.cleanText(testQuestion)
        tempQueryTerms = self.removeStopWords(cleanedTestQuestion);
        print tempQueryTerms
        q = re.sub(' ','+',tempQueryTerms);
        wt = "python";
        defType="edismax";
        tempQF = "movie_name_space+actor_name_space+oscar_name_space+director_name_space+oscar_type+oscar_year+winner_pob_space";
        qf = re.sub(predictedClassLabel,predictedClassLabel,tempQF);
        stopwords="true";
        lowercaseOperators = "true";
        mm="100%25"
        solrQuery = baseURL+"q="+q+"&wt="+wt+"&defType="+defType+"&qf="+qf+"&stopwords="+stopwords+"&lowercaseOperators="+lowercaseOperators+"&mm="+mm;
        if predictedClassLabel == "oscar_name_space":
            filterQuery = "category:oscar";
            solrQuery = solrQuery + "&fq="+filterQuery;
        return solrQuery;
     

process = SealsPreprocess() 
solrClassifier = QAclassifierSolr()
#process.xls_to_txt('QADatabase.xlsx','QADatabase.txt')
#print("Text file saved")           
#process.clean_text_files('QADatabase_cleaned.txt','QADatabase.txt')
#print("Cleaned Text file saved") 
analysis = feature_extraction("QADatabase_cleaned.txt",1)
training_set = nltk.classify.apply_features(analysis.extract_features, analysis.tweets)
print("Starting...")
classifier = nltk.NaiveBayesClassifier.train(training_set)

query = "Did a French actor win the oscar in 2012??"#input('Enter a query within double quotes: ')
db = classifier.classify(analysis.extract_features(analysis.generate_input_tokens(1, process.cleanup(query)))) 
print db

yes_no = set(["was","did", "is", "does", "were", "could", "do", "are", "have", "had", "should"])
yes_no_type = False
if(query.split(' ', 1)[0].lower() in yes_no):
    yes_no_type = True
    
if(db == "music\n"):
    solrClassifier.execute_query(query, 'music_questions.csv', "music", yes_no_type)
elif(db == "WorldGeography\n"):
    solrClassifier.execute_query(query, 'geography_questions.csv', "WorldGeography", yes_no_type)
elif(db == "oscar-movie_imdb\n"):
    solrClassifier.execute_query(query, 'movies_questions.csv', "movies", yes_no_type)
    
    



    
    


