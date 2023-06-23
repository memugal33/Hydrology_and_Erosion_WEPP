# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 15:57:57 2022

@author: mugalsamrat.dahal
"""
import os
import glob
import pandas as pd
#import numpy as np

### Convert slope file into two different OFEs
readdir = "F:\\WORK\\Project_2\\WEPPwatershed\\int_sol_cal\\wepp\\runs"
writedir = "F:\\WORK\\Project_2\\WEPPwatershed\\int_2ofes\\wepp\\runs"
ofeno = 2
def convsoils(readdir,writedir,ofeno):

    os.chdir(readdir)
    #os.getcwd()
    
    sollist = glob.glob("*.sol")
    def mysolfunct(x):
        b='w' in list(x)[1]
        return not b
    
    c=[mysolfunct(x) for x in sollist]
    
    from itertools import compress
    nsols=list(compress(sollist,c))
    
    
    for solnm in nsols:
        #solnm = sollist[1]
        solr = open(solnm, 'r')
        my = solr.readlines()
        for m in range(1,len(my)):
            
            if my[m-1] == "7778\n":
                my[m+1]= str(ofeno)+' 1\n' ### 1 means adjust hydraulic conductivity internally
                my[len(my)-1] = my[len(my)-1]+"\n"
                l1 = my[m+2:(len(my))]
                for nof in range(1,ofeno):
                    for ind in range(0,(len(l1))):
                        my.append(l1[ind])
                break
        #my.append(l1)
        myfile = open(writedir+"\\"+solnm, "w+")
        myfile.writelines(my)
        myfile.close()







