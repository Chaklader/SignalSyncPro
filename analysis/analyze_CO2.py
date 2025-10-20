#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example for parsing a emissioninfo file
"""

import sys

sys.path.append("C:/Users/aref_ch/sumo-svn/tools")
# sys.path.append('D:/sumo-erdmann/tools')
import sumolib.output
from constants.constants import (
    numberOfPrivateCarPerHour,
    numberOfBiCyclePerHour,
    numberOfPedestrianPerHour,
    MINOR_TO_MAJOR_TRAFFIC_RATIO,
)

ATTR = "co2"
emissioninfos = list(sumolib.output.parse_fast(sys.argv[1], "vehicle", ["id", ATTR]))

emissionValueList = []
totalEmissionValue = 0

for emission in emissioninfos:
    co2 = float(emission.co2)

    # bus
    if "bus" in emission.id:
        emissionValueList.append(co2)

    # private cars
    elif int(emission.id) < 4e5:
        emissionValueList.append(co2)

    else:
        pass

totalEmissionValue = int(sum(emissionValueList))

senarioValue = open("emission_CO2_Senario_1.csv", "w")
senarioValue.write("Thesis Model Emission Analysis\n")
senarioValue.write("---------------------\n\n\n")

# in kg for whole simulation
senarioValue.write("Scenario name = \n\n")
senarioValue.write(
    "total emission of CO2 for the whole simulation time = {0} kg\n\n\n".format(
        totalEmissionValue / 1000000
    )
)

# SENARIO DESCRIPTION
# -------------------
senarioValue.write("Description of senario\n")
senarioValue.write("---------------------\n\n")

senarioValue.write("number of private cars ={0}\n".format(numberOfPrivateCarPerHour))
senarioValue.write("number of bicycles ={0}\n".format(numberOfBiCyclePerHour))
senarioValue.write("number of pedestrains ={0}\n".format(numberOfPedestrianPerHour))
senarioValue.write("minor to major traffic ratio ={0}\n\n\n".format(MINOR_TO_MAJOR_TRAFFIC_RATIO))
