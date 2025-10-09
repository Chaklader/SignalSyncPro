"""
FIXED Reward Function for DRL Traffic Control
"""
import numpy as np
from drl.config import DRLConfig

class RewardCalculator:
    """
    Calculate multi-objective reward for traffic control with NORMALIZED rewards
    """
    def __init__(self):
        self.prev_metrics = {}
        self.episode_step = 0
        
    def reset(self):
        """Reset for new episode"""
        self.prev_metrics = {}
        self.episode_step = 0
        
    def calculate_reward(self, traci, tls_ids, action, current_phases):
        """
        Modal-weighted reward calculation
        """
        self.episode_step += 1
        
        # Count stopped vehicles by mode
        stopped_by_mode = {'car': 0, 'bicycle': 0, 'bus': 0, 'pedestrian': 0}
        total_by_mode = {'car': 0, 'bicycle': 0, 'bus': 0, 'pedestrian': 0}
        
        for veh_id in traci.vehicle.getIDList():
            try:
                vtype = traci.vehicle.getTypeID(veh_id)
                speed = traci.vehicle.getSpeed(veh_id)
                
                # Classify vehicle by vType ID
                if vtype == 'Volkswagen':
                    mode = 'car'
                elif vtype == 'Raleigh':
                    mode = 'bicycle'
                elif vtype == 'bus':
                    mode = 'bus'
                elif vtype == 'Berliner':
                    mode = 'pedestrian'
                else:
                    mode = 'car'  # Default fallback
                
                total_by_mode[mode] += 1
                if speed < 0.1:  # Stopped
                    stopped_by_mode[mode] += 1
            except:
                continue
        
        # Calculate weighted stopped ratio
        weights = {'car': 1.2, 'bicycle': 1.0, 'bus': 1.5, 'pedestrian': 1.0}
        
        weighted_stopped = 0
        weighted_total = 0
        
        for mode in stopped_by_mode:
            weighted_stopped += stopped_by_mode[mode] * weights[mode]
            weighted_total += total_by_mode[mode] * weights[mode]
        
        if weighted_total > 0:
            stopped_ratio = weighted_stopped / weighted_total
        else:
            stopped_ratio = 0.0
        
        # Reward calculation
        reward = -stopped_ratio  # Penalty for stopped vehicles
        reward += (1.0 - stopped_ratio) * 0.5  # Bonus for flow
        
        # Sync bonus
        phase_list = list(current_phases.values())
        both_phase_1 = len(phase_list) >= 2 and all(p in [0, 1] for p in phase_list)
        if both_phase_1:
            reward += 1.0
        
        reward = np.clip(reward, -2.0, 2.0)
        
        info = {
            'stopped_by_mode': stopped_by_mode,
            'total_by_mode': total_by_mode,
            'weighted_stopped_ratio': stopped_ratio,
            'sync_achieved': both_phase_1,
            'event_type': 'sync_success' if both_phase_1 else 'normal'
        }
        
        return reward, info
    
    def _get_instantaneous_waiting_times(self, traci):
        """
        Get CURRENT waiting times (not cumulative)
        Only count vehicles currently waiting
        """
        waiting_times = {
            'car': [],
            'bicycle': [],
            'pedestrian': [],
            'bus': []
        }
        
        # Get all vehicles currently in simulation
        for veh_id in traci.vehicle.getIDList():
            try:
                vtype = traci.vehicle.getTypeID(veh_id)
                
                # Get CURRENT waiting time (seconds stopped)
                wait_time = traci.vehicle.getAccumulatedWaitingTime(veh_id)
                speed = traci.vehicle.getSpeed(veh_id)
                
                # Only count if currently stopped
                if speed < 0.1:
                    if 'Volkswagen' in vtype or 'passenger' in vtype.lower():
                        waiting_times['car'].append(wait_time)
                    elif 'Raleigh' in vtype or 'bicycle' in vtype.lower():
                        waiting_times['bicycle'].append(wait_time)
                    elif 'bus' in vtype.lower():
                        waiting_times['bus'].append(wait_time)
            except:
                continue
        
        # Calculate AVERAGE for this timestep
        for mode in waiting_times:
            if waiting_times[mode]:
                waiting_times[mode] = np.mean(waiting_times[mode])
            else:
                waiting_times[mode] = 0.0
        
        return waiting_times
    
    def _calculate_weighted_waiting(self, waiting_times):
        """Calculate weighted average (in seconds)"""
        weighted_sum = (
            DRLConfig.WEIGHT_CAR * waiting_times['car'] +
            DRLConfig.WEIGHT_BICYCLE * waiting_times['bicycle'] +
            DRLConfig.WEIGHT_PEDESTRIAN * waiting_times.get('pedestrian', 0) +
            DRLConfig.WEIGHT_BUS * waiting_times['bus']
        )
        total_weight = (DRLConfig.WEIGHT_CAR + DRLConfig.WEIGHT_BICYCLE + 
                       DRLConfig.WEIGHT_PEDESTRIAN + DRLConfig.WEIGHT_BUS)
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def _check_sync_success(self, current_phases):
        """
        Simple sync check: both intersections in Phase 1 simultaneously
        """
        phase_list = list(current_phases.values())
        if len(phase_list) >= 2:
            # Check if both are in Phase 1 (phases 0 or 1)
            return all(phase in [0, 1] for phase in phase_list)
        return False
    
    def _pedestrian_demand_high(self, traci, tls_ids):
        """Check if pedestrian demand justifies Phase 5"""
        # Simple heuristic: count pedestrians
        # This is placeholder - implement based on your pedestrian detection
        return False
    
    def _classify_event(self, action, sync_achieved, ped_phase_active):
        """Classify event type for PER prioritization"""
        if ped_phase_active:
            return 'pedestrian_phase'
        elif sync_achieved:
            return 'sync_success'
        elif action == 1:  # Skip to Phase 1
            return 'sync_attempt'
        else:
            return 'normal'
