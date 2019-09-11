'''
    Here are some miscellanous utility functions that help with the data input and output.
'''
import os
import pandas as pd
import numpy as np
import pickle
from tqdm import tqdm

def readin(filename, table_delimiter = ',', table_headers = None):
    '''
    A function used to read in field contained data file in the form of 
    dataframe. The warning of specifying dtype is to be ignored because of
    the current way of first reading in data then convert to numerics.
    Some helpful features are:
    1. Check if the file is damaged
    2. avoid corrupted lines by forcing converting to numeric and drop NAN
    
    filename: string
        The name of the data file. (Not supposed to be iterative. Iterating is performed by a 
        higher level function.)
    table_delimiter: string, optional
        Either '' or ',', default ','
    table_headers: list of keys, optional
        Names of the field attributes. Default is None.      
    '''
    
    # An implementation of droppping lines according to the return value of logic
#     def logic(index):
#         if index % 100 == 0:
#             return False
#         return True
#         energy = pd.read_table(filename, delimiter = ' ', skiprows= lambda x: logic(x), error_bad_lines=False)
    # An implementation of dropping duplicate in a certain column
#         data = data.drop_duplicates(subset=['t'], keep='last')

    exists = os.path.exists(filename)
    if not exists:
        print(filename + ' cannot be read!')        
    if exists:
        data = pd.read_table(filename, delimiter = table_delimiter, names = table_headers, error_bad_lines=False)
        columns = list(data) 
        for i in columns: 
            data[i] = pd.to_numeric(data[i],errors='coerce')
        data = data.dropna()
        data = data.reset_index(drop=True)
        return data

def put_together(filename, core_number, table_delimiter = ',', table_headers = None):
    '''
    A function used to put data files from different cores together.
    
    filename: string
        The common part of the name of the data file. (Not supposed to be iterative.)
    core_number: int
        Number of cores used during the parallel computing.
    table_delimiter, table_headers: same as above
      
    '''
    filename_number = filename + '_0.dat' 
    data = pd.read_table(filename_number, names = table_headers, delimiter = table_delimiter)
    for i in range (0, core_number):
        filename_number = filename + '%g.dat' % i
        data_append = pd.read_table(filename_number, names = table_headers, delimiter = table_delimiter)
        data = data.append(data_append, ignore_index=True)
    return data

def ensemble_pickle(clock, headers=['x', 'y', 'z', 'u.x', 'u.y', 'u.z', 'omega'], 
                    filename_common = './field_direct', picklename = 'ensemble', sort_and_halve = True):
    '''
    Read data across different dump files. Better to be called from a separate script instead
    of inside a notebook cell. See /postprocessing/turbulence/prepare.py
    Put together in list field; record respective time in list tseries;
    count number of points in list ptnumber(for checking if maximum level is reached).
    
    clock: list of time
    headers: keys of data file headers
    filename_common: string of the file name without time postsuffix
    picklename: string of the output pickle file name
    sort_and_halve: boolean to perform extra data clean, optional, default True    
    '''
    
    field = []
    tseries = []
    ptnum = []
    for t in tqdm(clock):
        filename = filename_common + '%g' % t
        snapshot = readin(filename, table_headers = headers)
        # Sort dataframe by y value, only taking the upper half, optional
        if sort_and_halve:
            snapshot = snapshot.sort_values(by = ['x','y','z'])
            snapshot = snapshot.loc[snapshot.y >= 0]
            # Reset the index which is important! AlWAYS reset the fucking index!!!
            snapshot = snapshot.reset_index(drop=True)
        field.append(snapshot)
        tseries.append(t)
        ptnum.append(len(snapshot))
    # After reading all the data, pickle them  
    outfile = open(picklename,'wb')
    data = (field, tseries, ptnum)
    pickle.dump(data,outfile)