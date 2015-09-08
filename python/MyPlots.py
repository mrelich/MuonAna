
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
# Not having the ROOT histogram class has made it a little dificult to   #
# plot error bars and add different features. So here make some simple   #
# classes to take care of basic plotting functions                       #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

import matplotlib.pyplot as plt
import numpy as np

#--------------------------------------------#
# Get error bars
#--------------------------------------------#
def getErrorBars(data, weights, nbins, xmin, xmax):
    
    # Get the bincontent
    bc, bins = np.histogram(data,weights=weights,
                            bins=nbins,range=(xmin,xmax))
    
    # Get the errors
    be, bins = np.histogram(data,weights=weights*weights,
                           bins=nbins,range=(xmin,xmax))

    # take sqrt
    be = np.sqrt(be)

    # Get bin centers
    center = (bins[:-1] + bins[1:])/2.

    return bc, be, center


#--------------------------------------------#
# Plot error bars
#--------------------------------------------#
def plotErrorBars(data, weights, nbins, xmin, xmax,
                  color, label):
    
    bc, be, center = getErrorBars(data, weights, nbins, xmin, xmax)
    plt.errorbar(center, bc, yerr=be, fmt='.', c='b', label=label)
