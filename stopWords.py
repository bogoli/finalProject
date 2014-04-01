# stopWords.py
# adds stop words to a dictionary

import xml.etree.ElementTree as xml
import re

stopWords = dict()
with open('stopwords.txt', 'r') as wordList:
	for line in wordList:
		# strip() gets rid of the newline char
		stopWords[line.strip()] = 1 
	

class DOC:
	#document frequency statically referenced
	df = dict()
	
	def __init__(self, doc):
		self.title = doc.find("TITLE").text.strip()
		self.author = doc.find("AUTHOR").text.strip()
		self.text = doc.find("TEXT").text.strip()
		
		#word frequency
		self.wf = dict()
		self.__index(self.title)
                self.__index(self.author)
                self.__index(self.text)
	
	def __index(self, str):
		#replace punctation delimiters with whitespace delimiters and split
		for word in re.sub('[^\w]+', ' ', str).split():
			if len(word) > 4 and re.search('[a-zA-Z]', word):
				if not word in DOC.df:
					DOC.df[word] = 0
				if not word in self.wf:
					DOC.df[word] += 1
					self.wf[word] = 1
				else:
					self.wf[word] += 1
	

docs = []
for i in range(1, 51):
	str = "documents/cranfield00" + ("0" + `i` if i < 10 else `i`)
	docs.append(DOC(xml.parse(str).getroot()))

#make sure it all works
print docs[0].wf['study']
for word, df  in DOC.df.iteritems():
	print word, ': ', df
