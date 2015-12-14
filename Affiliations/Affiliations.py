#http://www.scimagojr.com/journalsearch.php?q=ACM&tip=jou
from BeautifulSoup import BeautifulSoup
#from time import sleep
from random import choice
from csv import DictWriter
import urllib2
#import sys
#import json
#import readFile
#import datetime
#import codecs

def writeToSpreadsheet(dictItem):
    with open('../dump/CountryOfOrigin.csv','a') as outfile:
        writer = DictWriter(outfile, ['JName', 'URL', 'CountryOfOrigin'])
        writer.writerow(dictItem)


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

#readFile.readConfig()
lines = [line.rstrip('\n') for line in open('JList')]
for s in lines:
    #s = readFile.ReadJName()
    journalName = s.replace(" ", "+")
    print s
    url = "http://www.scimagojr.com/journalsearch.php?q="+journalName+"&tip=jou"
    print url

#url = "http://www.scimagojr.com/journalsearch.php?q=Applied+Soft+Computing&tip=jou&exact=yes"  #"http://www.scimagojr.com/journalsearch.php?q=ACM&tip=jou"
    html_page = urlopener(url)
    if html_page!= False:
        soup = BeautifulSoup(html_page)
        td_list = []
        table = soup.find('div', {'id': 'derecha_contenido'})
        for row in table.findAll("p"):
            tmp= row.text
            td_list = (tmp.strip()).split('.')
            if td_list.__len__() > 1: 
                print td_list[2]
                dict1={'JName':td_list[1].strip(), 'URL':url, 'CountryOfOrigin':td_list[2].strip()}
                writeToSpreadsheet(dict1)
                #.next_element(string=True)
            #country_info = row.find('href')
            #print country_info            