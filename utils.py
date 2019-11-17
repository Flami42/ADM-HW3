#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 17:03:07 2019

@author: flaminia
"""
import requests
from bs4 import BeautifulSoup
import csv
import index_utils
import pandas as pd

# This function extract and return the number of the film we are are looking at
def extract_i_from_movie_name(string):
    start= string.find('_')
    end= string.find('.')
    i= int(string[start+1:end])
    return i

# This function extract and return the number of the film we are are looking at
def extract_i_from_html_name(string):
    start= string.find('_')
    i= int(string[start+1:])
    return i

#This function returns name and film of the film we want. This function is usefull when I wanto to create the dataframe of the film connected to the query
def get_info(i):
    fname='article_'+str(i)+'.tsv'
    with open(fname, 'r') as out_file:
        reader_tsv = csv.reader(out_file, delimiter='\t')
        lista=list(reader_tsv)
    return lista[0][0],lista[0][1]

# This function retun the list of all wikipedia links. This function is usefull when I wanto to create the dataframe of the film connected to the query
def get_linklist():
    url1= "https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies1.html"
    request1 = requests.get(url1)
    soup1= BeautifulSoup(request1.text, "html.parser") #so i navigate through the document
    
    url2='https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies2.html'
    request2 = requests.get(url2)
    soup2= BeautifulSoup(request2.text, "html.parser")
    
    linklist=[]
    for link in soup1.find_all('a'):
        linklist.append(link.get('href'))
    
    for link in soup2.find_all('a'):
        linklist.append(link.get('href'))
    return linklist

# This function is the core of the search engine. When called, it ask the user what film he is looking for, parse the query and return the dataframe of the movies in whose informations appear all the words in the query.
def search_engine(parameter,linklist, vocabulary, df_inverted_index):
    query=list((input().split(' ')))
    
    films=[]
    for i in range(len(query)):
        word=index_utils.remove_unnecessary(query[i]) #Parsing the query. every word is reduced to its root, so I can look for it in the vocabulary
        if word in vocabulary.keys(): #If in the vocabukary, I take its term_id and append to the list "films" the set of movies connected to that word.
            term_id=vocabulary[word]
            films.append(set(df_inverted_index[0][term_id]))
        else:
            print('word "' +query[i]+ '" not found in database')
            continue
    
    # Since i want only the movies connected to ALL words in the query, I take the insersection of the elements of the list "films" (Whose elements are themselves sets of films)
    intersec={} 
    intersec = films[0].intersection(*films[:1])
    intersec= list(intersec)
    
    
    # I make a list of the indicies of the movies we are looking for.
    indx=[]
    for i in range(len(intersec)):
        indx.append(extract_i_from_movie_name(intersec[i]))
    # and sort it
    indx.sort()
    
    #these lists will become the colums of my datafame (each element is, respectevly, the name, the intro, and the url of the i-th movie )
    film_names=[]
    film_intros=[]
    links=[]
    
    for i in indx: #Here I fill the (futere)columns ( aka, the lists) of ONLY the values I want 
        name_i, intro_i = get_info(i)
        film_names.append(name_i)
        film_intros.append(intro_i)
        links.append(linklist[i])
    
    #I make a dict of these infos
    results={'names': list(film_names), 
             'intro': list(film_intros),
             'url':list(links)}
    # And turn it into the dataframe I return
    
    result= pd.DataFrame(results, columns = ['names', 'intro', 'url'])
    result.rename( columns = {'names': 'Movie Name', 'intro':'Movie Intro', 'url': 'URL'}, inplace = True)
    return result
