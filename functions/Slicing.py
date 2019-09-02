# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 09:57:14 2019
@author: jiarongw
"""

import numpy as np
import scipy.interpolate
import os
from tqdm import tqdm
import pickle
import matplotlib.pyplot as plt

'''
###############################################################################
# A class for slicing through space and perform calculation
###############################################################################
'''

class SlicingInterp:
    '''
    Class for slicing of a bulk data. Takes in a field.
    '''
    
    def __init__(self, field_data, dimension, axis_handle = None):
        '''
        Parameters
        ----------

        field_data : dataframe
            A set of data containing the position vector (x,y,z) and other 
            vector or scalar fields (ux,uy,uz,omega,f...), already parsed into
            a dictionary format. The order has to be (x,y,z) plus other fields.       
		
		dimension : integer, either 2 or 3
			A "macro" that of either 2D or 3D.
        
        axis_handle : handle 
            Handle to the plot for visualization.        
        '''     

        self._axis = axis_handle
        self._dimension = dimension
        self._field_data = field_data
        if self._dimension == 2:
        	self._pos = field_data[["x", "y"]]
        else:
        	self._pos = field_data[["x", "y", "z"]]
            
    def basic(self, direction, base, clearance, header):
        '''
        The most basic function that returns the other two coordinate and desired field of the slice.
        '''
        headers = ['x', 'y', 'z', header]
        headers.remove(direction)
        field_2D = self._field_data[(self._field_data[direction]>(base-clearance))&
                                    (self._field_data[direction]<(base+clearance))][headers]
        return field_2D
    

    def average(self, direction, base, clearance = 1e-8, header = None):
        '''
        For average a quantity across the plan, e.g. velocity.

        direction : string
            "x" or "y" or "z"

        base : float
            The value of coordinate speified in direction that completely 
            determines the plane. (Currently only able to do ones aligned with
            the coordinate.)

        clearance : float, optional, default 1e-8
            Tolerance as criteria to include points that are close enough to 
            the designated plane.    	

        header : a list of keys or a single key
            The desired field to perform the average.

        Return the averaged single value.
        '''
        a = self._field_data[(self._field_data[direction]>(base-clearance))&(self._field_data[direction]<(base+clearance))][header]
        aver = np.average(a)
        # fluctuation amplitude
        fluc = np.std(a)**2
        number = len(a)
        return (aver,fluc,number)
        # def func2():

        # '''
        # Define different drawing and plotting functions. More can be added later.
        # '''

        # def drawing1():

        # 	return line1 # return the line so that the legend can be specified

        # def drawing2():
