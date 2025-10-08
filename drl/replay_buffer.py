"""
Prioritized Experience Replay Buffer
"""
import numpy as np
import random
from collections import deque
from drl.config import DRLConfig

class SumTree:
    """
    Binary tree for efficient prioritized sampling
    """
    def __init__(self, capacity):
        self.capacity = capacity
        self.tree = np.zeros(2 * capacity - 1)
        self.data = np.zeros(capacity, dtype=object)
        self.write_index = 0
        self.n_entries = 0
    
    def _propagate(self, idx, change):
        parent = (idx - 1) // 2
        self.tree[parent] += change
        if parent != 0:
            self._propagate(parent, change)
    
    def _retrieve(self, idx, s):
        left = 2 * idx + 1
        right = left + 1
        
        if left >= len(self.tree):
            return idx
        
        if s <= self.tree[left]:
            return self._retrieve(left, s)
        else:
            return self._retrieve(right, s - self.tree[left])
    
    def total(self):
        return self.tree[0]
    
    def add(self, priority, data):
        idx = self.write_index + self.capacity - 1
        self.data[self.write_index] = data
        self.update(idx, priority)
        
        self.write_index = (self.write_index + 1) % self.capacity
        if self.n_entries < self.capacity:
            self.n_entries += 1
    
    def update(self, idx, priority):
        change = priority - self.tree[idx]
        self.tree[idx] = priority
        self._propagate(idx, change)
    
    def get(self, s):
        idx = self._retrieve(0, s)
        data_idx = idx - self.capacity + 1
        return (idx, self.tree[idx], self.data[data_idx])

class PrioritizedReplayBuffer:
    """
    Prioritized Experience Replay Buffer for DRL
    """
    def __init__(self, capacity=DRLConfig.BUFFER_SIZE):
        self.tree = SumTree(capacity)
        self.capacity = capacity
        self.epsilon = DRLConfig.EPSILON_PER
        self.alpha = DRLConfig.ALPHA
        self.beta = DRLConfig.BETA_START
        self.beta_increment = (1.0 - DRLConfig.BETA_START) / DRLConfig.BETA_FRAMES
    
    def _get_priority(self, error, event_type='normal'):
        """
        Calculate priority with traffic-specific multipliers
        """
        priority = (abs(error) + self.epsilon) ** self.alpha
        
        # Traffic-specific priority multipliers
        multipliers = {
            'pedestrian_phase': 5.0,
            'bus_conflict': 4.0,
            'sync_success': 3.0,
            'sync_failure': 6.0,
            'safety_violation': 10.0,
            'normal': 1.0
        }
        
        return priority * multipliers.get(event_type, 1.0)
    
    def add(self, state, action, reward, next_state, done, td_error, event_type='normal'):
        """
        Add experience to buffer with priority
        """
        priority = self._get_priority(td_error, event_type)
        experience = (state, action, reward, next_state, done)
        self.tree.add(priority, experience)
    
    def sample(self, batch_size):
        """
        Sample batch with prioritized sampling
        Returns:
            experiences, indices, weights
        """
        batch = []
        indices = []
        priorities = []
        segment = self.tree.total() / batch_size
        
        # Anneal beta
        self.beta = min(1.0, self.beta + self.beta_increment)
        
        for i in range(batch_size):
            a = segment * i
            b = segment * (i + 1)
            s = random.uniform(a, b)
            
            idx, priority, data = self.tree.get(s)
            if data is not None:
                batch.append(data)
                indices.append(idx)
                priorities.append(priority)
        
        # Calculate importance sampling weights
        sampling_probs = np.array(priorities) / self.tree.total()
        weights = np.power(self.tree.n_entries * sampling_probs, -self.beta)
        weights /= weights.max()
        
        return batch, indices, weights
    
    def update_priorities(self, indices, errors):
        """
        Update priorities for sampled experiences
        """
        for idx, error in zip(indices, errors):
            priority = self._get_priority(error)
            self.tree.update(idx, priority)
    
    def __len__(self):
        return self.tree.n_entries
