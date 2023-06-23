# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 20:23:13 2022

@author: mugalsamrat.dahal
"""
#### There is another better file for this
import os
import datetime
from datetime import date, timedelta
#os.getcwd()
import glob
import pandas as pd
import numpy as np


def calcyearlywat(mydirs, f,startdate, enddate):
    from determine_wateryear import determine_wateryear
    from datetime import datetime, timedelta, date
    
    names = pd.read_table(mydir+"\\"+watfile, delim_whitespace= True, header=None, skiprows=19, nrows=1)
    df = pd.read_table(mydir+"\\"+watfile, delim_whitespace= True, header=None, skiprows=22)
    df.columns = names.values.tolist()[0]
    df['WY'] = 'NA'
    df['Month'] = 'NA'
    df['Day'] = 'NA'
    for o in ofe:
    
        df = df[df['OFE']==o]
    
        # for i in range(0,len(df)):
        #     ### Use Julian day -1 because this function assums julian day starts from 0
        #     #i=0
        #     df['WY'] = determine_wateryear(int(df['Y'][0]),int(df['J'][0]-1))[0]
        #     df['Month'] = determine_wateryear(int(df['Y'][i]),int(df['J'][i]-1))[1]
        #     df['Day'] = determine_wateryear(int(df['Y'][i]),int(df['J'][i]-1))[2]
        
        
        chnge = df[['Y','J']].apply(pd.to_numeric, errors='coerce', axis =1)
        df['WY']  = chnge.apply(lambda x: determine_wateryear(x['Y'], x['J']-1)[0], axis = 1)
        df['Month']  = chnge.apply(lambda x: determine_wateryear(x['Y'], x['J']-1)[1], axis = 1)
        df['Day']  = chnge.apply(lambda x: determine_wateryear(x['Y'], x['J']-1)[2], axis = 1)
        df['ET'] = df['Ep']+df['Er']+df['Es']
        
        
        
if __name__ == "__main__":
    maindir = 'C:\\Users\\mugalsamrat.dahal\\OneDrive - Washington State University (email.wsu.edu)\\Paper2\\Weppwatershed'
    mydir = "F:\\WORK\\Project_2\\WEPPwatershed\\springflatcreek2\\wepp\\output"
    watfile = "H1.wat.dat"
    os.chdir(maindir)
    yearly_agg_watershed(mydir)

