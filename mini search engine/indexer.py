#Program to create the inverted index

# import system libraries

from collections import Counter
from collections import defaultdict

#####################################################################
# data type definations

docid_terms={}
frequency = Counter()
count=0
term_tf={}
termsList=[]
temp_dict={}
final_dict={}
temp_list=[]
index={}
another_temp=[]

#####################################################################
# The function counts the number of times a word or terms ahs occured in the given document.
def countWordInKey(wordDict):
	for key,value in wordDict.items():
		for i in value:
			frequency[i]+=1
		temp_dict=dict(frequency)
		frequency.clear()
		final_dict[key]=temp_dict
	createIndex(final_dict)

#####################################################################
#The function creates the index and stores into the file called index.out
# The function receives a dictionary as input and creates a index dictioanry with the terms as key
# and docid and frequency as values.

def createIndex(v1dict):
	main_list=[]
	for k,v in v1dict.items():
		for k1,v1 in v.items():
			if (k1 in index.keys()):
				temp_list=index[k1]	
				another_temp=[k,v1]
				temp_list.append(another_temp)
				index[k1]=temp_list
				temp_list=[]
			else:
				another_temp=[k,v1]
				main_list.append(another_temp)
				index[k1]=main_list
				main_list=[]
	ofile=open('index.out','w')    # Creates the output file index.out. Writes the index to this file.
	for key,value in index.items():
		ofile.write(str(key))
		ofile.write("->")
		ofile.write(str(value))
		ofile.write("\n")
#####################################################################
 # The following function reads the corpus file and creates the dictionary for each document with docid as kye and the terms as values.
def indexer(corpusfile):                 
	with open(corpusfile,'r') as f:     # corpusfile is the input corpus file.
		for line in f:
			a=line.split()
			for item in a:
				if(item is "#"):
					docid=a[a.index(item)+1]
					termsList=[]
					continue
				else:
					if (not(item.isdigit())):
						termsList.append(item)
					docid_terms[docid]=termsList
		countWordInKey(docid_terms)
######################################################################
indexer('tccorpus.txt')
print("index output file has been generated")
