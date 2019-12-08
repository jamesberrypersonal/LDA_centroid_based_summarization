# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 22:27:46 2019

@ author: Hair Albeiro Parra Barrera 

This script is a wrapper of the Gensim's LDA algorithm implemented as a class  
for encapsulation and practicality purposes. 

""" 

### 1. Imports ### 

import re 
import os
import sys
import time
import argparse  
import warnings 
import pickle  # used to save the model 
import pandas as pd

from operator import itemgetter
from preprocessor import nltk_preprocessor 
from preprocessor import spacy_preprocessor

from gensim import corpora 
from gensim.models.ldamodel import LdaModel  

from tqdm import tqdm
from langdetect import detect


### 2. Warnings ### 

## Ignore warnings for this script ## 
def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()
    
    
### 3. Command line arguments setting ### 
    
#parser = argparse.ArgumentParser(description='Parses an input text into LDA format')
#
#
#parser.add_argument("cipher_folder", help="Input cipher folder path realive to the script")
#parser.add_argument("-laplace", help="Apply Laplace smoothing", 
#                    action="store_true")
#parser.add_argument("-lm", help="Improved plaintext modelling", 
#                    action="store_true")
#
#args = parser.parse_args()

    
### 4. Class implementation ### 
    
class LDA_parser(): 
    
    def __init__(self, corpus='', 
                 language='english', 
                 preprocessor_type = "spacy", 
                 lemmatize = False, 
                 stem = False, 
                 num_topics=10, 
                 passes=100): 
        """ 
        Parses the input text into a suitable format, then performs all LDA extraction tasks. 
        It expects the input corpus to be a list of texts. If input is a long string, it will attempt 
        create documents by splitting by 
        @ params: 
            @ corpus: Input corpus in str or ['str','str','str', ... ] format, where each entry
                      is a document of type str. Alternatively, a str format input (not recommended).
            @ preprocessor_type: Use nltk-based or spaCy-base preprocessor 
            @ lemmatize: use lemmatization in the preprocessing 
            @ stem: use stemming in the preprocessing  
            @ num_topics: maximum number of topics in the LDA algorithm 
            @ passes: number of training epochs in the LDA 
        """
        
        print("Initializing model...\n")
        if preprocessor_type == "nltk": 
            print("NLTK preprocessor selected.")
            self.preprocessor = nltk_preprocessor(language=language)
        if preprocessor_type == "spacy": 
            print("spaCy preprocessor selected.")
            self.preprocessor = spacy_preprocessor(language=language)
            
        self.language = language # input language 
        self.raw_corpus = "" # simply stores the input if in str type 
        self.clean_corpus = [] # [doc, doc, ..., doc] = [[sent, sent, ...], ... ,[sent, sent, ...]]
        self.dictionary = None # holds a corpora.Dictionary representation of corpus 
        self.doc2bow_corpus = None # contains doc2bow vector representations of each document in the corpus
        self.lda_model = None # LDA model trained on the input corpus 
        self.topic_mixtures = [] # contains str representations of mixtures of words with their probabilities  
        self.topics = {} # Contains a dictionary of topics with words and respective mix probabilities once "extract topics" is called.
        self.topic_words = {} # As above, but only contains the respective words of the topic
        

        if isinstance(corpus,str): 
            print("***WARNING***\nRaw input (str) received. Text will be sentence-tokenized and parsed accordingly.")
            print("Make sure this is intended. \n")
            self.raw_corpus = str(corpus) 
            self.clean_corpus = self.preprocessor.preprocess_str_corpus(corpus,
                                                                        stem=stem, 
                                                                        lemmatize=lemmatize)
        elif corpus == '': 
            print("***WARNING***\nNull Corpus") 
        # assume input corpus is in the right format  
        else: 
            self.fit(corpus, language=language, num_topics=num_topics, passes=passes) 
    
            
    
    def fit(self, corpus, language = 'english', min_len=2, num_topics=10, passes = 100):  
        """ 
        Assumes input corpus is in the right format. 
        @args: 
            @ corpus = input corpus  
            @ language = input language  
            @ num_topics = number of topics to choose in the algorithm 
            @ passes = number of epochs of the LDA 
            @ min_len = minimum length of words to consider when preprocessing words
        """
        
        print("Fitting LDA topic modelling...")
        self.raw_corpus = corpus # input corpus as is 
        self.language = language # in case initial language changed 
        print("Preprocessing corpus...")
        self.clean_corpus = self.preprocessor.preprocess_texts(self.raw_corpus, min_len=2) # preprocess text list  
        print("Creating corpora dictionary...")
        self.dictionary = corpora.Dictionary(self.clean_corpus) # create corpora.Dictionary mapping 
        print("Translating doc2bow corpus...")
        self.doc2bow_corpus = [self.dictionary.doc2bow(text) for text in self.clean_corpus] # doc2bow corpus representation 
        print("Running LDA...")
        self.lda_model =  LdaModel(self.doc2bow_corpus, num_topics = num_topics , id2word=self.dictionary, passes=passes) 
        self.topic_mixtures = self.lda_model.print_topics(num_words=10) # string representation of topics mixtures   
        print("\nDone.")
     
        
        
    def print_topics(self, words_per_topic=5): 
        """
        Displays the topics in string format
        """ 
        topics = self.lda_model.print_topics(num_words=words_per_topic) 
        for topic in topics: 
            print(topic) 
        
        
    def extract_topics(self, max_words_per_topic = 50, threshold = 0.005): 
        """
        Returns all topics as a dictionary of tuples, where the key is the topic 
        number, and the value is a list of tuples of words_per_topic many words with 
        probability at least as high as threshold, where the second value is the density 
        for the topic. 
        @params: 
            @ max_words_per_topic: Maximum topic mixture component words to consider. 
            @ threshold: select words whose density is at least this value
        """
        topics = {} # to store the topics 
        num_topics = len(self.topic_mixtures) # we have this many number of topics 
        
        # assign the topics mixtures  
        for i in range(num_topics): 
            topics[i] = [tup for tup in self.lda_model.show_topic(i,topn=max_words_per_topic) if tup[1] >= threshold]  # extract mosst probable words for topic i  
            
        self.topics = topics # update attribute  
        
        return topics 
    
    def extract_topic_words(self, max_words_per_topic = 50, threshold = 0.005): 
        """
        Returns all topics as a dictionary of tuples, where the key is the topic 
        number, and the value is a list of words_per_topic many words with 
        probability at least as high as threshold. 
        """
        topics = {} # to store the topics 
        num_topics = len(self.topic_mixtures) # we have this many number of topics 
        
        # assign the topics mixtures  
        for i in range(num_topics): 
            topics[i] = [tup[0] for tup in self.lda_model.show_topic(i,topn=max_words_per_topic) if tup[1] >= threshold]  # extract mosst probable words for topic i  
            
        self.topic_words= topics # update attribute  
        
        return topics 
    
    def parse_new(self, new_text, verbose=True): 
        """
        Parses a new text by obtaining the most likely topics for the new input, 
        as well as the respective words. This function should be used only after 
        the LDA parser has been fitted. 
        @params: 
            @ new_text: new input text 
            @ verbose: display information
        @returns: 
            @ max_topic: most likely topic for the document 
            @ doc_max_topic_words: words associated with the most likely topic 
            @ doc_topics: all topics related to the document 
            @ doc_topic_words: all words from all topics associated with the document 
        """
        if len(self.topic_words) < 1: 
            self.extract_topic_words() 
            
        new_text_clean = self.preprocessor.preprocess_sentence(new_text)  # preprocess input text
        new_doc_bow = self.dictionary.doc2bow(new_text_clean)  # convert to doc2bow 
        doc_topics = self.lda_model.get_document_topics(new_doc_bow) # obtain topics for input document 
        max_topic = max(doc_topics, key=itemgetter(1)) # most likely topics for the document 
        topic_idx = [tup[0] for tup in doc_topics] # topic indices 
        doc_topic_words = [word for idx in topic_idx for word in self.topic_words[idx] ] # extract all words from every topic 
        doc_max_topic_words = [word for  word in self.topic_words[max_topic[0]] ] # extract max density topic 
        
        if verbose: 
            print("*** Most likely topic: ***\n", max_topic) 
            print("*** Words for most likely topic: ***\n", doc_max_topic_words) 
            print("*** All topics: ***\n", doc_topics) 
            print("*** All topics words: ***\n", doc_topic_words) 
            
        return max_topic, doc_max_topic_words, doc_topics, doc_topic_words
            
        
    
    def save_model(self, name="LDA_model"):
        """ 
        Saves the LDA model, doc2bow_corpus and dictionary.
        These parameters can be used to instantiate a gensim 
        model, so there is no load in this class. 
        """   
        dictionary_name = name + "_dictionary.gensim"
        corpus_name = name + "_doc2bow_corpus.pkl"
        model_name = name + ".gensim"
        
        pickle.dump(self.doc2bow_corpus, open(corpus_name,'wb'))  # save the doc2bow_corpus 
        self.dictionary.save(dictionary_name) # save corpus dictionary mapping
        self.lda_model.save(model_name)  # save the full model 
        
        
# *********************************************************************************
        
#        
## TESTS # 
#        
#PATH = "topic_modelling_dataset.xlsx"
#
## example df 
#df = pd.read_excel(PATH) # load into a data-frame 
#print(df.head()) 
#print(df.columns)
#
#text_list = list(map(str, list(df['RESULTATS_2018'])))
#
### Fitting the text list to the parser ###  
#
#parser = LDA_parser(text_list, 
#                    language='french', 
#                    preprocessor_type='spacy', 
#                    min_len = 2, 
#                    num_topics = 10, 
#                    passes = 100) 
#
#
#parser.print_topics(words_per_topic = 10) 
#topic_mixtures = parser.extract_topics(max_words_per_topic=50, threshold=0.005)
#print(topic_mixtures)
#
## extract topics as a fictionary 
#topics = parser.extract_topic_words(max_words_per_topic=50, threshold=0.005)
#print(topics)
#
#
#test_text = """C'est très difficile de faire des avances à moins qu'on commence 
#                à facilitier des activités pour des enfants et les familles. Une 
#                activité de plus peut faire la différence dans des projets sociaux. 
#                On a donc besoin de la collaboration des organismes pour obtenir 
#                des meilleurs résultats. """ 
#
## parse a new text using the model 
#max_topic, doc_max_topic_words, doc_topics, doc_topic_words = parser.parse_new(test_text)
        
# *********************************************************************************


