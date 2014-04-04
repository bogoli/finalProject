# searchEngine.py
# adds stop words to a dictionary
# parses 50 documents and indexes the words found in them
# accepts a query string with limited boolean operations allowed
# returns a list of documents that match a given query string
# can be run in interactive mode or as a single command with the -q flag

import xml.etree.ElementTree as xml
import argparse
import re

# index a list of stopwords so we don't indnex unnecesarily short or common words
stopWords = dict()
with open('stopwords.txt', 'r') as wordList:
	for line in wordList:
		stopWords[line.strip()] = 1 
	

class DOC:
	# document frequency statically referenced
	# each key maps to an array of DOC references that have that key
	docsHave = dict()
	
	def __init__(self, file):
		# prep the xml parser
		doc = xml.parse("documents/" + file).getroot()
		
		# set document attributes
		self.file = file
		self.docno = int(doc.find("DOCNO").text.strip())
		self.title = doc.find("TITLE").text.strip()
		self.author = doc.find("AUTHOR").text.strip()
                self.biblio = doc.find("BIBLIO").text.strip()
		self.text = doc.find("TEXT").text.strip()
		
		# index words in document
		self.docHas = dict()
		self.__index(self.title)
                self.__index(self.author)
                self.__index(self.biblio)
                self.__index(self.text)
	
	def __index(self, str):
		# replace punctation delimiters with whitespace delimiters and split
		for word in re.sub('[^\w]+', ' ', str.upper()).split(): 
			# don't index unnecessarily short words or numbers
			if word not in stopWords and re.search('[a-zA-Z]', word): 
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
	docs.append(DOC("cranfield00" + ("0" + `i` if i < 10 else `i`)))

# utility methods for handling array merging based on boolean logic
def mergeAND(left, right):
	return [e for e in left if e in right]
def mergeOR(left, right):
	return left + [e for e in right if e not in left]
def mergeNOT(word):
	if word not in DOC.docsHave:
		return docs
	
	return [e for e in docs if e not in DOC.docsHave[word]]

# recursive method for handling the query word at a time, AND operation gets precedence
def parseQuery(mergee, words):
	# simplest base case, an empty list of words
	if not words:
		return mergee;

	# next simplest base case, the first word is not found in the query
	elif words[0] not in DOC.docsHave:
                return parseQuery([], words[1:])
	
	elif words[0] == 'NOT':
		# there better be at least one word after NOT that's neither NOT nor OR
		if len(words) == 1 or words[1] == 'NOT' or words[1] == 'OR':
			return -1;
		
		#resolve the immediate word and continue to parse since NOT has high priority
		return parseQuery(mergeAND(mergee, mergeNOT(words[1])), words[2:])
	
	elif words[0] == 'OR':
		# there better be at least one word after OR that is not also OR or there is a query sytnax error
		if len(words) == 1 or words[1] == 'OR':
			return -1
		
		# resolve the right hand side and then merge with the left since OR has low priority
		return mergeOR(mergee, parseQuery(docs, words[1:]))
	
	else:
		# resolve the immediate word and continue to parse since AND has highest priority
		return parseQuery(mergeAND(mergee, DOC.docsHave[words[0]]), words[1:])

# prepare the query statement to be handled by the recursive parser - AND gets priority so replace it with space
def fetchQuery(str):
        # regex to replace AND or -'s with a space, as that is the default operation for two words, then convert to upper for case insensitivity and split into an array of words
        result = parseQuery(docs, re.sub('(AND|-)', ' ', str.upper()).split())
	
	# sort the result
	# TODO: Insert sort method call
	
	# return the sorted list
	return result

# Console output
def printQuery(str):
	results = fetchQuery(str)
	if len(results) == 0:
		print 'No documents match your query'
	else:
		for i, doc in enumerate(results):
			print `i + 1` + ' - Calculated Rank: ' + `doc.calcRank(re.sub('(AND|-)', ' ', str.upper()).split())` + ' - File: ' +  doc.file

# Command line interaction
parser = argparse.ArgumentParser(description='Scan documents based on a simple query')
parser.add_argument('-i', '--interactive', action="store_true", help='Run in interactive mode')
parser.add_argument('--query', help='Allows for basic AND, OR, and NOT logical operators.')

# Parse the arguments and handle the situation appropriately
args = parser.parse_args()
if args.query:
	printQuery(args.query)
elif args.interactive:
	print "Enter a query or '-q' to exit: "
	interactiveQuery = raw_input()
	while interactiveQuery != '-q':
		if interactiveQuery.strip() != "":
			printQuery(interactiveQuery.strip())
		
		print "\nEnter a query or '-q' to exit: "
		interactiveQuery = raw_input()
