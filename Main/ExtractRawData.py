#Author: Gouri Ginde
#This program computes the selfcitations for 3 sub categories under Engg and Computer Science of GS
# Mainly AI, Evolutionary computation and Computing Systems
from BeautifulSoup import BeautifulSoup
from time import sleep
from random import choice
import urllib2
import sys
import json
import readFile
import datetime
import codecs

#import re
IsTesting = 1 #is True
J_info = "" 
J_articles = []
Article_cited = [] 
year= ['2012', '2013', '2014', '2015']
h5_index = 0
count = 1
# create wait range between 20 and 40 seconds
r = range(20,60)

stopat1000 = 0
stopFortheDay = 0  #stop scraping for that day as the limit is just this! 2500
orig_stdout = sys.stdout
#f = 0 #file('../dump/selfcites.txt', 'a')
#sys.stdout = f

    
def checkForDwnldThreshold():
    #controlling the blocking of program
    global stopat1000, stopFortheDay
    print "Count down: " + str(stopat1000)
    if stopat1000 > 490:
        current_time = datetime.datetime.now().time()
        print "sleeping for 15 mins now: " + current_time.isoformat()
        #sleep(3600)
        sleep(900)
        print "sleep over at: " + (datetime.datetime.now().time()).isoformat()
        stopFortheDay = stopFortheDay + stopat1000
        stopat1000 = 0
    if stopFortheDay > 2500:
        current_time = datetime.datetime.now().time()
        print "sleeping for day: " + current_time.isoformat()
        sleep(86400)
        print "sleep over"
        stopFortheDay = 0

#this is depricated as directly data is written to spreadsheet
def writeToFile(somestr):
    global f
    json.dump(somestr, f)
         
def urlopener(url):
    opener = urllib2.build_opener()
    ####################################################################################################
    # different user agents to use to keep from being banned.
    user_agents = [
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'               
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
    ]
    version = choice(user_agents)
    #opener.addheaders = [('User-Agent', 'OpenAnything/1.0 +http://diveintopython.org/')]
    #Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0
    #opener.addheaders = [('User-agent', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0')]
    opener.addheaders = [('User-agent', version)]
    
    try:
        html_page = (opener.open(url)).read()
    except urllib2.HTTPError, err:
        print "Error code is: " , err.code
        print "Reason is: ", err.reason
        return False
    
        
    return html_page

# function to get the link to all papers of that Journal 
def getLinktoAllPapers( jName):
    url = "https://scholar.google.com/citations?hl=en&view_op=search_venues&vq="+jName
    html_page = urlopener(url)
    #html_page = urllib2.urlopen(url)
    if html_page!= False : 
        soup = BeautifulSoup(html_page)
        table = soup.find('table', {'id': 'gs_cit_list_table'})
        td_list = table.findAll("td")
        #print td_list 
        h5_indexSTR = td_list[2].text
        h5_medianSTR = td_list[3].text
        global h5_index 
        h5_index = int(h5_indexSTR)
        #print h5_index , h5_median
        venue = (td_list[2].find("a")).get('href')
        youRL = "https://scholar.google.com/"+ venue
        print "Extracting cited docs for: " + youRL
        global J_info
        J_info = {'JName': jName, 'h5_index' : h5_indexSTR, 'h5_median': h5_medianSTR, 'venue' : youRL };
        #writeToSpreadsheet(dict1)
        #writeToFile ("link to main is: "+youRL+"\n") 
        return youRL

#for every publication/paper in the journal compute the self-citation and add to the JInfo List
def getPubInfo(pubsLink, jName, pages):
    #pages = 20
    #list1 = [2]
    #dict1 = {'Id': '1', 'JName': "3D Research ", 'Authors_name': 'First', 'YearOfPub':2014, 'CitedByLink': 'test', 'CitesPerPaper':1000, 'SelCitesPerPaper':200 };
    #dict1['Author_name'] = "Gouri"; # update existing entry
    #list1[0] = dict1
    #dict2 = {'Id': '1', 'JName': "3D Research ", 'Authors_name': 'First', 'YearOfPub':2014 };
    #list1.append(dict2)
    #print "dict1['Id']: ", dict1['JName']
    #print  list1
    append = "&cstart="+str(pages)
    url = pubsLink+append
    html_page = urlopener(url)
    if html_page!= False:
        soup = BeautifulSoup(html_page)
        td_list = []
        global count
        table = soup.find('table', {'id': 'gs_cit_list_table'})
        #for testing this will halp start from the middle of scraping at particular paper
        global IsTesting
        if int(IsTesting) == 1:
            skipCount = 0
            IsTesting = 0
        else:
            skipCount = 0
        for row in table.findAll("tr"):
            # print row.text
            td_list = row.findAll("td")
            if (td_list.__len__() > 0 ):
                if any(x in td_list[2].text for x in year) :
                    if skipCount == 0:
                        selfcites_count = 0
                        #print td_list[0].text
                        authors = (td_list[0].find("span", attrs={"class": "gs_authors"})).text
                        citesLink = (td_list[1].find("a")).get('href')
                        title = (td_list[0].find("span")).text
                        citesCount = int(td_list[1].text)
                        print "title: " + str(title.encode('utf-8'))
                        dict1 = {'Id': count, 'JName': jName, 'Authors_name': authors.encode('utf-8'), 'YearOfPub':td_list[2].text, 'CitedByLink': citesLink, 'TotalCites':citesCount, 'SelCitesPerPaper':-1, 'Title': title.encode('utf-8')};
                        count = count+1
                        #writeToFile("https://scholar.google.com/"+citesLink+"\n" )
                        #for this paper review the cited papers and compute self citations
                        for pages in range(0, citesCount, 20):
                            #controlling the blocking of the program
                            global stopat1000
                            checkForDwnldThreshold()
                            stopat1000 = stopat1000 + 20
              
                            Link = citesLink + "&cstart=" + str(pages)
                            print "fetching all 20 cited papers from: " + Link
                            articleList = fetchCitedArticles(Link)
                            #writeToFile(Link)
                        dict1['CitedPapers'] = articleList      
                        global J_articles
                        J_articles.append(dict1)           
                        
                    else:
                        print "skipped: " + str(skipCount)
                        skipCount= skipCount - 1
                    
    #print JInfo  
      
#function to extract and check the self citations per paper
def fetchCitedArticles(citesLink):
    citedList = []
    # wait random time then download object
    #sleep(choice(r))d
    url = "https://scholar.google.com"+citesLink
    html_page = urlopener(url)
    if html_page != False:
        soup = BeautifulSoup(html_page)
        table = soup.find('table', {'id': 'gs_cit_list_table'})
        for row in table.findAll("tr"):
            #print row.text
                 
            td_list = row.findAll("td")
            if (td_list.__len__() > 0 ):
                #if any(x in td_list[1].text for x in year): WAS THIS RIGHT TO CHECK YEAR for each cited? 
                #print td_list[0].text
                #print td_list[0].text
                link = (td_list[0].find("a")).get('href')
                year = td_list[1].text
                #title = (td_list[0].find("span")).text
                attList = []
                for spans in td_list[0].findAll('span'):
                    attList.append(spans.text) 
    
                title = attList[0]
                authors = attList[1]
                    
                if len(attList) > 2:
                    pubName = attList[2]       
                else :
                    pubName = "null"
                
                dict1 = {'Title':title, 'Link':link, 'year':year, 'authors':authors, 'pubName':pubName}    
                print dict1
                citedList.append(dict1)
    
    return citedList            
                

#--------------Main Function----------
if sys.stdout.encoding != 'cp850':
    sys.stdout = codecs.getwriter('cp850')(sys.stdout, 'strict')
if sys.stderr.encoding != 'cp850':
    sys.stderr = codecs.getwriter('cp850')(sys.stderr, 'strict')

#read the names one by one from the JournalList file and print it

#read the confif file in ./settings/settings.ini
readFile.readConfig()
IsTesting = readFile.IsTesting()
print "Testing set to: " + str(IsTesting)    
#For testing
if int(IsTesting) == 1:
    TotJnames = 1    
else:
    TotJnames = readFile.GetJlistCount()

while (TotJnames > 0):    
    #For testing
    
    if int(IsTesting) == 1: 
        s ="Applied Soft Computing" #"3D Research" #"4OR"#"Expert Systems with Applications" #"The Journal of Machine Learning Research"#"ACM Computing Surveys"#"3D Research" #"ACM Transactions on Computational Logic" #"ACM Computing Surveys"#"AAAI Conference on Artificial Intelligence"#"ACM Communications in Computer Algebra"  #"AAAI Conference on Artificial Intelligence" #"ACM Transactions on Applied Perception" #"ACM Transactions on Autonomous and Adaptive Systems" #"ACM Computing Surveys" #"ACM Transactions on Applied Perception" #"4OR" 
    else: #from file
        s = readFile.ReadJName()  
    
    print "JName in process is: " + s
    journalName = s.replace(" ", "+")
    start = "------------------" + s + "-----------------\n"
    
    global f
    f = file('../dump/'+s+'.txt', 'a')
    #writeToFile(start)
    #NOTE: init all the global variables after printing data to file
    #print journalName
    pubsForjNameURL = getLinktoAllPapers(journalName) #when the JOURNAL name is searched in search box
    pages = 0
    #stopat1000 = stopat1000 + h5_index
    #writeToFile( str(h5_index) )
    totPages = h5_index
    for pages in range(0, totPages, 20):
    #for pages in range(0, 40, 20):
        sys.stdout = orig_stdout
        #checkForDwnldThreshold()
        stopat1000 = stopat1000 + 20
        #try:
        getPubInfo(pubsForjNameURL, journalName, pages) #PAGING logic
        #except: # catch *all* exceptions
        #    e = sys.exc_info()[0]
        #    print e
        #writeToFile( str(pages)+"\n" )
    global J_articles
    J_info['article'] = J_articles  
    writeToFile(J_info)
    #print JInfo
    #writeToSpreadsheet(JInfo)
    #sys.stdout = orig_stdout
    #f.close()
    TotJnames = TotJnames -1



