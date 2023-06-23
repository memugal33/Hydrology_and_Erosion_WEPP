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
def change_aniso(readdir, writedir, an_rto, solflg):
    
    os.chdir(readdir)
    sollist = glob.glob("*.sol")
    def mysolfunct(x):
        b='w' in list(x)[1]
        return not b
    
    c=[mysolfunct(x) for x in sollist]
    
    from itertools import compress
    nsols=list(compress(sollist,c))    
    sa = "\t"
    for solnm in nsols:
        #solnm = sollist[1]
        solr = open(solnm, 'r')
        my = solr.readlines()
        for m in range(1,len(my)):
            #m=53
            if my[m-1] == "7778\n":
                # my[m+1]= str(ofeno)+' 1\n'
                value_mat = my[(m+2):(len(my))]
                soil_det = value_mat[0].split(sa)
                numvv = len(soil_det)
                lnumb = 6 ### when you count from the back this is where the number of layer value normally is (unless if the soil file dont have the Ksurf)
                if solflg > 0:
                    numvv = numvv + 1
                n_layers = int(soil_det[numvv-lnumb-1])
                for k in range(0,len(value_mat)):
                    #k=2
                    nmat = len(value_mat[k].split(sa))
                    if(nmat<4):

                        for layers in range(1,(n_layers+1)):
                            #layers = 2
                            if layers == 1:
                                ani_val = an_rto
                            else:
                                ani_val = 1.0
                                
                            mod_mat = value_mat[k-layers].split(sa)
                            ls = len(mod_mat) - 1
                            mod_mat[ls-7] = '  ' + str(ani_val)
                            mod_mat = sa.join(mod_mat)
                            value_mat[k-layers] = mod_mat
                
                my[(m+2):(len(my))] = value_mat
                # my[len(my)-1] = my[len(my)-1]+"\n"
                # l1 = my[m+2:(len(my))]
                # for nof in range(1,ofeno):
                #     for ind in range(0,(len(l1))):
                #         my.append(l1[ind])
                # break
        #my.append(l1)
        myfile = open(writedir+"\\"+solnm, "w+")
        myfile.writelines(my)
        myfile.close()


if __name__ == "__main__":
    
    readdir = "F:\\WORK\\Project_2\\WEPPwatershed\\after_anisotropy\\springcreek_past\\wepp\\runs"
    writedir = "F:\\WORK\\Project_2\\WEPPwatershed\\after_anisotropy\\springcreek_past\\wepp\\runs"
    an_rto = 5.0
    change_aniso(readdir, writedir, an_rto)
    
    
