import urllib
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup as bs
import pymongo
import sys, traceback
import datetime

url = 'https://www.cpp.edu'
frontier = 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml'

try:
    html = urllib.request.urlretrieve('https://www.cpp.edu/sci/computer-science/')
except HTTPError as e:
    print(e)
except URLError as e:
    print('The server could not be found!')
else:
    print('It Worked!')

def crawlPage(frontier):
    return 