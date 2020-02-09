import sys
import os
import subprocess
from tqdm import tqdm


os.chdir('/home/jiarong/research/projects/windwave')
print(os.getcwd())
os.chdir('/home/jiarong/research/projects/windwave/' + 
	'linear_m5B0Ustar0.5ak0.02Bo3.45Re31000.LEVEL10/')
print(os.getcwd())
subprocess.call(['cd', '/home/jiarong/research/projects/windwave/'])
print(os.getcwd())