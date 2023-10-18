import numpy as np
import timeit
import concurrent.futures

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def calculate_eta(x, y, t):
    global kx_tile, ky_tile, dkx, dky, F_kxky_tile, omega_tile
    ampl = (2 * F_kxky_tile * dkx * dky) ** 0.5
    np.random.seed(0) 
    phase_tile = np.random.random_sample(kx_tile.shape) * 2 * np.pi
    return np.sum(ampl * np.cos((kx_tile * x + ky_tile * y) - omega_tile * t + phase_tile))

def calculate_eta_parallel(x_tile_row, y_tile_row):
    return [calculate_eta(x, y, t) for x, y in zip(x_tile_row, y_tile_row)]

def eta_random_parallel(t, x_tile, y_tile, N_grid):
    eta_tile = []
    
    # Flatten x_tile and y_tile arrays
    x_tile_flat = x_tile.flatten()
    y_tile_flat = y_tile.flatten()

    # Divide the flattened arrays into smaller chunks for parallel processing
    chunk_size = N_grid * N_grid // num_workers
    x_tile_chunks = [x_tile_flat[i:i+chunk_size] for i in range(0, N_grid * N_grid, chunk_size)]
    y_tile_chunks = [y_tile_flat[i:i+chunk_size] for i in range(0, N_grid * N_grid, chunk_size)]

    # Parallel processing using concurrent.futures.ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(calculate_eta_parallel, x_row, y_row) for x_row, y_row in zip(x_tile_chunks, y_tile_chunks)]
    
    for i, future in enumerate(futures):
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, N_grid * N_grid)
        eta_tile_flat = future.result()
        eta_tile.append(eta_tile_flat)
    
    eta_tile = np.array(eta_tile)
    eta_tile = eta_tile.reshape((N_grid, N_grid))

    return eta_tile

# Set the number of parallel workers (adjust this based on the number of available CPU cores)
num_workers = 16

# read in
path='/projects/DEIKE/jiarongw/multilayer/revision/field_new_200m_P0.02_RE40000_10_15_rand4_Htheta0.503/'
N = 1024; L = 200; kp = 2*np.pi/(L/5); omegap = (9.8*kp)**0.5

t = 200
filename = path + 'surface/eta_matrix_%g' %t
eta = np.fromfile(filename, dtype=np.float32)
eta = eta.reshape(N+1,N+1); eta = eta[1:,1:]
wavenumber = 2*np.pi*np.fft.fftfreq(n=N,d=L/N)
spectrum = np.fft.fft2(eta) / (N*N)**0.5 # FFT normalization 
F = np.absolute(spectrum)**2 / N**2 # Per area normalization
kx = np.fft.fftshift(wavenumber); ky = kx
kx_tile, ky_tile = np.meshgrid(kx,ky)
dkx = kx[1] - kx[0]; dky = ky[1] - ky[0]
F_center = np.fft.fftshift(F)/dkx/dky # Further normalization by independent variables
print('Done computing spectrum!')

N_grid = 256; L = 200
x = np.linspace(-L/2,L/2,N_grid); y = np.linspace(-L/2,L/2,N_grid)
x_tile, y_tile = np.meshgrid(x, y)
kmod_cart_tile, theta_cart_tile = cart2pol(kx_tile,ky_tile)
omega_tile = (9.8*kmod_cart_tile)**0.5 # frequency based on kx or kmod
dkx = kx_tile[0,1]-kx_tile[0,0]; dky = ky_tile[1,0]-ky_tile[0,0]

d = 450
kx_tile = kx_tile[512-d:512+d,512-d:512+d]
ky_tile = ky_tile[512-d:512+d,512-d:512+d]
F_kxky_tile = F_center[512-d:512+d,512-d:512+d]
omega_tile = omega_tile[512-d:512+d,512-d:512+d]

starttime = timeit.default_timer()
eta_tile = eta_random_parallel(0, x_tile, y_tile, N_grid)
print("The time difference is :", timeit.default_timer() - starttime)
