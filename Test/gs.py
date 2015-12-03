from BeautifulSoup import BeautifulSoup
import urllib2
#import re
#html_page = "gs.html" 
html_page = urllib2.urlopen('file:dump.html')
soup = BeautifulSoup(html_page)
for link in soup.findAll('a'):
    m= "https://scholar.google.com"+link.get('href')
    #print m
    html_subpage = urllib2.urlopen(m)
    soup1 = BeautifulSoup(html_subpage)
    for sublink in soup1.findAll('td', "gs_title"):
        print sublink
      

