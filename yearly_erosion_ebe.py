# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 22:10:08 2022

@author: mugalsamrat.dahal
"""

import os
import glob
import numpy as np
import pandas as pd
#import docx

def wy(y,m):
    if m>9:
        y = y+1
    else:
        y = y
    return y


def calcyearlyerr(mydirs,ebefile, startyr, wateryr=True):
    
    '''
    Given the following value, this code gives back the yearly erosion 
    using the eve by eve file
    
    mydirs = Give the directory name
    file = give the hillslope file name
    startyr
    
    Output:
        The output is in tonne, tonne/ha and mm
    '''
    
    from determine_wateryear import determine_wateryear
    from datetime import datetime, timedelta, date
    myebedf=pd.read_table(mydirs+"\\"+ebefile, sep= "\s{1,}", skiprows=3, header = None, engine = 'python')
    names = pd.read_table(mydirs+"\\"+ebefile, sep= "\s{1,}", skiprows=1, nrows =1, header = None, engine = 'python')
    myebedf.columns = names.values.tolist()[0]
    chnge = myebedf[['year','mo']]
    chnge = chnge.apply(pd.to_numeric, errors='coerce', axis =1)
    myebedf['WY'] = chnge.apply(lambda x: wy(x['year'],x['mo']), axis = 1)
    
    if wateryr==True:
        aggval = 'WY'
    else:
        aggval = 'year'
        
    agglist = ['Precp', 'Runoff','IR-det','Av-det', 'Av-dep','Sed.Del']
    
    myagg_df = myebedf.groupby(aggval,as_index=False)[agglist].sum()
    myagg_df['Water Year'] = myagg_df['WY'].apply(lambda x: int(x)+int(startyr)-1)
    myagg_df[['IR-det','Av-det', 'Av-dep']] = myagg_df[['IR-det','Av-det', 'Av-dep']]*10
    myagg_df[['Sed.Del']] = myagg_df[['Sed.Del']]*0.001
    
    return myagg_df
    

if __name__ == "__main__":
    maindir = 'C:\\Users\\mugalsamrat.dahal\\OneDrive - Washington State University (email.wsu.edu)\\Paper2\\Weppwatershed'
    mydirs = "F:\\WORK\\Project_2\\WEPPwatershed\\springflatcreek2\\wepp\\output"
    ebefile = "H1.ebe.dat"
    startyr = "1989"
    endyr = "2018"
    os.chdir(maindir)
    calcyearlyerr(mydirs,ebefile, startyr)
