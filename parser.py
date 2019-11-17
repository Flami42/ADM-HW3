"""
Created on Sat Nov 16 10:41:51 2019

@author: flaminia
"""
####   ***  The python file that contains the line of code needed to parse the entire collection of html pages and save those in tsv files.  ***


import parser_utils

# 1.3 Parse downloaded pages
for i in range(20000):
    fname= "article_"+str(i)
    parser_utils.save_data(i, fname)
    