import math
import csv
import os
import glob
import re
from math import log
from collections import OrderedDict
from collections import Counter
################################################################################
posLength=0
negLength=0
vocabLength=0
posProb=0
negProb=0
posTermProbab={}
negTermProbab={}
probPosToNegRatio={}
probNegToPosRatio={}
c=Counter()
def read_model_file(opath,modelfile):
    dictwithterms={}
    poslist={}
    neglist={}
    input_file=open(modelfile,'r')
    for line in input_file:
        a=line.split(",")
        if a[0] == 'pos-length':
            posLength=a[1]
        if a[0] == 'neg-length':
            negLength=a[1]
        if a[0] == 'vocab-length':
            vocabLength=a[1]
        if a[0] == 'pos-prob':
            posProb=a[1]
        if a[0] == 'neg-prob':
            negProb=a[1]
        if a[0] == 'pos':
            poslist[a[1]]=a[2]
        if a[0] == 'neg':
            neglist[a[1]]=a[2]
    create_path(opath,poslist,neglist,vocabLength,posLength,negLength, posProb, negProb)
    find_prob(poslist,neglist,vocabLength)

# find the probabilities

def find_prob(plist,nlist,vocablen):
    posScore=0
    negScore=0
    newPosLength=0
    newNegLength=0
    for k,v in plist.items():
        newPosLength=newPosLength+ int(v)
    for k,v in nlist.items():
        newNegLength=newNegLength+ int(v)
    for k,v in plist.items():
        posScore = (int(v) + 1) / (int(vocablen) + int(newPosLength))
        posTermProbab[k]=posScore
    for k,v in nlist.items():
        negScore = (int(v) + 1) / (int(vocablen) + int(newNegLength))
        negTermProbab[k]=negScore
    calculateProbRatio(posTermProbab, negTermProbab)

def create_path(opath,poslist,neglist,vocabLength,posLength,negLength,posProb,negProb):
    if opath== 'textcat\dev':
        path=opath
        path1 = path+"\\pos\\"
        path2 = path+"\\neg\\"
        read_data("pos",path1,poslist,neglist,vocabLength,posLength,negLength,posProb,negProb)
        read_data("neg",path2,poslist,neglist,vocabLength,posLength,negLength,posProb,negProb)
    else:
        read_data("test",opath,poslist,neglist,vocabLength,posLength,negLength,posProb,negProb)


# Function to calculate the probabilities for test and dev data.
def read_data(dirval,path,poslist,neglist,vocabLength,posLength,negLength,posProb,negProb):
    outputFile = open("cut.csv",'a')
    pattern = re.compile("[^A-Za-z]")
    newPosLength=0
    newNegLength=0
    for k,v in poslist.items():
        if not v is '':
            newPosLength=newPosLength + int(v)
    for k,v in neglist.items():
        if not v is '':
            newNegLength=newNegLength+ int(v)
    for filename in glob.glob(os.path.join(path, '*.txt')):
        posScore=0
        negScore=0
        f = open(filename,'r')
        lines = f.read()
        line = lines.split()
        for item in line:
            if not re.match(pattern,item):
                if item in poslist.keys():
                    posScore += log((int(poslist[item]) + 1) / (int(vocabLength) + int(newPosLength)))
                else:
                    posScore += log(0+1/ (int(vocabLength) + int(newPosLength)))
                if item in neglist.keys():
                    negScore += log((int(neglist[item]) + 1)/( int(vocabLength) + int(newNegLength)))
                else:
                    negScore += log(0+1/(int(vocabLength) +  int(newNegLength)))
        posScore += float(posProb)
        negScore += float(negProb)
        outputFile.write(dirval+","+filename+","+str(posScore)+","+str(negScore)+"\n")

def calculateProbRatio(posTermProbab, negTermProbab):
    ratiofile=open('ratio.txt','a')
    posProbSorted={}
    negProbSorted={}
    for key1,value1 in posTermProbab.items():
        if key1 in negTermProbab.keys():
            probPosToNegRatio[key1]=log(posTermProbab[key1]/negTermProbab[key1])
            probNegToPosRatio[key1]=log(negTermProbab[key1]/posTermProbab[key1])
    posProbSorted = OrderedDict(sorted(probPosToNegRatio.items(), key=lambda x: x[1]))
    negProbSorted = OrderedDict(sorted(probNegToPosRatio.items(), key=lambda x: x[1]))
    c=Counter(posProbSorted)
    c1=Counter(negProbSorted)
    d1=c.most_common(20)
    d2=c1.most_common(20)
    for item in d1:
        ratiofile.write(str(item[0])+","+str(item[1])+"\n")
    for item1 in d2:
        ratiofile.write(str(item1[0])+","+str(item1[1])+"\n")
mypath2=input("Enter the path: ")
myfile=input("Enter the model file: ")
read_model_file(mypath2,myfile)
