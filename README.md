Search Engine
=============

##CS 2420 — Data Structures and Algorithms Final Project
John Call
Lia Bogoev
April 2014

This final project is a simple python search engine that references 50 documents (included) in XML format.
It accepts any combination of simple boolean operators (AND, OR, NOT).
It removes common words (stopwords) for better results.
It ranks search results by relevance.

##Included files

- python script
- related html interface
- 50 sample documents
- stopwords file
- project description

##Installation

The search engine requires python 2.7 to be installed. It can be run as a unix-styled console application.
To see all available usages, type "python searchEngine.py -h", but the ones of most interest are probably "-i" or "-q QUERY".
Using either of these arguments will output the results, and show you the calculated document rank as well.
For an example type: python searchEngine.py -q "boundary-layer OR increment"

To access the web interface, install apache with php on a unix-based machine (linux or mac)
Make the DocumentRoot of the apache server the "html" directory, and the DirectoryIndex "index.html"
If you wish you may set ServerName to cs2420.localhost or something similar but you may need to add it to your hosts file
Open a web browser (preferably Firefox or Chrome) and navigate to "localhost" (or whatever you made the ServerName in the last step)
