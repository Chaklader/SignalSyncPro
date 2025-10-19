"""
@file    experiment.py
@author  Jakob.Erdmann@dlr.de
@date    2011-12-14
@version $Id$

shared code for all control algorithms

Copyright (C) 2010 DLR/TS, Germany
All rights reserved
"""

import os
import sys

if "SUMO_HOME" in os.environ:
    sys.path.append(os.path.join(os.environ["SUMO_HOME"], "tools"))
else:
    exit("please declare environment variable SUMO_HOME")
import traci


def all_vehicles_arrived():
    return traci.simulation.getMinExpectedNumber() == 0


def simstep():
    traci.simulationStep()
    return traci.simulation.getTime() / 1000
