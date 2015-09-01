
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#
# Plot the effective area for a specificly chosen bdt cut #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-#

from MyData import Data
import numpy as np
from Options import Options

from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

import matplotlib.pyplot as plt
from sklearn.externals import joblib

from math import cos, log10, pi

#------------------------------------------------------#
# Plotting method
#------------------------------------------------------#
def ploteffarea(dt_eval, dt_train, opts):

    # If modelinput is specified then read in model
    bdt = None
    if opts.modelinput != "":
        bdt = joblib.load(opts.modelinput)
        print "Loaded model back"
        print bdt        
    else:
        print "Model not specified..."
        print "Creating classification and training again"
        bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=opts.maxdepth),
                                 algorithm = 'SAMME',
                                 n_estimators=opts.ntrees,
                                 learning_rate=opts.lrate)

        bdt.fit(dt_train.getDataNoWeight(), dt_train.targets)

    
    # Now get the bdt scores
    sig_scores = bdt.decision_function(dt_eval.getDataNoWeight()[dt_eval.targets > 0.5])
    sig_data   = dt_eval.data[dt_eval.targets > 0.5]

    # Specify the number of bins and the range
    nbins = int(30)
    xmin  = float(5)
    xmax  = float(8)
    
    # Some constants
    #solidangle = 4*pi
    solidangle = 2 * (1 + cos(85*pi/180)) * pi
    ebins_per_decade = float(nbins/(xmax-xmin))

    # Some stuff from the data
    oneweightloc = len(dt_eval.t_varnames) + dt_eval.w_varnames.index('OneWeight') 
    Eloc         = len(dt_eval.t_varnames) + dt_eval.w_varnames.index('nuE') 

    NEvents = sig_data[0][ len(dt_eval.t_varnames) + dt_eval.w_varnames.index('NEvents') ]
    nfiles  = dt_eval.sf / (NEvents*961) 

    # Basic methods
    def mcLogEBin(E):
        return int(log10(E)*ebins_per_decade)
    def mcEMin(mc_log_ebin):
        return pow(10,mc_log_ebin/ebins_per_decade)
    def mcEMax(mc_log_ebin):
        return pow(10,(1+mc_log_ebin)/ebins_per_decade)


    # Calculate effective area
    effA = np.zeros(len(sig_scores),dtype=float)
    energy = np.empty(len(sig_scores),dtype=float)
    for i in range(len(effA)):
        #print sig_data[i]
        E = sig_data[i][Eloc]
        OneWeight = sig_data[i][oneweightloc]

        mclogebin = mcLogEBin(E)
        mcemin = mcEMin(mclogebin)
        mcemax = mcEMax(mclogebin)

        if(i < 10):
            print log10(E), OneWeight, NEvents, nfiles, mclogebin, mcemin, mcemax, log10(E), ebins_per_decade, 1e-4 * OneWeight * nfiles * 1/(solidangle*(mcemax-mcemin))

        #print 1e-4 * OneWeight * nfiles * 1/(solidangle*(mcemax-mcemin))
        effA[i] = 1e-4 * OneWeight * nfiles * 1/(solidangle*(mcemax-mcemin))
        energy[i] = log10(E)



    # Draw eff area
    fig, ax = plt.subplots(ncols=1, figsize=(10,7))
    bdtcut = 0.7
    plt.hist(energy[sig_scores > bdtcut], weights=effA[sig_scores > bdtcut],
             color='b', label='NuGen (bdt > %0.2f)'%bdtcut,
             range=(xmin,xmax),
             bins=nbins,
             log=True,
             histtype='step')
    
    plt.ylim([1.e-3, 1.e4])
    plt.xlabel('log$_{10}$(E/GeV)')
    plt.ylabel('Effective Area [m$^2$]')
    plt.grid()
    plt.tight_layout()

    plt.savefig("plots/EffArea/EffArea_bdtcut%0.2f.eps"%bdtcut)
    plt.show()
