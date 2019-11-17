#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 10:41:51 2019

@author: flaminia
"""


import json #(for the vocabulary)
import index_utils
# I create a copy of the i-th article, and make it parsable. From this copy I will extract all the words of the vocabulary, and create the inverted index
for i in range(20000):
    fname= "article_"+str(i)+'.tsv'
    index_utils.file_to_raw(i,fname)
   
#we create the vocabukary   
vocabulary= {}
n=0
for i in range(20000):
    fname= "raw_"+str(i)+".tsv"
    n, vocabulary= index_utils.build_vocabulary(n, fname, vocabulary)

#and save it in a file json
with open('vocabulary.json', 'w') as outfile:
    json.dump(vocabulary, outfile)

# We create the inverted_index 

inverted_index={}

for parola in vocabulary:
    inverted_index[vocabulary[parola]]=[]   
    
for i in range(20000): #Scanning all 20000 file
    fname= "raw_"+str(i)+".tsv"
    index_utils.build_inverted_index(vocabulary, fname, inverted_index)
    
 # And save it in a file json   
with open('inverted_index.json', 'w') as outfile:
    json.dump(inverted_index, outfile)