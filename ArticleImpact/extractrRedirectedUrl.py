#program PART1: to extract just the URL's of the articles from google scholar.
# when the raw data is extracted from the GS the URL's are of the form 
# http://scholar.google.com/scholar?oi=bibs&cluster=3392336939730115962&btnI=1&nossl=1&hl=en
#but when we open this in browser we will get : http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=6253534&url=http%3A%2F%2Fieeexplore.ieee.org%2Fxpls%2Fabs_all.jsp%3Farnumber%3D6253534
#which is the actual article URL
#here we just extract the redirected URL's by processing the raw data of the Journals already scrapped.
 
from BeautifulSoup import BeautifulSoup
from random import choice
import urllib2
import pprint
import json
from time import sleep
# create wait range between 20 and 40 seconds
r = range(20,60)
authorsList = []
AffiliationsList = [] 
out_file = file('../dump/TEst2.txt','a')
path = "../dump/TEst2.txt"
#def wrtietoFile(ele):
#    writer = csv.writer(open('dict.csv', 'wb'))
#    for key, value in mydict.items():
#        writer.writerow([key, value])
def printToFile(somestr):
    #print somestr
    #global out_file
    #json.dump(somestr, out_file)
    print somestr
    global path
    with open(path, 'a') as f:
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
    print url
    try:
        html_page = (opener.open(url)).read()
    except urllib2.HTTPError, err:
        print "Error code is: " , err.code
        print "Reason is: ", err.reason
        return False
    
        
    return html_page

def getAffsSpringer(ArticleEle):
    item = ArticleEle['A_URL']
    #item = "http://link.springer.com/article/10.1007/s00500-010-0591-1"#"http://link.springer.com/article/10.1007/s00500-012-0824-6"
    soup1 = getPageContent(item)
    
    affs = []
    aa = soup1.find('ul', {'class' : "AuthorNames"})
    ab = aa.findAll('li')
    for row in ab:
        auth = (row.find('span', {'class': "AuthorName"})).text
        Aff_tp = row.find('span', {'class': "AuthorsName_affiliation"})
        Aff = (Aff_tp.span).text
        L1 = [auth, Aff]
        affs.append(L1)
        print auth, Aff
        
    ct = 1
    for x in affs:
        ArticleEle.update({'Auth_'+str(ct)+'_Aff':x[1]})
        ct = ct + 1
            
    return ArticleEle

def getAffsACM(ArticleEle):
    item = ArticleEle['A_URL']
    
    #item = "http://dl.acm.org/citation.cfm?id=2168843"#"http://dl.acm.org/citation.cfm?id=2168841" #"http://dl.acm.org/citation.cfm?id=2451146"
    soup1 = getPageContent(item)
    #get the affiliations
    affs = [] #list which stores authname, id, affs in that order
    # get the author names "authorName svAuthor"
    ab = soup1.find('div', {'id' : "divmain"})
    x = ab.table
    tables = x.findAll('table')
    
    bibs = tables[4].findAll("tr")
    tmp =  (bibs[2].find("td")).text
    tml = tmp.replace(";&nbsp;", "")
    dwlnds = tml.split("&middot")
    
    dwn = dwlnds[3].split(":")
    local = dwlnds[4].split(":")
    print dwlnds[3],dwlnds[4],dwn[1]
    ArticleEle.update({'Downloads':dwn[1]})
    ArticleEle.update({'local_cites':local[1]})
    
    return ArticleEle

def getAffsIEEEXplore(ArticleEle):
    #item = "http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=6189779&url=http%3A%2F%2Fieeexplore.ieee.org%2Fxpls%2Fabs_all.jsp%3Farnumber%3D6189779"
    #item = "http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=6342908&url=http%3A%2F%2Fieeexplore.ieee.org%2Fxpls%2Fabs_all.jsp%3Farnumber%3D6342908    "
    item = ArticleEle['A_URL']
    soup1 = getPageContent(item)
    ab = soup1.find('div', {'id' : "nav-article"})
    x = ab.ul
    lis = x.findAll('li')
    
    dwnld_extn = ( (lis[5].find('a')).get('href')).encode("utf-8")
    print dwnld_extn
    soup1 = getPageContent("http://ieeexplore.ieee.org" + dwnld_extn)
    strg = soup1.find('div', {'class' : "total-count"})
    #print strg
    lst =  [s.strip() for s in str(strg).splitlines()]
    print lst[1]
    ArticleEle.update({'Downloads':lst[1]})
    
    cites_extn = ( (lis[3].find('a')).get('href')).encode("utf-8")
    print cites_extn
    soup = getPageContent("http://ieeexplore.ieee.org" + cites_extn)
    stg = soup.find('div', {'class' : "countHeader"})
    print stg
    txt = stg.text
    print txt
    lt = [int(s) for s in txt.split() if s.isdigit()]
    print lt[0]
    ArticleEle.update({'localCites':lst})
    return

def getAuthorAffiliations(ArticleEle):
    item = ArticleEle['A_URL']
    if "sciencedirect" in item:
        updatedEle = getAffsScienceDirect(ArticleEle)
        return updatedEle
    elif "springer" in item:
        updatedEle = getAffsSpringer(ArticleEle)
        return updatedEle
    elif "dl.acm" in item:
        updatedEle = getAffsACM(ArticleEle)
        return updatedEle
    elif "ieeexplore" in item:
        updatedEle = getAffsIEEEXplore(ArticleEle)
        return updatedEle
    else:
        return False
    

def getAffsScienceDirect(ArticleEle):
    
    item = ArticleEle['A_URL']
    soup1 = getPageContent(item)
    #add logic here to get check if the article is from springer/ACM or the IEEE
    
    #get the affiliations
    affs = [] #list which stores authname, id, affs in that order
    # get the author names "authorName svAuthor"
    ab = soup1.find('ul', {'class' : "authorGroup noCollab svAuthor"})
    #print ab
    for bb in ab.findAll('li'):
        aa = bb.findAll('a')
        #print aa
        Authname = aa[0].text
        #Id = 'null'
        if len(aa)>1 and (aa[1].get('title') is not None):
        #if aa is not None and len(aa) > 2:
        #if aa[1].has_attr('title'):
            Id = aa[1].get('href')
            #print Id
        #if aa[1].get('title') == None :
        else:
            if len(affs) > 1:
                Id = affs[0][1]
            else:
                Id = 'null'            
        
        L1 = [Authname, Id]
        affs.append(L1)
    
    #print affs    
    
    x = soup1.find('ul', {'class': "affiliation authAffil"})
    #print x
    
    if len(affs) == 1:
        y = x.findAll('span')
        ele =[n.text for n in y]
        #print ele[0]
        affs[0].append(ele[0])
        #print affs
    
    elif (len(affs) == 2) and (affs[1][1] == 'null'):
        y = x.findAll('span')
        ele =[n.text for n in y]
        affs[0].append(ele[0])
        affs[1].append(ele[0])
        #print affs
    
        
    else:
        #print "here"
        for y in x.findAll('li'):
            tp = y.get('id')
            #print tp,y.text
            for z in affs:
                #tp1 = [value for key, value in z.items() if key.startswith('Auth_')]
                #tp2 = [value for key, value in z.items() if key.startswith('id')]
                if str(z[1])[1:] == y.get('id'):
                        ele = y.text
                        z.append(ele)
                        #print z
                elif tp is None:
                    ele = y.text
                    z.append(ele)
                    #print z
    #print "Full n Final Affs"
    #print affs
    for m in affs:
        if m[1] == 'null' and affs[0][1]!='null':
            x = affs[0][2]
            m.append(x)
    
    ct =0
    for m in affs:
        ct = ct +1
        if m[1] == 'null':
            ArticleEle.update({'Auth_'+str(ct)+'_Aff':"god help"})
        else:
            ArticleEle.update({'Auth_'+str(ct)+'_Aff':m[2]})
  
    return ArticleEle

def cleanUp(Clist):
    for i in Clist:
        if len(i) < 15:
            Clist.remove(i)
    
    return Clist

def createAuthElements(AList):
    authDict = {}
    ct=1
    #print "List has: " + str(AList)
    for i in AList:
        name = 'Auth_'+str(ct)
        ct  = ct + 1
        authDict[name] = i
          
    return authDict
    

def getRedirectedUrl(OrigUrl):
    #OrigUrl = "https://scholar.google.co.in/citations?hl=en&view_op=list_hcore&venue=d7jJgmnpNuIJ.2015&cstart=20"
    #print OrigUrl
    soup = getPageContent(OrigUrl)
    #print soup
    re_direct = (soup.find('script')).text
    extract = re_direct.split("'")
    #print extract
    
    #et = "http://dl.acm.org/citation.cfm?id=2168841"
    #print extract[1]
    return extract[1] # overwrite the existing to actual one
    #return et
    

def generateDictionaryNode(ArticleInfo, selfciteCount ):
    #authNameEle = createAuthElements(list1)
    #print ArticleInfo
    URl = getRedirectedUrl(ArticleInfo['A_URL'])
    URL = URl.replace("\\x3d", "=")
    #create a new dictionary element and return
    dictEle = {'A_Year':ArticleInfo['A_Year'] , 'A_articlePub':ArticleInfo['A_articlePub'] , 
               'A_Title':ArticleInfo['A_Title'], 'A_CitedByLink':ArticleInfo['A_CitedByLink'] ,
               'A_TotalCites':ArticleInfo['A_TotalCites'] , 'J_h5_index':ArticleInfo['J_h5_index'] ,
               'J_venue':ArticleInfo['J_venue'], 'J_h5_median': ArticleInfo['J_h5_median'], 
               'A_URL':URL, 'J_Name':ArticleInfo['J_Name'],
               'A_SelfCites': selfciteCount}
    #dictEle.update(authNameEle)
    
    return dictEle

def getPageContent(link):
    html_page = urlopener(link)
    #print html_page
    if html_page!= False: 
        soup = BeautifulSoup(html_page)
        return soup
    return False


data = json.load(open('../dump/DataforcitesNdownloads.txt'))
# Springer: data = json.load(open('../dump/Genetic Programming and Evolvable Machines.txt'))
#data = json.load(open('../dump/Genetic Programming and Evolvable Machines.txt'))
#print data
#print len(data)

AllArticleURLs = []
All_tmpArticleInfo = []
AllArticleInfo = []
#tp = getAffsACM("dummy")
#getAffsSpringer("dummy")
#getAffsIEEEXplore("ArticleEle")

for i in data: #i is each dictionary element
    if 'A_URL' in i:
        url = i['A_URL']
        jname = i['J_Name']
        if jname != "AAAI+Conference+on+Artificial+Intelligence":
        #print url
            AllArticleURLs.append(i)
 
print len(AllArticleURLs)
listJs = []
count = 0 
#getRedirectedUrl("OrigUrl")
for i in AllArticleURLs:
    #i = AllArticleURLs[0]
    self_cites = 0
    
    if count>188:
        #print i
        if i['A_URL'].startswith("/scholar"):
            newUrl = "https://scholar.google.com" +i['A_URL']
            i.update({'A_URL':newUrl})         
        
        sleep(choice(r))
        ArticleInfo = generateDictionaryNode(i, self_cites)
        
        All_tmpArticleInfo.append(ArticleInfo)
        #ArticleInfo = {'a':232, 'b':343, 'c':43}
         
        printToFile(ArticleInfo)
    else:
        print "skipped"
        count = count +1
    
#pprint.pprint(ArticleInfo, width=1)

# for m in All_tmpArticleInfo:
#     #m  = All_tmpArticleInfo[0]
#     Affs_Info = getAuthorAffiliations(m)
#     AllArticleInfo.append(Affs_Info)
#     printToFile(Affs_Info)
    #pprint.pprint(All_tmpArticleInfo, width=1)
  
#pprint.pprint(AllArticleInfo, width=1)
  
    
