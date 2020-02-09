 /**
   Run from dump with one or two level more refined grid. Direct output for more accurate interpolation.
   Looping over dump files is achieved with a python script.
   The output files are field_direct+time, field_interp+time, eta+time  */

// #include "grid/multigrid.h"
#include "navier-stokes/centered.h"
#include "two-phase.h"
#include "navier-stokes/conserving.h"
#include "tension.h"
#include "reduced.h"  //reduced gravity
#include "view.h"
#include "tag.h"
#include "curvature.h"
#include "vof.h"

#  define POPEN(name, mode) fopen (name ".ppm", mode)

/* Direct output on each grid point */
void redump (double time) {
  
  char fieldname[100], etaname[100], pressurename[100];
  scalar pos[], p_air[], omega[], omega_air[], omega_water[];
  vector tau[], u_water[];
  tensor SDeform = new tensor;

#if dimension == 2 
  coord G = {0.,1.}, Z = {0.,0.};
#else
  coord G = {0.,1.,0.}, Z = {0.,0.,0.};
#endif
  position (f, pos, G, Z);    
  vorticity (u, omega);

  foreach()
  {
    omega_air[] = omega[]*(1-f[]);
    omega_water[] = omega[]*f[];
    p_air[] = p[]*(1-f[]);
    u_water.x[] = u.x[]*f[];
    u_water.y[] = u.y[]*f[];
    double dudx = (u.x[1]     - u.x[-1]    )/(2.*Delta);
    double dudy = (u.x[0,1]   - u.x[0,-1]  )/(2.*Delta);
    // double dudz = (u.x[0,0,1] - u.x[0,0,-1])/(2.*Delta);
    double dvdx = (u.y[1]     - u.y[-1]    )/(2.*Delta);
    double dvdy = (u.y[0,1]   - u.y[0,-1]  )/(2.*Delta);
    // double dvdz = (u.y[0,0,1] - u.y[0,0,-1])/(2.*Delta);
    // double dwdx = (u.z[1]     - u.z[-1]    )/(2.*Delta);
    // double dwdy = (u.z[0,1]   - u.z[0,-1]  )/(2.*Delta);
    // double dwdz = (u.z[0,0,1] - u.z[0,0,-1])/(2.*Delta);
    SDeform.x.x[] = dudx;
    SDeform.x.y[] = 0.5*(dudy + dvdx);
    // double SDeformxz = 0.5*(dudz + dwdx);
    SDeform.y.x[] = SDeform.x.y[];
    SDeform.y.y[] = dvdy;
    double mu_eff = mu1/rho[]*f[] + mu2/rho[]*(1. - f[]); // compute effective viscosity
    tau.x[] = 2*mu_eff*(SDeform.x.x[]*0 + SDeform.y.x[]*1);
    tau.y[] = 2*mu_eff*(SDeform.x.y[]*0 + SDeform.y.y[]*1);
  }
  p.nodump = false;
  pf.nodump = false;
  dump("dump_diagnostics", list = all);
}

/* Some info about the snapshot time and the refining criteria */
int NUMBER = 32; // Time gap in taking the snapshots
double TIME = 2; // Total number of run time
double snapshot_time; // Current snapshot time
double uemax = 0.0000001;
double femax = 0.0000001;
int LEVEL = 12;
int counting = 0;

/* All the constant that comes with the case, will be changed after input */
double ak = 0.05;
double BO = 200.;
double RE = 40000.;
// double PRESSURE = 0;
double m = 5.;  // vary between 5 and 8
double B = 0.;
double Karman = 0.41;   // Karman universal turbulence constant
double UstarRATIO = 1; // Ratio between Ustar and c

double k_ = 2.*pi;
double h_ = 0.5;
double g_ = 1.;

double RATIO = (1./850.);
double MURATIO = (17.4e-6/8.9e-4); // dynamic viscosity: air/water



int main (int argc, char * argv[])
{
  if (argc > 1)
    LEVEL = atoi (argv[1]);
  if (argc > 2)
    ak = atof(argv[2]);
  if (argc > 3)
    BO = atof(argv[3]);
  if (argc > 4)
    RE = atof(argv[4]);   
  if (argc > 5)
    m = atof(argv[5]);
  if (argc > 6)
    B = atof(argv[6]);
  if (argc > 7)
    UstarRATIO = atof(argv[7]);
  if (argc > 8)
    snapshot_time = atof(argv[8]);
  // if (argc > 8)
  //   PRESSURE = atof(argv[8]);
  
  origin (-L0/2, -L0/2, -L0/2);
  periodic (right);
  // We temporally give up the pressure idea
  // p[left] = dirichlet(PRESSURE);
  // p[right] = dirichlet(0); 
  // Notice that the following should be changed according to the specific condition in the case
  u.n[top] = dirichlet(0);
  u.t[top] = neumann(0);

  rho1 = 1.; // 1 stands for water and 2 for air
  rho2 = RATIO;
  mu1 = 1.0/RE; //using wavelength as length scale
  mu2 = 1.0/RE*MURATIO;
  f.sigma = 1./(BO*sq(k_));
  G.y = -g_;

  run();
  return 0;
}

int phony = 1;  // initialize phony as 1, just a trick to play around the way i is treated in basilisk
int j = 0;  // j substitute i as the indexing number

event init (i = 0)
{
  char targetname[100];
  sprintf (targetname, "dump%g", snapshot_time);
  if (!restore (targetname)) 
    fprintf(ferr, "Not restored!\n");
  restore (targetname);
  phony = 0;
  fprintf(ferr, "Starting step number = %d\n", phony);  // phony is always 0 here
  fprintf(ferr, "snapshot = %g\n", snapshot_time);
}

event adapt (i++) {
  fprintf(ferr, "Testing... %d, %g\n", i, t);
  adapt_wavelet ({f,u}, (double[]){femax,uemax,uemax,uemax}, LEVEL);
  if (phony == 0) {
    j = i;
    phony = 1;
    fprintf(ferr, "New indexing set to j = %d!\n", j);
  }
}

event end (t = 1000) {
  fprintf(ferr, "end\n");
  // return 1;
}

/*event outfield_end (t=end) {
  fprintf(ferr, "outfield_end running!\n");
  outfield(snapshot_time);
  }*/

event runredump (i++) {
if(i == j+2) {
  fprintf(ferr, "redump running!\n");
  redump(snapshot_time);  
  return 1;
}
}



