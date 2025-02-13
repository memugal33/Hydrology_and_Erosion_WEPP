# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 13:14:23 2022

@author: mugalsamrat.dahal
"""

import os
#os.getcwd()
import glob
import pandas as pd
import numpy as np
#os.getcwd()
#os.chdir("C:\\Users\\mugalsamrat.dahal\\OneDrive - Washington State University (email.wsu.edu)\\Paper2\\Weppwatershed")

def allhillslope_average(mydir):
    
    '''
    This function Lists out all the loss file and compile
    
    Lists out annual average erosion for all hillslope in dataframe
    
    mydir: output directory where the loss files are located.
    
    '''

    os.chdir(outdir)
    losslist = glob.glob("*.loss*")
    #losslist = glob.glob(mydir+"/*.loss*")
    def letter_identifier (lst, strs):
        for m in range(0,(len(lst)-1)):
            t = lst[m].split(" ")
    #         if m < (len(lst)-1):
            for k in t:    
                    if k == strs:
                        ret_val = m
                        break
                    else:
                        ret_val = "NA"
                    
            if ret_val != "NA":
                break
        return ret_val
    
    erlist = []
    for f in losslist:
        nm = f.split('.loss')[0]
        nms=nm.split('H')[1]
        fl = open(f,'r+')
        f2 = fl.readlines()
        i1 = letter_identifier(f2,"II.")
        i2 = letter_identifier(f2, "III.")
        i3 = letter_identifier(f2[i1:i2], "A.")
        if i3=='NA':
            f5 = 0
        else:
            i4=i1+i3
            f3 = f2[i4+2].split("=   ")[1] ##pick out the average from that line
            f4 = f3.split("kg/m2")[0] ### use the unit to pick out just the number
            f5 = f4.strip() ### remove spaces
        tlist = [nms, f5]
        erlist.append(tlist)
    
    myerrdata = pd.DataFrame(erlist, columns = ['Hillslope', 'Average Erosion'])
    #con = lambda x: int(x)
    myerrdata['Average Erosion']=pd.to_numeric(myerrdata['Average Erosion'])
    
    myerrdata['Average Erosion']= myerrdata['Average Erosion']*10 # converting to ton per ha from kg per m2
    
    return myerrdata


if __name__ == "__main__":
    mydir = "F:\WORK\Project_2\WEPPwatershed\\springcreek_with_large_graph\\wepp\\output"
    myerrdata = allhillslope_average(mydir)
    ##myerrdata.to_csv(("F:\WORK\Project_2\WEPPwatershed\\run_analysis\\springflatcreek_intense.txt"),
      ##               header = True, sep =",", index=False)

