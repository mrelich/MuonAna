
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
                  'hs_cogz',
                  'sqrt(pow(hs_cogx,2)+pow(hs_cogy,2))',
                  'dhC_track_length',
                  'hs_z_travel',
    ]

    # Names for output tree
    treenames = ['hs_q_tot_pulses',
                 'cos_spline_mpe_zen',
                 'spline_mpe_rlogl',
                 'hs_cogz',
                 'hs_cogrho',
                 'track_length',
                 'hs_z_travel',
             ]
                 
    
    # Names of variables for a legend or axis
    l_varnames = ['NPE',
                  r'cos($\theta$)',
                  'Fit Quality',
                  'COGz',
                  r'COG$\rho$',
                  'track length',
                  'ztravel',
    ]

    # Variable names needed for weights
    # TODO: Clean up... not all of this is weight info!
    w_varnames = ['nuE',
                  'NEvents',
                  'OneWeight',
                  'primPDG',
                  'primE',
                  'CorsikaDiffFlux',
                  'cor_Weight',
                  'cor_DiplopiaWeight',
                  'cor_Polygonato',
                  'cor_TimeScale',
                  'honda2006_gaisserH3a_elbert_numu',
                  'sarcevic_max_gaisserH3a_elbert_numu',
                  'trunc_bins_MuEres',
                  'trunc_bins_E',
                  'trunc_doms_MuEres',
                  'trunc_doms_E',
                  'spline_mpe_zen'
                  #'muE',
                  ]

    # The sample name
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
        return self.data[:,:-len(self.w_varnames+m_weightnames)]

    # Maybe we want just the weights
    def getDataWeights(self):
        return self.data[:,-len(m_weightnames)]


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
    emptydata = []
    for i in range(len(m_weightnames)):
        emptydata.append(np.zeros(len(indata),dtype=float))
    indata = append_fields(base  = indata,
                           names = m_weightnames, 
                           data  = emptydata,
                           usemask = False,
                           dtypes=float)

    # Loop and calculate the weights
    weight_tool = WeightTool()
    for i in range(len(indata)):
        
        if sname == m_sname_corsika or sname == m_sname_corsikaLE:
            indata[i][m_weightnames[0]] = weight_tool.getWeight(indata[i],sname)
            indata[i][m_weightnames[1]] = 0
            indata[i][m_weightnames[2]] = 0
        elif sname == m_sname_data:
            indata[i][m_weightnames[0]] = 1
            indata[i][m_weightnames[1]] = 0
            indata[i][m_weightnames[2]] = 0

        else:
            indata[i][m_weightnames[0]] = weight_tool.getWeight(indata[i],m_sname_E2)
            indata[i][m_weightnames[1]] = weight_tool.getWeight(indata[i],m_sname_Conv)
            indata[i][m_weightnames[2]] = weight_tool.getWeight(indata[i],m_sname_Prompt)

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
    
