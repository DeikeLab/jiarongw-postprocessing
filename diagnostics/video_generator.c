 /**
  A series of diagnostics without running from dump.  */

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


/* Some info about the snapshot time and the refining criteria */
int NUMBER = 32; // Time gap in taking the snapshots
double TIME = 2; // Total number of run time
double snapshot_time; // Current snapshot time
double uemax = 0.0000001;
double femax = 0.0000001;
int LEVEL = 12;
int counting = 0;
int frame = 0;

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
  if (argc > 9)
  	frame = atoi(argv[9]);
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

event init (i = 0)
{
  char targetname[100], imagename[100];
  sprintf (targetname, "dump%g", snapshot_time);
  if (!restore (targetname)) 
  	fprintf(ferr, "Not restored!\n");
  restore (targetname);
  fprintf(ferr, "outfield_mid running!\n");
  scalar omega[], omega_air[], omega_water[];
  vorticity (u, omega);
  foreach()
  {
    omega_air[] = omega[]*(1-f[]);
    omega_water[] = omega[]*f[];
  }
  squares("omega_air", min = -450, max = 450);
  draw_vof("f");
//  cells();
  sprintf (imagename, "movie/omega_air-%d.ppm", frame);
  {
    static FILE * fp = fopen (imagename, "w");
    save (fp = fp);
  }
  clear();
  squares("omega_water");
  draw_vof("f");
  sprintf (imagename, "movie/omega_water-%d.ppm", frame);
  {
    static FILE * fp = fopen (imagename, "w");
    save (fp = fp);
  } 
  clear();
  squares("u.x");
  draw_vof("f");
  sprintf (imagename, "movie/ux-%d.ppm", frame);
  {
    static FILE * fp = fopen (imagename, "w");
    save (fp = fp);
  }
  dump("dump", list = all);
  return 1;
}



event stop (t = snapshot_time + 200) {
	fprintf(ferr, "end\n");
  return 1;
}

/*event outfield_end (t=end) {
  fprintf(ferr, "outfield_end running!\n");
  outfield(snapshot_time);
  }*/




