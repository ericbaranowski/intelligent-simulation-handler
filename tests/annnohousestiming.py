# -*- coding: utf-8 -*-
"""
Plotting the effect of number of houses on power flow time

@author: mikey
"""

import sys # import for utils 
sys.path.append('../utils'); sys.path.append('../'); sys.path.append('../../')
import numpy as np
import time

from utils import import_zp
from montecarlo import generateJson
from powerflowsim import PowerFlowSim
from regression_tools import TrainANN

def train(pfs):
    """
    :type pfs: PowerFlowSim object
    """
    # ANN function mapping
    before = time.time()
    ann = TrainANN(pfs.nodeloads, pfs.nodevoltages)
    ann.buildModel()
    ann.trainModel()
    ann.evaluateModel()
    ann.predictWithModel(False)
    after = time.time()
    return after - before

def viewLoadProfile(filename, length = 1000):
    import matplotlib.pyplot as plt
    sim = import_zp(filename)
    plt.plot(sim['load']['profile'][0:length])
    
def plotit(x, y):
    import matplotlib.pyplot as plt
    from textwrap import wrap
    fit = np.polyfit(x,y,1)
    fit_fn = np.poly1d(fit)        
    plt.plot(x, y, 'yo', x, fit_fn(x), '--k')
    plt.legend(['Real', 'Regression'])
    
    plt.ylabel('Training Time (s)')
    plt.xlabel('Number of Houses')
    title = 'Artifical Neural Network Training Time vs Number of Houses for a Radial Network'
    plt.title('\n'.join(wrap(title,50)))
    plt.savefig('training_time_' + str(len(x)) + 'houses.pdf', transparent = True)
    plt.show()
    
simlength = 100

data = [[], []]; k = 0
for no_houses in np.arange(10, 250, 10):
    data[0].append(no_houses);    
    generateJson(no_houses, 'mikework')
    pfs = PowerFlowSim(simlength, 'radial', '../_configs/montecarlo' + str(no_houses) + '.json')
    pfs.nrPfSim()
    
    traintime = train(pfs)
    data[1].append(traintime)
    
    print('Training time (s): ', data[1][k], ' Number of Houses: ', data[0][k]); k += 1
    
plotit(data[0], data[1])