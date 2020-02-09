import pandas as pd
import numpy as np
import math
from matplotlib import pyplot as plt
from scipy import signal
# from scipy.signal import savgol_filter
from smooth_func import Smooth
# import logging
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

'''
See http://www.developintelligence.com/blog/2017/08/data-cleaning-pandas-python/
    https://stackoverflow.com/questions/38562435/ignoring-rows-with-unmatching-dtype-in-pandas
    for the method used to clean the data
See https://stackoverflow.com/questions/40755680/how-to-reset-index-pandas-dataframe-after-dropna-pandas-dataframe 
    for reset index and the use of inplace
    
There are a few places where the original data is smoothed:
1. Read in every n=100 data ()
2. Energy smoothed with window size 101
3. Growth rate further smoothed with window size 11
'''

def energy_process(filename, smooth = 'NO'):
    '''
    The function is to read in the energy budget, perform simple manipulation and calculate growth rate
    Example: [energy, total, diss, growth_rate, growth_rate_diss] = energy_process(filename)
    '''
# energy = pd.read_table(filename, delimiter = ' ', dtype={"t": np.float64, "ke": np.float64, "gpe": np.float64,       "dissipation":np.float64}, error_bad_lines=False)
# The above specification of datatype doesn't work for damaged data
# Try the following way to clean it (OK to ignore the following warning "DtypeWarning: Columns (0) have mixed types. Specify dtype option on import or set low_memory=False.")

    # Skip rows from based on condition like skip every 3rd line

    def logic(index):
        if index % 100 == 0:
           return False
        return True

    energy = pd.read_table(filename, delimiter = ' ', skiprows= lambda x: logic(x), error_bad_lines=False)
#     energy.drop(energy.tail(1).index)
    energy.t = pd.to_numeric(energy.t,errors='coerce')  # 'coerce' results in NaN for entries that can't be converted
    energy.ke = pd.to_numeric(energy.ke,errors='coerce')
    energy.gpe = pd.to_numeric(energy.gpe,errors='coerce')
    energy.dissipation = pd.to_numeric(energy.dissipation,errors='coerce')
#     energy.dropna(inplace=True)
#     energy.reset_index(drop=True, inplace=True)
    energy = energy.dropna()
    energy = energy.drop_duplicates(subset=['t'], keep='last')
    energy = energy.reset_index(drop=True)
    
# Do the above line the following way seem to not resolve the index replacement causing index excess
# energy = energy[energy.t.notnull()&energy.ke.notnull()&energy.gpe.notnull()&energy.dissipation.notnull()]

    diss = np.zeros(energy.shape[0])
    total = energy.ke + energy.gpe
    for i, row in energy.iterrows():
        if i == 0:
            diss[i] = 0
            last_t = row['t'] # record t in last row
        else:
            diss[i] = diss[i-1] + row['dissipation'] * (row['t'] - last_t)
            last_t = row['t']
    # smooth the energy curve if needed for computing growth
    total_diss = total + diss
#     with np.errstate(divide='ignore'): 
    if (smooth == 'YES'):
            # the energy is filtered and normalized
            # smooth method 1
    #         b, a = signal.ellip(4, 0.01, 120, 0.001)  # Filter to be applied. Might need to change
    #         total_hat = signal.filtfilt(b, a, total/total[0], method="gust")
    #         total_diss_hat = signal.filtfilt(b, a, (total+diss)/(total[0]+diss[0]), method="gust")
            # smooth method 2
            # windows=['flat', 'hanning', 'hamming', 'bartlett', 'blackman']
        total_hat = Smooth(np.array(total/total[0]),501,'hanning')
        total_diss_hat = Smooth(np.array((total+diss)/(total[0]+diss[0])),501,'hanning')
        growth_rate = np.gradient(total_hat, energy.t) / total_hat
        growth_rate_diss = np.gradient(total_diss_hat, energy.t) / total_diss_hat
    else:
        total_hat = np.ones(total.size) # these are actually not used
        total_diss_hat = np.ones(total.size)
        growth_rate = np.gradient(total, energy.t) / total
        growth_rate_diss = np.gradient(total+diss, energy.t) / (total+diss)
    return [energy, total, total_diss, growth_rate, growth_rate_diss, total_hat, total_diss_hat]; 


def energy_plot(energy, total, total_hat, total_diss, total_diss_hat, ax, legend, smooth = 'NO', simp = 'YES'):   
    '''
    This function is to plot the energy. If raw data has already been smoothed, the input should be smoothed 
    enegy. If simp == 'True', only the total + diss curve is plotted.
    Example:
    energy_plot(raw, total_hat, total_diss_hat, ax1, label, simp = 'YES', smooth = 'YES') 
    energy_plot(raw, total, total_diss, ax1, label, simp = 'YES', smooth = 'NO') 
    '''
#     if smooth == 'YES':
#         ax.plot(energy.t, total_diss_hat, label = legend + ' smoothed')
#     else:
# No matter smoothed or not the enegy is plotted as the original data
#     ax.plot(energy.t, total_diss_hat, label = legend + ' smoothed')
    ax.plot(energy.t, total_diss/total[0], label = legend)        
    if simp == 'NO':
        ax.plot(energy.t, total/total[0], label = legend+'sub_diss')
#         ax.plot(energy.t, energy.ke/energy.ke.iloc[0],  label = str())
#         ax.plot(energy.t, energy.gpe/energy.gpe.iloc[0],  label = str())
    ax.set_xlabel('time')
    ax.set_ylabel('energy')
#     ax.set_yscale('log')
    ax.set_xlim([0, 4])


def energy_growthrate_plot(energy, growth_rate, growth_rate_diss, ax, legend, smooth = 'NO'):
    '''
    This function is to plot the growth rate. If raw data has already been smoothed, the input should be smoothed 
    enegy. If simp == 'True', only the total + diss curve is plotted.
    Example:
    energy_plot(raw, total, total_diss, ax1, label, simp = 'NO') 
    energy_growthrate_plot(raw, growth_rate, growth_rate_diss, ax2, label)
    
    Probably needs to rewrite because of the wrong way to compute rate beta.
    '''
    # shouldn't be using smoothing at this stage anymore
#     growth_rate_hat = savgol_filter(growth_rate, 1001, 3)
#     growth_rate_diss_hat = savgol_filter(growth_rate_diss, 1001, 3)

    if smooth == 'YES':
        growth_rate_hat = Smooth(np.array(growth_rate),11,'hanning')
        growth_rate_diss_hat = Smooth(np.array(growth_rate_diss),11,'hanning')
#         ax.plot(energy.t, growth_rate, label = legend + ' smoothed')
#         ax.plot(energy.t, growth_rate_diss, label = legend + ' with dissipation smoothed')
#         ax.plot(energy.t, growth_rate_hat, label = legend + ' smoothed second time')
        ax.plot(energy.t, growth_rate_diss_hat, label = legend + ' with dissipation smoothed second time')
    else:
        growth_rate_hat = Smooth(np.array(growth_rate),51,'hanning')
        growth_rate_diss_hat = Smooth(np.array(growth_rate_diss),51,'hanning')
        ax.plot(energy.t, growth_rate_hat, label = legend)
        ax.plot(energy.t, growth_rate_diss_hat, label = legend + ' with dissipation') 
    ax.set_xlabel('time')
    ax.set_ylabel('growth rate')
    return growth_rate_diss_hat
    
def energy_comparison(filename_set, label_set, ax1, ax2, smooth = 'YES', simp = 'YES'):
    growth_rate_set = [None] * len(filename_set)
    for i, filename in enumerate(filename_set):
#     for filename, label in zip(filename_set, label_set):
        if (smooth == 'YES'):
            [energy, total, total_diss, growth_rate, growth_rate_diss, total_hat, total_diss_hat] = energy_process(filename, smooth = 'YES')
            if simp == 'YES':
                energy_plot(energy, total, total_hat, total_diss, total_diss_hat, ax1, label_set[i], smooth = 'YES', simp = 'YES') 
            else:
                energy_plot(energy, total, total_hat, total_diss, total_diss_hat, ax1, label_set[i], smooth = 'YES', simp = 'NO') 
            growth_rate_set[i] = energy_growthrate_plot(energy, growth_rate, growth_rate_diss, ax2, label_set[i], smooth = 'YES')
        else:    
            [energy, total, total_diss, growth_rate, growth_rate_diss, useless1, useless2] = energy_process(filename)
            if simp == 'YES':
                energy_plot(energy, total, useless1, total_diss, useless2, ax1, label_set[i], smooth = 'NO',  simp = 'YES') 
            else:
                energy_plot(energy, total, useless1, total_diss, useless2, ax1, label_set[i], smooth = 'NO', simp = 'NO')
            growth_rate_set[i] = energy_growthrate_plot(energy, growth_rate, growth_rate_diss, ax2, label_set[i], smooth = 'NO')
    return energy
    