'''
    Here are some miscellanous utility functions that help with the data input and output.
'''
import os
import pandas as pd
import numpy as np

def readin(filename, table_delimiter = ',', table_headers = None):
    '''
    A function used to read in field contained data file in the form of 
    dataframe. Some helpful features are:
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