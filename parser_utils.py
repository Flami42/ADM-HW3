"""
Created on Sat Nov 16 10:41:51 2019

@author: flaminia
"""

####  ** A python file that gathers the function you used in parser.py  **

from bs4 import BeautifulSoup
import csv
import re
import utils

#This function is used to clean all the information
def clean(ReviewText):
    ReviewText = ReviewText.replace("\n", "")
    ReviewText = ReviewText.replace('[1]', '')
    ReviewText = ReviewText.replace('[2]', '') 
    ReviewText = ReviewText.replace('[3]', '') 
    ReviewText = ReviewText.replace('[4]', '')
    ReviewText = ReviewText.replace('[5]', '') 
    ReviewText = ReviewText.replace('[6]', '') 
    ReviewText= ReviewText.replace('(film)', '')
    ReviewText= ReviewText.replace(' - Wikipedia', '')

    ReviewText= ReviewText.encode('ascii', 'ignore').decode('utf-8') #this is for the release_date
    
    return ReviewText




#this function separate the names of actors, directors... (because when there are multiple names, the surname of the first is attached to the name of the second one and so on... )
def separate_names(stringa):
    names= re.findall('[A-Z][^A-Z]*', stringa)
    for i in range(len(names)):
        names[i]= names[i].strip()
    names= ' '.join(names)
    return names

# This function extract the release date, it' a bit confused in the infobox table, so this take only the date inside the "( )", if there is no "()", means that the date is in good place, and doesn't require anything.
def extract_date(data):
    if "(" in data:
        inizio= data.find('(')
        fine= data.find(')')
        data= data[inizio+1:fine]
        data= data.split('-')
        data=(' ').join(data)
    return data



#This function take as input the name of the file (movie-i) open its tsv that we saved before and explore it in order to get all the info required
def save_data(j, fname):
    #At first we inizialize all the info as NA, so if the page does't exist, we save only the name, and the rest of infos are NA (in this way we don't skip any file, and it's all ordered)
    movie_name='NA'
    intro="NA"
    plot='NA'
    writer='NA'
    starring='NA'
    director='NA'
    music='NA'
    producer='NA'
    release_date="NA"
    runtime='NA'
    country='NA'
    language='NA'
    budget='NA'
    
    
    # we open it the html file
    html_file = open(fname, 'r') 
    source_code = html_file.read()
    soup_movie = BeautifulSoup(source_code, 'html.parser')
    
    #we get the name of the movie
    movie_name= soup_movie.title.string
    movie_name= clean(movie_name)
    
    #We select 1st and 2nd paragraph, (They should be most of the times) respectively intro and plot of the film
    if soup_movie.select('p'):
        paragraph= soup_movie.select('p')
        if ('refer to' in paragraph[0].get_text()) or ('has been adapted to film twice' in paragraph[0].get_text()) or ('may relate to' in paragraph[0].get_text()): #as we said in line 56, we see there is no page associated but still we want to save its tsv file (now is all "NA" exept the movie_name)
            newfname= "article_"+str(j)+".tsv"
            with open(newfname, 'wt') as out_file:
                tsv_writer = csv.writer(out_file, delimiter='\t')
                tsv_writer.writerow([movie_name, intro, plot, director,producer, writer,starring, music, release_date, runtime, country, language, budget])
                #and terminate the function
                return
        #else if we have something to parse....
        
        elif paragraph[0].get_text():
            intro=paragraph[0].get_text()
            intro= clean(intro)
        if len(paragraph)==1:
            plot="NA"
            
        elif 'This section is empty' in paragraph[1].get_text():
            plot="NA"
        else:
            plot=paragraph[1].get_text()
            plot= clean(plot)
    
    #Scanning the infobox table
    table = soup_movie.find_all('table', class_="infobox vevent")
    if table:
        table= table[0]
        for i in range(len(table.find_all('tr'))): #We iterate on the table rows (i)
            header= table.find_all("tr")[i].find("th")
            data= table.find_all("tr")[i].find("td")
            # If there is no data abaible a a given row i we skip that row to the next one
            if not data or not header: #if there is nothing in the a specific table row, we skip its parsing and move to the next row
                continue
                
            #if the header is one of our interested information we store its data 
            if header.text== "Directed by":
                if data.text != "See below":
                    director= separate_names(data.text)
                    director= clean(director)
                    
            elif header.text== 'Produced by':
                if data.text != "See below":
                    producer= separate_names(data.text)
                    producer= clean(producer)
                                      
            elif header.text== "Written by":
                if data.text != "See below":
                    writer= separate_names(data.text)
                    writer=clean(writer)

            elif header.text== "Starring":
                if data.text != "See below":
                    starring= separate_names(data.text)
                    starring=clean(starring)
            
            elif header.text== "Music by":
                if data.text != "See below":
                    music= separate_names(data.text)
                    music=clean(music)
                    
            elif header.text== "Release date":
                if data.text != "See below":
                    if data.select('ul'): #often the release date is in a unordered list, so we clean it and extract only the part we are interested in
                        ulist=data.select('ul')[0]
                        release_date= clean(ulist.text)
                        release_date= extract_date(release_date)
                        
                    else:
                        release_date= data.text
                        
            elif header.text== "Running time":
                if data.text != "See below":
                    runtime=clean(data.text)
            
            elif header.text== "Country":
                if data.text != "See below":
                    country=clean(data.text)
            
            elif header.text== "Language":
                if data.text != "See below":
                    language=separate_names(data.text)
                    language=clean(language)
                    
            elif header.text== "Budget":
                if data.text != "See below":
                    budget=clean(data.text)
            
    #SAVING ALL INFOS IN A TSV FILE 
    
    newfname= "article_"+str(j)+".tsv"
    with open(newfname, 'wt') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow([movie_name, intro, plot, director,producer, writer,starring,
                             music, release_date, runtime, country, language, budget])