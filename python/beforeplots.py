
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-# 
# In order to decide the variables to use, we should plot   #
# the normed variations.  I have these done with root but   #  
# I want this package to handle everything, so do that here #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-# 

from root_numpy import root2array, rec2array
import pandas as pd
from WeightTool import WeightTool
from Constants import *
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.recfunctions import append_fields

#-----------------------------------------#
# Specify file to use
#-----------------------------------------#

f_nugen   = 'trees/NuGen_10634_Aug31.root'
f_corsika = 'trees/Corsika_11362_Aug31.root'

#-----------------------------------------#
# Define variables to be plotted and also
# weight variables
#-----------------------------------------#

variables = [#'log10(hs_q_tot_pulses)',
             #'cos(spline_mpe_zen)',
             #'spline_mpe_rlogl',
             #'hs_cogz',
             #'sqrt(pow(hs_cogx,2)+pow(hs_cogy,2))',
             #'dhC_qdir_pulses/dhC_ndir_doms',
             '((q_out0/28.+q_out1/22.)/((q_out0/28.+q_out1/22.+q_out2/15.+q_in/13.)))']

plotinfo = {'xtitle' : [#'Total Charge [PE]',
                        #r'cos($\theta$)',
                        #'Fit Quality',
                        #'Center of Gravity z [m]',
                        #r'Center of Gravity $\rho$ [m]',
                        #r'Q$^{dir}$/Nch$^{dir}$',
                        'qratio'],
            'nbins' : [100], #100, 60, 50, 50, 50, 100,100],
            'range' : [(0,1)] #(0,8), (-1,1), (0,40), (-500,500), (0,800), (0,1000),(0,1)]
        }

weightvars = ['nuE',
              'NEvents',
              'OneWeight',
              'primPDG',
              'primE',
              'CorsikaDiffFlux',]
              #'honda2006_gaisserH3a_elbert_numu',
              #'sarcevic_max_gaisserH3a_elbert_numu']

#-----------------------------------------#
# Read in data
#-----------------------------------------#

# Add some selection for nonsense variables
sel="spline_mpe_zen > -999&&log10(nuE)>=6"

dt_nugen = root2array(filenames = f_nugen,
                      branches=variables + weightvars,
                      treename = "tree",
                      selection = sel)

dt_corsika = root2array(filenames = f_corsika,
                        branches=variables + weightvars,
                        treename = "tree",
                        selection = sel+"&&primPDG >= 1000260530")

#-----------------------------------------#
# Calculate the weights
#-----------------------------------------#

wt = WeightTool()

w_nugen = np.zeros(len(dt_nugen),dtype=float)
for i in range(len(dt_nugen)):
    w_nugen[i] = wt.getE2(dt_nugen[i])

w_corsika = np.zeros(len(dt_corsika),dtype=float)
for i in range(len(dt_corsika)):
    w_corsika[i] = wt.getCorsika(dt_corsika[i])

#w_nugen = w_nugen.reshape((len(w_nugen),1))
#w_nugen = pd.DataFrame(w_nugen,columns=['w'])

#-----------------------------------------#
# Merge data
#-----------------------------------------#

dt_nugen = append_fields(base  = dt_nugen,
                         names = 'we2',
                         data  = w_nugen,
                         usemask = False,
                         dtypes=float)


dt_corsika = append_fields(base  = dt_corsika,
                           names = 'wcor',
                           data  = w_corsika,
                           usemask = False,
                           dtypes=float)


#-----------------------------------------#
# Specific info for plots
#-----------------------------------------#

info = {'colors' : ['r','b'],
        'names' : [r'E$^{-2}$',r'Atmospheric $\mu$'],
        'weights' : ['we2', 'wcor'],
        }

datas = [dt_nugen] #, dt_corsika]


#-----------------------------------------#
# Loop and plot
#-----------------------------------------#


for j in range(len(variables)):

    fig, ax = plt.subplots(ncols=1, figsize=(9,6))

    var = variables[j]
    xtitle = plotinfo['xtitle'][j]

    for i in range(len(datas)):
        data = datas[i]
        name = info['names'][i]
        color = info['colors'][i]
        print "working on ", name

        plt.hist(data[var],
                 weights=data[info['weights'][i]],
                 histtype='step',
                 color=color,
                 range=plotinfo['range'][j],
                 bins=plotinfo['nbins'][j],
                 label = name,
                 #normed=True)
             )

    plt.xlabel(xtitle)
    plt.ylabel("Normalized")
    plt.legend(loc='best',numpoints=1) #,fontsize=13) #,framealpha=0)                             
    ax.set_yscale("log")
    plt.grid()
    plt.tight_layout()
    
    plt.show()






