# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 12:23:24 2022

@author: mugalsamrat.dahal
"""

import os
import glob
import numpy as np
import pandas as pd
import docx


###################### Write pd dataframe to document ################
def pdDataframe_to_word(dirs, docname, df):
    '''
    Parameters
    ----------
    dirs : Name of output directory
    docname: Name of new document
    df: dataframe
    
    Given the output directory and dataframe
    This files write a pd dataframe to a word file
    Returns
    -------
    None.

    '''
    docname=dirs+"\\"+docname+"_water balance.docx"
    doc = docx.Document()
    t = doc.add_table(df.shape[0]+1, df.shape[1])
    
    # add the header rows.
    for j in range(df.shape[-1]):
        t.cell(0,j).text = df.columns[j]
    
    # add the rest of the data frame
    for i in range(df.shape[0]):
        for j in range(df.shape[-1]):
            t.cell(i+1,j).text = str(df.values[i,j])
       
    doc.save(docname)
##########################################################################


############### Aggregate water Balance ####################################
def aggregate_water_balance(filename):
    
    '''
    Given the filename this function will return major component of water balance
    
    after aggregation
    
    '''
    mywatdf=pd.read_table(filename, sep= "\s{1,}", skiprows=22, header = None, engine = 'python') ## Separator says spaces greater than 1
    
    mywatnames=pd.read_table(filename, sep= "\s{1,}", skiprows=19, nrows=1, header = None, engine = 'python')
    
    colnames = mywatnames.values.tolist()
    
    mywatdf.columns = colnames[0]
    
    mywatdf.groupby(by = ['Y','OFE']).sum()
    
    mywatdf["E"]= mywatdf["Ep"]+mywatdf["Es"]+mywatdf["Er"]
    
    myaggregate = round(mywatdf.groupby(by = ['Y','OFE'])[["RM","Q","E","Dp","latqcc"]].sum(),2)
    
    return myaggregate

##################################################################################


#########Aggregate change in components ################################
def aggregate_change_in_soilm(filename):
    
    '''
    Given the filename this will return the change in soil moisture
    and change in frozen water
    '''
    mywatdf=pd.read_table(filename, sep= "\s{1,}", skiprows=22, header = None, engine = 'python') ## Separator says spaces greater than 1
    
    mywatnames=pd.read_table(filename, sep= "\s{1,}", skiprows=19, nrows=1, header = None, engine = 'python')
    
    colnames = mywatnames.values.tolist()
    
    mywatdf.columns = colnames[0]
    
    mychangedf = mywatdf[["Y","OFE","J","Total-Soil", "frozwt"]]
    
    years = mychangedf.Y.unique()
    ofes = mychangedf.OFE.unique()
    list_of_changes = list()
    for i in years:
        for j in ofes: 
            #i = years[1]
            #j = ofes[0]
            tempdf = mychangedf[(mychangedf['Y']==i)&(mychangedf['OFE']==j)].reset_index(drop=True)
            chnge_soilwater = round(tempdf['Total-Soil'][len(tempdf)-1]-tempdf['Total-Soil'][0],2)
            chnge_frzwater = round(tempdf['frozwt'][len(tempdf)-1]-tempdf['frozwt'][0],2)
            tlist = [i,j,chnge_soilwater, chnge_frzwater]
            list_of_changes.append(tlist)
            
    mychanges = pd.DataFrame(list_of_changes,
                             columns = ["Year","OFE",
                                        "Change in Soil water",
                                        "Change in Frozen Water"])
    return mychanges
##############################################################################

############# Function execution ##########################################

#############################################################

if __name__ == "__main__":
    
    #dirs = input("Enter the directory")
    #
    #filename = input("Enter the full path of waterbalance file:")
    
    dirs = 'F:\\WORK\\Project_2\\WEPP_runs\\WEPPrun\\One_ofe\\past\\scratch'
    os.chdir(dirs)

    #list_of_file = glob.glob("*wat.dat")
    #filename = list_of_file[1]
    
    filename = "h_Sl_dp_S1_slp_nwbp_wat.txt"
    myaggregate = aggregate_water_balance(filename)
    mychanges = aggregate_change_in_soilm(filename)
    ofes = mychanges.OFE.unique()
    watbal_sheets = pd.merge(myaggregate, mychanges, how="right", left_on=("Y","OFE"),right_on=("Year","OFE"))
    
    for ofe in ofes:
        ####################################################################
        ##### This part processes the water balance to look at yearly error###
        #### It also calculates the overall total and percent change ######
        watbal_sheet=watbal_sheets[watbal_sheets['OFE']==ofe]
        watbal_sheet['Error'] = round(watbal_sheet['RM']-(watbal_sheet['Q']+
                                                    watbal_sheet['E']+
                                                    watbal_sheet['Dp']+
                                                    watbal_sheet['latqcc'])-(
                                                    watbal_sheet['Change in Soil water']+
                                                    watbal_sheet['Change in Frozen Water']),2)
        vals = round(watbal_sheet[['RM','Q','E','Dp',
                             'latqcc','Change in Soil water',
                             'Change in Frozen Water',"Error"]].sum(),2)
        
        pervals = round((vals/vals[0])*100,2)
        
        finsheet = watbal_sheet.append(vals,ignore_index=True).append(pervals, ignore_index=True)
        
        finsheet = finsheet.reindex(['Year','OFE','RM','Q','E','Dp',
                             'latqcc','Change in Soil water',
                             'Change in Frozen Water',"Error"], axis = 1)
        
        #finsheet.to_csv(dirs+"\\"+filename+"water balance.csv",index=False)
        if (ofe==1):
            finsheet2 =  finsheet
        else:
            finsheet2 = pd.concat([finsheet2,finsheet])
        #####################################################################
        #####################################################################
        
    pdDataframe_to_word(dirs, filename, finsheet2)
    #print(finsheet)
    
