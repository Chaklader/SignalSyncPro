'''

@file    loopDelayObj.py
@author  Robert Oertel, Jakob Erdmann
@date    2010-03-05
@version 2013-07-31 (for theis:  Arefe, C.,A.)
Copyright (C) 2010 DLR/TS, Germany
All rights reserved

'''

import os, sys 
import subprocess
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from constants import YELLOW_TIME, ALLRED_TIME, MIN_GREEN_TIME, simulationLimit
from common import traci, all_vehicles_arrived, simstep
from tls_constants import initialPhase, is_green, is_yellow, is_red, is_bus_priority, is_pedestrian_priority, next_phase, pOne, \
    pFour, busPriorityLane, maxGreen
from detectors import detectorInfo, pedPhaseDetector

from pedestrain_phase import pedestrainValue

PORT = 8816


class loopDelay():
	def __init__(self, tlsId,detectorsForPhase, maxGreen):
		self.tlsId = tlsId
		self.maxGreen = maxGreen
		self.detectorsForPhase = detectorsForPhase
		self.green_steps = [0,0]
		self.yellow_steps = [0,0]
		self.red_steps = [0,0]
		self.critical_delay = 3.0
		self.skipStartingPhase=[9999, 9999]
		self.busArrivalValue = [False, False]		
		self.syncronizationTime = [999999, 999999]
		self.syncronizationValue = [False, False]
		self.pedestrainPhaseNumber = 0

	def check_detector(self, det_id):
		return traci.inductionloop.getTimeSinceDetection(det_id) > self.critical_delay

	def check_pedestrian(self, det_id):
		speed = traci.inductionloop.getLastStepMeanSpeed(det_id)
		return speed != -1 and speed < 0.1

	def chek_phaseSkipping(self, currentPhase,nodeNumber, step):
		# works if pedestrain high volume: p4 -> p5 in end of Red after p4
		if is_pedestrian_priority(currentPhase) and any( self.check_pedestrian(det_id) for det_id in pedPhaseDetector[nodeNumber]) :
			# For counting how many p5 required, where  and when 
			self.pedestrainPhaseNumber = self.pedestrainPhaseNumber +1
			pedestrainString='Interesction number = {0}, Simulation time ={1}, Pedestrain phase number = {2}'.format(nodeNumber, step, self.pedestrainPhaseNumber)
			pedestrainValue.write('{0}\n'.format(pedestrainString))
			# --------------------------------------------------
			traci.trafficlight.setPhase(self.tlsId[nodeNumber], next_phase(currentPhase)) # towards p5
			self.red_steps[nodeNumber] = 0

		# no pedestrian, bus or normal skipping from p4 -> p1
		elif currentPhase == self.skipStartingPhase[nodeNumber]+2:
			# co-ordination
			if self.syncronizationValue[nodeNumber]: 
			
				traci.trafficlight.setPhase(self.tlsId[nodeNumber], initialPhase)
				self.syncronizationValue[nodeNumber] = False

			# bus
			elif self.busArrivalValue[nodeNumber]:
				traci.trafficlight.setPhase(self.tlsId[nodeNumber], pOne)
				self.busArrivalValue[nodeNumber] = False

			# max green or actuation logic
			else:
				traci.trafficlight.setPhase(self.tlsId[nodeNumber], initialPhase)

			self.skipStartingPhase[nodeNumber] = 9999
			self.red_steps[nodeNumber] = 0

		else:
			traci.trafficlight.setPhase(self.tlsId[nodeNumber], next_phase(currentPhase))
			self.red_steps[nodeNumber] = 0

	def control(self, step):
		for node_Nr in range(len(self.tlsId)):
			current_phase = traci.trafficlight.getPhase(self.tlsId[node_Nr]) 

			if current_phase == pOne:
				self.synchronization(node_Nr, step)

			# enter the phases
			self.greenActuation(current_phase, node_Nr, step) 
			self.yellowActuation(current_phase, node_Nr)
			self.redActuation(current_phase, node_Nr, step)

	def greenActuation(self, currentPhase,nodeNumber,step):
		# works for p1,p2,p3,p4
		if is_green(currentPhase):
			detectorList = self.detectorsForPhase[currentPhase][nodeNumber]
			self.green_steps[nodeNumber] = self.green_steps[nodeNumber] + 1

			if self.green_steps[nodeNumber] >= MIN_GREEN_TIME:
				# maximum green time check
				if self.green_steps[nodeNumber] == self.maxGreen[currentPhase]:                   
					self.mainCircularFlow(currentPhase,nodeNumber)

				#	syncronization condition
				elif step >= self.syncronizationTime[nodeNumber]:
					if currentPhase == pOne: 
						self.syncronizationTime[nodeNumber] = 999999

					else:
						traci.trafficlight.setPhase(self.tlsId[nodeNumber], next_phase(currentPhase))                     
						self.skipStartingPhase[nodeNumber] = currentPhase
						self.syncronizationValue[nodeNumber] = True 
						self.syncronizationTime[nodeNumber] = 999999
						self.green_steps[nodeNumber] = 0

				# 2	p2,p3,p4
				elif is_bus_priority(currentPhase) and any(self.busPriority(lane) for lane in busPriorityLane[nodeNumber]): 			
					traci.trafficlight.setPhase(self.tlsId[nodeNumber], next_phase(currentPhase))                    
					self.skipStartingPhase[nodeNumber] = currentPhase
					self.busArrivalValue[nodeNumber] = True                    
					self.green_steps[nodeNumber] = 0
					

				# 3 p1,p2,p3,p4 

				elif all( self.check_detector(det_id) for det_id in detectorList[0]): # car's 	    
																					
					if all( self.check_detector(det_id) for det_id in detectorList[1]): # bicycle's
					
						if currentPhase == pOne and any(self.busPriority(lane) for lane in busPriorityLane[nodeNumber]):                    
							pass
						else:
							self.mainCircularFlow(currentPhase,nodeNumber)

				else:
					pass

	def yellowActuation(self, currentPhase,nodeNumber):
		if is_yellow(currentPhase): 
			self.yellow_steps[nodeNumber] = self.yellow_steps[nodeNumber] + 1

			if self.yellow_steps[nodeNumber] == YELLOW_TIME:
				traci.trafficlight.setPhase(self.tlsId[nodeNumber], next_phase(currentPhase))
				self.yellow_steps[nodeNumber] = 0

	def redActuation(self, currentPhase,nodeNumber, step):
		if is_red(currentPhase): 
			self.red_steps[nodeNumber] = self.red_steps[nodeNumber] + 1

			if self.red_steps[nodeNumber] == ALLRED_TIME:
				self.chek_phaseSkipping(currentPhase,nodeNumber, step)

	def busPriority(self, laneName):
		for vehicleName in  traci.lane.getLastStepVehicleIDs(laneName):
			if traci.vehicle.getTypeID(vehicleName)=='bus':
				return True
			else:
				return False

	# p1 to p4 circular flow
	def mainCircularFlow(self, currentPhase,nodeNumber): 
		if currentPhase == pFour:
			traci.trafficlight.setPhase(self.tlsId[nodeNumber], next_phase(currentPhase))
			self.skipStartingPhase[nodeNumber] = currentPhase
			self.green_steps[nodeNumber] = 0

		# p1,p2,p3
		else:
			traci.trafficlight.setPhase(self.tlsId[nodeNumber], next_phase(currentPhase))
			self.green_steps[nodeNumber] = 0

	def synchronization(self,nodeNum, step):
		if nodeNum == 0:
			self.syncronizationTime[1] = 22+step
		elif nodeNum == 1:
			self.syncronizationTime[0] = 22+step
		else:
			print("co-ordination error")


def run(sumoExe, max_steps):
	sumoProcess = subprocess.Popen([sumoExe, "-c", "test.sumocfg"], stdout=sys.stdout, stderr=sys.stderr)
	traci.init(PORT)

	TLS_ID = traci.trafficlight.getIDList()

	for trafficLightId in TLS_ID:
		traci.trafficlight.setPhase(trafficLightId, initialPhase)

	loopDelayObj = loopDelay(TLS_ID, detectorInfo, maxGreen)
	step = simstep()

	while step < max_steps and not all_vehicles_arrived():
		step = simstep()
		loopDelayObj.control(step)

	traci.close()
	sys.stdout.flush()


def main():
	sumoExe = "sumo-gui"  # if len(sys.argv) == 1 else "sumo-gui"

	if "SUMO_BINDIR" in os.environ:
		sumoExe = os.path.join(os.environ["SUMO_BINDIR"], sumoExe)

	run(sumoExe,simulationLimit)


if __name__ == "__main__":
	main()
