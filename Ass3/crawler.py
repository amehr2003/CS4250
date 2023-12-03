import re
import urllib
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import sys, traceback
import datetime
import pymongo
from bs4 import BeautifulSoup
import requests

seed = 'https://www.cpp.edu'
frontier_list = ['https://www.cpp.edu/sci/computer-science/']

def crawlPage(frontier):
    httpRq=requests.get(frontier)
    bs = BeautifulSoup(httpRq.text, 'html.parser')

    links = bs.find_all('a')
    count=0
    for link in links:
        innerLink=link.get("href")
        if str(innerLink).startswith("http") or str(innerLink).endswith("/sci/computer-science/"):
            frontier_list.append(innerLink)
            print(innerLink)

            if innerLink in frontier_list:
                print("Already visited.")
            else:
                if innerLink.startswith('/sci/computer-science/'):
                    string=seed+innerLink
                frontier_list.append(string)
            print(frontier_list)
            title=getPageTitle(innerLink)
            saveToDB(innerLink, title)
            if str(title).strip()=='Permanent Faculty':
                frontier_list.clear()
                print("target page found.")
                break
        count+=1
        print(count)
    return 0


def saveToDB(innerLink, title):
    db=connectDataBase()
    col = db.cppFaculties
    create_date=datetime.datetime.now()

    if innerLink.startswith("/sci/computer-science/"):
        string = seed + innerLink
    else:
        string=innerLink

    html=urlopen(string)
    bs= BeautifulSoup(html.read(), "html.parser")
    text=bs.find_all('html')

    doc={
        "url": string,
        "title": title,
        "html": str(text),
        "created": create_date
    }
    result = col.insert_one(doc)

def getPageTitle(innerLink):
    if innerLink.startswith('/sci/computer-science/'):
        urlString = seed + innerLink
    else:
        urlString=innerLink
    htmlPage=urlopen(urlString)
    bs=BeautifulSoup(htmlPage.read(), "html.parser")
    headerTag = bs.find('h1', {"class": "cpp-h1"})

    if headerTag:
        rtnstr=headerTag.get_text()
    else:
        rtnstr=''

    return rtnstr

def connectDataBase():
    try:
        client = pymongo.MongoClient(host="localhost", port=27017)
        db = client.ass3
        print("Database: ")
        print(db)
        return db
    except Exception as error:
        traceback.print_exc()
        print("Database not connected successfully")
        return 0

try:
    html = urllib.request.urlretrieve('https://www.cpp.edu/sci/computer-science/')
except HTTPError as e:
    print(e)
except URLError as e:
    print('The server could not be found!')
else:
    print('It Worked!')
    crawlPage(seed)
