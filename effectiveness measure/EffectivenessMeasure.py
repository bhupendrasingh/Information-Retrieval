# Program to read the query output and cacm relevance judgement and calculate
# the effectiveness measure liek precision,recall,ndcg,p@K etc for the search engine.

from math import log
import collections

resultslist= []
relevancelist= []
dlist= []
dcg=0
imdcg=0
idcg=[]
mdcg=[]
ndcg=[]
ideal_relevance=[]
relevanceWithRank=[]
mavgp=[]
def read_results_file():
    with open('ResultsSetLucene.txt','r') as f:
        for line in f:
            l=line.split()
            resultslist.append(l)

def read_relevance_file():
    with open('cacm.txt','r') as f:
        for line in f:
            l=line.split()
            relevancelist.append(l[:5])
        for item in relevancelist:
            item[2]=item[2][5:]
            dlist.append(item)

def calculate_relevance_levels(qidr,qidc,total_doc_list):
    relevanceWithRank.clear()
    mlist=[]
    for x in resultslist:
        relevance_level=0
        if x[0] == str(qidr):
            for y in dlist:
                if y[0] == str(qidc):
                    if x[2] == y[2]:
                        relevance_level=1
            relevanceWithRank.append(relevance_level)
    mlist=calculate_ndcg(relevanceWithRank,total_doc_list)
    return(mlist)

def process_query(qid,cqid):
    relcount=0
    total=0
    precision1=0
    rel_doc_count=0
    recall_qurey_one=0
    pre_list=0
    rec_list=0
    count=0
    tc=0
    total_relevant_doc_count=[0]*100
    get_ndcg=[]
    for z in relevancelist:
        if z[0]== str(cqid):
            rel_doc_count=rel_doc_count+1
            total_relevant_doc_count[rel_doc_count]=1
    get_ndcg=calculate_relevance_levels(qid,cqid,total_relevant_doc_count)
    for x in resultslist:
        relevance_level=0
        if x[0] == str(qid):
            for y in dlist:
                if y[0] == str(cqid):
                    if x[2] == y[2]:
                        relevance_level=1
                        relcount=relcount+1
                        premap=relcount/float(x[3])
                        total=total+premap
            precision1= relcount/float(x[3])
            pre_list=precision1
            recall_qurey_one=relcount/rel_doc_count
            rec_list=recall_qurey_one
            outfile=open("MeasureForQuery"+str(qid)+".csv",'a')
            outfile.write(str(x[3])+","+str(x[2])+","+str(x[4])+
            ","+str(relevance_level)+","+str(pre_list)+","+
            str(rec_list)+","+str(get_ndcg[count])+"\n")
            total1=total/rel_doc_count
            count+=1
    mavgp.append(total1)
    #print(mavgp)
    # if str(qid)=='3':
    #     tc=sum(mavgp)/len(mavgp)
    #     print(tc)

def calculate_ndcg(relevanceWithRank,total_rel_docs):
    ndcg.clear()
    dcg=0
    idcg.clear()
    mdcg.clear()
    firstvalue=relevanceWithRank[0]
    for i in range(1,100):
       k=i+1
       rvalue=relevanceWithRank[i]
       logvalue=log(k,2)
       if rvalue is 0:
           dcg=0
       else:
           dcg=rvalue/logvalue
       mdcg.append(dcg)

    for m in range((len(mdcg)+1),1):
        mdcg[m]=mdcg[m-1]
    mdcg.insert(0,firstvalue)

    for j in range(1,100):
        mdcg[j]=mdcg[j]+mdcg[j-1]

    ideal_relevance=total_rel_docs
    ideal_relevance=sorted(ideal_relevance)
    ideal_relevance=ideal_relevance[::-1]
    fvalue=ideal_relevance[0]
    for i in range(1,100):
      k=i+1
      rvalue=ideal_relevance[i]
      logvalue=log(k,2)
      if rvalue is 0:
          imdcg=0
      else:
          imdcg=rvalue/logvalue
      idcg.append(imdcg)

    for m in range((len(idcg)+1),0):
        idcg[m]=idcg[m-1]
    idcg.insert(0,fvalue)


    for j in range(1,100):
        idcg[j]=idcg[j]+idcg[j-1]

    for k in range(0,100):
      ndcgvalue=mdcg[k]/idcg[k]
      ndcg.append(ndcgvalue)
    return(ndcg)
####################################################################

read_results_file()
read_relevance_file()
process_query(1,12)
process_query(2,13)
process_query(3,19)
