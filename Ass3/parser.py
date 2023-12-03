from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import pymongo
import sys, traceback
import datetime

def saveToDB(db, pName, pTitle, pOffice, pPhone, pEmail, pWeb):
    try:
        col = db.cppFaculty
        if pName != '':
            doc = {
                "name": pName,
                "title": pTitle,
                "office": pOffice,
                "phone": pPhone,
                "email": pEmail,
                "web": pWeb
            }
            result = col.insert_one(doc)
        return True
    except Exception as error:
        print("database error")
        return False

def cleansing_list(input):
    # elements to remove
    rm = ['Title:', 'Title', 'Office:', 'Office', 'Phone:', 'Phone', 'Email:', 'Email', 'Web:', 'Web', ':', ':']
    for x in range(0, len(rm)):
        input.remove(rm[x])
    return input

def getTargetPage(db):
    try:
        col = db.cppPages
        pipeline = [
            {'$match': {'title': 'Permanent Faculty'}}
        ]

        docs = col.aggregate(pipeline)
        for x in docs:
            html_source = x['html']
            print(html_source)
        return html_source
    except Exception as error:
        print("database error")
        return None

def connectDataBase():
    try:
        client = pymongo.MongoClient(host="localhost", port=27017)
        db = client.ass3
        return db
    except Exception as error:
        traceback.print_exc()
        print("Database not connected successfully")
        return None

seed = 'https://www.cpp.edu'
db = connectDataBase()

try:
    html_page = getTargetPage(db)
    print(html_page)
except HTTPError as e:
    print(e)
else:
    bs = BeautifulSoup(html_page, "html.parser")
    allProfs = bs.find_all('div', {"class": "clearfix"})
    for prof in allProfs:
        pName=pTitle=pOffice=pPhone=pEmail=pWeb=''
        profName=prof.find_all('h2')
        for name in profName:
            pName=name.get_text().strip()
        ptag = prof.find_all('p')
        for p in ptag:
            info_list = p.get_text(strip=True, separator='\n').splitlines()
            clean_list = cleansing_list(info_list)
            pTitle = clean_list[0].replace(':', '').strip()
            pOffice = clean_list[1].replace(':', '').strip()
            pPhone = clean_list[2].replace(':', '').strip()
            pEmail = clean_list[3].replace(':', '').strip()
            pWeb = seed + clean_list[4].replace(':', '').strip()
        print(pName, pTitle, pOffice, pPhone, pEmail, pWeb)
        db_result = saveToDB(db, pName, pTitle, pOffice, pPhone, pEmail, pWeb)
        print(db_result)
