"""
Reward Function for DRL Traffic Control
"""
import numpy as np
from drl.config import DRLConfig

class RewardCalculator:
    """
    Calculate multi-objective reward for traffic control
    """
    def __init__(self):
        self.prev_waiting_times = {}
        self.prev_co2 = 0
        self.sync_success_count = 0
        
    def calculate_reward(self, traci, tls_ids, action, current_phases):
        """
        Calculate reward based on multiple objectives
        Returns:
            reward: float
            info: dict with reward components
        """
        # Get current metrics
        waiting_times = self._get_waiting_times(traci, tls_ids)
        co2_emission = self._get_co2_emission(traci, tls_ids)
        sync_achieved = self._check_sync_success(current_phases)
        equity_score = self._calculate_equity(waiting_times)
        safety_penalty = self._check_safety_violations(traci, tls_ids)
        
        # Calculate weighted average waiting time
        weighted_wait = self._calculate_weighted_waiting(waiting_times)
        
        # Reward components
        wait_penalty = -DRLConfig.ALPHA_WAIT * weighted_wait
        emission_penalty = -DRLConfig.ALPHA_EMISSION * (co2_emission / 100.0)
        sync_bonus = DRLConfig.ALPHA_SYNC if sync_achieved else 0
        equity_bonus = DRLConfig.ALPHA_EQUITY * equity_score
        safety_cost = -DRLConfig.ALPHA_SAFETY if safety_penalty else 0
        
        # Total reward
        reward = (wait_penalty + emission_penalty + sync_bonus + 
                 equity_bonus + safety_cost)
        
        info = {
            'waiting_time': weighted_wait,
            'co2_emission': co2_emission,
            'sync_achieved': sync_achieved,
            'equity_score': equity_score,
            'safety_violation': safety_penalty,
            'event_type': self._classify_event(action, sync_achieved, safety_penalty)
        }
        
        return reward, info
    
    def _get_waiting_times(self, traci, tls_ids):
        """Get waiting times by mode"""
        waiting_times = {
            'car': [],
            'bicycle': [],
            'pedestrian': [],
            'bus': []
        }
        
        for veh_id in traci.vehicle.getIDList():
            vtype = traci.vehicle.getTypeID(veh_id)
            wait_time = traci.vehicle.getWaitingTime(veh_id)
            
            if vtype == 'Volkswagen':
                waiting_times['car'].append(wait_time)
            elif vtype == 'Raleigh':
                waiting_times['bicycle'].append(wait_time)
            elif vtype == 'bus':
                waiting_times['bus'].append(wait_time)
        
        # Average per mode
        for mode in waiting_times:
            if waiting_times[mode]:
                waiting_times[mode] = np.mean(waiting_times[mode])
            else:
                waiting_times[mode] = 0
        
        return waiting_times
    
    def _calculate_weighted_waiting(self, waiting_times):
        """Calculate weighted average waiting time"""
        weighted_sum = (
            DRLConfig.WEIGHT_CAR * waiting_times['car'] +
            DRLConfig.WEIGHT_BICYCLE * waiting_times['bicycle'] +
            DRLConfig.WEIGHT_PEDESTRIAN * waiting_times['pedestrian'] +
            DRLConfig.WEIGHT_BUS * waiting_times['bus']
        )
        total_weight = (DRLConfig.WEIGHT_CAR + DRLConfig.WEIGHT_BICYCLE + 
                       DRLConfig.WEIGHT_PEDESTRIAN + DRLConfig.WEIGHT_BUS)
        return weighted_sum / total_weight
    
    def _get_co2_emission(self, traci, tls_ids):
        """Get CO2 emission rate"""
        total_co2 = 0
        for veh_id in traci.vehicle.getIDList():
            try:
                total_co2 += traci.vehicle.getCO2Emission(veh_id)
            except:
                pass
        return total_co2
    
    def _check_sync_success(self, current_phases):
        """Check if synchronization achieved"""
        # Simple check: both intersections in Phase 1
        phase_list = list(current_phases.values())
        if len(phase_list) >= 2:
            return phase_list[0] == 1 and phase_list[1] == 1
        return False
    
    def _calculate_equity(self, waiting_times):
        """Calculate equity score (lower variance = better)"""
        times = [waiting_times[mode] for mode in waiting_times]
        variance = np.var(times)
        return -variance  # Negative because lower variance is better
    
    def _check_safety_violations(self, traci, tls_ids):
        """Check for safety violations"""
        # Check for emergency stops
        for veh_id in traci.vehicle.getIDList():
            try:
                if traci.vehicle.getSpeed(veh_id) < 0.1 and traci.vehicle.getAcceleration(veh_id) < -4.5:
                    return True
            except:
                pass
        return False
    
    def _classify_event(self, action, sync_achieved, safety_violation):
        """Classify event type for PER prioritization"""
        if safety_violation:
            return 'safety_violation'
        elif action == 3:  # Pedestrian phase
            return 'pedestrian_phase'
        elif sync_achieved:
            return 'sync_success'
        else:
            return 'normal'
