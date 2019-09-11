# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 16:53:26 EDT 2019
@author: jiarongw
"""

import numpy as np
import pandas as pd
import scipy.interpolate
import os
import matplotlib.pyplot as plt
import sys

sys.path.append('/home/jiarong/research/postprocessing/functions/')
from visualization import contour, scatter


'''
###############################################################################
# A class for turbulence statistics
###############################################################################
'''

class TurStat:
    '''
    Class for slicing of a bulk data. Takes in a field.
    '''
    
    def __init__(self, fieldset, tset):
        '''
        Parameters
        ----------

        fieldset : ensemble of field       
		
		t_set : list of time 
        
        N : number of samples
        
        '''     

        self.fieldset = fieldset.copy()
        self.tset = tset.copy()
        self.N = len(self.tset)
        # A check to make sure all the field snapshot
        self.x = self.fieldset[0].x
        self.y = self.fieldset[0].y
        self.z = self.fieldset[0].z
        for f,t in zip(self.fieldset,self.tset):
            if not (pd.Series.equals(f.x,self.x))&(pd.Series.equals(f.y,self.y))&(pd.Series.equals(f.z,self.z)):
                print("t=%g field has wrong sample number!" %t)
        
            
    def ensemble_aver(self):
        '''
        The most basic function that returns the other two coordinate and desired field of the slice.
        '''
        # ALWAYS use copy to avoid changing the dataframe being copied!!!
        self.field_add = self.fieldset[0].copy()
        for i in range(1, self.N):
            # WATCHOUT if an operation takes inplace or not!
            self.field_add = self.field_add.add(self.fieldset[i])
#             self.field_en_aver += self.fieldset[i]   # same effect
        self.field_en_aver = self.field_add/self.N            
    
        
    # Function performed on averaged quantities
#     def law_wall_fit(self, ):
#         numpy.polyfit(numpy.log(x), y, 1)