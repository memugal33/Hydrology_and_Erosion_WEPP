# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 05:52:20 2022

@author: mugalsamrat.dahal
"""

import os
import glob
import pandas as pd
import numpy as np
import math


#This file can convert the anisotropy of soil file with two ofe

def watyr_calc(year,month):
    if month>9:
        wyr=year+1
    else:
        wyr = year
    return wyr


def change_climate(readdir, writedir, year_to_copy, year_to_replace):
    
    os.chdir(readdir)
    clilist = glob.glob("*.cli")
    def mysolfunct(x):
        b='w' in list(x)[1]
        return not b
    
    c=[mysolfunct(x) for x in clilist]
    
    from itertools import compress
    nclis=list(compress(clilist,c))    
    sa = "\t"
    for clinm in nclis:
        #clinm = clilist[0]
        clir = open(clinm, 'r')
        my = clir.readlines()
        copy_year_mat = list()
        for m in range(15,len(my)):
            #m=16+460
            #my2 = my[m].strip(" ")
            #my2.split(" ")
            my2 = my[m].strip(' ').split(' ')
            my3 = [x for x in my2 if x.strip()]
            
            wyr = watyr_calc(int(my3[2]),int(my3[1]))
            
            if wyr == year_to_copy:
                
                if int(my3[1])<=9:
                    toreplace = [x.replace(str(year_to_copy),str(year_to_replace)) for x in my[m].split(" ")]
                else:
                    toreplace = [x.replace(str(year_to_copy-1),str(year_to_replace-1)) for x in my[m].split(" ")]

                toreplace2 = " ".join(toreplace)
                copy_year_mat.append(toreplace2)
        a = 0
        #a=364
        for m in range(15,len(my)):
            #m=7958
            #my2 = my[m].strip(" ")
            #my2.split(" ")
            my2 = my[m].strip(' ').split(' ')
            my3 = [x for x in my2 if x.strip()]
         
            wyr = watyr_calc(int(my3[2]),int(my3[1]))
            
            if wyr == year_to_replace:
                my[m] = copy_year_mat[a]
                a = a+1
                if a==365:
                    a = a - 1 
    
        myfile = open(writedir+"\\"+clinm, "w+")
        myfile.writelines(my)
        myfile.close()


if __name__ == "__main__":
    
    readdir = "F:\\WORK\\Project_2\\WEPPwatershed\\after_anisotropy\\springcreek_past_slope_climate\\wepp\\runs"
    writedir = "F:\\WORK\\Project_2\\WEPPwatershed\\after_anisotropy\\springcreek_past_slope_climate\\wepp\\runs"
   # an_rto = 5.0
    year_to_copy = 1958
    year_to_replace = 1959
    change_climate(readdir, writedir, year_to_copy, year_to_replace)


