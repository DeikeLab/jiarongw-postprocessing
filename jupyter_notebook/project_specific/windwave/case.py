# -*- coding: utf-8 -*-
""" Case class that registers one single 2D windwave case. """

import os
import numpy as np
from helper import fields, interface, fields_original, from_matrix, RealWave
# Dependent on utility functions from util.py
from util import spectrum_filter, u_partition, capi_energy, water_profile

class Case:
    """Each single 2D windwave run.

    Attributes:
        availt: The longest running time.
        path: Path of the case file.
    """

    def __init__(self, ustar, ak, Bo, Re, LEVEL, L0=1., g=1., k=2.*np.pi, 
                 working_dir='/home/jiarong/research/projects/windwave/', prefix='linear_m5B0', PRINTWAVE = False):
        """Inits case with all the parameters and path prefix. """      
        # Register the metadata and spell the path
        self.ustar = ustar; self.ak = ak; self.Bo = Bo; self.Re = Re; self.LEVEL = LEVEL; self.L0 = L0; self.g = g; self.k = k
        self.rho1 = 1; self.rho2 = 1./850.
        self.path = working_dir + prefix + 'Ustar%gak%gBo%gRe%g.LEVEL%g' %(ustar,ak,Bo,Re,LEVEL) 
        # Run wave helper function to compute wave related info
        # Notice that this depends on the definition of the wave in the specific set of cases
        self.wave = RealWave(g = self.g, sigma = self.g/(self.Bo*self.k**2), rho = 1, rho_air = 1.225*10**(-3),mu = 1./self.Re,
                             mu_air = 1./self.Re/8.9e-4*17.4e-6)
        self.wave.k2omega(self.k)
        # Detect the available time
        for i in range (0,32*10):
            self.availt = 320
            exists = os.path.exists(self.path+'/matrix/u%g.dat' %(i/32.))
            if not exists:
                self.availt = i
                break
        # Print out wave info
        if PRINTWAVE:
            print("Given k = %g (1/m), calculated omega = %g (1/s), period = %g (s), "
                  + "phase speed c = %g (m/s), wavelength = %g (m), Bo = %g"
                  %(self.wave.k, self.wave.omega, 2*np.pi/self.wave.omega, self.wave.c, self.wave.wl, self.Bo))
                
    def drift_evolution(self):
        self.t = np.zeros(self.availt)
        self.drift_max = np.zeros(self.availt)
        for i in range(0, self.availt):
            self.t[i] = i/32.
            u_water, u_water_interp, u_water_1D, ygrid = water_profile(self.t[i],self.path,self.L0)
            self.drift_max[i] = np.max(u_water_1D)
    
    # Filter out the backward traveling wave and register the filtered time-space sequence 
    # If filtering = False
    # N_padding might need to be tweaked
    # N_point is the size of the eta array
    def spectrum_filtering(self, N_time = 96, N_padding = 9, N_point = 32, WINDOW = True):
        eta_series = []
        t = np.zeros(N_time)
        for i in range (0,N_time):
            t[i] = i/32.
            ampl = interface(self.path, Npoint=N_point, L0=self.L0, time=t[i])
            # Subtract the spatial avarage which does not change much
            eta_series.append(ampl.eta_interp-np.average(ampl.eta_interp)) 
        # kx = np.fft.fftfreq(n=N_point,d=1/N_point); 
        # komega = np.fft.fftfreq(n=N_total,d=1/32); 
        self.eta_unfiltered = np.array(eta_series)
        eta1,eta2,spectrum1,spectrum2 = spectrum_filter(eta_series = self.eta_unfiltered, N_padding = N_padding, WINDOW = WINDOW)
        self.eta_filtered = np.copy(np.real(eta1[N_padding:N_padding+N_time,:]))
        return eta1,eta2,spectrum1,spectrum2
    
    # Compute the velocity partition at a certain time t
    # Default compute stokes without capillary modification
    # Has to come after eta_filtered has been computed or use the unfiltered version
    def call_partition(self,t_index,FILTERING=True,CAPI=False):
        N = 512 # Can change or be passed as a parameter but seems unnecessary
        if FILTERING:
            ugroup_snapshot = u_partition(self.path, t_index/32, self.eta_filtered[t_index], 
                                          Bo = self.Bo, L0 = self.L0, N = N, CAPI=CAPI)
        else:
            ugroup_snapshot = u_partition(self.path, t_index/32, self.eta_unfiltered[t_index], 
                                          Bo = self.Bo, L0 = self.L0, N = N, CAPI=CAPI)    
        return ugroup_snapshot
        
    def plot_drift_filtered(self, ax):
        line1, = ax.plot(self.t,self.ke_drift,label='Bo=%g,Re=%g,Ustar=%g' %(self.Bo,self.Re,self.ustar))
        line2, = ax.plot(self.t,self.da*self.t+self.db,'--',label='%.4f t + %.4f' %(self.da,self.db), 
                         color=ax.lines[-1].get_color())
        return line1,line2
    
    def plot_wave_filtered(self, ax):
        line1, = ax.plot(self.t,self.energy_wave,label='Bo=%g,Re=%g,Ustar=%g' %(self.Bo,self.Re,self.ustar), linewidth = 0.5)
        line2, = ax.plot(self.t,np.exp(self.wa*self.t+self.wb),'--',label='exp(%.2f t + %.2f)' %(self.wa,self.wb), 
                         color=ax.lines[-1].get_color())
        return line1,line2
    
    def growth_rate(self,N_time,CAPI=False):
        N = 512 # Should match N in call_partition
        self.t = np.zeros(N_time)
        self.pe_g = np.zeros(N_time); self.pe_s = np.zeros(N_time)
        self.ke_wave = np.zeros(N_time)
        self.ke_drift = np.zeros(N_time)
        for i in range (0,N_time):
            self.t[i] = i/32
            if CAPI:
                u_group = self.call_partition(i, CAPI=True)
                self.pe_g[i], self.pe_s[i] = capi_energy(self.eta_filtered[i,:], self.rho1*self.g/(self.Bo*self.k**2), 
                                                         g=self.g, L0=self.L0)
            else:
                u_group = self.call_partition(i, CAPI=False)
                self.pe_g[i] = np.std(self.eta_filtered[i,:])**2/2*self.g*self.L0
                self.pe_s[i] = 0
            self.ke_wave[i] = np.sum(u_group[1]**2 + u_group[3]**2)/N**2/2
            self.ke_drift[i] = np.sum(u_group[2]**2)/N**2/2
            self.pe_wave = self.pe_g + self.pe_s
            self.energy_wave = self.ke_wave + self.pe_wave
        self.wa, self.wb = np.polyfit(self.t[1:], np.log(self.energy_wave[1:]), 1)
        self.da, self.db = np.polyfit(self.t[1:], self.ke_drift[1:], 1)
    
    def growth_rate_notfiltered(self, N_time, CAPI=False):
        """Compute growth with unfiltered surface evolution.""" 
        N = 512 # Should match N in call_partition
        self.t = np.zeros(N_time)
        self.pe_g = np.zeros(N_time); self.pe_s = np.zeros(N_time)
        self.ke_wave = np.zeros(N_time)
        self.ke_drift = np.zeros(N_time)
        for i in range (0,N_time):
            self.t[i] = i/32
            if CAPI:
                u_group = self.call_partition(i, CAPI=True, FILTERING=False)
                self.pe_g[i], self.pe_s[i] = capi_energy(self.eta_unfiltered[i,:], self.rho1*self.g/(self.Bo*self.k**2),
                                                         g=self.g, L0=self.L0)
            else:
                u_group = self.call_partition(i, CAPI=False, FILTERING=False)
                self.pe_g[i] = np.std(self.eta_unfiltered[i,:])**2/2*self.g*self.L0
                self.pe_s[i] = 0
            self.ke_wave[i] = np.sum(u_group[1]**2 + u_group[3]**2)/N**2/2
            self.ke_drift[i] = np.sum(u_group[2]**2)/N**2/2
            self.pe_wave = self.pe_g + self.pe_s
            self.energy_wave = self.ke_wave + self.pe_wave
        self.wa, self.wb = np.polyfit(self.t[1:], np.log(self.energy_wave[1:]), 1)
        self.da, self.db = np.polyfit(self.t[1:], self.ke_drift[1:], 1)
        