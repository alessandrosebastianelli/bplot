import matplotlib.pyplot as plt
import numpy as np

def test():

    fig, ax = plt.subplots(nrows=1, ncols=1)

    ax.plot(np.sin(np.linspace(-np.pi, np.pi, 1000)))
    plt.show()