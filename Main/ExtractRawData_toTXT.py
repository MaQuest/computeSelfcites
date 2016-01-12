#Author: Gouri Ginde
#This program scrapes all the raw data for a journal and stores it in the dictionaries format.
#the advantage is that the data can be written as and when scraped.
#while loading this data for further processing, we ahve to add [ at the beginning and ] at the end of the file
#also }{ has to be replaced with },{
from BeautifulSoup import BeautifulSoup
from time import sleep
from random import choice
import urllib2
import sys
import json
sys.path.append('/home/gouri/workspace/Prj/Test')
import readFile
import datetime
import codecs

out_file = file('../dump/OneStopData.txt','a')
#import re
IsTesting = 1 #is True
J_info = "" 
year= ['2012', '2013', '2014', '2015']
h5_index = 0
count = 1
SingleLineData = ""
# create wait range between 20 and 40 seconds
r = range(20,60)

stopat1000 = 0
stopFortheDay = 0  #stop scraping for that day as the limit is just this! 2500
#orig_stdout = sys.stdout
#f = 0 #file('../dump/selfcites.txt', 'a')
#sys.stdout = out_file

    
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

def printToFile(somestr):
    global out_file
    json.dump(somestr, out_file)
    
        
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
        J_info = {'J_Name': jName, 'J_h5_index' : h5_indexSTR, 'J_h5_median': h5_medianSTR, 'J_venue' : youRL };
        print J_info
        #writeToSpreadsheet(dict1)
        #writeToFile ("link to main is: "+youRL+"\n") 
        printToFile(J_info)
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
        global count, cited_doc_Count
        table = soup.find('table', {'id': 'gs_cit_list_table'})
        #for testing this will halp start from the middle of scraping at particular paper
        global IsTesting
        if int(IsTesting) == 1:
            skipCount = 4
            IsTesting = 0
        else:
            skipCount = 0
        for row in table.findAll("tr"):
            # print row.text
            td_list = row.findAll("td")
            if (td_list.__len__() > 0 ):
                if any(x in td_list[2].text for x in year) :
                    if skipCount == 0:
                        #print td_list[0].text
                        authors = (td_list[0].find("span", attrs={"class": "gs_authors"})).text
                        article_link = (td_list[0].find("a")).get('href')
                        citesLink = (td_list[1].find("a")).get('href')
                        title = (td_list[0].find("span")).text
                        citesCount = int(td_list[1].text)
                        articlePub = (td_list[0].find("span", attrs={"class": "gs_pub"})).text
                        #print "title: " + str(title.encode('utf-8'))
                        
                        dict1 = {'A_Id': count, 'A_Authors_names': authors.encode('utf-8'), 'A_Year':td_list[2].text, 'A_CitedByLink': citesLink, 'A_TotalCites':citesCount, 'A_Title': title.encode('utf-8'), 'A_articlePub':articlePub, 'A_URL':article_link};
                        
                        #print dict1
                        
                        
                        #to COMBINE THE TWO DICTIONARIES AND TO CREATE A SINGLE ENTRY 
                        global SingleLineData
                        SingleLineData = "" #intialize for every new article entry
                        SingleLineData = J_info.copy() 
                        SingleLineData.update(dict1)
                        print "inside getPub: " + str(SingleLineData)
                        printToFile(SingleLineData)
                        
                        count = count+1
                        cited_doc_Count = 0
                        for pages in range(0, citesCount, 20):
                            #controlling the blocking of the program
                            global stopat1000
                            checkForDwnldThreshold()
                            stopat1000 = stopat1000 + 20
              
                            Link = citesLink + "&cstart=" + str(pages)
                            print "fetching all 20 cited papers from: " + Link
                            fetchCitedArticles(Link)
                            #cited_doc_list.append(citedPapers)
                            #writeToFile(Link)
                        #dict1['CitedPapers']= cited_doc_list
                        #print dict1      
                                                
                    else:
                        print "skipped: " + str(skipCount)
                        skipCount= skipCount - 1
                    
    #print JInfo  
      
#function to extract and check the self citations per paper
def fetchCitedArticles(citesLink):
    #citedList = []
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
                global cited_doc_Count
                cited_doc_Count = cited_doc_Count +1
                #dict1 = {'citedId':cited_doc_Count, 'Title':title.encode('utf-8'), 'Link':link, 'year':year, 'authors':authors.encode('utf-8'), 'CitedDocPubName':pubName}
                dict1 = {'C_citedId':cited_doc_Count, 'C_Title':title.encode('utf-8'), 'C_Link':link, 'C_year':year, 'C_authors':authors.encode('utf-8'), 'C_CitedDocPubName':pubName}    
                #print dict1
                #citedList.append(dict1)
                
                #One entry with all of the data e
                global SingleLineData
                print "Before: " + str(SingleLineData)
                zis = SingleLineData.copy() 
                zis.update(dict1)
                print "Inside Fetch: " + str(zis)
                printToFile(zis)        
    #return citedList            
                

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
        s ="IEEE Transactions on Fuzzy Systems"#"3D Research"#"Applied Soft Computing"#"Expert Systems with Applications"#"3D Research" #"Applied Soft Computing" #"4OR"#"Expert Systems with Applications" #"The Journal of Machine Learning Research"#"ACM Computing Surveys"#"3D Research" #"ACM Transactions on Computational Logic" #"ACM Computing Surveys"#"AAAI Conference on Artificial Intelligence"#"ACM Communications in Computer Algebra"  #"AAAI Conference on Artificial Intelligence" #"ACM Transactions on Applied Perception" #"ACM Transactions on Autonomous and Adaptive Systems" #"ACM Computing Surveys" #"ACM Transactions on Applied Perception" #"4OR" 
    else: #from file
        s = readFile.ReadJName()  
    
    print "JName in process is: " + s
    journalName = s.replace(" ", "+")
    start = "------------------" + s + "-----------------\n"
    
    pubsForjNameURL = getLinktoAllPapers(journalName) #when the JOURNAL name is searched in search box
    pages = 0
    totPages = h5_index
    for pages in range(0, totPages, 20):
    #for pages in range(0, 40, 20):
        #sys.stdout = orig_stdout
        #checkForDwnldThreshold()
        stopat1000 = stopat1000 + 20
        #try:
        getPubInfo(pubsForjNameURL, journalName, pages) #PAGING logic
        #except: # catch *all* exceptions
        #    e = sys.exc_info()[0]
        #    print e
        #writeToFile( str(pages)+"\n" )
 
    #print JInfo
    #writeToSpreadsheet(JInfo)
    #sys.stdout = orig_stdout
    #out_file.close()
    TotJnames = TotJnames -1



