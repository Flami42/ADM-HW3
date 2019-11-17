#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 17:00:39 2019

@author: flaminia
"""
import pandas as pd
import json
import utils

# I open both file inverted_index and vocabulary (that we created before) and get the respective informations from ther, without recompute the inverted index and vocabulary every time you use the Search Engine 
with open('inverted_index.json') as json_file:
    data = json.load(json_file)
    df_inverted_index=pd.DataFrame([data])
# I store the file in a dataframe    
df_inverted_index= df_inverted_index.T

with open('vocabulary.json') as json_file:
    data = json.load(json_file)
    vocab=pd.DataFrame([data])
# I store the file in a dataframe from which extract the vocabulary as a dictonary
vocab= vocab.T
pd.DataFrame.reset_index(vocab, inplace= True)
vocab.rename( columns = {'index': 'term', 0:'term_id'}, inplace = True)
dic_vocab= vocab.to_dict()
vocabulary= dic_vocab['term']
vocabulary = {y:x for x,y in vocabulary.items()}  #switch values with the key

#We need the linklist 
linklist= utils.get_linklist()
print("Enter parameter: 1/2/3")
parameter=int(input())
#result: is the dataframe of the movies related to the query 
result = utils.search_engine(parameter, linklist,vocabulary, df_inverted_index)
print("Files found: ")
print(result)
