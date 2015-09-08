
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=# 
# Plotting script for comparing variables after sets of selection. #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=# 

from root_numpy import root2array
import matplotlib.pyplot as plt
from MyPlots import plotAll
from optparse import OptionParser
import sys

#-----------------------------------------------#
# Options
#-----------------------------------------------#

# Variables that can be plotted
vardefs = [('log10(hs_q_tot_pulses)',r'log$_{10}$(Qtot)',50,0,6,1e-4), 
           ('cos_spline_mpe_zen',r'cos($\theta^{splinempe})$',30,-1,1,1e-5), 
           ('spline_mpe_rlogl',r'Spline MPE rlogl',100,0,20,1e-5), 
           ('hs_cogz',r'COG$_z$',100,-500,500,1e-5),
           ('hs_cogrho',r'COG$_{\rho}$',80,0,800,1e-5), 
           ('dhC_qdir_pulses_over_dhC_ndir_doms',r'Q$^{dir}$/Nch$^{dir}$',100,0,2000,1e-8),
           ('log10(trunc_bins_E)',r'log$_{10}$(Energy Proxy)',40,2,7,1e-5)]   

selections = [('','L3Muon'),
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
# Some constants to be used
#-----------------------------------------------#

savedir   = "plots/processed/"

indir     = 'processed_trees/'
f_nugen   = indir + 'tots_sig.root'
f_corsika = indir + 'tots_bkg.root'

info = { 'names' : [r'Conv. $\nu_{\mu}$',r'Prompt $\nu_{\mu}$','E$^{-2}$'],
         'files'   : [ f_nugen , f_nugen, f_nugen ],
         'colors'  : [ 'b', 'g', 'm' ],
         'weights' : ['w_conv', 'w_prompt', 'w'] }


#-----------------------------------------------#
# Load Data
#-----------------------------------------------#

indata = []
for f in info['files']:
    indata.append( root2array(f, treename="tree", branches=branches, selection=sel) )

plotAll(indata, info, var, xtitle, 
        nbins, xmin, xmax, ysf,
        options.logy,
        options.show,
        options.save,
        savename)
