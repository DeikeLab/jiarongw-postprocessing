## Useful websites
[all kinds of plots] https://python-graph-gallery.com/ <br>
[seaborn style] https://seaborn.pydata.org/ <br>
[one more tutorial] https://www.machinelearningplus.com/plots/matplotlib-tutorial-complete-guide-python-plot-examples/#7.-Understanding-the-rcParams,-Colors-and-Plot-Styles <br>


## Style
### With `.mplstyle` files
[customized style files] https://matplotlib.org/tutorials/introductory/customizing.html <br>
Usage:
```python
import matplotlib.pyplot as plt
plt.style.use(['dark_background', 'presentation'])
```
### With rcParams
```python
# Method 1
mpl.rcParams['lines.linewidth'] = 2
# Method 2
mpl.rc('lines', linewidth=4, color='g')
# Reset to default
matplotlib.rcdefaults()
```


## Standalone colorbar 
Generated from specified portion of the colormap and value range. <br>
See `~/research/postprocessing/windwave/animation.ipynb`

## Quick fix
```python
fig.tight_layout()
```

## Image
`imread` read in the image as a numpy array that is of shape [height pixel number, width pixel number, color(3 or 4)]. <br>
See https://matplotlib.org/3.1.0/tutorials/introductory/images.html#sphx-glr-tutorials-introductory-images-py  <br>
Some related manipulations:
```python
image = ax.imshow(img, aspect='equal')
ax.get_xaxis().set_visible(False)
ax.set_aspect('auto')
ax.set_xlim([62, 538]) # For cropping the image
ax.set_ylim([538, 62]) # Notice that the y is in reversed order because of the correspondence between the image coordinate and the numpy array coordinate
```