
from root_numpy import root2array, rec2array
import numpy as np
from numpy.lib.recfunctions import append_fields

from WeightTool import WeightTool
from Constants import *

#-----------------------------------------------------#
# Holder Class
#-----------------------------------------------------#
class Data:

    # Variables to read in
    t_varnames = ['hs_q_tot_pulses',
                  'cos(spline_mpe_zen)',
                  'spline_mpe_rlogl',
                  #'spefit2bayes_logl-spefit2_logl',
                  'hs_cogz',
                  'sqrt(pow(hs_cogx,2)+pow(hs_cogy,2))',
                  '(dhC_ndir_doms != 0 ? dhC_qdir_pulses/dhC_ndir_doms : 0)',
                  'DP_20Per'
    ]
    
    # Names of variables for a legend or axis
    l_varnames = ['NPE',
                  'cos(Spline MPE Zen)',
                  'Spline MPE rlogl',
                  'llh ratio',
                  'COGz',
                  'COGrho',
                  'NPEdir/Nchdir',
                  'Dark Percentage']

    # Variable names needed for weights
    w_varnames = ['nuE',
                  'NEvents',
                  'OneWeight',
                  'primPDG',
                  'primE',
                  'CorsikaDiffFlux',
    ]

    # THe sample name
    sname = ""

    # Variables needed for calculating eff area
    spectators = ['nuE',
                  'OneWeight',
    ]

    # Simple constructor
    def __init__(self,data=None,targets=None,sname=None,sf=1):
        self.data    = data         # list of variables per event
        self.targets = targets      # target 1-sig, 0-bkg
        self.sname   = sname        # some name in case we want to check later
        self.sf      = sf           # weight scale factor for when we divide up dataset

    def setData(self,data):
        self.data = data
    
    def setTargets(self,targets):
        self.targets = targets
    
    def setName(self,sname):
        self.sname = sname

    def setSF(self,sf):
        self.sf = sf

    def setSpectators(self, spec):
        self.specdata = spec

    # When we train and predict for 
    # the BDT we want to remove the 
    # weights from the list. 
    def getDataNoWeight(self):
        #return self.data[:,:-1]
        return self.data[:,:-len(self.w_varnames+['w'])]

    # Maybe we want just the weights
    def getDataWeights(self):
        return self.data[:,-1]

#-----------------------------------------------------#
# Data Reader
#-----------------------------------------------------#
def ReadData(path_to_file, sname, selection=""):

    # Make data object
    dataobj = Data()

    # Get the data
    indata = root2array(filenames = path_to_file,
                        treename  = "tree",
                        branches = dataobj.t_varnames+dataobj.w_varnames,
                        selection = selection)

    # Add an extra field for the weights
    indata = append_fields(base  = indata,
                           names = 'w', 
                           data  = np.zeros(len(indata),dtype=float),
                           usemask = False,
                           dtypes=float)

    # Loop and calculate the weights
    weight_tool = WeightTool()
    for i in range(len(indata)):
        indata[i]['w'] = weight_tool.getWeight(indata[i],sname)


    # Convert to record array
    #indata = rec2array(indata,fields=dataobj.t_varnames + ['w'])
    indata  = rec2array(indata)

    # Remove nan if exists
    indata = indata[~np.isnan(indata).any(axis=1)]

    # Get Entries
    nEntries = len(indata)
        
    # Set the targets
    # 1 -- signal
    # 0 -- background
    if sname == m_sname_E2: 
        targets = np.ones(nEntries,dtype=int)
    else:  
        targets = np.zeros(nEntries,dtype=int)

    # Set properties of data object
    dataobj.setData(indata)
    dataobj.setTargets(targets)
    dataobj.setName(sname)

    #print "---------------------------------------"
    #print dataobj.data
    #print dataobj.targets
    #print ""

    return dataobj
    
