import matplotlib.pyplot as plt
from tkinter import filedialog
import pandas as pd
import numpy as np
import argparse
import logging
import random
import json


def __read_data(path : str, sep : str) -> pd.DataFrame():
    '''
        Load and/or process pandas dataframe using path

        Parameters
        ----------
        - path: string containing the path to the pandas dataframe,
                if none a file manager will ask for the file path
        - sep: pandas dataframe separator

        Returns
        -------
        - db: a pandas dataframe
    '''

    if path is None: path = filedialog.askopenfilename()

    db  = pd.read_csv(path, sep=sep)
    return db

def hist1d() -> tuple:
    '''
        Histogram of 1D variables

        Arguments
        ---------
        - -p/--path   [optional]: path of the pandas-readable file from where to load the data,          
        - -y/--yvar   [optional]: name of the variable in the pandas-readable file to be used for the y-axis
        - -g/--grid   [optional]: it will add grids to the plot
        - -s/--sep    [optional]: pandas dataframe separator
        - -a/--all    [optional]: it will diplay all the variables in different plots
        - -l/--legend [optional]: it will add the legend to the plots
        - -m/--marker [optional]: it will add markers to the plot
        - -b/--bins   [optional]: number of bins for the histogram

        Returns
        -------
        - fig: matplotlib figure
        - ax: matplolib ax/axes
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path',   default=None,    action="store",       help='Path to file')
    parser.add_argument('-y', '--yvar',   required=True,   action="append",      help='Variable for y-axis (append using -y y1 -y -y2)')
    parser.add_argument('-g', '--grid',                    action="store_true",  help='Activate Grid')
    parser.add_argument('-s', '--sep',    default=',',     action="store",       help='Pandas dataframe separator')
    parser.add_argument('-a', '--all',                     action="store_true",  help='Create separate plots')
    parser.add_argument('-l', '--legend',                  action="store_true",  help='Add legend')
    parser.add_argument('-b', '--bins',   default=100,     action="store",       help='Bins for histogram')
    args = parser.parse_args()


    # Read Data    
    data = __read_data(args.path, args.sep)
    # Arguments  
    yvars = args.yvar
    grid = args.grid
    allp = args.all
    lege = args.legend
    bins = int(args.bins)

    if allp:
        
        for yvar in yvars:
            args = []
            kwargs = {}

            # Filling kwargs
            if lege is True: kwargs['label'] = yvar
            kwargs['bins'] = bins

            # Filling args
            args.append(data[yvar])


            fig, ax = plt.subplots(nrows=1, ncols=1)
            ax.hist(*args, **kwargs)


            if lege is True: ax.legend()
            if grid is True: ax.grid()
            plt.show(block=False)

        plt.show()

    
    else:
        args = []
        kwargs = {}

        # Filling kwargs
        if lege is True: kwargs['label'] = yvars
        kwargs['bins'] = bins

        # Filling args
        args.append(data[yvars])


        fig, ax = plt.subplots(nrows=1, ncols=1)
        ax.hist(*args, **kwargs)

        if lege is True: ax.legend()
        if grid is True: ax.grid()
        plt.show()

    return fig, ax


if __name__ == '__main__':
    hist1d()