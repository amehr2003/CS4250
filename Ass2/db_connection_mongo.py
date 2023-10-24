#-------------------------------------------------------------------------
# AUTHOR: your name
# FILENAME: title of the source file
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #2
# TIME SPENT: how long it took you to complete the assignment
#-----------------------------------------------------------*/
import random
import pymongo

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
from pymongo import MongoClient
import re

from pymongo.collection import Collection
from collections import Counter

def connectDataBase():
    DB_NAME = "corpus"
    DB_HOST = "localhost"
    DB_PORT = 27017
    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        return db
    except:
        print("Database not connected successfully")

def createDocument(col, docId, docText, docTitle, docDate, docCat):

    # create a dictionary to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.
    col = connectDataBase().get_collection("documents")
    terms= {}
    Text = re.sub(r'[?!.]', '', docText)
    Text2 = Text.lower().split()
    for term in Text2:
        if term not in terms:
            terms[term]=1
        else:
            terms[term]+=1

    # create a list of dictionaries to include term objects.
    listOfTerms = []
    for term, count in terms.items():
        term_elements = {"term":term, "count":count, "numChars":len(term)}
        listOfTerms.append(term_elements)

    catId=0
    if docCat == "Sports":
        catId=1
    elif docCat== "Seasons":
        catId=2
    elif docCat!= "Sports" or docCat!="Seasons":
        catId=random.randint(3,10)

    #Producing a final document as a dictionary including all the required document fields
    document = {
        "_id": docId,
        "text": docText,
        "title": docTitle,
        "num_chars": len(docText),
        "date": docDate,
        "category": {
            "categoryID": catId,
            "name": docCat},
        "terms": listOfTerms
    }

    # Insert the document
    col.insert_one(document)

def deleteDocument(col, docId):
    col.delete({"_id": docId})

def updateDocument(col, docId, docText, docTitle, docDate, docCat):

    # Delete the document
    deleteDocument(col, docId)

    # Create the document with the same id
    createDocument(col, docId, docText, docTitle, docDate, docCat)

def getIndex(col):
    client = MongoClient("localhost", 27017)  # Adjust the connection parameters as needed
    db = client["corpus"]
    collection: Collection = db["documents"]
#Query the database to return the documents where each term occurs with their corresponding count. Output example:
#{'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}

    pipeline = [
        {
            "$project": {
                "title": 1,  # Include the "title" field
                "terms": {
                    "$split": ["$text", " "]  # Split the text into an array of terms
                }
            }
        },
        {
            "$unwind": "$terms"  # Unwind the terms array
        },
        {
            "$group": {
                "_id": {
                    "term": "$terms",
                    "title": "$title"  # Group by both term and title
                },
                "count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "title": "$_id.title",
                "term": "$_id.term",
                "count": 1
            }
        }
    ]

    # Execute the aggregation
    result = list(collection.aggregate(pipeline))

    # Create a dictionary to store the results
    term_count_dict = {}
    for item in result:
        title = item["title"]
        term = item["term"]
        count = item["count"]
        if title not in term_count_dict:
            term_count_dict[title] = {}
        term_count_dict[title][term] = count

    # Print the result
    for title, term_counts in term_count_dict.items():
        print(f"Title: {title}")
        print(term_counts)