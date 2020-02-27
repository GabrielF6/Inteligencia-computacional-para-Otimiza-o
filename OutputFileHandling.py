# -*- coding: utf-8 -*-
import re
import os
def saveTestCase(text,result,executiontime,index):
    filename = "src/outputests/TestCase_"+str(index)+".txt"
    f= open(filename,"w+")
    f.write(text+"\n")
    leng = len(result)
    for i in range(leng):
        if(isinstance(result[i],tuple)):
            for j in range(len(result[i])):
                f.write(str(result[i][j])+"\n")
        else:
            f.write(str(result[i]))
        f.write("\n")
    f.write("\nExecution Time:"+str(executiontime)+"\n")
    f.close()

def parsefile(path):
    fil = open("src/files/aux2.TXT", "w") 
    fil.write("") 
    fil.close() 

    f = open("src/files/aux2.TXT","a")
    f2 = open(path,"r+")
    for line in f2:
        newline =  re.split(r'\D+',line)
        if(newline[0]==''):
            newline = newline[1]+" "+newline[2]+" "+newline[3]+"\n"
        else:
            newline = newline[0]+" "+newline[1]+" "+newline[2]+"\n"
        f.write(newline)
    f.close()
    f2.close()
