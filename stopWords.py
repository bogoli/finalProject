# stopWords.py
# adds stop words to a dictionary

stopWords = dict()

with open('stopwords.txt', 'r') as wordList:
	for line in wordList:
		# strip() gets rid of the newline char
		stopWords[line.strip()] = 1 
	
