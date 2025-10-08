"""
Enhanced SUMO Environment Wrapper integrating with existing SignalSyncPro infrastructure
"""
import numpy as np
import sys
import os

# Add SUMO tools to path
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)

import traci

# Import existing infrastructure
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from drl.config import DRLConfig
from drl.reward import RewardCalculator
from constants import MIN_GREEN_TIME, YELLOW_TIME, ALLRED_TIME
from tls_constants import pOne, pTwo, pThree, pFour
from detectors import detectorInfo, pedPhaseDetector

class TrafficEnvironment:
    """
    Enhanced environment wrapper using existing SignalSyncPro infrastructure
    """
    def __init__(self, sumo_config_file, tls_ids, gui=False):
        self.sumo_config_file = sumo_config_file
        self.tls_ids = tls_ids
        self.gui = gui
        self.reward_calculator = RewardCalculator()
        
        # Phase tracking (from existing code)
        self.current_phase = {tls_id: pOne for tls_id in tls_ids}
        self.phase_duration = {tls_id: 0 for tls_id in tls_ids}
        self.green_steps = {tls_id: 0 for tls_id in tls_ids}
        
        # Synchronization tracking
        self.sync_timer = {tls_id: 999999 for tls_id in tls_ids}
        self.sync_success_count = 0
        
        # Detector infrastructure (from existing code)
        self.detector_info = detectorInfo
        self.ped_phase_detectors = pedPhaseDetector
        
    def reset(self):
        """
        Reset environment for new episode
        """
        # Start SUMO using subprocess (matching main.py approach)
        import subprocess
        import time
        
        sumo_binary = "sumo-gui" if self.gui else "sumo"
        
        # Check for SUMO_BINDIR (like main.py does)
        if "SUMO_BINDIR" in os.environ:
            sumo_binary = os.path.join(os.environ["SUMO_BINDIR"], sumo_binary)
        
        # Start SUMO as subprocess (keep output visible like main.py)
        sumo_cmd = [sumo_binary, "-c", self.sumo_config_file]
        self.sumo_process = subprocess.Popen(sumo_cmd, stdout=sys.stdout, stderr=sys.stderr)
        
        # Wait a bit for SUMO to start and open port
        time.sleep(2)
        
        # Connect via TraCI (port 8816 from test.sumocfg)
        try:
            traci.init(8816)
        except Exception as e:
            print(f"Failed to connect to SUMO: {e}")
            if hasattr(self, 'sumo_process'):
                self.sumo_process.terminate()
            raise
        
        # Initialize traffic lights
        for tls_id in self.tls_ids:
            traci.trafficlight.setPhase(tls_id, pOne)
            self.current_phase[tls_id] = pOne
            self.phase_duration[tls_id] = 0
            self.green_steps[tls_id] = 0
            self.sync_timer[tls_id] = 999999
        
        self.sync_success_count = 0
        
        return self._get_state()
    
    def _get_state(self):
        """
        Extract comprehensive state from SUMO using existing infrastructure
        """
        state_features = []
        
        for node_idx, tls_id in enumerate(self.tls_ids):
            # Current phase information
            current_phase = self.current_phase[tls_id]
            phase_duration = self.phase_duration[tls_id]
            
            # One-hot encode current phase
            phase_encoding = self._encode_phase(current_phase)
            state_features.extend(phase_encoding)
            
            # Normalized phase duration
            state_features.append(min(phase_duration / 60.0, 1.0))
            
            # Queue lengths from detectors
            vehicle_queues = self._get_detector_queues(node_idx, current_phase, 'vehicle')
            bicycle_queues = self._get_detector_queues(node_idx, current_phase, 'bicycle')
            
            state_features.extend(vehicle_queues)
            state_features.extend(bicycle_queues)
            
            # Pedestrian detection
            ped_demand = self._get_pedestrian_demand(node_idx)
            state_features.append(ped_demand)
            
            # Bus presence detection
            bus_present = self._check_bus_presence_in_lanes(node_idx)
            state_features.append(float(bus_present))
            
            # Synchronization timer
            sync_timer_normalized = min(self.sync_timer[tls_id] / 30.0, 1.0)
            state_features.append(sync_timer_normalized)
            
            # Time of day (simulation time)
            sim_time = traci.simulation.getTime()
            time_normalized = (sim_time % 3600) / 3600.0  # Normalized within hour
            state_features.append(time_normalized)
        
        return np.array(state_features, dtype=np.float32)
    
    def _encode_phase(self, phase):
        """One-hot encode phase"""
        phases = [pOne, pTwo, pThree, pFour, 16]  # 16 = pedestrian phase
        encoding = [0.0] * len(phases)
        
        # Map to green phase
        if phase in [0, 1]:  # Phase 1
            encoding[0] = 1.0
        elif phase in [4, 5]:  # Phase 2
            encoding[1] = 1.0
        elif phase in [8, 9]:  # Phase 3
            encoding[2] = 1.0
        elif phase in [12, 13]:  # Phase 4
            encoding[3] = 1.0
        elif phase == 16:  # Pedestrian phase
            encoding[4] = 1.0
        
        return encoding
    
    def _get_detector_queues(self, node_idx, current_phase, vehicle_type):
        """
        Get queue lengths from detectors using existing infrastructure
        """
        queues = []
        
        try:
            if current_phase in [0, 1]:
                detector_list = self.detector_info[pOne][node_idx]
            elif current_phase in [4, 5]:
                detector_list = self.detector_info[pTwo][node_idx]
            elif current_phase in [8, 9]:
                detector_list = self.detector_info[pThree][node_idx]
            elif current_phase in [12, 13]:
                detector_list = self.detector_info[pFour][node_idx]
            else:
                return [0.0] * 4
            
            # Count vehicles at detectors
            for detector_group in detector_list:
                if isinstance(detector_group, list):
                    for det_id in detector_group:
                        try:
                            last_detection = traci.inductionloop.getTimeSinceDetection(det_id)
                            if last_detection < 3.0:
                                queues.append(1.0)
                            else:
                                queues.append(0.0)
                        except:
                            queues.append(0.0)
        except:
            queues = [0.0] * 4
        
        # Pad or truncate to fixed size
        while len(queues) < 4:
            queues.append(0.0)
        return queues[:4]
    
    def _get_pedestrian_demand(self, node_idx):
        """
        Check pedestrian demand using existing pedestrian detectors
        """
        try:
            ped_detectors = self.ped_phase_detectors[node_idx]
            for det_id in ped_detectors:
                try:
                    speed = traci.inductionloop.getLastStepMeanSpeed(det_id)
                    if speed != -1 and speed < 0.1:
                        return 1.0
                except:
                    continue
        except:
            pass
        return 0.0
    
    def _check_bus_presence_in_lanes(self, node_idx):
        """
        Check bus presence using existing bus priority lane setup
        """
        from tls_constants import busPriorityLane
        
        try:
            bus_lanes = busPriorityLane[node_idx]
            for lane_id in bus_lanes:
                for veh_id in traci.lane.getLastStepVehicleIDs(lane_id):
                    if traci.vehicle.getTypeID(veh_id) == 'bus':
                        return True
        except:
            pass
        return False
    
    def step(self, action):
        """
        Execute action in environment
        Actions:
          0: Continue current phase
          1: Skip to Phase 1 (major through)
          2: Progress to next phase
          3: Activate pedestrian phase
        """
        step_time = traci.simulation.getTime()
        
        # Execute action for all intersections
        for tls_id in self.tls_ids:
            self._execute_action_for_tls(tls_id, action, step_time)
        
        # Advance simulation by 1 second
        traci.simulationStep()
        
        # Update phase durations
        for tls_id in self.tls_ids:
            self.phase_duration[tls_id] += 1
            self.green_steps[tls_id] += 1
        
        # Update synchronization timer
        self._update_sync_timer(step_time)
        
        # Get new state
        next_state = self._get_state()
        
        # Calculate reward
        reward, info = self.reward_calculator.calculate_reward(
            traci, self.tls_ids, action, self.current_phase
        )
        
        # Check if episode done
        done = traci.simulation.getMinExpectedNumber() == 0
        
        return next_state, reward, done, info
    
    def _execute_action_for_tls(self, tls_id, action, step_time):
        """
        Execute action for specific traffic light
        """
        current_phase = self.current_phase[tls_id]
        
        if action == 0:  # Continue current phase
            pass
        
        elif action == 1:  # Skip to Phase 1
            if current_phase != pOne and self.phase_duration[tls_id] >= MIN_GREEN_TIME:
                traci.trafficlight.setPhase(tls_id, pOne)
                self.current_phase[tls_id] = pOne
                self.phase_duration[tls_id] = 0
                self.green_steps[tls_id] = 0
        
        elif action == 2:  # Next phase
            if self.phase_duration[tls_id] >= MIN_GREEN_TIME:
                next_phase = self._get_next_phase(current_phase)
                traci.trafficlight.setPhase(tls_id, next_phase)
                self.current_phase[tls_id] = next_phase
                self.phase_duration[tls_id] = 0
                self.green_steps[tls_id] = 0
        
        elif action == 3:  # Pedestrian phase
            if self.phase_duration[tls_id] >= MIN_GREEN_TIME:
                traci.trafficlight.setPhase(tls_id, 16)
                self.current_phase[tls_id] = 16
                self.phase_duration[tls_id] = 0
                self.green_steps[tls_id] = 0
    
    def _get_next_phase(self, current_phase):
        """
        Get next phase in sequence
        """
        if current_phase in [0, 1, 2, 3]:  # Phase 1
            return 4  # Phase 2 leading green
        elif current_phase in [4, 5, 6, 7]:  # Phase 2
            return 8  # Phase 3 leading green
        elif current_phase in [8, 9, 10, 11]:  # Phase 3
            return 12  # Phase 4 leading green
        elif current_phase in [12, 13, 14, 15]:  # Phase 4
            return 0  # Phase 1 leading green
        else:  # Pedestrian or other
            return 0  # Default to Phase 1
    
    def _update_sync_timer(self, step_time):
        """
        Update synchronization timer
        """
        for idx, tls_id in enumerate(self.tls_ids):
            if self.current_phase[tls_id] == pOne:
                # Set sync time for other intersection
                other_idx = 1 - idx
                other_tls_id = self.tls_ids[other_idx]
                self.sync_timer[other_tls_id] = step_time + 22  # Coordination offset
    
    def close(self):
        """Close SUMO connection and terminate subprocess"""
        try:
            traci.close()
        except:
            pass
        
        # Terminate SUMO subprocess if it exists
        if hasattr(self, 'sumo_process'):
            try:
                self.sumo_process.terminate()
                self.sumo_process.wait(timeout=5)
            except:
                try:
                    self.sumo_process.kill()
                except:
                    pass
