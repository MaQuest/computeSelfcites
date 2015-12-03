from time import sleep
import datetime

def checkForSleep():
    current_time = datetime.datetime.now().time()
    print "sleeping for an hour now: " + current_time.isoformat()
    sleep(3600)
    current_time = datetime.datetime.now().time()
    print "sleep over: " + current_time.isoformat()
    
checkForSleep()