import numpy as np
from matplotlib import pyplot as plt
import sys
from helper import fields, interface, fields_original, from_matrix, RealWave
sys.path.append('/home/jiarong/research/postprocessing/jupyter_notebook/functions/')

""" Several utility function. """

# compute mean drift
from scipy.interpolate import interp1d
def water_profile(t,path,L0):
    # Read in the fields
    u_air, u_water, omega_air, omega_water = fields(path, t)
    # Average profile (wave coordinate!)
    u_water_1D_nointerp = np.average(u_water, axis=0)
    u_water_interp = np.zeros(u_water.shape)
    ampl = interface(path, Npoint=512, L0=1, time=t)
    zmax = L0/2 - ampl.eta_interp.max(); zmin = -L0/2 - ampl.eta_interp.min()
    zgrid = np.linspace(zmin, zmax, 512)
    for i in range(u_water.shape[0]):
        z = np.linspace(-L0/2,L0/2,512) - ampl.eta_interp[i]
        f = interp1d(z, u_water[i,:])
        ugrid = f(zgrid)
        u_water_interp[i] = ugrid
    u_water_1D = np.average(u_water_interp[:,:], axis=0)
    return u_water, u_water_interp, u_water_1D, zgrid

def air_profile(t,path,L0):
    # Read in the fields
    u_air, u_water, omega_air, omega_water = fields(path, t)
    # Average profile (wave coordinate!)
    u_air_1D_nointerp = np.average(u_air, axis=0)
    u_air_interp = np.zeros(u_air.shape)
    ampl = interface(path, Npoint=512, L0=1, time=t)
    zmax = L0/2 - ampl.eta_interp.max(); zmin = -L0/2 - ampl.eta_interp.min()
    zgrid = np.linspace(zmin, zmax, 512)
    for i in range(u_air.shape[0]):
        z = np.linspace(-L0/2,L0/2,512) - ampl.eta_interp[i]
        f = interp1d(z, u_air[i,:])
        ugrid = f(zgrid)
        u_air_interp[i] = ugrid
    u_air_1D = np.average(u_air_interp, axis=0)
    return u_air, u_air_interp, u_air_1D

# Compute stokes wave velocity profile
# http://basilisk.fr/src/test/stokes.h but double multiplied ak
# https://www.wikiwand.com/en/Stokes_wave#/Second-order_Stokes_wave_on_arbitrary_depth
def stokes(phase_tile,z_tile,Bo,ak,L0,CAPI=False):
    k_ = 2*np.pi; h_ = L0/2; g_ = 1; rho_ = 1
    sigma_ = 1/(Bo*k_**2)
    # Use modified gravity or not
    if not CAPI:
        g_ = 1.
    else:
        g_ = g_ + sigma_*k_**2/rho_
    alpa = 1./np.tanh(k_*h_)
    a_ = ak/k_
    sgma = ((g_*k_*np.tanh(k_*h_)*(1. + k_*k_*a_*a_*(9./8.*(alpa**2 - 1.)*(alpa**2 - 1.) + alpa**2))))**0.5
    A_ = a_*g_/sgma    
    ux = A_*np.cosh(k_*(z_tile + h_))/np.cosh(k_*h_)*k_*np.cos(phase_tile) 
    + ak*3.*A_/(8.*alpa)*(alpa**2 - 1.)*(alpa**2 - 1.)*np.cosh(2.0*k_*(z_tile + h_))*2.*k_*np.cos(2.0*phase_tile)/np.cosh(2.0*k_*h_) 
    + ak*ak*1./64.*(alpa**2 - 1.)*(alpa**2 + 3.)*(9.*alpa**2 - 13.)*np.cosh(3.*k_*(z_tile + h_))/np.cosh(3.*k_*h_)*A_*3.*k_*np.cos(3.*phase_tile)
    uy = A_*k_*np.sinh(k_*(z_tile + h_))/np.cosh(k_*h_)*np.cos(phase_tile-np.pi/2.) 
    + ak*3.*A_/(8.*alpa)*(alpa**2 - 1.)*(alpa**2 - 1.)*2.*k_*np.sinh(2.0*k_*(z_tile + h_))*np.cos(2.0*phase_tile-np.pi/2.)/np.cosh(2.0*k_*h_) 
    + ak*ak*1./64.*(alpa**2 - 1.)*(alpa**2 + 3.)*(9.*alpa**2 - 13.)*3.*k_*np.sinh(3.*k_*(z_tile + h_))/np.cosh(3.*k_*h_)*A_*np.cos(3.*phase_tile-np.pi/2.)
    return ux,uy

"""
Here the velocity partition is computed.
Input: 
eta - can come from either filtered data or original data

Hilbert transform reference
https://www.youtube.com/watch?v=VyLU8hlhI-I
https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.hilbert.html
https://dsp.stackexchange.com/questions/46291/why-is-scipy-implementation-of-hilbert-function-different-from-matlab-implemen
"""
from scipy.signal import hilbert
def u_partition (path, t, eta, Bo=0.27, L0=1, N=512, CAPI=False): 
    u_air, u_water, omega_air, omega_water = fields(path,t)
    u,f,omega = fields_original(path,t)
    ak = np.std(eta)*2*np.pi*2**0.5
    x_eta = np.linspace(-L0/2,L0/2,np.size(eta),endpoint = False) + L0/np.size(eta)/2
    # Construct mesh (of size N)
    x = np.linspace(-L0/2,L0/2,N,endpoint = False) + L0/N/2
    z = np.linspace(-L0/2,L0/2,N,endpoint = False) + L0/N/2
    eta_interp = np.interp(x, x_eta, eta)
    # Hilbert transformation to get the phase
    analytic_signal = hilbert(eta_interp)
    phase = np.unwrap(np.angle(analytic_signal))
    z_tile, phase_tile = np.meshgrid(z,phase)
    # Linear wave velocity field; a bunch of parameters are specified
    c_ = 0.51713; k_ = 2.*np.pi
    # Using linear relation
#     ux = ak*c_*np.cos(phase_tile)*np.exp(k_*z_tile)
#     uy = ak*c_*np.cos(phase_tile-np.pi/2.)*np.exp(k_*z_tile)
    # Using Stokes wave
    ux,uy = stokes(phase_tile,z_tile,Bo,ak,L0,CAPI)
    ux_irrot = ux
    uy_irrot = uy
    # A different f field computed from interpolated eta
    for i in range(0,N):
        for j in range(0,N):
            if (z_tile[i,j]>=eta_interp[i]):
                ux_irrot[i,j] = 0.
                uy_irrot[i,j] = 0.
    ugroup = (u_water, ux_irrot,u_water-ux_irrot, uy_irrot)
    return ugroup

# Input: 
# eta_series - a real 2d numpy array with dim1 time and dim2 space
# Optional padding point number
# Output: seperated foward traveling eta1 and backward traveling eta2 as time-space 2d array 
def spectrum_filter(eta_series, N_padding = 8, WINDOW = True):
    N_time = eta_series.shape[0] # Number of time snapshots
    N_point = eta_series.shape[1] # Number of horizontal sample points    
    # Add padding so that the hanning window does not cause big changes on both ends 
    N_total = 2*N_padding + N_time
    # Use Hanning window to force ends to zero or not
    if WINDOW:
        window = np.hanning(N_total)
    else:
        window = np.ones(N_total) 
    padded_eta = np.zeros([N_total, N_point])   
    for i in range (0,N_point):
    #     zeropadded_eta[N_zero:N_time+N_zero,i] = eta_series[:,i]-np.average(eta_series[:,i])
        padded_eta[N_padding:N_time+N_padding,i] = eta_series[:,i]
        padded_eta[0:N_padding,i] = eta_series[0,i]*np.ones(N_padding)
        padded_eta[N_padding+N_time:,i] = eta_series[-1,i]*np.ones(N_padding)
        padded_eta[:,i] = padded_eta[:,i]*window
    spectrum = np.fft.fftn(padded_eta)
    # Separate the quadrants of the 2D spectrum
    spectrum1 = np.zeros(spectrum.shape); spectrum1 = spectrum1.astype(complex)
    N_half1 = np.int(N_total/2); N_half2 = np.int(N_point/2)
    spectrum1[N_half1:,:N_half2] = np.copy(spectrum[N_half1:,:N_half2])
    spectrum1[:N_half1,N_half2:] = np.copy(spectrum[:N_half1,N_half2:])
#     spectrum1[0:N_half1,:N_half2] = np.copy(spectrum[0:N_half1,:N_half2])
#     spectrum1[N_half1:,N_half2:] = np.copy(spectrum[N_half1:,N_half2:])
    # How to deal with the omega=0 part    
    spectrum2 = spectrum-spectrum1
    eta1 = np.fft.ifftn(spectrum1)
    eta2 = np.fft.ifftn(spectrum2)
    for i in range(0,N_point):
        eta1[:,i] = eta1[:,i]/(window+0.000000001)
        eta2[:,i] = eta2[:,i]/(window+0.000000001)
    return (eta1,eta2,spectrum1,spectrum2)

def capi_energy(eta, sigma, g=1, L0=1):
    pe_g = np.sum(eta**2)*L0/eta.size/2*g
    grad = np.gradient(eta)/(L0/eta.size)
    pe_s = (np.sum((1+grad**2)**0.5)*L0/eta.size-L0)*sigma
    eta_0 = 0.05/2/np.pi*np.cos(np.linspace(0,1,32)*2*np.pi)
    grad_0 = np.gradient(eta_0)/(L0/eta.size)
    pe_s0 = (np.sum((1+grad_0**2)**0.5)*L0/eta_0.size-L0)*sigma
    return (pe_g, pe_s)