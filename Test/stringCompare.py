list1 = [u'S LACOSTE-JULIEN', u' M JAGGI', u' M SCHMIDT', u' P PLETSCHER']
list2 = [u'M JAGGI']

print list1 
print list2
print "----------------------------------------"
check = ' '.join(list(set(list1) & set(list2)))
if check.__len__() > 0:
    print "check is : " + str(check)
#writeToFile("\n"+str(1)+"\n")
