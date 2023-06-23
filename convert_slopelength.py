
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 19:34:33 2022

@author: mugalsamrat.dahal
"""

import os
import glob
import pandas as pd
import numpy as np
import math


#This file can convert the anisotropy of soil file with two ofe
def change_sl(readdir, writedir, limit):
    
    os.chdir(readdir)
    slplist = glob.glob("*.slp")
    def mysolfunct(x):
        b='w' in list(x)[1]
        return not b
    
    c=[mysolfunct(x) for x in slplist]
    
    from itertools import compress
    nslps=list(compress(slplist,c))    
    sa = " "
    for slpnm in nslps:
        #slpnm = slplist[1]
        slpr = open(slpnm, 'r')
        my = slpr.readlines()
        nofe = float(my[1].split(' ')[0].split('\n')[0])
        saspect = float(my[2].split(' ')[0])
        swidth=float(my[2].split(' ')[1].split('\n')[0])
        spoints =  int(my[3].split(' ')[0])
        
        slength = float(my[3].split(' ')[1].split('\n')[0])*nofe
        
        slopearea= swidth*slength
        
        if slength>limit:
            
            swidth = slopearea/limit
            slen_ofe = limit/nofe
            
            my[2] = str(saspect)+sa+str(swidth)+'\n'
            my[3] = str(spoints)+sa+str(slen_ofe)+'\n'
            my[5] = str(spoints)+sa+str(slen_ofe)+'\n'
    
        myfile = open(writedir+"\\"+slpnm, "w+")
        myfile.writelines(my)
        myfile.close()


if __name__ == "__main__":
    
    readdir = "F:\\WORK\\Project_2\\WEPPwatershed\\after_anisotropy\\springcreek_past_slope_length_soildepth_100m\\wepp\\runs"
    writedir = "F:\\WORK\\Project_2\\WEPPwatershed\\after_anisotropy\\springcreek_past_slope_length_soildepth_100m\\wepp\\runs"
    limit = 100
    change_sl(readdir, writedir, limit)
