#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example for parsing a tlsinfo file
"""
import os,sys
# sys.path.append('C:/Users/aref_ch/sumo-svn/tools') 
sys.path.append('D:/sumo-erdmann/tools')
import sumolib.output
from sumolib.miscutils import Statistics

# phasing variables
phaseOneCalled = 0 # 0
totalPhaseOneDuration = 0  # 1

phaseTwoCalled = 0 # 4
totalPhaseTwoDuration = 0 # 5

phaseThreeCalled = 0 # 8
totalPhaseThreeDuration = 0 # 9

phaseFourCalled = 0 # 12
totalPhaseFourDuration = 0 # 13

ATTR = 'phase'
tlsinfos = list(sumolib.output.parse_fast(sys.argv[1], 'tlsState', [ATTR]))

# phase numbers
# lead 	g 	y 	r
# 0		1 	2 	3 
# 4 	5 	6 	7 
# 8 	9 	10 	11
# 12 	13 	14 	15
# 16 	17 (pedestrian phase)

for tls in tlsinfos:

	if tls.phase =='0':
		phaseOneCalled = phaseOneCalled +1

	elif tls.phase =='1':
		totalPhaseOneDuration = totalPhaseOneDuration +1

	elif tls.phase =='4':
		phaseTwoCalled = phaseTwoCalled +1

	elif tls.phase =='5':
		totalPhaseTwoDuration = totalPhaseTwoDuration +1

	# p-3
	elif tls.phase =='8':
		phaseThreeCalled = phaseThreeCalled +1

	elif tls.phase =='9':
		totalPhaseThreeDuration = totalPhaseThreeDuration +1

	elif tls.phase =='12':
		phaseFourCalled = phaseFourCalled +1

	elif tls.phase =='13':
		totalPhaseFourDuration = totalPhaseFourDuration +1

	else:
		pass

phaseValue = open("Pr_1_t_phase_stretching.csv", "w") 
phaseValue.write('Node-3 informations\n')
phaseValue.write('-------------------\n')

phaseValue.write('Average duration of phase One = {0}\n'.format(totalPhaseOneDuration/phaseOneCalled))
phaseValue.write('Average duration of phase Two = {0}\n'.format(totalPhaseTwoDuration/phaseTwoCalled))
phaseValue.write('Average duration of phase Three = {0}\n'.format(totalPhaseThreeDuration/phaseThreeCalled))
phaseValue.write('Average duration of phase Four = {0}\n'.format(totalPhaseFourDuration/phaseFourCalled))




