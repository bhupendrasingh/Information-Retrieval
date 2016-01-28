# Web Crawler
import http.client
import html.parser 
import urllib.request
import urllib
from urllib.parse import urlsplit
import time
import re


link_count = 0


#Creating a class for parsing html links and inheriting HTMLParser.
class myhtmlParser(html.parser.HTMLParser):  
        def handle_starttag(self,tag,attributes):
                if tag=='a':
                    for (nextLink,value) in attributes:
                        if nextLink=='href':
                            nextUrl=urllib.parse.urljoin(self.baseUrl,value)
                            self.allLinks.append(nextUrl)

                            
#The following function is used to fetch the links from the webpage visted and append append the same to the baseurl to create the absoluteurl.          
        def fetchLinks(self,urlToVisit):
                self.allLinks=[]
                self.baseUrl=urlToVisit
                myResponse = urllib.request.urlopen(urlToVisit)
                if myResponse.getheader("Content-Type")=='text/html; charset=UTF-8':
                        pageData=myResponse.read()
                        dataString=pageData.decode('utf-8')
                        self.feed(dataString)
                        return dataString,self.allLinks
                else:
                        print("",[])
                        
# The following function filter the link acquired for region,wikipedia domain,admin pages,links within page and also removes duplication creating unique links.
def filterLinks(getLinks):
        uniqueUrls=set(getLinks)
        newUrlList=[]
        for item in uniqueUrls:
                nextUrl=item
                pattern=re.compile("https://en.wikipedia.org/wiki/")
                if re.match(pattern,nextUrl):
                        desiredUrl=nextUrl 
                        if not re.search("#",desiredUrl)and not re.match("http(s)://.+:.+",desiredUrl)and not re.match("https://en.wikipedia.org/wiki/Main_Page",desiredUrl):
                                nextUrl=desiredUrl
                                newUrlList.append(nextUrl)
        return newUrlList




        
#The function takes the two arguments as the page to visit, word to find on the page and the max number of pages to be traversed.
def mySuperSpiderWithKey(urlToVisit,wordToFind):
        linksToVisit = [urlToVisit]
        linksTraversed=0
        wordHit= False
        myLink=[]
        hitUrl=[]     
        visitedList = []
        depthCounter=0
        allLinksCrawled={}
        key=0
        value=[]
        totalLinks=0
        global link_count
        count=0
        ctr=0
        newlist=[]
        f = open("outputWithKey.txt", "w")
        while((linksToVisit!= [] and not wordHit) and (linksToVisit!= [] and depthCounter < 5) or (linksToVisit!= [] and count <= 1000)):
                linksTraversed = linksTraversed + 1
                while linksToVisit != [] and linksToVisit[0] not in visitedList:
                        urlToVisit = linksToVisit.pop(0)
                print(linksTraversed,"Visiting:",urlToVisit)
                visitedList.append(urlToVisit)
                startParser = myhtmlParser()
                time.sleep(1) #for 1 secoond time delay before making new reuest for url open.
                data,links = startParser.fetchLinks(urlToVisit)
                print("at depth", depthCounter+1)
                mylinks=filterLinks(links)
                key=depthCounter
                value=list(mylinks)
                allLinksCrawled[depthCounter]=value
                depthCounter=depthCounter+1
                linksToVisit=mylinks[1:]
                linksToVisit.append(mylinks)
                count=len(linksToVisit)
##              print("Link crawled on this page: ", count)
                link_count+= count
                if data.find(wordToFind)>-1:
                        wordHit = True
                        print("Found word")
                        wordHit=False
                else:
                        print("Search didnt't return any result on this page\n")
                if (link_count>=1000) or (depthCounter==5):
                        for key, value in allLinksCrawled.items():
                                for item in value:
                                        ctr+=1
                                        if(ctr<=1000):
                                                f.write(item+"\n")
##                                                break
##                        print(ctr)
                        break
##        val1=len(mylinks)
##        val2=len(links)
##        print(val1,val2)
##        totalval=val1/val2
##        #proportion=len(mylinks)/len(links)
##        print(totalval)
        print("Reached depth 5 or 1000 links saved!")
        #print("Press enter to exit")
        #input()

#The following function crawl tge web without the keyphrase and thus accepts only one argument.
#The function visits the seed page extarcts out the links on the seed page and then visits them..
#in random order. The crawler crawles to the depth of 5 or until..
#it has acquired 1000 unqiue URLs.

def mySuperSpiderNoKey(urlNoKey):

        # Declaring all the variables that we are using in the given function.
        linksToVisit = [urlNoKey]
        linksTraversed=0
        visitedList = []
        depthCounter=0
        allLinksCrawled={}
        key=0
        value=[]
        totalLinks=0
        global link_count
        count=0
        ctr=0
        newlist=[]
        f = open("outputWithNoKey.txt", "w")
        #The while loop that compares if the depth or the unique URLs have reched the limit and
        #also the Url to visit anytime should not be empty.
        
        while((linksToVisit!= [] and depthCounter < 5) or (linksToVisit!= [] and count <= 1000)):
                linksTraversed = linksTraversed + 1
                while linksToVisit != [] and linksToVisit[0] not in visitedList:
                        urlToVisit = linksToVisit.pop(0)
                print("Visiting:",urlToVisit)
                visitedList.append(urlToVisit)
                startParser = myhtmlParser()
                data,links = startParser.fetchLinks(urlToVisit)
                print("At depth", depthCounter+1 ,"\n")
                mylinks=filterLinks(links)
                key=depthCounter
                value=list(mylinks)
                allLinksCrawled[depthCounter]=value
                depthCounter=depthCounter+1
                linksToVisit=mylinks[1:]
                linksToVisit.append(mylinks)
                count=len(linksToVisit)
                link_count+= count
##              print("Total: ", link_count)
                if (link_count>1000) or (depthCounter==5):
##                        print("Total links fetched", link_count)
                        for key, value in allLinksCrawled.items():
                                for item in value:
                                        ctr+=1
                                        if(ctr<=1000):
                                                f.write(item+"\n")                   
                        break
##                for key,value in linksToVisit.items():
##        val1=len(mylinks)
##        val2=len(links)
##        print(val1,val2)
##        totalval=val1/val2
##        #proportion=len(mylinks)/len(links)
##        print(totalval)
        print("Reached depth 5 or 1000 links saved!")
        #print("Press enter to exit")
        #input()



def mainFunction():
        seedUrl=input("Input the seed Url(no quotation marks): ")
        wordToSearch=input("Input the keyphrase to search, for no keyword just hit enter: ")
        if (seedUrl!=[] and wordToSearch!=""):
                mySuperSpiderWithKey(seedUrl,wordToSearch)
        elif (seedUrl!=[] and wordToSearch==""):
                mySuperSpiderNoKey(seedUrl)

        else:
                print("No input received")


mainFunction()                

