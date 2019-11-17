### **** a python file that contains the functions you used for creating indexes. ****

import csv
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import json #(for the vocabulary)
import utils


#takes a string in input,tokenize it, remove punctuations, stop-words,reduce all to the root of that word and return a list of those words
def remove_unnecessary(stringa):
    stop_word= set(stopwords.words('english')) #this is the set of english stop-words
    punteggiatura= string.punctuation #this is the set of punctuations

    ps = PorterStemmer()
    cleaned=[]
    
    words_tokens= word_tokenize(stringa) #1. tokenize the string in input
    
    for word in words_tokens:
        if word not in punteggiatura: #2. remove the punctuations
            Word= word.lower()
            
            cleaned.append(Word)  #3. put all lowercase
            
    cleaned= [w for w in cleaned if not w in stop_word] #4. remove stop_words
    
    for i in range(len(cleaned)):  # 5.stemming every word
        cleaned[i]=ps.stem(cleaned[i])
    # 6. Clean again every word from "'" or "."
    for i in range(len(cleaned)):
        if cleaned[i].startswith("'") or cleaned[i].startswith("."):
            cleaned[i]=cleaned[i][1:]
        
        elif cleaned[i].endswith("'") or cleaned[i].endswith("."):
            cleaned[i]=cleaned[i][:-1]
    
    #return a string cleaned from all the unnecessary      
    cleaned= " ".join(cleaned)
    return cleaned 


# Since the release date is always store is in a very difficult way to reach it, I use this function to ectraxt it when I have a case like these:
    # "Dicember 17 (1978-12-17)"  or similar cases
def extract_date(data):
    if "(" in data:
        inizio= data.find('(')
        fine= data.find(')')
        data= data[inizio+1:fine]
        data= data.split('-')
        data=(' ').join(data)
    return data


# This function apply remove_unnecessary the i-th movie  in order to have the file prepared 
# to be red and parsed to build bot vocabulary and reverted index
def file_to_raw(j, fname):
    mylist=[]
    with open(fname, 'r') as out_file:
        tsv_reader = csv.reader(out_file, delimiter='\t')
        mylist=list(tsv_reader) 
    for i in range(3):
        if mylist[0][i]== 'NA' :
            continue
        else:
            mylist[0][i]= remove_unnecessary(mylist[0][i])
    
    
    newfname='raw_'+str(j)+'.tsv'       
    with open(newfname, 'wt') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerows(mylist)




# This function takes in input n (to keep counting in the right order the term_ids), the file_name (so it can be opened and analysed ), and the vocabulary (to keep updating the vocabulary)
    # It builds the vocabulary, open a file, and for each word in each field (name, intro, plot), if a word is not in vocabulary, it is added to it and so on 
def build_vocabulary(n, fname, vocabulary):
    with open(fname, 'r') as out_file:
        reader_tsv = csv.reader(out_file, delimiter='\t')
        lista=list(reader_tsv)
        # lista is list in with every elemets is a row of the file (element 0= row 0 (the only row there is in it)), element 0 of row 0 (lista[0][0]) is the movie name, element 1 of row 0 (lista[0][1]) is the movie intro, and so on
        for i in range(len(lista[0][:3])):
            parte=list(lista[0][i].split(' '))
            for el in parte:
                if (el!= "NA") and (el not in vocabulary) and (el != ''):
                    vocabulary[el]=n
                    n+=1
            else: 
                continue
    return n, vocabulary

# This function builds the inverted index, takes in input the vocabulary (so we can ckech if a word is in the vocab or not), the filenmae we open and parse, the inverted inxed (to keep updating it)
    
def build_inverted_index(vocabulary, fname, inverted_index):
    lista_di_parole=[]
    with open(fname, 'r') as out_file:
        reader_tsv = csv.reader(out_file, delimiter='\t')
        lista_di_parole=list(reader_tsv) 
    # Fow each word in each field (name, intro, plot), if the word is in the vocab, and the moviename in not already in the list of movies connected to that word, we add the moviename to that list, else we keep analysing 
    for i in range(len(lista_di_parole[0][:3])):
        parte=list(lista_di_parole[0][i].split(' '))
        for parola in parte: 
            if (parola in vocabulary.keys()) and (fname not in inverted_index[vocabulary[parola]]):
                inverted_index[vocabulary[parola]].append(fname) #vocabulary[parola] is the unique term_id of that term
            else: 
                continue


