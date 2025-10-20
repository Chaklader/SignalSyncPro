#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Example for parsing a tripinfo file
"""

import sys

sys.path.append("C:/Users/aref_ch/sumo-svn/tools")
# sys.path.append('D:/sumo-erdmann/tools')
import sumolib.output
from sumolib.miscutils import Statistics
from constants.constants import (
    numberOfPrivateCarPerHour,
    numberOfBiCyclePerHour,
    numberOfPedestrianPerHour,
    MINOR_TO_MAJOR_TRAFFIC_RATIO,
)

ATTR = "waitSteps"
tripinfos = list(sumolib.output.parse_fast(sys.argv[1], "tripinfo", ["id", ATTR]))

numOfBuses = 0
maximumAllowedWaiting = 44
busStopTime = 40

vehStats = Statistics("motor vehicles")
bicStats = Statistics("bicycles")
pedStats = Statistics("pedestrians")
busStats = Statistics("busses")

for trip in tripinfos:
    waitSteps = float(trip.waitSteps)

    if "bus" in trip.id:
        waitingTime = waitSteps - busStopTime
        busStats.add(waitingTime, trip.id)

        if waitingTime > maximumAllowedWaiting:
            numOfBuses = numOfBuses + 1

    elif int(trip.id) < 4e5:
        vehStats.add(waitSteps, trip.id)

    elif int(trip.id) < 8e5:
        bicStats.add(waitSteps, trip.id)

    else:
        pedStats.add(waitSteps, trip.id)

senarioValue = open("waitingSenarioNumber_1.csv", "w")
senarioValue.write("Thesis Model Analysis\n")
senarioValue.write("---------------------\n\n")

senarioValue.write("NOTE:\n-----\nWe counted only the vehicles who finished their journey\n\n")

senarioValue.write("{0}\n{1}\n{2}\n{3}\n\n\n".format(vehStats, bicStats, pedStats, busStats))

senarioValue.write("Description of senario\n")
senarioValue.write("---------------------\n\n")

senarioValue.write("number of private cars ={0}\n".format(numberOfPrivateCarPerHour))
senarioValue.write("number of bicycles ={0}\n".format(numberOfBiCyclePerHour))
senarioValue.write("number of pedestrains ={0}\n".format(numberOfPedestrianPerHour))
senarioValue.write("minor to major traffic ratio ={0}\n\n\n".format(MINOR_TO_MAJOR_TRAFFIC_RATIO))

senarioValue.write(
    "maximum allowed waiting in two intersection model ={0}\n".format(maximumAllowedWaiting)
)
senarioValue.write("number of buses dont follow the model={0}\n\n".format(numOfBuses))
