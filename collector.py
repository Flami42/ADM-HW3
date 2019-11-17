"""
Created on Sat Nov 16 10:41:51 2019

@author: flaminia
"""


####    ***  The python file that contains the line of code needed to collect your data from the html page (from which you get the urls) and Wikipedia.  *** \
import requests
from bs4 import BeautifulSoup
import collector_utils
import time
import random


# Since we are a group of 2 members, we downloaded movies from movie1 and movie2

# 1.1. Get the list of movies


url1= "https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies1.html"
request1 = requests.get(url1)
soup1= BeautifulSoup(request1.text, "html.parser") #so i navigate through the document

url2= "https://raw.githubusercontent.com/CriMenghini/ADM/master/2019/Homework_3/data/movies2.html"
request2 = requests.get(url2)
soup2= BeautifulSoup(request2.text, "html.parser") #so i navigate through the document

linklist=[]

### In the for loops we took all the urls in the page movie1/ movie2 and store them in a list (linklist)

for link in soup1.find_all('a'):
    linklist.append(link.get('href'))
    
 
for link in soup2.find_all('a'):
    linklist.append(link.get('href'))   
    
    
# 1.2. Crawl Wikipedia

### In for loop we used the function save_page to save the html code of every link in linklist in a file "moviei" (where i is the i-th link we are looking at)

for i in range(len(linklist)):   
    collector_utils.save_page(linklist[i], i)
    time.sleep(random.randint(1,5+1))
    
