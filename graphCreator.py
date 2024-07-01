import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def createGraph():
    data = np.loadtxt('parameters.txt')
    x = data[:, 1]
    y = data[:, 0]

    plt.plot(x, y)
    plt.show()
    
createGraph()