# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 12:12:21 2022

@author: mugalsamrat.dahal
"""





def yearly_agg_watershed(mydir, wateryear=True):
    import os
    import pandas as pd
    from datetime import datetime, timedelta, date
    from determine_wateryear import determine_wateryear
    '''
    This function aggregates the total watershed data into year by year by both water year and year by year.
    
    mydir: The directory where the total watershed file is located
    wateryear: Boolean, True if wateryear aggregation needs to be done.
    
    '''
    
    # from datetime import datetime, timedelta, date
    # from determine_wateryear import determine_wateryear
    file ="totalwatsed.txt"
    
    names = ['Julian', 'Year', 'Area (m^2)', 'Precip Vol (m^3)', 'Rain + Melt Vol (m^3)',
               'Transpiration Vol (m^3)', 'Evaporation Vol (m^3)', 'Percolation Vol (m^3)',
               'Runoff Vol (m^3)', 'Lateral Flow Vol (m^3)', 'Storage Vol (m^3)', 'Sed. Det. (kg)',
               'Sed. Dep. (kg)', 'Sed. Del (kg)',
               'Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5']
    
    df = pd.read_table(mydir+"\\"+file, delim_whitespace=True, names= names)
 
    ######### This chunk includes the wateryear into the main dataframe #######################
    # df['WY'] = 'NA'
    # df['Month'] = 'NA'
    # df['Day'] = 'NA'

    
    # for i in range(0,len(df)):
    #     ### Use Julian day -1 because this function assums julian day starts from 0
    #     df['WY'][i] = determine_wateryear(int(df['Year'][i]),int(df['Julian'][i]-1))[0] 
    #     ##################################################################################
    #     df['Month'][i] = determine_wateryear(int(df['Year'][i]),int(df['Julian'][i]-1))[1]
    #     df['Day'][i] = determine_wateryear(int(df['Year'][i]),int(df['Julian'][i]-1))[2]
        
    
    chnge = df[['Year','Julian']].apply(pd.to_numeric, errors='coerce', axis =1)
    df['WY']  = chnge.apply(lambda x: determine_wateryear(x['Year'], x['Julian']-1)[0], axis = 1)
    df['Month']  = chnge.apply(lambda x: determine_wateryear(x['Year'], x['Julian']-1)[1], axis = 1)
    df['Day']  = chnge.apply(lambda x: determine_wateryear(x['Year'], x['Julian']-1)[2], axis = 1)
    ####################################################################################################################    
    
    
    val_in_mm = round((df[['Precip Vol (m^3)', 'Rain + Melt Vol (m^3)',
                          'Transpiration Vol (m^3)', 'Evaporation Vol (m^3)', 'Percolation Vol (m^3)',
                          'Runoff Vol (m^3)', 'Lateral Flow Vol (m^3)', 'Storage Vol (m^3)']]/df['Area (m^2)'].unique()[0])*1000,2)
    
    
    val_names = [(i.replace('m^3','mm')) for i in ['Precip m^3)', 'Rain + Melt (m^3)',
                          'Transpiration (m^3)', 'Evaporation (m^3)', 'Percolation (m^3)',
                          'Runoff (m^3)', 'Lateral Flow (m^3)', 'Storage (m^3)']]
    
    
    val_in_mm.columns = val_names
    
    sed_cols = round((df[['Sed. Det. (kg)','Sed. Dep. (kg)', 'Sed. Del (kg)']]/df['Area (m^2)'].unique()[0])*10,2)
    
    sed_cols.columns = ['Sed. Det. (t/ha)','Sed. Dep. (t/ha)', 'Sed. Del (t/ha)']
    
    new_df = pd.concat([df[['Julian', 'Year','WY','Month','Day']],val_in_mm,sed_cols], axis = 1)
    
    if wateryear==True:
        agg_year = 'WY'
    else:
        agg_year = 'Year'
    
    new_agg_sediments = new_df.groupby([agg_year])['Sed. Det. (t/ha)','Sed. Dep. (t/ha)', 'Sed. Del (t/ha)'].sum()
    new_agg_waterbal = new_df.groupby([agg_year])[list(val_in_mm.columns)].sum()
    finlist = [new_agg_sediments, new_agg_waterbal]
    
    return finlist


if __name__ == "__main__":
    maindir = 'C:\\Users\\mugalsamrat.dahal\\OneDrive - Washington State University (email.wsu.edu)\\Paper2\\Weppwatershed'
    mydir = "F:\\WORK\\Project_2\\WEPPwatershed\\springflatcreek2\\wepp\\output"
    os.chdir(maindir)
    yearly_agg_watershed(mydir)
