# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 09:57:14 2019
@author: jiarongw
"""

import numpy as np
import scipy.interpolate
import os
import pickle
import matplotlib.pyplot as plt
import sys
sys.path.append('/home/jiarong/research/postprocessing/functions/')
from visualization import contour, scatter


'''
###############################################################################
# A class for slicing through space and perform calculation
###############################################################################
'''

class Slicing:
    '''
    Class for slicing of a bulk data. Takes in a field.
    '''
    
    def __init__(self, field_data, dimension):
        '''
        Parameters
        ----------

        field_data : dataframe
            A set of data containing the position vector (x,y,z) and other 
            vector or scalar fields (ux,uy,uz,omega,f...), already parsed into
            a dictionary format. The order has to be (x,y,z) plus other fields.       
		
		dimension : integer, either 2 or 3
			A "macro" that of either 2D or 3D.
             
        '''     
        
        self._dimension = dimension
        self._field_data = field_data.copy() # Making a copy so that only the value is passed
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
    

    
    def statistics(self, direction, base, clearance = 1e-8, header = None):
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

    def plot_fluctuation(self, ax, direction, base, clearance = 1e-8, header = None, plotscatter = True, dotsize = 50):
        '''
        ax: handle
        plotscatter: boolean, optional
            Whether to plot scatter or contour. Default is scatter.
        dotsize: float, optional
            Size of scatter dots
        '''
            
        field_slice = self._field_data[(self._field_data[direction]>(base-clearance))&(self._field_data[direction]<(base+clearance))]
        aver = np.average(field_slice[header])
        # Subtract the average
        target = field_slice.copy()
        field_slice[header] = field_slice[header] - np.ones(len(field_slice))*aver
        # Set the plotting coordinate
        coord_slice = ['x', 'y', 'z']
        coord_slice.remove(direction)
        if not plotscatter:
            contour(field_slice, header, ax, coord=coord_slice, coordshow=True)
        else:
            scatter(field_slice, header, ax, coord=coord_slice, coordshow=True, area=dotsize)
        

# Functions that deals with multiple slicing
        
    def get_grid_set(self, direction):
        '''
        Get the grid point in a given direction, with extra restraints (e.g. greater than zero).
        For example for inhomogeneous boundary flow, the most interesting direction is normal to the wall. 
        '''
        sample = self._field_data.drop_duplicates(direction)
        self.grid_set = sample.loc[sample[direction] > 0][direction]