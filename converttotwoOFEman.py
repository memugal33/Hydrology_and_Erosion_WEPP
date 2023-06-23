# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 15:57:57 2022

@author: mugalsamrat.dahal
"""
import os
import glob
import pandas as pd
#import numpy as np

### Convert management file into two different OFEs
readdir = "F:\\WORK\\Project_2\\WEPPwatershed\\int_sol_cal\\wepp\\runs"
writedir = "F:\\WORK\\Project_2\\WEPPwatershed\\int_2ofes\\wepp\\runs"

ofeno = 2
def convmans(readdir,writedir,ofeno, conv_year, yearno ):
    import math
    '''
    Given the readdir and write dir and ofe no
    
    This function converts the man file to more than one ofe
    
    If conv_year = True (in this case 0)
    
    It also increases the number of years in the management files
    
    If conv_year = True, also provide the number of years in str format
    
    '''
    
    os.chdir(readdir)
   # os.getcwd()
    
    manlist = glob.glob("*.man")
    def mysolfunct(x):
        b='w' in list(x)[1]
        return not b
         
    c=[mysolfunct(x) for x in manlist]
    
    from itertools import compress
    nmans=list(compress(manlist,c))
    for mannm in nmans:
    #mannm = nmans[1]
        manr = open(mannm, 'r')
        my = manr.readlines()
        
        # for mannm in manlist:
        #     #mannm = manlist[1]
        #     manr = open(mannm, 'r')
        #     my = manr.readlines()
        #     for m in range(1,len(my)):
                
        #         if my[m-1] == "7778\n":
        #             my[m+1]='2 1\n'
        #             my[len(my)-1] = my[len(my)-1]+"\n"
        #             l1 = my[m+2:(len(my))]
        #             for ind in range(0,(len(l1))):
        #                 my.append(l1[ind])
        #             break
        #     #my.append(l1)
        #     myfile = open(writedir+"\\"+solnm, "w+")
        #     myfile.writelines(my)
        #     myfile.close()
        
        def word_identifier (lst, strs):
            ret_val = list() 
            for m in range(0,(len(lst)-1)):
                t = lst[m].split(" ")
        #         if m < (len(lst)-1):
                for k in t:    
                        if k == strs:
                            ret_val.append(m)
                        # else:
                        #     ret_val = "NA"
                        
                # if ret_val != "NA":
                #     break
            return ret_val
        #### Replace the no of ofes in the beginning of the file 
        
        rep_ind1 = word_identifier(my, "OFE's\n")[0]
        my[rep_ind1] = str(ofeno)+" # number of OFE's\n"
        #################################################
        ######### This chunck below will ensure addition of new years
        ###################################################
        ##########
        if conv_year==0:
            nyrs = str(yearno)
            my[rep_ind1+1]=str(nyrs)+" # (total) years in simulation\n"
        else:
            nyrs = my[rep_ind1+1].split(" ")[0]
       #######################################################     
        ####### Now find the management section and make replacement systematically
        
        rep_ind2 = word_identifier(my, "OFE's\n")[1]
        
        ### replace number of OFE's 
        my[rep_ind2] = str(ofeno)+" # number of OFE's\n"
        nrotsline = my[rep_ind2+3] ### n years in rotation
        nrots = nrotsline.split(" ")[0]
        if conv_year==0:
            ### This small chunk finds the new number of rotation rep
            ### This also rounds up the number of rotation
            rotrep = str(math.ceil(int(nyrs)/int(nrots)))
            my[rep_ind2+2] = rotrep + " # rotation repeats\n"
        rotrepline = my[rep_ind2+2] ### n rotation repeats
        rotrep = rotrepline.split(" ")[0]
        ####
        
        rotparalist = my[rep_ind2+4: len(my)]
        index_rot = word_identifier(rotparalist, "Rotation")
        
        singrot = rotparalist[(index_rot[0]-1):index_rot[1]]
        
        index_sing_rot = word_identifier(singrot, "<plants/yr")
        
        ########## The chunk below will create a new Rotation chunk for two ofes ####
        ####################
        newsingrot = list()
        flg1 = 0
        for rs in range(0,len(index_sing_rot)):
            indi1 = index_sing_rot[rs]
            if (rs<(len(index_sing_rot)-1)):
                indi2 = index_sing_rot[rs+1]
            else:
                indi2 = len(singrot)-1
                flg1 = flg1+1
            blck1 = singrot[indi1:indi2]
            copyblck1= blck1[1:(len(blck1)-1)] ## This block is repeated every year
            ####### make changes in the first line of each blocks ############
            
            fstline = blck1[0]
            newblck = list()
            for i in range(1,ofeno+1):  
                ls = fstline.split(" ")
                ls[len(ls)-1] = str(i)+"\n" ### This changes first line
                joiner = " "
                newblck.append(joiner.join(ls))
                for k in copyblck1:
                    newblck.append(k) ## This changes other two lines
                if(i<(ofeno)):
                    newblck.append('\n')
            for z in newblck:
                newsingrot.append(z)
            if flg1<1:
                newsingrot.append(singrot[index_sing_rot[1]-1])
        #################################################
        ###################################################
        
        ###### Iterate for number of rotation ####
        
        ## First identify rotation number line
        rotnumchunk = singrot[0:index_sing_rot[0]]
        rotnumlst = rotnumchunk[1].split(" ")
        yrind = word_identifier(rotnumlst, 'Rotation') ### In the above list which index have rotation?
        wholerotlist = list()
        yrinrot = 1
        for y in range(1,(int(rotrep)+1)):
            
            ### This part is not that important but still for clarity sake
            ### changing the Rotation number index inside the commented part
            rotnumlst[yrind[0]+1] = str(y)+":"
            rotnumlst[yrind[0]+3] = str(yrinrot)
            rotnumlst[yrind[0]+5] = str(yrinrot+int(nrots)-1)+"\n"
            #######################################################
            yrinrot = yrinrot+3
            joiner = " "
            newrotnumlst = joiner.join(rotnumlst)
            temp_rotnumchunk = singrot[0:index_sing_rot[0]]
            temp_rotnumchunk[1] = newrotnumlst
            for val in newsingrot:
                temp_rotnumchunk.append(val)
            if y<int(rotrep):
                temp_rotnumchunk.append('\n')
            for val in temp_rotnumchunk:
                wholerotlist.append(val)
        ######################################################################
        
        my2 = my[0:(rep_ind2+1)]
        inicond = my[rep_ind2+1]
        #### Now time to make a new management file and write it
        
        ### This will add new initial condition based on number of ofes
        for i in range(1,ofeno+1):
           my2.append(inicond)
        my2.append(rotrepline)
        my2.append(nrotsline)
        ###### Now need to add my whole rot list at the bottom
        
        for i in wholerotlist:
            my2.append(i)
        
        manr = open(writedir+"\\"+mannm, 'w+')
        manr.writelines(my2)
        manr.close()











