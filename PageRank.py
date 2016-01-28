from math import*
from collections import Counter
################################## Data Definations ###########################

N=0       # Total no of pages
d=0.85    # Damping or teleportation factor
pages_dictionary = {}
outgoingLinks = {}
SinkNodes={}
SinkNodesCount=0
intialPageRank={}
newPR={}
cnt = Counter()
incomingLinks= Counter()
lengthEntropy=0
lenarray=0
j=0
itrCount=0
run=True
entropy={}
perplexityOriginal={}
perplexity={}
runCount=0
###############################################################################
#Reading Dataset line by line and storing pages with corresponding in links

fileName=input("Enter File name with extension (.txt): ")
with open(fileName,'r') as f:
    for line in f:
      a = line.split()
      pages_dictionary[ a[0] ] = a[1:]
N=(len(pages_dictionary))
###############################################################################
# Calculating outgoing links

for key1,value1 in pages_dictionary.items():
  for item in value1:
    cnt[item]+=1
outgoingLinks=dict(cnt)
###############################################################################
#  Calculating sinkNodes

for key,value in pages_dictionary.items():
  countval = 0
  if not(key in outgoingLinks):
    countval+=1
    SinkNodes[key]=countval
#print("Sinknodes and their count: ",SinkNodes)
print("Total number of sink nodes: ",len(SinkNodes.keys())) 

###############################################################################
# Calculating page rank of each page

for key4,value4 in pages_dictionary.items():
  intialPageRank[key4]=1/N
#print("Page Rank of each page:\n",intialPageRank)         

###############################################################################
# Checking for convergence.
def checkstatus(j):
    if(
      ((perplexity[j-1]-perplexity[j-2]) <1) and 
      ((perplexity[j-2]-perplexity[j-3]) <1) and 
      ((perplexity[j-3]-perplexity[j-4]) <1) and 
      ((perplexity[j-4]-perplexity[j-5]) <1)):
      return False
    return True

################################################################################
# Calculating page rank iteratively while convergence has not reached. The loop
# woudl run until the convergence has reached.

while run:  
  sinkPR=0
  totalEntropy=0
  for key6,value6 in SinkNodes.items():
    sinkPR=sinkPR+intialPageRank[key6]
  for key,value in pages_dictionary.items():
    newPR[key]=(1-d)/N
    newPR[key]+=d*sinkPR/N
    for item in value:
      newPR[key]+=d*intialPageRank[item]/outgoingLinks[item]
    entropy[key]=(newPR[key])*(log(newPR[key],2))
    totalEntropy+=entropy[key]
  perplexityOriginal[runCount]=pow(2,(-1*(totalEntropy)))
  perplexity[itrCount]=perplexityOriginal[runCount]
  print("For Iteration:",runCount,"Perplexity is: ->",perplexityOriginal[runCount])
 
  if(len(perplexity.values()) == 5):
    run=checkstatus(len(perplexity.values()))
    perplexity={}
    itrCount=-1
  if(run == False):
    for key,value in pages_dictionary.items():
      inlinksCount=0
      for item in value:
        inlinksCount+=1
      #print("After iteration,",runCount,",",key,",",newPR[key],",",inlinksCount)
      print(key,",",newPR[key])
      
  itrCount+=1
  runCount+=1
  for key,value in pages_dictionary.items():
    intialPageRank[key]=newPR[key] 
    #print("Page Rank of: ",key," ->",intialPageRank[key])
#input()
