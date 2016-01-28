import os
import glob
import re
from math import log
from collections import Counter
################################################################################
posTermFrequency = {}
negTermFrequency = {}
termWithFrequency={}
c1=[]
################################################################################

# Read the folder for pos/neg file and create word list

def main_function(opath):
    path=opath
    path1 = path+"\\pos\\"
    path2 = path+"\\neg\\"
    posTermFrequency,count=read_data(path1)
    negTermFrequency,count=read_data(path2)
    word_less_than_five(posTermFrequency,negTermFrequency,count)

# Function to read the files in the given directory and return the
# filteredWords

def read_data(path):
     count=0
     termWithFrequency={}
     totalWords = []
     filteredWords = []
     c=Counter()
     for filename in glob.glob(os.path.join(str(path), '*.txt')):
         count+=1
         f = open(filename,'r')
         lines = f.read()
         line = lines.split()
         for item in line:
             totalWords.append(item)
     c1.append(count)
# Filtering out the word from the complete word list.
     pattern = re.compile("[^A-Za-z]")
     for item in totalWords:
         if not re.match(pattern,item):
             filteredWords.append(item)

# With counter counting the frequency
     for item in filteredWords:
         c[item]+=1
     termWithFrequency=dict(c)
     return(termWithFrequency,c1)

################################################################################
# Remove the word with combined frequency less than 5
def word_less_than_five(poslist,neglist,count):
    commonlist=[]
    newposdict = {}
    newnegdict = {}
    vclength=0
    cpos=0
    cneg=0
    for key1,value1 in poslist.items():
        if key1 in neglist.keys():
            total=value1+neglist[key1]
            if total < 5:
                commonlist.append(key1)

    for key,value in poslist.items():
        if key not in commonlist:
            newposdict[key]=value

    for key,value in neglist.items():
        if key not in commonlist:
            newnegdict[key]=value

    for k,v in newposdict.items():
        cpos=cpos+v

    for k1,v1 in newnegdict.items():
        cneg=cneg+v1
    vclength=create_vocabulary(newposdict,newnegdict,count)

def create_vocabulary(posdict,negdict,count):
    modelfile=open("model.txt",'w+')
    vocablist = []
    posProb=0
    negProb=0
    uniqueword = set()
    for key1 in posdict.keys():
        vocablist.append(key1)
    for key2 in negdict.keys():
        vocablist.append(key2)
    uniqueword=set(vocablist)

# Writing model file.
    modelfile.write("pos-length"+","+str(count[0])+"\n"+"neg-length"+","+str(count[1])+"\n")
    modelfile.write("vocab-length"+","+str(len(uniqueword))+"\n")
    posProb=log(count[0]/sum(count))
    negProb=log(count[1]/sum(count))
    modelfile.write("pos-prob"+","+str(posProb)+"\n")
    modelfile.write("neg-prob"+","+str(negProb)+"\n")
    for key,value in posdict.items():
        modelfile.write("pos"+","+str(key)+","+str(value)+"\n")
    for key,value in negdict.items():
        modelfile.write("neg"+","+str(key)+","+str(value)+"\n")
    return (len(uniqueword))

mypath=input("Enter path: ")
main_function(mypath)
