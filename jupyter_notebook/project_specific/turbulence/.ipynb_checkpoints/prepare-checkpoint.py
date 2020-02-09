# prepare the pickle 

import sys
import os
import numpy as np
sys.path.append('/home/jiarong/research/postprocessing/functions/')
from fio import ensemble_pickle

os.chdir('/home/jiarong/research/projects/turbulence/preliminary_cluster/stopforcing_restore_second')

def main():
    clock = np.arange(900, 950)
    ensemble_pickle(clock, picklename="ensemble")
    print(os.getcwd())

if __name__ == "__main__":
    main()

print("DONE")
