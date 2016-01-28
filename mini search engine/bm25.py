#BM25  Algorithm
#########################################
import ast
import math
import collections
from collections import Counter
from collections import OrderedDict
######################################################################
docScoreList={}
getpos=[]
getcount=[]
myQueries=[]
index_dict={}
queryTermDoc={}
lines=[]
listOfDocs=[]
total_doc_term=[]
qf=0
dl=0
docid_with_frequency=[]
doc_length={}
counter=0
avgLenth=0
avdl=0
c=Counter()
final_dict_rank={}
######################################################################
# The function reads the index.out file as input and creates the dictionary.
def reading_dict(ifile):
	lines=open(ifile)
	for line in lines:
		line=line.split("->")
		line[1]=ast.literal_eval(line[1])
		index_dict[line[0]]=line[1]
	calculate_doc_length(index_dict)

######################################################################
# The function the reads the index dictionary and calculates the length for each document.
def calculate_doc_length(word_dict):
	docid_with_frequency=index_dict.values()
	for item in docid_with_frequency:
		nlist=item
		for element in nlist:
			if element[0] in doc_length:
				doc_length[element[0]] += element[1]
			else:
				doc_length[element[0]]=element[1]
	averageDocLength(doc_length)		
######################################################################
# The following function receives the dictionary with length of each document calculated  as input
# and calculates the average length for each docuemnt with reference to total number of documents.

def averageDocLength(docavglngth):
	total=0
	totalwords=0
	for key,value in docavglngth.items():
		total=total+docavglngth[key]
	totalwords=len(docavglngth.keys())
	avgLenth=(total/totalwords)
	return avgLenth

######################################################################	
# The follwoing function recevies the index.out,queries.txt and a number that specifies top number of documents to be fetched accoridng to ranking.
# The function the calculates the bm25 score for each term and assigns it to the given doc and so onc alculates it for other terms.
# Finally the scores for the same document are added from the bm25 values for various terms. The value for a term being repeated in query is
# calculated once and ignored when encountered other time.

def bm25(indexFile,queryFile,topDocs):
	reading_dict(indexFile)
	ri=0
	R=0
	k1=1.2
	b=0.75
	k2=100
	bm25_for_term=0
	singleDoc=0
	currentDoc=0
	current_frequency=0
	fi=0
	dl=0
	fvalue1=0
	fvalue2=0
	N=(len(doc_length.keys()))
	avdl=averageDocLength(doc_length)
	dict_query_with_bm25={}
	dict_for_query={}
	i=1
	# Read the query file line by line and read each line term by term and calculate the bm25 for each term.
	with open(queryFile,'r') as fin:
		for line in fin:
			dict_bm25_forall_docs={}
			l=line.split()
			temp_query_dict=collections.Counter(l)
			for key1,value1 in temp_query_dict.items():
				qf=temp_query_dict[key1]                          # calculate the frequency of the term in the given query.
				total_doc_term=index_dict[key1]
				ni=len(total_doc_term)
				for doc in total_doc_term:	
					singleDoc=doc
					currentDoc=singleDoc[0]                      # get the document in which the term appears. repeat the process for other documents 
					current_frequency=singleDoc[1]
					fi=int(current_frequency)
					dl=int(doc_length[currentDoc])
					K =k1*((1-b)+(b*(dl/avdl)))
					fvalue1=math.log(((ri+0.5)/(R-ri+0.5)) /((ni-ri+0.5)/(N-ni-R+ri+0.5)))
					fvalue2=(((k1+1)*fi)/(K+fi)) * ((k2+1)*qf/(k2+qf))
					bm25_for_term= fvalue1*fvalue2
					if currentDoc in dict_bm25_forall_docs:
						dict_bm25_forall_docs[currentDoc]+=bm25_for_term
					else:
						dict_bm25_forall_docs[currentDoc]=bm25_for_term

				for key,value in doc_length.items():
					if key not in dict_bm25_forall_docs:
						dict_bm25_forall_docs[key]=0

			dict_for_query[i]=dict_bm25_forall_docs	
			i+=1

	for key,value in dict_for_query.items():
		final_dict_rank[key]=collections.Counter(value).most_common(topDocs)

	outfile=open('results.eval','w')
	for key,value in final_dict_rank.items():
		i=1
		for k in value:
			outfile.write(str(key) + " Q0 " + (str(k[0])) +"  " + (str(i)) +"  "+ (str(k[1]))+"  " +"System-devworks\n")
			i+=1	 		
#######################################################################
bm25('index.out','queries.txt',100)
print("results eval file has been generated")
			
