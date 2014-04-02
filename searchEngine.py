# searchEngine.py
# adds stop words to a dictionary
# parses 50 documents and indexes the words found in them
# accepts a query string with limited boolean operations allowed
# returns a list of documents that 

import xml.etree.ElementTree as xml
import re

stopWords = dict()
with open('stopwords.txt', 'r') as wordList:
	for line in wordList:
		# strip() gets rid of the newline char
		stopWords[line.strip()] = 1 
	

class DOC:
	# document frequency statically referenced
	# each key maps to an array of DOC references that have that key
	docsHave = dict()
	
	def __init__(self, doc):
		self.index = int(doc.find("DOCNO").text.strip())
		self.title = doc.find("TITLE").text.strip()
		self.author = doc.find("AUTHOR").text.strip()
		self.text = doc.find("TEXT").text.strip()
		
		# index words in document
		self.docHas = dict()
		self.__index(self.title)
                self.__index(self.author)
                self.__index(self.text)
	
	def __index(self, str):
		# replace punctation delimiters with whitespace delimiters and split
		for word in re.sub('[^\w]+', ' ', str).split():
			# don't index unnecessarily short words or numbers
			if word not in stopWords and len(word) >= 4 and re.search('[a-zA-Z]', word):
				if not word in DOC.docsHave:
					DOC.docsHave[word] = []
				if not word in self.docHas:
					DOC.docsHave[word].append(self)
					self.docHas[word] = 1
				else:
					self.docHas[word] += 1
	
	def calcRank(self, words):
		sum = 0
		for word in words:
			# if word is in self.docHas it should also be in DOC.docsHave unless something bizarre goes terribly wrong
			if word in self.docHas:
				sum += self.docHas[word] / float(len(DOC.docsHave[word]))
		return sum

# fill an array of DOC instances parsed from each file
docs = []
for i in range(1, 51):
	str = "documents/cranfield00" + ("0" + `i` if i < 10 else `i`)
	docs.append(DOC(xml.parse(str).getroot()))

# make sure it all works
print DOC.docsHave["data"]
