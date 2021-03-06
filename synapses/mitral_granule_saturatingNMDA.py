#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import math

# The PYTHONPATH should contain the location of moose.py and _moose.so
# files.  Putting ".." with the assumption that moose.py and _moose.so
# has been generated in ${MOOSE_SOURCE_DIRECTORY}/pymoose/ (as default
# pymoose build does) and this file is located in
# ${MOOSE_SOURCE_DIRECTORY}/pymoose/examples
# sys.path.append('..\..')
try:
    import moose
except ImportError:
    print "ERROR: Could not import moose. Please add the directory containing moose.py in your PYTHONPATH"
    import sys
    sys.exit(1)

from synapseConstants import *
    
class mitral_granule_saturatingNMDA(moose.KinSynChan):
    """Saturating NMDA synapse from mitral to granule cell."""
    def __init__(self, *args):
        #### The Mg_block way
        moose.KinSynChan.__init__(self,*args)
        self.mgblock = moose.Mg_block(self.path+"/mgblock")
        self.mgblock.CMg = mitral_granule_NMDA_MgConc
        self.mgblock.KMg_A = mitral_granule_NMDA_KMg_A
        #### KMg_B has not been wrapped properly in pymoose, needed to set it via setField available in every pymoose object
        #mgblock.KMg_B = mitral_granule_NMDA_KMg_B
        self.mgblock.setField('KMg_B',str(mitral_granule_NMDA_KMg_B))
        #### connect source to destination. excsyn2 sends Gk and Ek to mgblock. other way around gives error.
        self.connect("origChannel", self.mgblock, "origChannel")
        self.addField('mgblock')
        self.setField('mgblock','True')
        #### The Mg_block way ends
        
        ##### The NMDAChan way
        #moose.NMDAChan.__init__(self,*args)
        #self.MgConc = mitral_granule_NMDA_MgConc
        #connect this in the calling script in the usual way as below:
        #granulecomp.connect("channel", excsyn2, "channel")
        ##### The NMDAChan way - ends

        self.Ek = mitral_granule_NMDA_Ek
        self.Gbar = mitral_granule_saturatingNMDA_Gbar
        # KinSynChan is implemented from Destexhe, Mainen and Sejnowski, 1994
        # pulseWidth is the time for which the neurotransmitter is on
        self.pulseWidth = mitral_granule_saturatingNMDA_pulseWidth
        # decay time after neurotransmitter is switched off 1/beta in Destexhe, Mainen and Sejnowski, 1994
        self.tau1 = mitral_granule_saturatingNMDA_tau1
        # the fraction of bound/open receptors in infinite time with one synaptic event.
        # rise time tau2 or tau_r in the paper is calculated as tau_1*(1-rInf) and cannot be set.
        self.rInf = mitral_granule_saturatingNMDA_rInf
        self.addField('graded')
        self.setField('graded','False')

