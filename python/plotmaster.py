
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=# 
# Plotting script for comparing variables after sets of selection. #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=# 

from root_numpy import root2array
import matplotlib.pyplot as plt
from MyPlots import plotAll, plotStacked
from optparse import OptionParser
import sys
import numpy as np

#-----------------------------------------------#
# Options
#-----------------------------------------------#

# Variables that can be plotted
vardefs = [('log10(hs_q_tot_pulses)',r'log$_{10}$(Qtot)',50,0,6,1e-7), 
           ('cos_spline_mpe_zen',r'cos($\theta^{splinempe})$',30,-1,1,1e-7), 
           ('spline_mpe_rlogl',r'Spline MPE rlogl',30,5,20,1e-7), 
           ('hs_cogz',r'COG$_z$',100,-500,500,1e-7),
           ('hs_cogrho',r'COG$_{\rho}$',80,0,800,1e-7), 
           ('dhC_qdir_pulses_over_dhC_ndir_doms',r'Q$^{dir}$/Nch$^{dir}$',30,0,2000,1e-10),
           ('log10(dhC_qdir_pulses)',r'Q$^{dir}$',20,0,10,1e-8),
           ('dhC_ndir_doms',r'Nh$^{dir}$',25,0,500,1e-8),
           ('hs_z_travel','Z Travel$',25,-500,500,1e-8),
           ('cogz_sigma',r'COG$_{z}$ $\sigma$',50,0,450,1e-8),
           ('log10(trunc_bins_E)',r'log$_{10}$(Energy Proxy)',40,2,7,1e-5)]   

selections = [('EHEFilter','L3Muon'),
              ('log10(hs_q_tot_pulses)>3','Qtot1k'),
              ('cos_spline_mpe_zen<0.2','Upgoing'),
              ('cos_spline_mpe_zen>=0.2','Downgoing'),
              ('score>0.6','L3Muon_bdt06'),
              ('score>0.7','L3Muon_bdt07')]

# Setup opt parser
parser = OptionParser()
parser.add_option("--vopt", action="store",
                  default=-1, dest="varopt",
                  type="int",
                  help="Which branch to plot")
parser.add_option("--sopt", action="store",
                  default=-1, dest="selopt",
                  type="int",
                  help="Which pre-defined selection to use")
parser.add_option("--save", action="store_true",
                  default=False, dest="save",
                  help="Save figure?")
parser.add_option("--show", action="store_true",
                  default=False, dest="show",
                  help="Show figure")
parser.add_option("--logy", action="store_true",
                  default=False, dest="logy",
                  help="Show figure")


# Load options
options, args = parser.parse_args()
vopt   = options.varopt

if vopt < 0:
    print "Please select a variable to plot"
    print "that is in vardefs"
    sys.exit()

sopt = options.selopt
if sopt < 0:
    print "Please choose a predefined selection"
    print "that is in selections"
    sys.exit()

vopt   = options.varopt
var    = vardefs[vopt][0]
xtitle = vardefs[vopt][1]
nbins  = vardefs[vopt][2]
xmin   = vardefs[vopt][3]
xmax   = vardefs[vopt][4]
ysf    = vardefs[vopt][5]

branches = [var] + ['w','w_conv','w_prompt']

sel      = selections[sopt][0]
savename = selections[sopt][0]

#-----------------------------------------------#
# Load the data
#-----------------------------------------------#

savedir   = "plots/processed/"

indir     = 'processed_trees/'
f_nugen   = indir + 'total_withweights_sig.root'
f_corsika = indir + 'total_withweights_bkg.root'
f_data    = indir + 'total_withweights_data.root'

dt_nugen   = root2array(f_nugen, treename="tree", branches=branches, selection=sel)
dt_corsika = root2array(f_corsika, treename="tree", branches=branches, selection=sel)
dt_data    = root2array(f_data, treename="tree", branches=branches, selection=sel)

# Get the variable to plot for each
var_data  = dt_data[var]
var_cor   = dt_corsika[var]
var_E2    = dt_nugen[var]
var_atmos = np.concatenate((var_E2,var_E2))
var_mc    = np.concatenate((var_cor, var_atmos))

 
# Get the weights
w_data  = dt_data['w']
w_cor   = dt_corsika['w']
w_E2    = dt_nugen['w']
w_atmos = np.concatenate((dt_nugen['w_conv'],dt_nugen['w_prompt'])) 
w_mc    = np.concatenate((w_cor, w_atmos))

info = { 'data'    : [var_data, var_mc, var_cor, var_atmos, var_E2],
         'weights' : [w_data, w_mc, w_cor, w_atmos, w_E2],
         'colors'  : ['black', 'r', 'b', 'g', 'm'],
         'names'   : ['Data', 'Bkg. Sum', r'Atmos. $\mu$', 
                      r'Atmos $\nu_{\mu}$', r'Astro $\nu_{\mu}$'],
         'ls'      : ['solid','solid','solid','solid','solid'],
         'lw'      : [0,1.5,1,1,1],
         'marker'  : ['.', ' ', ' ', ' ', ' ']}


#-----------------------------------------------#
# Make plots
#-----------------------------------------------#

plotStacked(info, var, xtitle, 
            nbins, xmin, xmax, ysf,
            options.logy,
            options.show,
            options.save,
            savename)
