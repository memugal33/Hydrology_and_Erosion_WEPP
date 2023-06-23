# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 13:10:23 2022
@author: mugalsamrat.dahal
"""
 

#import os
import glob

def edityear_rf(readdir, writedir, year):
    '''
    This function can edit in the current runfile from 
    
    WEPPcloud
    
    input: directory of read and write
    and year no
    '''
    runlist = glob.glob(readdir+"\\*.run")
    runlist = [i.split((readdir+"\\"))[1] for i in runlist]
    
    def mysolfunct(x):
        b='w' in list(x)[1]
        return not b
     
    c=[mysolfunct(x) for x in runlist]
     
    from itertools import compress
    nruns=list(compress(runlist,c))
    
    for runnm in nruns:
        #runnm=nruns[0]
        runr = open(readdir+"\\"+runnm, 'r')
        my = runr.readlines()
        my[len(my)-2] = str(year)+'\n'
        myfile = open(writedir+"\\"+runnm,"w+")
        myfile.writelines(my)
        myfile.close()
    
if __name__ == "__main__":
    

    readdir = "F:\\WORK\\Project_2\\WEPPwatershed\\upper_imbler_creek_altrot\\wepp\\runs"
    writedir = "F:\\WORK\\Project_2\\WEPPwatershed\\upper_imbler_creek_altrot\\wepp\\runs"
    
    year = 45
    
    edityear_rf(readdir,writedir, year)