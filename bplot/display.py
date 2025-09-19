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

def display() -> tuple:
    '''
        Plot images

        Arguments
        ---------
        - -p/--path   [optional]: path of the image to show

        Returns
        -------
        - fig: matplotlib figure
        - ax: matplolib ax/axes
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path',   default=None,    action="store",       help='Path to file')
    args = parser.parse_args()

    # Read Data    
    path = args.path

    if path is None: path = filedialog.askopenfilename()
    print(path)
    data, _, _ = load(path)
    
    
    # Plot 
    fig, ax = plt.subplots(nrows=1, ncols=1)

    p = ax.imshow(data)

    plt.show()

    return fig, ax


if __name__ == '__main__':
    display()
