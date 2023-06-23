# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 13:41:40 2022

@author: mugalsamrat.dahal
"""

import os
import datetime
from datetime import date, timedelta
#os.getcwd()
import glob
import pandas as pd
import numpy as np
#os.getcwd()
#os.chdir("C:\\Users\\mugalsamrat.dahal\\OneDrive - Washington State University (email.wsu.edu)\\Paper2\\Weppwatershed")
#os.chdir("F:\WORK\Project_2\WEPPwatershed\\springflatcreek\\wepp\\output")
#os.chdir("F:\\WORK\\Project_2\\WEPP_runs\\WEPPrun\\Two_ofe\\past\\scratch\\finsum")

os.chdir('/Users/mcluffy/OneDrive - Washington State University (email.wsu.edu)/Paper2/Weppwatershed')
files = glob.glob("*_large_grph_2.txt")

f = files[0]

mytable = pd.read_table(f, delim_whitespace= True, header=None, skiprows=121)

#### Need to cut out last two rows from this ############


########################################################


ofeno = [1,2]*len(mytable)

sdate = datetime.date(1989,1,1)
edate = datetime.date(2018,12,31)
datedf = pd.date_range(sdate,edate-timedelta(days=1),freq='d').strftime('%Y-%m-%d')

datedf = pd.DataFrame(datedf, columns=["date"])

x = [str(x) for x in datedf["date"]]

datedf = pd.DataFrame([i.split('-') for i in x], columns = ["Year", "Month","Day"])


