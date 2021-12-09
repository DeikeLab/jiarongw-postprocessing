from defs import Case, Interface2D
case1 = Case(ustar=0.25, Retau=720, Bo=200, g=1, ak=0.2, LEVEL=10, emax=0.3, alterMU=16, NOMATCH=True, 
             PRINTWAVE=True, OUTLEVEL=9, working_dir='/projects/DEIKE/jiarongw/turbulence/', prefix='curved_fixREtau_boundary_')
case1.tstart = 57
case2 = Case(ustar=0.25, Retau=720, Bo=200, g=4, ak=0.2, LEVEL=10, emax=0.3, alterMU=8, NOMATCH=True, 
             PRINTWAVE=True, OUTLEVEL=9, working_dir='/projects/DEIKE/jiarongw/turbulence/', prefix='curved_fixREtau_boundary_')
case2.tstart = 57
case3 = Case(ustar=0.25, Retau=720, Bo=200, g=16, ak=0.2, LEVEL=10, emax=0.3, alterMU=4, NOMATCH=True, 
             PRINTWAVE=True, OUTLEVEL=9, working_dir='/projects/DEIKE/jiarongw/turbulence/', prefix='curved_fixREtau_boundary_')
case3.tstart = 57
case4 = Case(ustar=0.25, Retau=720, Bo=200, g=1, ak=0.1, LEVEL=10, emax=0.1, alterMU=16, NOMATCH=True, 
             PRINTWAVE=True, OUTLEVEL=9, working_dir='/projects/DEIKE/jiarongw/turbulence/', prefix='curved_fixREtau_boundary_')
case4.tstart = 307
case5 = Case(ustar=0.25, Retau=720, Bo=200, g=4, ak=0.1, LEVEL=10, emax=0.1, alterMU=8, NOMATCH=True, 
             PRINTWAVE=True, OUTLEVEL=9, working_dir='/projects/DEIKE/jiarongw/turbulence/', prefix='curved_fixREtau_boundary_')
case5.tstart = 301.5
case6 = Case(ustar=0.25, Retau=720, Bo=200, g=16, ak=0.1, LEVEL=10, emax=0.1, alterMU=4, NOMATCH=True, 
             PRINTWAVE=True, OUTLEVEL=9, working_dir='/projects/DEIKE/jiarongw/turbulence/', prefix='curved_fixREtau_boundary_')
case6.tstart = 307
case7 = Case(ustar=0.25, Retau=720, Bo=200, g=1, ak=0.15, LEVEL=10, emax=0.3, alterMU=16, NOMATCH=True, 
             PRINTWAVE=True, OUTLEVEL=9, working_dir='/projects/DEIKE/jiarongw/turbulence/', prefix='curved_fixREtau_boundary_')
case7.tstart = 43
case8 = Case(ustar=0.25, Retau=720, Bo=200, g=2.25, ak=0.15, LEVEL=10, emax=0.3, alterMU=10.666, NOMATCH=True, 
             PRINTWAVE=True, OUTLEVEL=9, working_dir='/projects/DEIKE/jiarongw/turbulence/', prefix='curved_fixREtau_boundary_')
case8.tstart = 43
case9 = Case(ustar=0.25, Retau=720, Bo=200, g=4, ak=0.15, LEVEL=10, emax=0.3, alterMU=8, NOMATCH=True, 
             PRINTWAVE=True, OUTLEVEL=9, working_dir='/projects/DEIKE/jiarongw/turbulence/', prefix='curved_fixREtau_boundary_')
case9.tstart = 43
case10 = Case(ustar=0.25, Retau=720, Bo=200, g=9, ak=0.15, LEVEL=10, emax=0.3, alterMU=5.333, NOMATCH=True, 
             PRINTWAVE=True, OUTLEVEL=9, working_dir='/projects/DEIKE/jiarongw/turbulence/', prefix='curved_fixREtau_boundary_')
case10.tstart = 43
case11 = Case(ustar=0.25, Retau=720, Bo=200, g=16, ak=0.15, LEVEL=10, emax=0.3, alterMU=4, NOMATCH=True, 
             PRINTWAVE=True, OUTLEVEL=9, working_dir='/projects/DEIKE/jiarongw/turbulence/', prefix='curved_fixREtau_boundary_')
case11.tstart = 43
case12 = Case(ustar=0.25, Retau=720, Bo=200, g=64, ak=0.15, LEVEL=10, emax=0.3, alterMU=2, NOMATCH=True, 
             PRINTWAVE=True, OUTLEVEL=9, working_dir='/projects/DEIKE/jiarongw/turbulence/', prefix='curved_fixREtau_boundary_')
case12.tstart = 43

from phase import extract_phase

""" To-do: write something that compare the timesteps but not rereadin everything everytime. """
case = case1
case.tsimu = np.arange(58,108,1)
extract_phase(case, case.tsimu)

case = case2
case.tsimu = np.arange(58,101,1)
extract_phase(case, case.tsimu)

case = case3
case.tsimu = np.arange(58,73,1)
extract_phase(case, case.tsimu)

case = case4
case.tsimu = np.arange(308,346,1)
extract_phase(case, case.tsimu)

case = case5
case.tsimu = np.arange(302,342,1)
extract_phase(case, case.tsimu)

case = case6
case.tsimu = np.arange(308,321,1)
extract_phase(case, case.tsimu)

case = case7
case.tsimu = np.arange(44,56,1)
extract_phase(case, case.tsimu)

case = case8
case.tsimu = np.arange(43.1,48.1,0.1)
extract_phase(case, case.tsimu)
case.phase['t'] = case.tsimu - case.tstart

case = case9
case.tsimu = np.arange(44,54,1)
extract_phase(case, case.tsimu)

case = case10
case.tsimu = np.arange(43.1,47.1,0.1)
extract_phase(case, case.tsimu)

case = case11
case.tsimu = np.arange(43.5,52.5,0.5)
extract_phase(case, case.tsimu)

case = case12
case.tsimu = np.arange(43.5,45,0.5)
extract_phase(case, case.tsimu)

"""p time"""
case = case7
case.p = {"t":[], "p_2D":[], 'phat':[], 'dphase':[]}
case.p['t'] = np.concatenate((np.arange(44,54,1), np.arange(55,66,0.2))) - case.tstart
print(case.p['t'])
read_p(case)

case = case9
case.p = {"t":[], "p_2D":[], 'phat':[], 'dphase':[]}
case.p['t'] = np.concatenate((np.arange(44,54,1), np.arange(55,63,0.2))) - case.tstart
print(case.p['t'])
read_p(case)

case = case11
case.p = {"t":[], "p_2D":[], 'phat':[], 'dphase':[]}
case.p['t'] = np.arange(44,53,1) - case.tstart
read_p(case)





case7.field_t = np.arange(44,66,1) - case7.tstart
read_fields(case8)

case9.field_t = np.arange(44,63,1) - case9.tstart
read_fields(case9)