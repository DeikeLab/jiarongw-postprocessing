import sys
import os
import subprocess
from tqdm import tqdm


os.chdir('/home/jiarong/research/projects/windwave/linlog/')
print(os.getcwd())
def main():
	LEVEL = 11
	start = int(sys.argv[1])
	end = int(sys.argv[2])
	if len(sys.argv) != 3:
		print('Parameter number wrong!\n')

	para_name = ['Ustar', 'ak', 'Bo', 'Re', 'LEVEL']
	para_pair_set = [[0.8,0.1,200,100000,11]]

	# Assemble the directory name corresponding to each parameter set
	for p in tqdm(para_pair_set):
		dirname = 'linlog_withforcing_4_m5B0'
		# dirname = 'linlog_adaptive_limited_m5B0'
		for i, name in enumerate(para_name):
			if name == 'Re':
				dirname += name + '%g' % p[i] + '.'
			else:
				dirname += name + '%g' % p[i]
		# dirname += '_secondrun'
		# Call iter_onecase, pass directory name as a parameter
		subprocess.call(["cp", "/home/jiarong/research/postprocessing/diagnostics/norun", './'+dirname])
		subprocess.call(['mkdir', './matrix'], cwd='/home/jiarong/research/projects/windwave/' + dirname)
		subprocess.call(['mkdir', './field'], cwd='/home/jiarong/research/projects/windwave/' + dirname) 
		subprocess.call(['mkdir', './movie'], cwd='/home/jiarong/research/projects/windwave/' + dirname) 
		for i in range(start, end):
			Snapshot = str(i/32.)
		#                 cmd = './directout'+'\t'+LEVEL+'\t'+ak+'\t'+BO+'\t'+RE+'\t'+m+'\t'+B+'\t'+UstarRATIO+'\t'+Snapshot
			subprocess.call(['./norun', '%g' %LEVEL, '%g' % p[1], '%g' % p[2],
				'%g' % p[3], '5', '0', '%g' % p[0], Snapshot], 
				cwd='/home/jiarong/research/projects/windwave/' + dirname)


if __name__ == "__main__":
	main()
print("DONE")