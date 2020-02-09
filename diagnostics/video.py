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
	# para_pair_set = [(0.4, 0.05, 3.45, 31000., 10), (0.45, 0.05, 3.45, 31000, 10), (0.5, 0.05, 3.45, 31000, 10), (0.55, 0.05, 3.45, 31000, 10),
	# 				 (0.6, 0.05, 3.45, 31000., 10), (0.5, 0.01, 3.45, 31000, 11), (0.5, 0.02, 3.45, 31000, 10), (0.5, 0.1, 3.45, 31000, 10),
	# 				 (0.5, 0.15, 3.45, 31000., 10), (0.5, 0.2, 3.45, 31000, 10), (0.5, 0.02, 3.45, 31000, 10)]
	para_pair_set = [ (1.2, 0.05, 0.53, 5000., 11) ]
					
	# Assemble the directory name corresponding to each parameter set
	for p in tqdm(para_pair_set):
		dirname = 'linear_m5B0'
		for i, name in enumerate(para_name):
			if name == 'Re':
				dirname += name + '%g' % p[i] + '.'
			else:
				dirname += name + '%g' % p[i]
		# dirname = 'linear_plane_test2_Ustar0.5Bo3.45Re31000.LEVEL10'
		# dirname += '/'
		# Call iter_onecase, pass directory name as a parameter
		subprocess.call(["cp", "./common/video_generator", './'+dirname])
		subprocess.call(["mkdir", "movie"], cwd='/home/jiarong/research/projects/windwave/' + dirname)
		for i in range(start, end):
			Snapshot = str(i/32.)
		#                 cmd = './directout'+'\t'+LEVEL+'\t'+ak+'\t'+BO+'\t'+RE+'\t'+m+'\t'+B+'\t'+UstarRATIO+'\t'+Snapshot
			subprocess.call(['./video_generator', '%g' %LEVEL, '%g' % p[1], '%g' % p[2],
				'%g' % p[3], '5', '0', '%g' % p[0], Snapshot, '%g' %i], 
				cwd='/home/jiarong/research/projects/windwave/' + dirname)


if __name__ == "__main__":
	main()

print("DONE")
