# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 09:42:48 EDT 2019
@author: jiarongw
"""

import numpy as np
import pandas as pd
import scipy.interpolate
import os
import pickle
import matplotlib.pyplot as plt
from scipy import signal

'''
###############################################################################
# A class for dealing with amplitude
###############################################################################
'''

class Amplitude:
    '''
    Class for analyzing the interface elevation. Instantiation takes the eta data.
    
    self._eta_data: dataframe
        The complete dataframe, sorted by value of x.
    self.eta: 1D array
        Only the amplitude info without coordinate.
    self.stdev: float
        Standard deviation of amplitude. Calculated by std = sqrt(mean(abs(x - x.mean())**2)).
    self.phase: float
        Given a certian elevation profile, there should be a 
            
    '''
    
    def __init__(self, eta_data):
        '''
        eta_data : dataframe
            A set of data containing the position x, interface elevation eta, and scalar fraction
            field f. The corresponding keywords are ['x', 'eta', 'f']. f is used for filtering out 
            stand alone little points.
            Later a 3D feature might be added.
        '''   
        # A clean-up process
        # First filter out points with extreme values of f (tolerance can be adjusted)
        # Then sort the array according to position x
        tol = 1e-5
        self._eta_data = eta_data.loc[(eta_data.f > tol) & ((1-eta_data.f) > tol)]
        self._eta_data = self._eta_data.sort_values(by = ['x'])
        self.eta = eta_data['eta'].values
        if np.any(self.eta): # prevent an all zero array as it happens sometimes
            self.stdev = np.std(self.eta)
        else:
            self.stdev = 0                
    
    # A plotting function
    def plot(self, ax, label_choice, color_choice):
        ax.plot(self._eta_data.x, self._eta_data.eta, label = label_choice, color = color_choice)
        
    def phase(self):
        phase = 0
        '''
        There is a uniquely determined phase for a given amplitude profile
        '''

    def spectrum(self, direction, base, clearance, header):

            Fs = 2048;  # sampling rate
            Ts = 1.0/Fs; # sampling interval
            x = np.arange(-0.5,0.5,Ts) # space vector

            y = np.interp(x, interface.x, interface.pos)
            n = len(y) # length of the signal
            k = np.arange(n)
            T = n/Fs
            frq = k/T # two sides frequency range
            frq = frq[0:int(n/256)] # one side frequency range
            Y = np.fft.fft(y)/n # fft computing and normalization
            Y = Y[0:int(n/256)]

            ax[0].plot(x, y*2*3.14, label = 't = %.0f' %i, color=plt.cm.get_cmap('summer')(color_idx[(i-start)//M]))

    #         t_smooth = t[0::20]
    #         y_smooth = spline(t, y, t_smooth)
    #         ax[0].plot(t_smooth, y_smooth, label = 't = %.0f' %(i/100), color=plt.cm.get_cmap('summer')(color_idx[i]))
            ax[0].set_xlabel('Time')
            ax[0].set_ylabel('Amplitude')
            ax[0].legend()
            ax[1].plot(frq, abs(Y), label = 't = %.0f' %i, color=plt.cm.get_cmap('summer')(color_idx[(i-start)//M])) # plotting the spectrum
            ax[1].set_xlabel('Wavenumber')
            ax[1].set_ylabel('|Y(Wavenumber)|')
            ax[1].legend()
            fig.show()
