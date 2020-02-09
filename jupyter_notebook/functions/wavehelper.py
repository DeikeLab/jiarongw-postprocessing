'''
###############################################################################
# A class for wave properties
# Requirements:
# from scipy.optimize import fsolve
###############################################################################

'''

import numpy as np
import math
from matplotlib import pyplot as plt
from scipy.optimize import fsolve

class RealWave:
    '''
    Class for calculating a set of physical properties and non-dimensional numbers
    of a monochromic wave given some quantities. All the quantities 
    are in SI units.
    '''
    
    def __init__(self, g = 9.8, sigma = 0.074, rho = 1000, rho_air = 1.225):
        '''
        Parameters
        ----------

        g : gravity acceleration (m/s^2)  
        sigma : surface tension of water/air interface (N/m)
        rho : density of water (kg/m^3)
        rho_air : density of air
        
        self.k : wave number (1/m)
        self.omega : wave frequency (1/s)
        self.c : phase speed (m/s)
        self.wl : wavelength (m)
        self.Bo : Bond number 
        
        '''
        self.g, self.sigma, self.rho, self.rho_air = g, sigma, rho, rho_air
        self.k, self.omega, self.c, self.wl, self.Bo = 0, 0, 0, 0, 0
        
    def k2omega(self,k):
        self.k = k
        # Gravity-capillary wave dispersion relation
        self.omega = (self.g*self.k + self.sigma*self.k**3/self.rho)**0.5
        self.c = self.omega/self.k
        self.wl = 2*np.pi/self.k
        self.Bo =  (self.rho-self.rho_air)*self.g/self.sigma/self.k**2
        print("Given k = %g (1/m), calculated omega = %g (1/s), phase speed c = %g (m/s), wavelength = %g (m), Bo = %g" 
              %(self.k, self.omega, self.c, self.wl, self.Bo))

    # Implicit function of w(k)
    def omega2k(self,omega):
        self.omega = omega
        k = fsolve(lambda k : (self.g*k + self.sigma*k**3/self.rho)**0.5 - omega, 0)
        self.k = k[0]
        self.c = self.omega/self.k
        self.wl = 2*np.pi/self.k
        self.Bo =  (self.rho-self.rho_air)*self.g/self.sigma/self.k**2
        print("Given omega = %g (1/s), calculated k = %g (1/m), phase speed c = %g (m/s), wavelength = %g (m), Bo = %g" 
              %(self.omega, self.k, self.c, self.wl, self.Bo))
              
    # If Bond number is given instead of k
    def Bo2k(self,Bo):
        self.Bo = Bo
        self.k = ((self.rho-self.rho_air)*self.g/Bo/self.sigma)**0.5
        self.wl = 2*np.pi/self.k
        self.omega = (self.g*self.k + self.sigma*self.k**3/self.rho)**0.5
        self.c = self.omega/self.k
        viscosity = 8.9*10**(-7)
        self.Re = self.c*self.wl/viscosity        
        c_simu = (1/2/np.pi*(1+1/Bo))**0.5
        self.Re_nominal = self.Re/c_simu
        print("Given Bo = %g, calculated lambda = %g (m), k = %g (1/m), omega = %g (1/s), phase speed c = %g (m/s)" 
              %(self.Bo, self.wl, self.k, self.omega, self.c))
        print("Re = %g, c in simulation is %g. Reynolds number that should be passed in is %g" %(self.Re, c_simu, self.Re_nominal))
        