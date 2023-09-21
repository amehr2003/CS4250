#-------------------------------------------------------------------------
# AUTHOR: ANITA MEHRAZARIN
# FILENAME: title of the source file
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #1
# TIME SPENT: how long it took you to complete the assignment
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard arrays

#importing some Python libraries
import csv
import math

documents = []
labels = []

#reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append (row[0])
            labels.append(row[1])

#Conduct stopword removal.
#--> add your Python code here
stopWords = {'I', 'and', 'She', 'They', 'her', 'their'}
temp = ""
filteredWords = []
for i in range(len(documents)):
    temp = documents[i]
    for j in stopWords:
        temp = temp.replace(j," ")
    filteredWords.append(temp)

#Conduct stemming.
#--> add your Python code here
steeming = {
  "cats": "cat",
  "dogs": "dog",
  "loves": "love",
}
steemedWords = []

for i in range(len(filteredWords)):
    temp = filteredWords[i]
    for j in steeming.keys():
        temp = temp.replace(j, steeming[j])
    steemedWords.append(temp)

#Identify the index terms.
#--> add your Python code here
for i in range(len(steemedWords)):
    indexTerms = steemedWords[i].split()

#Build the tf-idf term weights matrix.
#--> add your Python code here
#---------------------------------

loveC = []
catC = []
dogC = []
counter = 0

for i in steemedWords:
    words = i.split()
    counter += words.count("love")
    loveC.append(counter)
    counter = 0
    counter += words.count("cat")
    catC.append(counter)
    counter = 0
    counter += words.count("dog")
    dogC.append(counter)


d1 = steemedWords[0].split()
d2 = steemedWords[1].split()
d3 = steemedWords[2].split()
docu = [d1, d2, d3]

tfValues = []
j = 0
while j < len(indexTerms):
    index = indexTerms[j]
    j += 1
    for i in docu:
        occurances = 0
        for term in i:
            if term == index:
                occurances += 1
        tf = occurances / len(i)
        tfValues.append(tf)

idfValues = []

x = 0
while x < len(indexTerms):
    idf = 0
    index = indexTerms[x]
    x += 1
    occurances = 0
    for doc in docu:
        if index in doc:
            occurances += 1
    idf = math.log10(3 / occurances)
    idfValues.append(idf)

# Calculate the document scores (ranking) using document weights (tf-idf) calculated before and query weights (binary - have or not the term).
# --> add your Python code here
docScores = []
tfidfScores = []
dex = 0
while dex < len(idfValues):
    currentIdf = idfValues[dex]
    tfidf_group = []
    for i in range(3 * dex, 3 * (dex + 1)):
        tfidf = currentIdf * tfValues[i]
        tfidf = round(tfidf, 4)
        tfidf_group.append(tfidf)
    tfidfScores.append(tfidf_group)
    dex += 1

print("td_idf")

print(tfidfScores)

doc1Score = sum(section[0] for section in tfidfScores)
doc2Score = sum(section[1] for section in tfidfScores)
doc3Score = sum(section[2] for section in tfidfScores)

print("d1 SCORE:", doc1Score)
print("d2 SCORE:", doc2Score)
print("d3 SCORE:", doc3Score)

newCounter = 0
if doc1Score>0.1:
    newCounter+=1
if doc2Score>0.1:
    newCounter+=1
if doc3Score>0.1:
    newCounter+=1

print("PRECISION = " + str((newCounter/newCounter) * 100))
print("RECALL = " + str((newCounter/newCounter) * 100))
