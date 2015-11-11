from ConfigParser import SafeConfigParser
lineNum = 1
Jlist = ''
path = '../settings/settings.ini'
parser = SafeConfigParser()
parser.read(path)

#function to read from which line to rear from the JournalList.txt
#this is to automate the web scraping that once one journal is over pick up next in line in jounralList.txt 
def readConfig():
    global lineNum
    global Jlist
    lineNum = int(parser.get('line_num', 'line'))
    Jlist = parser.get('line_num', 'JournalFile')
    #print lineNum, Jlist
    
#function to increment the count
def setConfig(count):
    parser.set('line_num', 'line', count)
    # write changes back to the config file
    with open(path, "wb") as config_file:
        parser.write(config_file)

def ReadJName():
    infile = open(Jlist, 'r')
    data = infile.read() 
    infile.close()
    print "Reading JName now"
    # Return a list of the lines, breaking at line boundaries.
    my_list = data.splitlines()
    if lineNum > 0:
        Jname = my_list[lineNum-1] #line numbers start with 0 
    else: 
        Jname = my_list[lineNum]    
    #now update the linenumber in the config file
    setConfig(str(lineNum+1))
    
    #print Jname
    return Jname  

#function to check if the istesting flag is set in .ini file. So as to run the small run on a Journal with fewer papers
#in no time.
def IsTesting():
    isTesting = parser.get('line_num', 'IsTesting')
    return int(isTesting)

#function to get the total count
def GetJlistCount():
    infile = open(Jlist, 'r')
    data = infile.read() 
    infile.close()
    # Return a list of the lines, breaking at line boundaries.
    my_list = data.splitlines()
    #print len(my_list)
    return len(my_list)

#function to make sure the header info is printed just once in the .csv (output file)
#if it is 0 then set it to 1 and this way only once header is written to csv 
def HeaderExists():
    headerInfo = parser.get('line_num', 'headerAdded')
    if headerInfo == 0:
        parser.set('line_num', 'headerAdded', 1)
        
    print headerInfo
    return headerInfo 
         
#HeaderExists()
#readConfig()
#ReadJName()
#GetJlistCount()
#check =  IsTesting()
#if int(check) == 1:
#    print True
    
#else: 
#    print False