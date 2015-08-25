
from Constants import *

from math import log, cos, log10, pi

class WeightTool:

    # Wrapper method
    def getWeight(self,varlist,sname):
        if sname == m_sname_E2:        return self.getE2(varlist)
        elif sname == m_sname_corsika: return self.getCorsika(varlist)
        else:
            print "WTF you are trying to get weight that doesn't exist!"
            print "Returning a weight of 0"
            return 0.    

    # Method to get E2 weight
    def getE2(self,varlist):
        return m_livetime * \
            varlist['OneWeight'] * \
            m_astronorm * \
            1./pow(varlist['nuE'],2) * \
            1./(m_nugenNFiles * varlist['NEvents'])
        
    # Get Corsika weight
    # For total iron primary
    def getCorsika(self, varlist):

        # only pick out iron primary
        if varlist['primPDG'] < 1000260530: 
            return 0.
                           
        shower_iron_ratio = 3 + 2.25 + 1.1 + 1.2 + 1
        number_of_shower_in_file = 1./30000;
        shower_norm_iron = shower_iron_ratio * number_of_shower_in_file;
        
        areasum = pi * pi * 800 * 2400
        fluxsum = ((pow(10.0,-5.0)-pow(10.0,-11.0))*pow(varlist['primE'],1.0))/log(10.0)
        cm2_m2  = 1.0e4

        val = m_livetime * \
              1./m_corsikaNFiles * \
              shower_norm_iron * \
              varlist['CorsikaDiffFlux'] * \
              areasum * cm2_m2 * \
              fluxsum
        
        return val
        
