# Set the style
from matplotlib import rc
from matplotlib import pyplot as plt
def set_style():
    # text and font
    ## small, medium, large, x-large, xx-large, larger, or smaller
#     rc('font',**{'family':'serif','serif':['Palatino']})
    rc('text', usetex=True)
    plt.rcParams['text.latex.preamble'] = [r'\boldmath']
    plt.rcParams['font.size'] = 14
    plt.rcParams['axes.labelsize'] = 'medium'
    plt.rcParams['axes.titlesize'] = 'medium'
    plt.rcParams['xtick.labelsize'] = 'medium'
    plt.rcParams['ytick.labelsize'] = 'medium'
    plt.rcParams['legend.fontsize'] = 'small'
    # Figure size
    plt.rcParams['figure.figsize'] = 8, 4.8 ## figure size in inches
    plt.rcParams['figure.dpi'] = 1200        ## figure dots per inch
    # Line
    plt.rcParams['lines.linewidth'] = 2
    plt.rcParams['lines.markersize'] = 10
    # Ticks
    plt.rcParams['xtick.minor.visible'] = False
    plt.rcParams['xtick.major.size'] = 3.5