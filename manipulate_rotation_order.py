# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 15:33:58 2022

@author: mugalsamrat.dahal
"""

######## This file copys all files from a folder ##############

### except slope file is brought from different folder, change it to two ofes and slope length is modified ###

import os, glob
#### This code will copy files from multiple folders and paste it into other folders after doing some manipulation in run files

ref_dirs = "F:\\WORK\\Project_2\\WEPPwatershed\\after_anisotropy\\New_batch_past_and_present_slope_length_200m"
new_run_dirs = "F:\\WORK\\Project_2\\WEPPwatershed\\after_anisotropy\\New_batch_past_and_present_slope_length_200m"
cli_input_dirs = "F:\\WORK\\Project_2\\WEPPwatershed\\after_anisotropy\\New_batch_past_and_present_slope_length_200m"
# slope_input_dirs = "F:\\WORK\\Project_2\\save\\after_change_in_csa_mcl"
scenario_list = os.listdir(ref_dirs)
mj_inp_list = ["springcreek_past_altrot","upper_imbler_creek_altrot","winn_lake_canyon_altrot"]
# mj_inp_list = ["springcreek","upper","winn"]
module_dir = "C:\\Users\\mugalsamrat.dahal\\OneDrive - Washington State University (email.wsu.edu)\\Paper2\\Weppwatershed"
os.chdir(module_dir)
from copy_files import copyfiles
from converttotwoOFEslope import convslps
from convert_slopelength import change_sl
from chng_rot_order_sing_dir import chng_rot_ord

def wordfinders(lista, worda):
    for a in lista:
        if a == worda:
            val = True
            break
        else:
            val = False
    return val

  
scena2 = list()
scena_new=list()

s = ['bpw', 'pwb']
u = ['bfw', 'fwb']
w = ['fw']


old_simyears = 39

# for m in scenario_list:
    
#     if (wordfinders(m.split('_'), "present")==True):
        
#         if(wordfinders(m.split('_'), "wf")!=True):
#             scena2.append(m)
#             if(wordfinders(m.split('_'), "springcreek")==True):
                
#                 for j in s:
#                     m2=m+"_"+j
#                     scena_new.append(m2)
            
#             # elif(wordfinders(m.split('_'), "upper")==True):
                
#             #     for j in u:
#             #         m2=m+"_"+j
#             #         scena_new.append(m2)
                    
#             # else:
#             #     for j in w:
#             #         m2=m+"_"+j
#             #         scena_new.append(m2)


# scena_new = ['springcreek_present_intense_bpw',
#  'springcreek_present_intense_pwb',
#  'springcreek_present_notill_bpw',
#  'springcreek_present_notill_pwb',
#  'springcreek_present_reduced_bpw',
#  'springcreek_present_reduced_pwb',
#  'upper_imbler_present_intense_bfw',
#  'upper_imbler_present_intense_fwb',
#  'upper_imbler_present_notill_bfw',
#  'upper_imbler_present_notill_fwb',
#  'upper_imbler_present_reduced_bfw',
#  'upper_imbler_present_reduced_fwb',
#  'winn_lake_canyon_present_intense_fw',
#  'winn_lake_canyon_present_notill_fw',
#  'winn_lake_canyon_present_reduced_fw']





for sce in scena_new:
    #sce = scena_new[1]
    #sce = 'springcreek_present_intense_bpw'
    ##################################
    ####### Create folders ###########
    new_fold = new_run_dirs+"\\"+sce
    wepp_fold = new_fold+"\\wepp"
    run_fold = wepp_fold+"\\runs"
    output_fold = wepp_fold+"\\output"
    
    
    fctrs = sce.split('_')
    alrt = fctrs[len(fctrs)-1]
    oldsce = '_'.join(fctrs[0:len(fctrs)-1])
    
###### This small chunk will decide the number of years that is to be added in the file #####

    if(alrt=='bpw'):
        n_years = 1
    elif(alrt=='pwb'):
        n_years = 2
    elif(alrt=='bfw'):
        n_years = 1
    elif(alrt=='fwb'):
        n_years = 2
    else:
        n_years = 1

##############################################################################################   
    
    
    
    
    if not os.path.isdir(new_fold):
        os.makedirs(new_fold)
    if not os.path.isdir(wepp_fold):
        os.makedirs(wepp_fold)
    if not os.path.isdir(run_fold):
        os.makedirs(run_fold)
    if not os.path.isdir(output_fold):
        os.makedirs(output_fold)
    #################################
    #################################
    
    
        
    read_dirs = ref_dirs+"\\"+oldsce+"\\wepp\\runs"
    writedir = run_fold
    
    new_simyears = old_simyears + n_years
    
    
    
    copyfiles(read_dirs, writedir, 'rs', False)
    # convslps(slpdir2, writedir)
    


    chng_rot_ord(writedir, writedir, n_years, new_simyears)

    