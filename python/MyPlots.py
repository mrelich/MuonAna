
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
                  color,label,marker='.',norm=False):
    
    bc, be, center = getErrorBars(data, weights, nbins, xmin, xmax)
    plt.errorbar(center, bc, yerr=be, fmt=marker, c=color, label=label,ms=7)
    return bc, be, center

#-----------------------------------------------#
# Method to plot sets of data on same histogram
#-----------------------------------------------#
def plotAll(datas, info, 
            var, xtitle,
            nbins, xmin, xmax, ysf,
            logy=False,
            show=False,            
            save=False,
            savename="",
            norm=False):

    fig, ax = plt.subplots(ncols=1, figsize=(9,6))
    ymin = 99999
    ymax = -99999

    for i in range(len(datas)):
        data  = datas[i]
        name  = info['names'][i]
        color = info['colors'][i]
        
        # Make histogram plots
        plt.hist(data[var], 
                 weights=data[info['weights'][i]],
                 histtype='step',
                 color=color,
                 range=(xmin,xmax),
                 bins=nbins,
                 normed=norm,
        )

        # Plot Error bars
        bc, d, d = plotErrorBars(data[var], data[info['weights'][i]], 
                                 nbins, xmin, xmax, color, name)

        # Save y min and max
        if ymin > bc.min(): 
            ymin = bc.min()
        if ymax < bc.max(): 
            ymax = bc.max()

    # Logy scale
    if logy:
        plt.ylim([ysf*ymax, 5*ymax])
        ax.set_yscale("log")

    plt.xlabel(xtitle)
    plt.ylabel("Events / year / bin")
    plt.legend(loc='best',numpoints=1) #,fontsize=13) #,framealpha=0)
    plt.grid()
    plt.tight_layout()
    


    if save and len(savename) != 0:
        plt.savefig(savedir + var + "_" + savename + ".png")

    if show:
        plt.show()



#-----------------------------------------------#
# Method to plot sets of data on same histogram
#-----------------------------------------------#
def plotStacked(info, 
                var, xtitle,
                nbins, xmin, xmax, ysf,
                logy=False,
                show=False,            
                save=False,
                savename="",
                norm=False):

    fig, ax = plt.subplots(ncols=1, figsize=(9,6))
    ymin = 99999
    ymax = -99999

    for i in range(len(info['data'])):
        data   = info['data'][i]
        weight = info['weights'][i]
        name   = info['names'][i]
        color  = info['colors'][i]

        # Make histogram plots
        plt.hist(data,
                 weights=weight,
                 histtype='step',
                 color=color,
                 range=(xmin,xmax),
                 bins=nbins,
                 normed=norm,
                 #log=logy,
                 ls = info['ls'][i],
                 lw = info['lw'][i]
                 )

        # Plot Error bars
        bc, be, center = plotErrorBars(data, weight, nbins, xmin, xmax, 
                                       color, name, info['marker'][i])

        # Save y min and max
        if ymin > bc.min(): 
            ymin = bc.min()
        if ymax < bc.max(): 
            ymax = bc.max()
            
    # Hack for now: replot data so it's on top
    plotErrorBars(info['data'][0], info['weights'][0], 
                  nbins, xmin, xmax, 
                  info['colors'][0], '',
                  info['marker'][0])

    # Logy scale
    if logy:
        plt.ylim([ysf*ymax, 5*ymax])
        ax.set_yscale("log")

    plt.xlabel(xtitle)
    plt.ylabel("Events / 34 days / bin")
    plt.legend(loc='best',numpoints=1,) #,fontsize=13) #,framealpha=0)
    plt.grid()
    plt.tight_layout()
    
    if save and len(savename) != 0:
        plt.savefig(savedir + var + "_" + savename + ".png")

    if show:
        plt.show()

