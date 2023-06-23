# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 15:57:57 2022

@author: mugalsamrat.dahal
"""
import os
import glob
import pandas as pd
#import numpy as np

### Convert slope file into two different OFEs
#readdir = "F:\\WORK\\Project_2\\save\\Saved_watershed\\closing-marquetry\\wepp\\runs"
#writedir = "F:\\WORK\\Project_2\\WEPPwatershed\\springflatcreek\\wepp\\runs"

def convslps(readdir,writedir):
    os.chdir(readdir)
    #os.getcwd()
    
    slplist = glob.glob("*.slp")
    
    def mysolfunct(x):
        b='w' in list(x)[1]
        return not b
    
    c=[mysolfunct(x) for x in slplist] 
    
    from itertools import compress
    nslps=list(compress(slplist,c))
    
    def interpol(x1,x2,y1,y2,x):
            '''calculates interpolation using two points of x & y coordinates'''
            y = round(y1 + (x-x1)*((y2-y1)/(x2-x1)),4)
            return y 
    
    
    for slopnm in nslps:
    
        m = open(slopnm, 'r')
        my = m.readlines()
        slplen = float(my[3].split(" ")[1]) ## This is slope length
        nps =  float(my[3].split(" ")[0]) ## number of points in the slope
        slppnts = my[4].split(", ")
        
        slppnt2 = list()
        for p in slppnts:
            t = p.split(" ")
            for a in t:
                slppnt2.append(a)    
        
        slppnt2.remove('')
        
        ldist=list()
        lslp = list()
        for n in range(0,(len(slppnt2)-1)):
            if n%2==0:
                ldist.append(slppnt2[n])
                lslp.append(slppnt2[n+1])
        
        
        slppnt3 = [list(x) for x in zip(ldist,lslp)]
        slparr = pd.DataFrame(slppnt3, columns=['dist', 'slope'])
        
        #### This part will find the minimum absolute value ###########
        diff = list()
        for v in ldist:
            s = abs(float(v) - 0.50)
            diff.append(s)
        ######################################################
        ####### Use the minimum value to identify the number in the middle
        for m in range(0,(len(diff)-1)):
            if diff[m]-min(diff)==0:
                minind = m
                break
        ############################################################
        ### Now use the middle value to create a middle slope point #######
        
        ldist = [round(float(i),4) for i in ldist]
        lslp = [round(float(i),4) for i in lslp]
        middis = 0.50
        mid_slop = interpol(ldist[minind], ldist[minind+1],lslp[minind], lslp[minind+1],middis)
        #############################
        
        ### join distance and slope values ###
        slppnt4 = [list(x) for x in zip(ldist,[str(i) for i in lslp])]
        
        ### separate ofe 1 and 2
        ##add midpoint values
        
        ###### Some times the point closest to minimum value can fall closer to 
        ##### ofe 2, in that case there needs to be a guard
        ###so that value greater than 0.5 is not appenede to ofe 1
        
        
        if slppnt4[minind][0]>0.50:
            ofe1 = slppnt4[0:minind]
            ofe2 = slppnt4[minind:(len(ldist)+1)]
            minind = minind-1 ## if this condition is fulfill there is a new minind
        else:
            ofe1 = slppnt4[0:minind+1]
            ofe2 = slppnt4[(minind+1):(len(ldist)+1)]
        if ofe1[minind][0] < 0.50:  ### If there is already a 0.50 than i dont have to append to the top ofe
            ofe1.append([0.50, str(mid_slop)])
        ofe2.insert(0, [0.50, str(mid_slop)])
        
        ### Need to change the distance from top values 
        ##now that ofe is broken into 2
        ldistleno1 = [i[0]*slplen for i in ofe1]
        ldistleno1 = [str(round(i/(slplen/2),4)) for i in ldistleno1]
        np_ofe1 = len(ldistleno1)
        
        ldistleno2 = [i[0]*slplen for i in ofe2]
        ldistleno2 = [str(round(((i-(slplen/2))/(slplen/2)),4)) for i in ldistleno2]
        np_ofe2 = len(ldistleno2)
        
        joiner1 = " "
        joiner2 = ", "
        
        #### dissolve the list and prepare for slope file
        
        newofe1 = [list(x) for x in zip(ldistleno1,[i[1] for i in ofe1])]
        newofe1 = joiner1.join([joiner2.join(i) for i in newofe1])
        newofe2 = [list(x) for x in zip(ldistleno2,[i[1] for i in ofe2])]
        newofe2 = joiner1.join([joiner2.join(i) for i in newofe2])
        
        npandlen_ofe1 = str(np_ofe1)+" "+str(round(slplen/2,4))+"\n"
        npandlen_ofe2 = str(np_ofe2)+" "+str(round(slplen/2,4))+"\n"
        
        my[1]='2\n'  ## change number of ofe paramter
        
        my[3] = npandlen_ofe1 ## change parameter slope length and points
        my[4] = newofe1+"\n" ## replace new values
        my.append(npandlen_ofe2)
        my.append(newofe2)
        
        myfile = open(writedir+"\\"+slopnm, "w+")
        myfile.writelines(my)
        myfile.close()


