#-------------------------------------------------------------------------
# AUTHOR: your name
# FILENAME: title of the source file
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #1
# TIME SPENT: how long it took you to complete the assignment
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

# importing some Python libraries
import psycopg2
from psycopg2.extras import RealDictCursor
import re

def connectDataBase():
    # Create a database connection object using psycopg2
    DB_name = "corpus"
    DB_user = "postgres"
    DB_pass = "123"
    DB_host = "localhost"
    DB_port = "5432"
    try:
        connection = psycopg2.connect(database=DB_name, user=DB_user, password=DB_pass, host=DB_host, port=DB_port, cursor_factory=RealDictCursor)
        return connection
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def createCategory(cur, catId, catName):
    sql = "Insert into Category (id, name) Values (%s, %s)"
    recset = [catId, catName]
    cur.execute(sql, recset)

def createDocument(cur, docId, docText, docTitle, docDate, docCat):
    sql = 'Select id from Category where name = %s'
    recset = [docCat]
    cur.execute(sql, recset)
    id = cur.fetchall()[0]["id"]

    sql = 'Select title from Documents'
    recset = [docText]
    cur.execute(sql, recset)
    string = recset[0]
    cstring = re.sub(r'[!.?\s]', '', string)
    numChars = len(cstring)

    sql = "Insert into Documents (docnum, text, title, numChars, date, category_id) Values (%s, %s, %s, %s, %s, %s)"
    recset = [docId, docText, docTitle, numChars, docDate, id]
    cur.execute(sql, recset)

    cstring2 = re.sub(r'[?!.]', '', string)
    newTerm = cstring2.lower().split()
    sql = 'Select * from terms where term = %s'
    for i in newTerm:
        recset = [i]
        cur.execute(sql, recset)
        if cur.fetchall():
            hello = 0
        else:
            num_charTerm = len(i)
            sql2 = 'Insert into terms (term, numChars) Values (%s, %s)'
            recset = [i, num_charTerm]
            cur.execute(sql2, recset)
    tc = {}
    for word in newTerm:
        if word in tc:
            tc[word] += 1
        else:
            tc[word] = 1

    for term, count in tc.items():
        newTerm = term
        newCount = count
        sql = 'Insert into Index (docNumber, term, count) Values (%s, %s, %s)'
        recset = [docId, newTerm, newCount]
        cur.execute(sql, recset)


def deleteDocument(cur, docId):
    sql = 'Select term from Index where docNumber = %s'
    recset = [docId]
    cur.execute(sql, recset)
    test = cur.fetchall()
    for term in test:
        delete_term = term["term"]
        sql2 = 'Delete from Index where term = %s'
        recset = [delete_term]
        cur.execute(sql2, recset)

    sql = "Delete from Documents where docNumber = %(docId)s"
    cur.execute(sql, {'docId': docId})


def updateDocument(cur, docId, docText, docTitle, docDate, docCat):
    deleteDocument(cur, docId)

    createDocument(cur, docId, docText, docTitle, docDate, docCat)


def getIndex(cur):
    sql = 'SELECT Index.term, Documents.title, count(*) AS count FROM Index INNER JOIN Documents ON Index.docNumber = ' \
          'Documents.docNumber GROUP BY term, title'
    cur.execute(sql)
    result = cur.fetchall()
    term_occur = {}
    for row in result:
        term = row['term']
        docu = row['title']
        count = row['count']
        if term in term_occur:
            term_occur[term] += f',{docu}:{count}'
        else:
            term_occur[term] = f'{docu}:{count}'

    for term, occurrences in term_occur.items():
        print(f"'{term}':'{occurrences}'")
