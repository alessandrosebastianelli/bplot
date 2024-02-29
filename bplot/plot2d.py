import cartopy.mpl.ticker as cticker
import matplotlib.pyplot as plt
from tkinter import filedialog
import cartopy.crs as ccrs
import numpy as np
import argparse
import cartopy
import logging
import random
import json


from pyosv.io.reader import load

def plot2d() -> tuple:
    '''
        Plot images

        Arguments
        ---------
        - -p/--path   [optional]: path of the pandas-readable file from where to load the data,          
        - -v/--var    [optional]: name of the variable to bplot if the image contains dictionary 
        - -b/--band   [required]: idex or idexes (in append mode e.g. -b 1 -b 2 -b 3) for band/s to be plotted
        - -l/--vmin   [optional]: min value to be plotted
        - -u/--vamx   [optional]: max value to be plotted
        - -c/--cbar   [optional]: add color bar
        - -m/--cmap   [optional]: colormap to be used

        Returns
        -------
        - fig: matplotlib figure
        - ax: matplolib ax/axes
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path',   default=None,    action="store",       help='Path to file')
    parser.add_argument('-v', '--var',    default=None,    action="store",       help='Variable to plot')
    parser.add_argument('-b', '--band',   required=True,   action="append",      help='Bands to plot')
    parser.add_argument('-l', '--vmin',   default=0,       action="store",       help='Max pixel value')
    parser.add_argument('-u', '--vmax',   default=1,       action="store",       help='Min pixel value')
    parser.add_argument('-c', '--cbar',                    action="store_true",  help='Add colorbar')
    parser.add_argument('-m', '--cmap',   default=None,    action="store",       help='Modify colormap')
    args = parser.parse_args()

    # Read Data    
    path = args.path

    if path is None: path = filedialog.askopenfilename()
    data, _, _ = load(path)
    
    # Arguments  
    var   = args.var
    bands = [int(b) for b in args.band]
    vmin  = float(args.vmin)
    vmax  = float(args.vmax)
    cbar  = args.cbar
    cmap  = args.cmap

    
    if '.nc' in args.path: data = np.moveaxis(data.variables[var], 0, -1)
    if (len(bands) != 1) and (len(bands) != 3): raise Exception('Bands can be 1 or 3')
    if len(bands) == 1: args = data[:,:,bands[0]]
    if len(bands) == 3: 
        args = np.moveaxis(np.array([data[:,:,bands[0]],data[:,:,bands[1]],data[:,:,bands[2]]]), 0, -1)
        args = (args - vmin) / (vmax - vmin)
        args = args.tolist()


    kwargs = {"vmin": vmin, "vmax": vmax}
    if cmap is not None: kwargs['cmap'] = cmap

    # Plot 
    fig, ax = plt.subplots(nrows=1, ncols=1)

    p = ax.imshow(args, **kwargs)

    if cbar is True: plt.colorbar(p)  # Add colorbar with label

    plt.show()

    return fig, ax


if __name__ == '__main__':
    plot2d()
