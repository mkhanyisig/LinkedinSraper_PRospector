"""
Generate profile HTML profile cards
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common import exceptions
from bs4 import BeautifulSoup
import time
import json
import os



# Define Browser Options
print("Setting Up Driver")
chrome_options = Options()
chrome_options.add_argument("--headless")  # Hides the browser window

# Reference the local Chromedriver instance
chrome_path = '/usr/local/bin/chromedriver'

browser = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)

def get_profile(name):
    s="search('"+name+"');"

    f = open("search.js", "w")

    f.write(s)

    f.close()

    browser.get("file:///Users/colby/Desktop/Prospector/Linkedin%20Scraping/template.html")

    src = browser.page_source
    soup = BeautifulSoup(src, 'lxml')

    bd=soup.find('div',id="mainhtml")
    #bd.script.decompose()

    print("Body: \n",bd)

    html_string=str(bd)
    html_string=html_string.replace('\"','"')
    #ss=str('\')
    #html_string=html_string.replace(ss,'')
    html_string=html_string.replace('\n','')


    profile_map.update({name:html_string})


    #SCROLL_PAUSE_TIME=20

    # Wait to load page
    #time.sleep(SCROLL_PAUSE_TIME)
    print(name," done")

def export(pmap):
    f = open("profile_map.json", "w")

    f.write(json.dumps(pmap,indent=4))

    f.close()


def get_authors(export_path):
    #
    f = open(export_path, "r")
    data =[]
    if(os.stat(export_path).st_size == 0):
    	print("*** empty file")
    else:
    	data= json.loads(f.read())
    	#print("***  data : ",data)
    f.close()

    #
    for obj in data:
        author_names.append(obj["Name"])

def main():
    # get profiles list and create profile template divs

    profile_map={}
    author_names=[]

    # update author names list
    get_authors("profiles.json")

    for author in author_names:
        get_profile(author)

    print("************\n**********\n")
    print(profile_map[nm])

    export(profile_map);


    print("\n***\n***\n***\n",author_names,"\n***\n***\n***\n")
    print("total profiles: ",len(author_names))

    # close chrome tab
    browser.close()

if __name__ == "__main__":

    main()

    print("\n ********** Profiles iFrame HTML list generated **********")
    
    # close chrome tab
    browser.close()
