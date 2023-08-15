# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 20:52:34 2023

@author: royasplund
"""

#EMAIL SCRAPER, TAKES URL AS ARGUMENT, RETURNS A LIST OF ALL EMAIL ADDRESS FOUND ON PAGE
#ALSO TAKES ALL LINKS FOUND ON PAGE AND CHECKS THEM FOR EMAIL ADDRESSES AS WELL
#REMOVES DUPLICATE EMAILS

import re
import argparse
import requests
import httplib2
from bs4 import BeautifulSoup, SoupStrainer

#pip install requests
#pip install bs4
#pip install httplib2

parser = argparse.ArgumentParser()
parser.add_argument("url", metavar="url", type=str, help="URL to scan for email addresses")
args = parser.parse_args()



emails = []
url_lst = []
flat_email = []
url_str = args.url


        
def page_Data(url):
    page = requests.get(url)

    try:
        soup = BeautifulSoup(page.content, 'html.parser')
        data = soup.get_text()

    except:
        pass
        
    return str(data)



def recursive_url_Search(url):
    http = httplib2.Http()
    status, response = http.request(url)
    
    for link in BeautifulSoup(response, features='html.parser', parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            url_lst.append(link['href'])
            

def flatten_List(l):
    for sublist in l:
        for item in sublist:
            flat_email.append(item)
            
            
def rem_Duplicates(x):
  return list(dict.fromkeys(x))
            



recursive_url_Search(url_str)

for i in url_lst:
    if url_str in i:
        #data = page_Data(i)
        pattern = re.findall('\S+@\S+', page_Data(i))
        emails.append(pattern)
        
flatten_List(emails)
emails = rem_Duplicates(flat_email)

print(emails)
