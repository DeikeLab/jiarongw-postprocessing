# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 16:53:26 EDT 2019
@author: jiarongw
"""

import numpy as np
import pandas as pd
import scipy.interpolate
import os
from tqdm import tqdm
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
    
    def ensemble_aver_quantity(self, formula, type_ = 'scalar'):
        '''
        Take a measure in fieldset. Pass it to a function. Get the operation done (by a separate function that 
        this function has nothing to do with). Return a quantity. Iterate and average through fieldset. Assemble 
        that quantity along desirable axis, usually normal to the wall.
        
        formula: function
            The function to compute a certain quantity.
        type_: string
            Either 'scalar' or 'array in y'
        '''
        
        # Initiate differently with different types of averaged quantities
        if type_ == 'scalar':
            aver = 0
        elif type_ == 'array in y':
            aver = np.zeros(len(self.y))
            
        for i in tqdm(range(0, self.N)):
            # The return value from formula should be of the same dimension with aver
            sample = formula(self.fieldset[i].copy())
            aver += sample
        aver = aver / self.N
        return aver
    
        
    # Function performed on averaged quantities
#     def law_wall_fit(self, ):
#         numpy.polyfit(numpy.log(x), y, 1)