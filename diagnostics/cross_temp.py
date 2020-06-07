import sys
import os
import subprocess
from tqdm import tqdm


os.chdir('/home/jiarong/research/projects/windwave')
print(os.getcwd())
def main():
	LEVEL = 11
	start = int(sys.argv[1])
	end = int(sys.argv[2])
	if len(sys.argv) != 3:
		print('Parameter number wrong!\n')

	para_name = ['Ustar', 'ak', 'Bo', 'Re', 'LEVEL']
	# para_pair_set = [(1,0.02,3.31,20000,11), (1,0.05,3.31,20000,11), (1,0.025,3.31,20000,11), (1,0.03,3.31,20000,11), (1,0.04,3.31,20000,11) ]
	# para_pair_set = [(0.7,0.05,0.27,2990,11), (0.8,0.05,0.27,2990,11), (0.4,0.05,1.47,10600,11), (0.5,0.05,1.47,10600,11), (0.2,0.05,3.31,20000,11), (0.3,0.05,3.31,20000,11) ]

	para_pair_set = [(0.9,0.05,0.27,2990,11)]
	# Assemble the directory name corresponding to each parameter set
	for p in tqdm(para_pair_set):
					# dirname = 'linear_m5B0'
		dirname = 'linear_m5B0'
		for i, name in enumerate(para_name):
			if name == 'Re':
				dirname += name + '%g' % p[i] + '.'
			else:
				dirname += name + '%g' % p[i]
		# dirname += '_secondrun'
		# Call iter_onecase, pass directory name as a parameter
		# subprocess.call(["cp", "/home/jiarong/research/postprocessing/diagnostics/norun_old", './'+dirname])
		subprocess.call(['mkdir', './matrix'], cwd='/home/jiarong/research/projects/windwave/' + dirname)
		subprocess.call(['mkdir', './field'], cwd='/home/jiarong/research/projects/windwave/' + dirname) 
		for i in range(start, end):
			Snapshot = str(i/32.)
		#                 cmd = './directout'+'\t'+LEVEL+'\t'+ak+'\t'+BO+'\t'+RE+'\t'+m+'\t'+B+'\t'+UstarRATIO+'\t'+Snapshot
			subprocess.call(['./norun', '%g' %LEVEL, '%g' % p[1], '%g' % p[2],
				'%g' % p[3], '5', '0', '%g' % p[0], Snapshot], 
				cwd='/home/jiarong/research/projects/windwave/' + dirname)


if __name__ == "__main__":
	main()
print("DONE")
