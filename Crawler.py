# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 12:05:34 2019

@author: Johnson
"""

import requests
from bs4 import beautifulsoup
from time import sleep

def spider(max_pages):
    page = 1
    while page <= max_pages:
        url = 'http://example.webscraping.com/places/default/index/' + str(page)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)
        for link in soup.findAll('a', {'places'});
            href = link.get('href')
            print(href)
        page += 1
    

from ast import literal_eval
import sys
import json

# Global Variables
globalLinks = []
indexUrl = 'http://example.webscraping.com'
hrefList = []
globalWords = []
allWords = []
# Dictionary structure used for JSON file
myDictionary = {}

def exportToJSON(data):
    filePathNameWExt = './data.json'
    with open(filePathNameWExt, 'w') as f:
        json.dump(data, f,indent=2)

def getAllLinks(url):
    global indexUrl
    sleep(5) # 5 second politeness window
    # get the html of the website
    source = requests.get(url).text

    # Set up beautifulsoup
    soup = BeautifulSoup(source, 'lxml')

    # Find all the links from the table
    links = soup.findAll('td')

    # Put all the hrefs from the table into a list
    for link in links:
        hrefList.append(indexUrl + link.div.a['href'])

    # If there's a next link, find it
    for link in soup.findAll("a", text="Next >"):
        print(link)
        hrefList.append(indexUrl + link['href'])
        getAllLinks(indexUrl + link['href'])

    print(hrefList)
    return hrefList

def getAllWords(links):
    global myDictionary
    # For each link from all links
    for link in links[0]:
        sleep(5) # 5 second politeness window

        # create a new request & soup for link
        linkSource = requests.get(link).text
        linkSoup = BeautifulSoup(linkSource, 'lxml')

        # extract only the relavent text from the web page
        [s.extract() for s in linkSoup(['style', 'script', '[document]', 'head', 'title'])]

        # split the words by space and new line characters
        renderedText = linkSoup.getText(separator="\n").split()

        for string in renderedText:
            word = string.replace(":","") # Get rid of semi-colons
            if word in myDictionary: # check if that word is in the dictionary
                for w,l in myDictionary.items(): # iterate through all words and their links
                    if w == word: # word in dictionary
                        if link in l: # link is in the link of the word of inner dictionary
                            l[link] += 1 # link exists: update frequency
                        else:
                            l.update({link:1}) # new link: create link
            else:
                myDictionary[word] = {link:1} # Else word is not in the dictionary, add it and create a list for it
        print("Building Inverted Index....")
    return globalWords

# Load data from json file
def load():
    with open('data.json', 'r') as f:
        jsonFile = json.load(f)
    return jsonFile

def printDictionary(word, dictionary):
    parseWord = word.split()
    if len(parseWord) == 1:
        if word in dictionary:
            print(dictionary[word])
        else:
            print("This word is not the inverted index")
    else:
        print("Please enter only 1 word.")

def findPhrase(phrase, dictionary):
    parsePhrase = phrase.split()
    userInput = phrase
    if parsePhrase[0] in dictionary: # Check if the first word is in the dictionary

        firstWordInvInd = dictionary[parsePhrase[0]] # return inverted index of first word

        #parsePhrase.remove(parsePhrase[0]) # Remove the first word from the phrase
        validLinks = []
        intersection = []
        if len(parsePhrase) == 1: # 1 word
            for link in firstWordInvInd:
                validLinks.append(link)
        elif len(parsePhrase) == 2: # 2 words
            intersection = firstWordInvInd.keys() & dictionary[parsePhrase[1]].keys()
        else: # More than 2 words
            listOfKeys = dictionary[parsePhrase[0]] # Add the keys of the first word to a list
            parsePhrase.remove(parsePhrase[0]) # Remove the first word
            for word in parsePhrase: # For all remaining words
                listOfKeys = listOfKeys &  dictionary[word].keys() # recursively compute set intersection

        for link in listOfKeys:
            validLinks.append(link)

        print("The following words: ", userInput, " appear in the following links: "  )
        print(validLinks)
    else:
        print("Word: ",parsePhrase[0]," is not in the inverted index.")

while(True):
    print("Select a command: 'build', 'load', 'print' , 'print', 'find' 'exit'")
    userInput = input()
    if(userInput == 'build'):
        globalLinks.append(getAllLinks(indexUrl)) # Crawl the website for links
        globalWords = getAllWords(globalLinks) # Build an inverted index
        exportToJSON(myDictionary) # Write to a file system
    elif(userInput == 'load'):
        jsonFile = load()
        if jsonFile == False:
            print("Please `build` first.")
    elif(userInput == 'print'):
        d = load()
        if d == False:
            print("Please `build` first.")
        else:
            print("Pass the word you want to print the inverted index for:")
            word = input()
            printDictionary(word,d)
    elif(userInput == 'find'):
        d = load()
        if d == False:
            print("Please `build` first.")
        else:
            print("Pass the phrase you want the inverted index for:")
            phrase = input()

            findPhrase(phrase, d)
    elif(userInput == 'exit'):
        sys.exit()
    else:
        print("Not Implemented")