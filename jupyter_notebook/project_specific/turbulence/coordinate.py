import numpy as np

""" This is aiming to do the orthogonal coordinate transform suggested by Benjamin 1958, but 2d interpolate is too expensive
    with non-uniform coordinate. (And not feasible with 512*512.)
"""
# def coordtrans_forward (x, y, a=0.2/4, k=4):
#     x_ = x + a*np.exp(-k*abs(y))*np.sin(k*x)
#     y_ = y - a*np.exp(-k*abs(y))*np.cos(k*x)
#     return (x_, y_)
# def coordtrans_backward (x,y):
#     pass

# """ A wrapper for the interp2d """
# from scipy import interpolate
# def interpolator2D(array, eta, transfunc):
#     """ Args:
#             array: the original array on a cartisian (uniform) grid (512*512).
#             eta: the surface position (512*1).
#             transfunc: the function that defines the new coordinate
#         Returns:
#             An interpolator f
#     """
#     if np.shape(array) != (512, 512):
#         print("Wrong array size!")
#         return (1)
#     else:
#         L0 = 2*np.pi
#         y = np.linspace(0,L0,512,endpoint=False) + L0/2/512
#         x = np.linspace(-L0/2,L0/2,512,endpoint=False) + L0/2/512
#         x_tile, y_tile = np.meshgrid(x,y)
#         xnew_tile, ynew_tile = transfunc(x_tile, y_tile) # x_, y_ are the new coordinates
#         # If the points lie on a regular grid, x can specify the column coordinates and y the row coordinates
#         # Otherwise, x and y must specify the full coordinates for each point
#         print(np.shape(np.ravel(xnew_tile)))
# #         f = interpolate.interp2d(np.ravel(xnew_tile[0:100,0:100]), np.ravel(ynew_tile[0:100,0:100]), array[0:100,0:100], kind='cubic') 
#         f = interpolate.interp2d(np.ravel(xnew_tile), np.ravel(ynew_tile), array, kind='cubic') 
#     return f     

# eta = np.roll(np.average(case.phase['eta'][0], axis=0), -case.phase['idx'][0], axis=0)
# f = interpolator2D(case.ux_2D[0], eta, coordtrans_forward)

""" As an alternative, only transform the vertical direction. """

""" Trandformation function z(zeta, xi)
    Version1: use acoskx """
def transfunc(zeta, xi, a0, k):
    sigma = 1 # rate of change (see Hara 2015)
    return zeta + a0*np.exp(-sigma*k*abs(zeta))*np.cos(k*xi)

""" Explicit backward mapping from zeta, xi to z, x"""
def coordtrans_backward (zeta, xi, a0=0.2/4, k=4):
    z = transfunc(zeta, xi, a0=a0, k=k)
    x = xi
    return (z,x)

""" Trandformation function z(zeta, xi)
    Version2: use local eta """
def transfunc_local(zeta, a, k=4):
    sigma = 1 # rate of change (see Hara 2015)
    return zeta + a*np.exp(-sigma*k*abs(zeta))

""" Explicit backward mapping from zeta, xi to z, x, but requires local a instead of a0"""
def coordtrans_backward_local (zeta, xi, a, k=4):    
    z = transfunc_local(zeta, a=a, k=k)
    x = xi
    return (z,x)

""" Implicit forward mapping from z,x to zeta, xi by solving z(zeta, xi) = z0 
    zeta is the active variable and x, a0, k, z0 are the arguments"""
def func_to_solve (zeta, x, a0, k, z0):
    return transfunc(zeta, xi, a0, k) - z0

def coordtrans_forward (z, x, a0=0.2/4, k=4):
    from scipy.optimize import fsolve
    xi = x
    zeta = fsolve(func_to_solve, z, args=(x, a0, k, z))[0] # Take a guess starting from z(z0), and if there are multiple solutions, take the first one
    return (zeta, xi)


""" Function to interpolate the simulation data onto a wave following coordinate. """
from scipy import interpolate
def array_newcoord(array_simu, case, eta=np.array([None]*2)):
    """ Args:
            array_simu: simulation output 2D array to remap.
            case: case object for metadata like h, ak and k. """
    h = case.h; L0=case.L0; N = case.N
    xarray = np.linspace(-np.pi, np.pi, N)
    array_interp = np.zeros(np.shape(array_simu))
    z_interp = np.zeros(np.shape(array_simu))
    # Do 1d interpolation for each x
    for i in range(np.shape(array_simu)[0]):
        xi = xarray[i]
        # Grid in simulation, translated vertically to have the resting interface at z=0
        z_simu = np.linspace(0,L0,N,endpoint=False) + L0/2/N - h 
        f = interpolate.interp1d(z_simu, array_simu[i,:], fill_value="extrapolate")
        # Uniform grid in new coordinate zeta
        zeta_grid = np.linspace(0,L0,N,endpoint=False) + L0/2/N - h 
        # Explicitly computed corresponding z, using a0cos(kxi)
        if eta.any() == None:
            z_grid = [coordtrans_backward(zeta=zeta, xi=xi, a0=case.ak/case.k, k=case.k)[0] for zeta in zeta_grid]
        # Explicitly computed corresponding z, using local a, if eta is given
        if eta.all() !=None:
            z_grid = [coordtrans_backward_local(zeta=zeta, xi=xi, a=eta[i], k=case.k)[0] for zeta in zeta_grid]
        array_grid = f(z_grid)
        array_interp[i] = array_grid
        z_interp[i] = z_grid
    return (array_interp, z_interp)