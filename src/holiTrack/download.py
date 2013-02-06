import os 
import urllib

def downloadICS():
    srcPath = 'https://www.gov.uk/bank-holidays/england-and-wales.ics'
    destPath = os.path.dirname(__file__)
    
    urllib.urlretrieve(srcPath,os.path.join(destPath,'england-and-wales.ics'))