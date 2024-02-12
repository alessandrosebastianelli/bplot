import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse
import json
import sys

def __read_data(path):
    return pd.read_csv(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', required=True,   action="store", help='Path to file')
    parser.add_argument('-x', '--xvar', default=None,    action="store", help='Variable for x-axis')
    parser.add_argument('-y', '--yvar', default=None,    action="store", help='Variable for y-axis')
    parser.add_argument('-g', '--grid', default='False', action="store", help='Activate Grid')
    parser.add_argument('-h', '--hist', default='False', action="store", help='Plot histogram')
    args = parser.parse_args()

    # Arguments    
    data = __read_data(args.path)
    xvar = args.xvar
    yvar = args.yvar
    grid = json.loads(args.grid.lower())
    hist = json.loads(args.hist.lower())

    # Plot
    fig, ax = plt.subplots(nrows=1, ncols=1)
    
    if xvar is not None and yvar is not None: ax.plot(data[xvar], data[yvar])
    elif xvar is not None and yvar is None:   ax.plot(data[xvar], data)
    elif xvar is None and yvar is not None:   ax.plot(data[yvar])
    else:                                     ax.plot(data)
    if grid: ax.grid()



    plt.show()


if __name__ == '__main__':
    main()