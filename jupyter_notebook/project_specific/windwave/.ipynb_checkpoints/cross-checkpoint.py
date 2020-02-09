import sys
import os
from tqdm import tqdm

print(os.getcwd())
os.chdir('/home/jiarong/research/projects/windwave')


def main():
    # arguments
    LEVEL = 11
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    if len(sys.argv) != 3:
        print('Parameter number wrong!\n')
        
    dirname = './linear_m5B0'
    para_name = ['Ustar','ak','Bo','Re','LEVEL']
    para_pair_set = [(0.4,0.05,3.45,31000.,10), (0.45,0.05,3.45,31000,10), (0.5,0.05,3.45,31000,10), (0.55,0.05,3.45,31000,10), 
                 (0.6,0.05,3.45,31000.,10), (0.5,0.01,3.45,31000,11), (0.5,0.02,3.45,31000,10), (0.5,0.1,3.45,31000,10),
                 (0.5,0.15,3.45,31000.,10), (0.5,0.2,3.45,31000,10), (0.5,0.02,3.45,20000,10), (0.5,0.02,3.45,31000,10)]
    def iter_para(para_pair_set, para_name):
    for p in tqdm(para_pair_set):
        # Assemble the directory name corresponding to each parameter set
        dirname = './linear_m5B0'
        for i,name in enumerate(para_name):        
            if name == 'Re':
                dirname += name + '%g' %p[i] + '.'
            else:
                dirname += name + '%g' %p[i] 
            # Call iter_onecase, pass directory name as a parameter
            os.system('cp /home/jiarong/research/projects/windwave/common/directout ' + dirname)
            os.system('cd ' + dirname)
            for i in range(start, end):
                Snapshot = str(i)
#                 cmd = './directout'+'\t'+LEVEL+'\t'+ak+'\t'+BO+'\t'+RE+'\t'+m+'\t'+B+'\t'+UstarRATIO+'\t'+Snapshot
                cmd = './directout'+'\t'+LEVEL+'\t'+'%g' %p[1]+'\t'+'%g' %p[2]+'\t'+'%g'
                       %p[3]+'\t'+5+'\t'+0+'\t'+'%g' %p[0]+'\t'+Snapshot
                print(cmd)
                os.system(cmd)

if __name__ == "__main__":
    main()

print("DONE")