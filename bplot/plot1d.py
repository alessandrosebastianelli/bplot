import matplotlib.pyplot as plt
from tkinter import filedialog
import pandas as pd
import numpy as np
import argparse
import logging
import json


def __best_axis_comb(c : int) -> list:
    '''
        Calculate a and b using c from the following equation 
        a*b=c (1) 
        a and b are used to define a matrix of plots (a rows and b columns).

        Parameters
        ----------
        - c: integers value used to get a and b from equation (1)

        Returns
        -------
        - valid_pairs: list containing pairs of a and b from equation (1)
    '''

    def find_factors(c):
        factors = []
        for i in range(1, int(c**0.5) + 1):
            if c % i == 0:
                factors.append((i, c // i))
        return factors

    factors = find_factors(c)
    valid_pairs = [(a, b) for a, b in factors if a * b == c]
    
    return valid_pairs

def __read_data(path : str, sep : str) -> pd.DataFrame:
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

def plot1d() -> tuple:
    '''
        Plot 1D variables

        Arguments
        ---------
        - -p/--path   [optional]: path of the pandas-readable file from where to load the data,          
        - -x/--xvar   [optional]: name of the variable in the pandas-readable file to be used for the x-axis
        - -y/--yvar   [optional]: name of the variable in the pandas-readable file to be used for the y-axis
        - -g/--grid   [optional]: it will add grids to the plot
        - -t/--hist   [optional]: it will add the histogram to the plot
        - -s/--sep    [optional]: pandas dataframe separator
        - -a/--all    [optional]: it will diplay all the variables in different plots
        - -l/--legend [optional]: it will add the legend to the plots

        Returns
        -------
        - fig: matplotlib figure
        - ax: matplolib ax/axes
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path',   default=None,    action="store",       help='Path to file')
    parser.add_argument('-x', '--xvar',   default=None,    action="store",       help='Variable for x-axis')
    parser.add_argument('-y', '--yvar',   default=None,    action="store",       help='Variable for y-axis')
    parser.add_argument('-g', '--grid',                    action="store_true",  help='Activate Grid')
    parser.add_argument('-t', '--hist',                    action="store_true",  help='Plot histogram')
    parser.add_argument('-s', '--sep',    default=',',     action="store",       help='Pandas dataframe separator')
    parser.add_argument('-a', '--all',                     action="store_true",  help='Plot all the variables separately')
    parser.add_argument('-l', '--legend',                  action="store_true",  help='Add legend')
    args = parser.parse_args()


    # Read Data    
    data = __read_data(args.path, args.sep)
    # Arguments  
    xvar = args.xvar
    yvar = args.yvar
    grid = args.grid
    hist = args.hist
    allp = args.all
    lege = args.legend

     # Plott all separated
    if allp:
        valid_pairs = __best_axis_comb(len(data.columns))
        if len(valid_pairs) > 1: valid_pairs = valid_pairs[1]
        else: valid_pairs = valid_pairs[0]

        if yvar is not None: logging.warning('\tWhen using -a/--all, -y/--yvar is ignored')
         # Plot with histogram
        if hist:    
            fig, ax = plt.subplots(nrows=valid_pairs[0], ncols=2*valid_pairs[1], gridspec_kw={'width_ratios': np.tile([3,1], valid_pairs[1])})

            cnt  = 0
            cols = data.columns

            for rrcc, ax2 in enumerate(ax.flatten()):

                if xvar is not None:
                    if rrcc % 2 == 0: ax2.plot(data[xvar], data[cols[cnt]], label=cols[cnt])
                    if rrcc % 2 == 1: ax2.hist(data[cols[cnt]], 200, orientation='horizontal', label=cols[cnt])
                else:                                     
                    if rrcc % 2 == 0: ax2.plot(data[cols[cnt]], label=cols[cnt])
                    if rrcc % 2 == 1: ax2.hist(data[cols[cnt]], 200, orientation='horizontal', label=cols[cnt])

                if rrcc % 2 == 1: cnt += 1
                if lege: ax2.legend()

        # Plot without histogram
        else:
            fig, ax = plt.subplots(nrows=valid_pairs[0], ncols=valid_pairs[1])

            cnt  = 0
            cols = data.columns 

            for rrcc, ax2 in enumerate(ax.flatten()):

                if xvar is not None:
                    ax2.plot(data[xvar], data[cols[cnt]], label=cols[cnt])
                else:                                     
                    ax2.plot(data[cols[cnt]], label=cols[cnt])

                cnt += 1
                if lege: ax2.legend()
    # Plott all togheter
    else:
        # Plot with histogram
        if hist:
            fig, ax = plt.subplots(nrows=1, ncols=2, gridspec_kw={'width_ratios': [3,1]})

            if xvar is not None and yvar is not None: 
                ax[0].plot(data[xvar], data[yvar], label=yvar)
                ax[1].hist(data[yvar], 200, orientation='horizontal', label=yvar)
            elif xvar is not None and yvar is None:   
                for col in data.columns:
                    if col is not xvar:
                        ax[0].plot(data[xvar], data[col], label=col)
                        ax[1].hist(data[col], 200, orientation='horizontal', label=col)
            elif xvar is None and yvar is not None:   
                ax[0].plot(data[yvar], label=yvar)
                ax[1].hist(data[yvar], 200, orientation='horizontal', label=yvar)
            else:                                     
                for col in data.columns:
                    ax[0].plot(data[col], label=col)
                    ax[1].hist(data[col], 200, orientation='horizontal', label=col)
        
            if lege: ax[0].legend()
            if lege: ax[1].legend()
    
            # Plot without histogram
        else:
            fig, ax = plt.subplots(nrows=1, ncols=1)

            if xvar   is not None and yvar is not None: 
                ax.plot(data[xvar], data[yvar], label=yvar)
            elif xvar is not None and yvar is     None: 
                for col in data.columns:
                    if col is not xvar:
                        ax.plot(data[xvar], data[col], label=col)
            elif xvar is     None and yvar is not None:
                ax.plot(data[yvar], label=yvar)
            else:                                       
                for col in data.columns:
                    ax.plot(data[col], label=col)
        
            if lege: ax.legend()
    
    # Global settings
    if grid: 
        for axis in ax.flatten(): 
            axis.grid()

    plt.show()

    return fig, ax


if __name__ == '__main__':
    plot1d()