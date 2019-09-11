# This is the repository for postprocessing

The basic structure is that the common functions are put under the /functions directory. Other project specific and on-the fly functions are put under their respective project directories, i.e. /turbulence, /windwave and /breaking.

## ./functions
Where functions are stored. Should 
```python
sys.path.append('/home/jiarong/research/postprocessing/functions/')
```
so that functions can be found. 

Files with capital letter contains classes, while files with lowercase letter can be called without an instance.