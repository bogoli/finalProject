# stopWords.py
# adds stop words to a dictionary

import xml.etree.ElementTree as xml

stopWords = dict()
with open('stopwords.txt', 'r') as wordList:
	for line in wordList:
		# strip() gets rid of the newline char
		stopWords[line.strip()] = 1 
	

class DOC:
	def __init__(self, doc):
		self.title = doc.find("TITLE").text.strip()
		self.author = doc.find("AUTHOR").text.strip()
		self.text = doc.find("TEXT").text.strip()

documents = []
for i in range(1, 51):
	str = "documents/cranfield00" + ("0" + `i` if i < 10 else `i`)
	documents.append(DOC(xml.parse(str).getroot()))

print documents[0].title
