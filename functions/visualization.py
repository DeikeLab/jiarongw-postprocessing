'''
    Here are some miscellanous utility functions that help with the visualization.
'''

from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.interpolate import griddata
import pandas as pd
import numpy as np
import math
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from matplotlib import animation
import matplotlib.gridspec as gridspec

# A help function for displaying the colorbar
def colorbar(mappable):
    ax = mappable.axes
    fig = ax.figure
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    return fig.colorbar(mappable, cax=cax)

# Contour plot function
def contour(field, target, axes, fieldmin = None, fieldmax = None):
    '''
    A function that interpolate a group of points on a certain plane to a x-y grid and then display
    contour of desired field on the fed in figure axes.
    Colormap used is RdBu. The extent of the plot is [-1, 1] with 100 points in each direction.
    
    field: dataframe
        Dataframe where relevant fields are contained. Necessary fields are x and y coordinate.
    target: string
        Key of the field that needs to be plotted
    figure:
        The handle of the instantiated figure axes.
    vmin, vmax: float, optional
        The minimum and maximum of color displayed. Defaults are the extrema of the field
    '''
    
    points = np.array([field.x, field.y])
    grid_x, grid_y = np.mgrid[-0.5:0.5:100j, -0.5:0.5:100j]
    grid_target = griddata((field.x, field.y), field[target], (grid_x, grid_y), method='cubic')
    # If max and min are nor specified, use field max and min
    # Notice that in griddata document: 
    # 'nearest' always puts the nearest value to a certain coordinate. But 'linear' and 'cubic' do not extrapolate 
    # but fill the values which are not within the input area with nan by default.
    # And nan propagates with np.amax, therefore nanmax needs to be used instead of amax
    if fieldmin is None:
        fieldmin = np.nanmin(grid_target)
    if fieldmax is None:
        fieldmax = np.nanmax(grid_target)
    img = axes.imshow(grid_target.T, extent=(-0.5,0.5,-0.5,0.5), vmin=fieldmin, vmax=fieldmax, cmap='RdBu', origin='lower')
    colorbar(img)

    
def series(grid, ):
    '''
    grid: tuple
        ncols = grid[1], nrows = grid[0]
    '''
    fig, ax = plt.subplots(ncols=grid[1], nrows=grid[0], figsize = [20, 40]) 
    

# A animation function that put different cases side by side in comparison
def subplot_animation(path_set, title_set, grid, subpath, frame_number = 200, interval_time = 100):
    '''
    Animate a batch of jpg images. A grid can be specified for comparison betweeen different cases.
    Slight modification to, e.g. the font size and text position, might be required for plotting different sized images.
    
    path_set: list of size n
        A list containing n sub folders
    title_set: list of size n
        A list containing all the subplot titles. Tags used to distinguish different cases.
    grid: array of 2 numbers
        Contains the desired layout of subplot. [# of lines, # of columns]
    subpath: string
        The subpath and the animation name(without frame number). For example '/test_animation/movie'.
    frame_number: int, optional
        The number of frame in total.
    interval_time: int, optional 
        The interval time between each frame in unit of micro second.
    '''

    # First set up the figure, the axis, and the plot element we want to animate
    fig = plt.figure(figsize = [15, 20])
    gs = gridspec.GridSpec(grid[0], grid[1])
    fig.tight_layout()
    ax = []
    imgplot = []
    n = len(path_set)
    for i in range(0,n):
        ax.append(fig.add_subplot(gs[(i//grid[1]), (i%grid[1])])) 
        
    # initialization function: plot the background of each frame
    def init():
        for j in range(0,n):
            img = mpimg.imread(path_set[j] + subpath +'-1.jpg')
            imgplot.append(ax[j].imshow(img)) 
        return imgplot

    # animation function.  This is called sequentially
    def animate(i):
        t = i
        for j in range(0,n):
            ax[j].clear()
            img = mpimg.imread(path_set[j] + subpath + '-%g.jpg' % (t*2))
            imgplot[j] = ax[j].imshow(img)
            ax[j].set_title(title_set[j],fontsize = 20) 
            ax[j].get_xaxis().set_visible(False)
            ax[j].get_yaxis().set_visible(False)
            ax[j].text(20, 40, "t = %0.2f T" % (t*0.1/((2*3.14)**0.5)), fontsize = 20)
        return imgplot

    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                   frames=frame_number, interval=interval_time, blit=True)

    # save the animation as an mp4.  This requires ffmpeg or mencoder to be
    # installed.  The extra_args ensure that the x264 codec is used, so that
    # the video can be embedded in html5.  You may need to adjust this for
    # your system: for more information, see
    # http://matplotlib.sourceforge.net/api/animation_api.html
    # anim.save('./basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])    
    return anim
