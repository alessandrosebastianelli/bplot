import matplotlib.pyplot as plt
from tkinter import filedialog
import pandas as pd
import argparse
import json

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
        - -p/--path [optional]: path of the pandas-readable file from where to load the data,          
        - -x/--xvar [optional]: name of the variable in the pandas-readable file to be used for the x-axis
        - -y/--yvar [optional]: name of the variable in the pandas-readable file to be used for the y-axis
        - -g/--grid [optional]: if True it will add grids to the plot
        - -t/--hist [optional]: if True it will add the histogram to the plot
        - -s/--sep [optional]:  pandas dataframe separator

        Returns
        -------
        - fig: matplotlib figure
        - ax: matplolib ax/axes
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', default=None,    action="store", help='Path to file')
    parser.add_argument('-x', '--xvar', default=None,    action="store", help='Variable for x-axis')
    parser.add_argument('-y', '--yvar', default=None,    action="store", help='Variable for y-axis')
    parser.add_argument('-g', '--grid', default='False', action="store", help='Activate Grid')
    parser.add_argument('-t', '--hist', default='False', action="store", help='Plot histogram')
    parser.add_argument('-s', '--sep',  default=',',     action="store", help='Pandas dataframe separator')
    args = parser.parse_args()


    # Read Data    
    data = __read_data(args.path, args.sep)
    # Arguments  
    xvar = args.xvar
    yvar = args.yvar
    grid = json.loads(args.grid.lower())
    hist = json.loads(args.hist.lower())

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
        
        ax[0].legend()
        ax[1].legend()
    
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
        
        ax.legend()
    
    # Global settings
    if grid: ax.grid()

    plt.show()

    return fig, ax


if __name__ == '__main__':
    plot1d()