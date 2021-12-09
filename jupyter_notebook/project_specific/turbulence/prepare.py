""" Functions related to pickle. """
import sys
import os
import numpy as np
sys.path.append('/home/jiarong/research/postprocessing/functions/')
sys.path.append('/projects/DEIKE/jiarongw/jiarongw-postprocessing/jupyter_notebook/functions/')
sys.path.append('/projects/DEIKE/jiarongw/jiarongw-postprocessing/jupyter_notebook/project_specific/windwave/')
from fio import ensemble_pickle

""" Helper functions """
import pickle
def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
def load_object(filename):
    with open(filename, 'rb') as input:  # Overwrites any existing file.
        obj = pickle.load(input)
    return obj


# os.chdir('/home/jiarong/research/projects/turbulence/preliminary_cluster/stopforcing_restore_second')

# def main():
#     clock = np.arange(900, 950)
#     ensemble_pickle(clock, picklename="ensemble")
#     print(os.getcwd())

# if __name__ == "__main__":
#     main()

# print("DONE")





