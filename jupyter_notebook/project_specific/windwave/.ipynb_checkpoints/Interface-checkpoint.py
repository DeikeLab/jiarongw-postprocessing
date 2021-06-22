"""This is the Interface1D class."""

from scipy.interpolate import griddata
import gc
class Interface1D():
    """Class for every interface related 1D output. Unstructured grid input.
            
    Attributes:
        xarray: equal distanced x grid 
        <field>data: row data of <field>
        <field>: interpolated data of <field>, including eta/p/grad/dudy/uxw...    
    """
     
    def __init__(self, L0, N, path, t, PRUNING=True, pre='/field/eta_loc_t'):
        """Example of docstring on the __init__ method.

        The __init__ method may be documented in either the class level
        docstring, or as a docstring on the __init__ method itself.

        Either form is acceptable, but the two should not be mixed. Choose one
        convention to document the __init__ method and be consistent with it.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            L0, N: The desired output grid number
            working_dir: The case's directory
            t: Time of this eta file.
            PRUNING: If eta is output by multiple processes and have multiple headers
                    (only applicable to MPI processed file).  
            pre: the prefix of the desirable data file.
        """
        self.L0 = L0; self.N = N; self.t = t
        self.xarray = np.linspace(-self.L0/2.,self.L0/2.,self.N,endpoint=False)+self.L0/2**self.N/2 # Centered grid for interpolation
        filename = path + pre + '%g' %self.t
        snapshot = pd.read_table(filename, delimiter = ',')
        snapshot = snapshot.sort_values(by = ['x'])
        # Field entries
        # x,pos,epsilon,p,p_p1,p_p2,dudy1,dudy2,dvdx1,dvdx2,dudx1,dudx2,dvdy1,dvdy2,uxa,uya,uxw,uyw
        if PRUNING:
            snapshot = snapshot[snapshot.x != 'x']
            snapshot = snapshot.astype('float')
            snapshot = snapshot[snapshot.pos < 0.4/(2*np.pi)] # Exclude data over slope 0.4
            
        self.xdata = np.array(snapshot.x, dtype=float)
        self.etadata = np.array(snapshot.pos, dtype=float)
        self.pdata = np.array(snapshot.p, dtype=float)
        self.graddata = np.array(snapshot.epsilon, dtype=float)
        self.dudydata = np.array(snapshot.dudy1, dtype=float)
        self.dvdxdata = np.array(snapshot.dvdx1, dtype=float)
        self.dudxdata = np.array(snapshot.dudx1, dtype=float)
        self.dvdydata = np.array(snapshot.dvdy1, dtype=float)
        self.uxwdata = np.array(snapshot.uxw, dtype=float)
        self.uywdata = np.array(snapshot.uyw, dtype=float)
        del (snapshot); gc.collect()  # Only necessary for 2D for memory issue              
        
        # Interpolate over x, 'nearest' is used to ensure that none of the interpolated point is 'nan' 
        self.eta = griddata(self.xdata.ravel(), self.etadata.ravel(), self.xarray, method='nearest')
        self.p = griddata(self.xdata.ravel(), self.pdata.ravel(), self.xarray, method='nearest')
        self.dudy = griddata(self.xdata.ravel(), self.dudydata.ravel(), self.xarray, method='nearest')
        self.dvdx = griddata(self.xdata.ravel(), self.dvdxdata.ravel(), self.xarray, method='nearest')
        self.dudx = griddata(self.xdata.ravel(), self.dudxdata.ravel(), self.xarray, method='nearest')
        self.dvdy = griddata(self.xdata.ravel(), self.dvdydata.ravel(), self.xarray, method='nearest')
        self.grad = griddata(self.xdata.ravel(), self.graddata.ravel(), self.xarray, method='nearest')
        self.uxw = griddata(self.xdata.ravel(), self.uxwdata.ravel(), self.xarray, method='nearest')
        self.uyw = griddata(self.xdata.ravel(), self.uywdata.ravel(), self.xarray, method='nearest')
    
    def uwater(self):
        """ Water velocity decomposition.
            The arrays are:
                uwx_smooth: smoothed direct output of uw
                uwx_orbit: orbital velocity from direct output of eta, u component (simplest estimation)
                uwy_orbit: orbital velocity from direct output of eta, v component
                ud: analytical time dependent drift, constant along x
                uwx_analy: ud + uwx_orbit
        """

        plt.figure(figsize=[4,2])
        from scipy.signal import hilbert

        # Output water velocity
        plt.plot(interface.xdata, interface.uxwdata, c='C0', alpha = 0.5) # Water velocity 
        plt.plot(interface.xdata, interface.uywdata, c='C2', alpha = 0.5) # Water velocity 
        uxw_smooth = butter_lowpass_filter(interface.uxw_tile, CUT=4)
        uyw_smooth = butter_lowpass_filter(interface.uyw_tile, CUT=4)
        plt.plot(interface.xarray, uxw_smooth, c='C0', label = '$u_s$, simu') # Water velocity 
        plt.plot(interface.xarray, uyw_smooth, c='C2', label = '$v_s$, simu') # Water velocity 

        # The analytical water velocity
        # plt.plot(interface.xarray, interface.eta_tile*case.wave.c*2*np.pi) # The orbital velocity
        from scipy.special import gamma
        t = 2
        ud = t**0.5*gamma(1)/gamma(3/2)/850 * (case.ustar*case.wave.c)**2 * (2*np.pi/case.wave.omega/(1/case.Re))**0.5 # Drift according to theoretical solution
        eta = butter_lowpass_filter(interface.eta_tile, CUT=4) # Filter eta
        analytic_signal = hilbert(eta)
        phase = np.unwrap(np.angle(analytic_signal))
        uwx_orbit = eta*case.wave.c*2*np.pi
        uwy_orbit = eta*case.wave.c*2*np.pi/np.cos(phase)*np.cos(phase-np.pi/2)
        uwx_analy = ud + uwx_orbit

        plt.plot(interface.xarray, uwx_orbit, '--', c='C1', label='$u_w$, analy', alpha = 0.5)
        plt.plot(interface.xarray, uwy_orbit, '--', c='C2', label='$v_w$, analy', alpha = 0.5)
        plt.plot(interface.xarray, uwx_analy, '--', c='C0', label = '$u_w$ + $u_d$, analy')

        plt.plot(interface.xarray, eta, c='gray', alpha = 0.5)
        plt.xlabel(r'$x/\lambda$')
        plt.ylabel(r'$u_s,v_s$')
        plt.xlim([-0.5,0.5])
        plt.ylim([-0.05,0.1])
        plt.legend(bbox_to_anchor=(1.02, 0.5), loc = 'center left')
        
    def vis(self):
        pass