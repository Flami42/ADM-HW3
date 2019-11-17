"""
Created on Sat Nov 16 10:41:51 2019

@author: flaminia
"""

import requests

# This function takes th i-th url and save the corresponding html page
def save_page(url,i):
    request= requests.get(url)
    name= "article_"+str(i)
    #soup= BeautifulSoup(request.text, "html.parser")
    with open (name, "w") as f: #writing mode, call the file tets as f
        f.write(request.text)