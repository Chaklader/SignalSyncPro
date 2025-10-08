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
        Calculate NORMALIZED reward based on INSTANTANEOUS metrics
        Returns:
            reward: float (clipped to [-2.0, +2.0])
            info: dict with reward components
        """
        self.episode_step += 1
        
        # Get CURRENT STEP metrics (not cumulative!)
        waiting_times = self._get_instantaneous_waiting_times(traci)
        
        # Calculate weighted average for THIS step
        weighted_wait = self._calculate_weighted_waiting(waiting_times)
        
        # Normalize to reasonable scale (0-1 range)
        # Average waiting time per vehicle should be 0-60 seconds
        normalized_wait = np.clip(weighted_wait / 60.0, 0, 1.0)
        
        # Check synchronization (binary: achieved or not)
        sync_achieved = self._check_sync_success(current_phases)
        
        # Check pedestrian phase activation
        ped_phase_active = any(phase == 16 for phase in current_phases.values())
        
        # FIXED REWARD CALCULATION (normalized scale)
        reward = 0.0
        
        # Waiting time penalty (scaled to -1.0 to 0)
        reward -= normalized_wait
        
        # Synchronization bonus (+0.5 if achieved)
        if sync_achieved:
            reward += 0.5
        
        # Pedestrian phase bonus (if needed and activated)
        if ped_phase_active:
            reward += 0.3
        
        # Action penalties
        if action == 3:  # Pedestrian phase
            # Penalize if activated unnecessarily
            if not self._pedestrian_demand_high(traci, tls_ids):
                reward -= 0.5
        
        # Clip final reward to reasonable range
        reward = np.clip(reward, -2.0, 2.0)
        
        info = {
            'waiting_time': weighted_wait,
            'normalized_wait': normalized_wait,
            'sync_achieved': sync_achieved,
            'reward_components': {
                'wait_penalty': -normalized_wait,
                'sync_bonus': 0.5 if sync_achieved else 0,
                'ped_bonus': 0.3 if ped_phase_active else 0
            },
            'event_type': self._classify_event(action, sync_achieved, ped_phase_active)
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
