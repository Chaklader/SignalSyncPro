"""
Prioritized Experience Replay (PER) Buffer for Deep Reinforcement Learning

This module implements a Prioritized Experience Replay buffer that stores and samples
experiences based on their learning value (TD error). Important experiences (large
prediction errors, rare events) are sampled more frequently, accelerating learning.

===================================================================================
PRIORITIZED EXPERIENCE REPLAY FOUNDATIONS
===================================================================================

1. THE PROBLEM WITH UNIFORM SAMPLING
-------------------------------------
Standard Experience Replay (DQN 2013):
    - Stores experiences in buffer: (s, a, r, s', done)
    - Samples uniformly at random for training
    - All experiences have equal probability

Limitations:
    ✗ Rare important events sampled infrequently (safety violations)
    ✗ Easy examples over-sampled (wastes computation)
    ✗ Learning signal diluted by uninteresting experiences
    ✗ Slow learning on critical situations

Example Problem:
    Buffer contains:
        - 98% routine green light decisions (boring)
        - 2% near-collisions, sync failures (critical!)
        
    Uniform sampling:
        - Critical events sampled only 2% of time
        - Agent takes 50x longer to learn safety

2. PRIORITIZED SAMPLING SOLUTION
----------------------------------
Priority-based sampling (Schaul et al., 2016):
    - Assign priority based on learning value
    - High priority → sampled more frequently
    - Low priority → sampled less frequently

Priority Metric: TD Error
    TD_error = |r + γ·max Q(s',a') - Q(s,a)|
    
    Large TD error = Bad prediction = Learn from this!
    Small TD error = Good prediction = Already learned

Priority Formula:
    p_i = (|TD_error| + ε)^α
    
    Where:
        ε = small constant (0.01) prevents zero priority
        α = prioritization exponent (0.6)
            α=0: uniform sampling (no prioritization)
            α=1: fully prioritized (greedy)

Sampling Probability:
    P(i) = p_i^α / Σ_k p_k^α

3. IMPORTANCE SAMPLING CORRECTION
----------------------------------
Problem: Prioritized sampling introduces bias
    - Over-samples high-priority experiences
    - Changes data distribution
    - Biases gradient estimates

Solution: Importance Sampling Weights
    w_i = (1 / (N · P(i)))^β
    
    Where:
        N = buffer size
        P(i) = sampling probability for experience i
        β = importance sampling exponent (0.4 → 1.0)
            β=0: no correction (biased)
            β=1: full correction (unbiased)

Weight Normalization:
    w_i = w_i / max_j(w_j)
    
    Ensures weights ≤ 1.0 (only down-weight, never up-weight)

Loss with IS Weights:
    L = (1/B) Σ_i w_i · (Q_target - Q_current)²
    
    High-priority samples get lower weight (correct over-sampling)

4. ANNEALING SCHEDULE
----------------------
β annealing from 0.4 → 1.0:
    - Early training (β=0.4): Accept some bias for faster learning
    - Late training (β→1.0): Remove bias for convergence
    
    β_t = β_start + (1 - β_start) · (t / T)
    
    Where t = current frame, T = total frames

===================================================================================
SUM TREE DATA STRUCTURE
===================================================================================

Efficient O(log n) prioritized sampling using binary tree:

Tree Structure:
                    [Root: sum=100]
                   /                \
            [Left: 60]            [Right: 40]
            /        \              /        \
        [30]        [30]        [20]        [20]  ← Internal nodes (sums)
        / \          / \          / \          / \
      [10][20]    [15][15]    [10][10]    [5][15] ← Leaf nodes (priorities)

Properties:
    - Leaf nodes: Store priorities
    - Internal nodes: Store sum of children
    - Root node: Total priority sum
    - N leaf nodes → 2N-1 total nodes

Operations:
    1. **Add**: O(log n)
        - Insert at next available leaf
        - Propagate sum changes up tree
        
    2. **Sample**: O(log n)
        - Generate random value [0, total]
        - Traverse tree comparing to left child sum
        - Return corresponding experience
        
    3. **Update**: O(log n)
        - Update leaf priority
        - Propagate change up tree

Sampling Algorithm:
    1. Generate random value s ∈ [0, total_priority]
    2. Start at root node
    3. If s ≤ left_child_sum:
        → Go left
    4. Else:
        → Go right, subtract left_child_sum from s
    5. Repeat until leaf node reached

Example Sampling:
    Total priority = 100
    Random value s = 65
    
    Start at root (100):
        Left child = 60
        s=65 > 60 → Go right, s = 65-60 = 5
        
    At right node (40):
        Left child = 20
        s=5 < 20 → Go left
        
    At left leaf (20):
        Return this experience

===================================================================================
TRAFFIC-SPECIFIC PRIORITY MULTIPLIERS
===================================================================================

Standard PER uses only TD error for priority. We add event-type multipliers
to emphasize traffic-critical situations:

Event Type Multipliers:
    'safety_violation':  10.0x  (Near-collisions, unsafe clearances)
    'sync_failure':      6.0x   (Failed coordination attempt)
    'pedestrian_phase':  5.0x   (Vulnerable road users)
    'bus_conflict':      4.0x   (Transit priority issues)
    'sync_success':      3.0x   (Successful coordination - positive example)
    'normal':            1.0x   (Routine decisions)

Final Priority Calculation:
    priority = ((|TD_error| + ε)^α) × multiplier[event_type]

Example:
    Safety violation:
        TD_error = 15.0
        priority = (15.0 + 0.01)^0.6 × 10.0 = 38.7 × 10.0 = 387
        
    Normal decision:
        TD_error = 0.5
        priority = (0.5 + 0.01)^0.6 × 1.0 = 0.68 × 1.0 = 0.68
        
    Ratio: Safety violation sampled ~570x more frequently!

Rationale:
    - Safety critical → must learn quickly
    - Pedestrians vulnerable → high priority
    - Bus delays affect many passengers → prioritize
    - Sync success rare → ensure learning from positive examples

===================================================================================
INTEGRATION WITH DQN AGENT
===================================================================================

Agent Training Loop:
    1. Execute action, observe (s, a, r, s', done)
    2. Calculate TD_error for priority
    3. Classify event_type
    4. buffer.add(s, a, r, s', done, TD_error, event_type)
    5. Sample prioritized batch: batch, indices, weights = buffer.sample(32)
    6. Compute loss: L = Σ w_i · (target - prediction)²
    7. Update priorities: buffer.update_priorities(indices, new_TD_errors)

The cycle:
    High TD error → High priority → Sample frequently → Learn → Low TD error
    → Low priority → Sample rarely → Focus on other experiences

===================================================================================
HYPERPARAMETER CHOICES
===================================================================================

Buffer Size: 50,000 experiences
    - Large enough for diverse traffic scenarios
    - Small enough for frequent sampling of important events
    - Typical DQN uses 100K-1M, we use 50K for traffic specificity

Alpha (α = 0.6): Prioritization exponent
    - Balances prioritization vs diversity
    - α=0: uniform (no benefit)
    - α=1: greedy (overfits to high-priority)
    - α=0.6: empirically optimal balance

Beta (β: 0.4 → 1.0): Importance sampling correction
    - Starts at 0.4: accept bias for fast initial learning
    - Anneals to 1.0: remove bias for convergence
    - Annealing over 50,000 frames

Epsilon (ε = 0.01): Small constant
    - Prevents zero priority (ensures all experiences can be sampled)
    - Adds numerical stability
    - Small value (0.01) doesn't significantly affect high priorities

===================================================================================
"""

import numpy as np
import random
from controls.ml_based.drl.config import DRLConfig


class SumTree:
    """
    Binary Sum Tree for O(log n) Prioritized Sampling
    
    Efficient data structure for storing priorities and sampling experiences
    based on those priorities. Uses a binary tree where:
        - Leaf nodes store priorities for individual experiences
        - Internal nodes store sum of their children's priorities
        - Root node stores total priority sum
        
    This structure enables:
        - O(log n) priority insertion
        - O(log n) priority update
        - O(log n) proportional sampling
        - O(1) total priority query
        
    Tree Structure Example (capacity=4):
                        [Sum=100]  ← Root (total priority)
                       /          \
                  [Sum=60]      [Sum=40]  ← Internal nodes
                  /      \       /      \
              [P=30]  [P=30] [P=20]  [P=20]  ← Leaf nodes (experiences)
                 ↓       ↓      ↓       ↓
               exp0    exp1   exp2    exp3   ← Stored experiences
               
    Array Layout (2*capacity - 1 = 7 elements):
        Index:  [0,   1,    2,    3,   4,   5,   6]
        Value:  [100, 60,   40,   30,  30,  20,  20]
        Level:   Root Internal Internal Leaf Leaf Leaf Leaf
        
    Indexing Rules:
        - Parent of node i: (i - 1) // 2
        - Left child of i: 2*i + 1
        - Right child of i: 2*i + 2
        - Leaf nodes: indices [capacity-1, 2*capacity-2]
        - Data index from tree index: tree_idx - capacity + 1
        
    Sampling Algorithm:
        1. Generate random value s ∈ [0, total_priority]
        2. Traverse tree from root:
            - If s ≤ left_sum: go left
            - Else: go right, s -= left_sum
        3. Reach leaf node → return corresponding experience
        
    Complexity:
        - Insert: O(log n) - one path from leaf to root
        - Update: O(log n) - one path from leaf to root
        - Sample: O(log n) - one path from root to leaf
        - Total: O(1) - stored at root
        
    Usage:
        tree = SumTree(capacity=1000)
        
        # Add experience with priority
        tree.add(priority=5.0, data=(state, action, reward, next_state, done))
        
        # Sample proportional to priority
        total = tree.total()
        random_value = np.random.uniform(0, total)
        idx, priority, experience = tree.get(random_value)
        
        # Update priority after training
        new_priority = 10.0
        tree.update(idx, new_priority)
        
    Attributes:
        capacity (int): Maximum number of experiences
        tree (np.ndarray): Binary tree storing priority sums [2*capacity - 1]
        data (np.ndarray): Array storing experiences [capacity]
        write_index (int): Next position to write (circular buffer)
        n_entries (int): Current number of stored experiences
    """

    def __init__(self, capacity):
        """
        Initialize Sum Tree with given capacity.

        Creates binary tree structure and data storage for experiences.
        Tree size is 2*capacity - 1 to accommodate all internal and leaf nodes.

        Args:
            capacity (int): Maximum number of experiences to store
                Typical values: 10,000 - 1,000,000
                For traffic: 50,000 (DRLConfig.BUFFER_SIZE)

        Tree Initialization:
            - tree array: All zeros initially (no priorities)
            - data array: Object dtype to store arbitrary experience tuples
            - write_index: 0 (start writing at beginning)
            - n_entries: 0 (no experiences yet)

        Memory Usage:
            - tree: (2*capacity - 1) * 8 bytes (float64)
            - data: capacity * ~200 bytes (experience tuples)
            - Total: For capacity=50,000 → ~12 MB

        Example:
            # Create tree for 1000 experiences
            tree = SumTree(capacity=1000)
            print(len(tree.tree))  # 1999 (2*1000 - 1)
            print(len(tree.data))  # 1000
            print(tree.total())    # 0.0 (no priorities yet)
        """
        self.capacity = capacity
        self.tree = np.zeros(2 * capacity - 1)
        self.data = np.zeros(capacity, dtype=object)
        self.write_index = 0
        self.n_entries = 0

    def _propagate(self, idx, change):
        """
        Propagate priority change up the tree to maintain sum property.
        
        When a leaf node's priority changes, all ancestor nodes must be
        updated to reflect the new sum. This method recursively updates
        parent nodes from leaf to root.
        
        Recursive Process:
            1. Calculate parent index: parent = (idx - 1) // 2
            2. Add change to parent's sum
            3. If parent is not root: recursively propagate to grandparent
            4. If parent is root: stop (base case)
            
        Args:
            idx (int): Tree index where change occurred
                Range: [0, 2*capacity - 2]
                Usually a leaf or internal node
                
            change (float): Amount to add to sum (can be negative)
                Positive: priority increased
                Negative: priority decreased
                Zero: no change (no-op)
                
        Complexity: O(log n) where n = capacity
            - Height of binary tree = log₂(n)
            - One operation per tree level
            
        Example:
            Tree before (capacity=4):
                     [100]
                    /     \
                 [60]     [40]
                /   \     /   \
              [30] [30] [20] [20]
                           ↑
                      Change leaf from 20 → 25
                      
            Call: _propagate(idx=5, change=+5)
            
            Step 1: Update parent of idx=5
                parent = (5-1)//2 = 2
                tree[2] += 5  → [40] becomes [45]
                
            Step 2: Recursively update grandparent
                parent = (2-1)//2 = 0  
                tree[0] += 5  → [100] becomes [105]
                
            Step 3: Reached root (idx=0), stop
            
            Tree after:
                     [105]  ← Updated
                    /     \
                 [60]     [45]  ← Updated
                /   \     /   \
              [30] [30] [20] [25]  ← Changed
                           
        Notes:
            - Called by add() and update() methods
            - Maintains tree invariant: parent = left_child + right_child
            - Recursive implementation (could be iterative)
            - Critical for correct sampling probabilities
        """
        parent = (idx - 1) // 2
        self.tree[parent] += change
        if parent != 0:
            self._propagate(parent, change)

    def _retrieve(self, idx, s):
        """
        Retrieve experience by traversing tree based on cumulative priority.
        
        Implements proportional sampling: given a random value s in [0, total],
        finds the leaf node whose cumulative priority range contains s.
        
        Tree Traversal Algorithm:
            1. Start at given node (usually root)
            2. If node is leaf: return it
            3. Compare s with left child's sum:
                - If s ≤ left_sum: descend to left child
                - If s > left_sum: descend to right child, subtract left_sum from s
            4. Repeat until leaf reached
            
        Args:
            idx (int): Current node index (start with 0 for root)
                Range: [0, 2*capacity - 2]
                Traversal begins at root (idx=0)
                
            s (float): Random value for proportional sampling
                Range: [0, total_priority]
                Represents cumulative priority threshold
                
        Returns:
            int: Tree index of selected leaf node
                Range: [capacity-1, 2*capacity-2]
                Corresponds to an experience in data array
                
        Complexity: O(log n)
            - One comparison per tree level
            - Height = log₂(capacity)
            
        Example:
            Tree priorities:
                     [100]
                    /     \
                 [60]     [40]
                /   \     /   \
              [30] [30] [20] [20]
              
            Cumulative ranges:
                Leaf 0: [0, 30)    → indices 3
                Leaf 1: [30, 60)   → indices 4
                Leaf 2: [60, 80)   → indices 5
                Leaf 3: [80, 100)  → indices 6
                
            Sample with s = 65:
                Step 1: At root (idx=0)
                    left_child=1 has sum=60
                    s=65 > 60 → go right, s = 65-60 = 5
                    
                Step 2: At right child (idx=2)
                    left_child=5 has sum=20
                    s=5 < 20 → go left
                    
                Step 3: At leaf (idx=5)
                    No children → return 5
                    
            Result: Leaf 5 selected (priority=20, range [60, 80))
            
        Sampling Probability:
            P(leaf_i) = priority_i / total_priority
            
            In example:
                P(leaf 0) = 30/100 = 30%
                P(leaf 1) = 30/100 = 30%
                P(leaf 2) = 20/100 = 20%
                P(leaf 3) = 20/100 = 20%
                
        Notes:
            - Implements proportional sampling without explicit probabilities
            - Automatically handles priority updates (tree sums maintained)
            - Returns tree index, caller converts to data index
            - Guarantees sampling proportional to priorities
        """
        left = 2 * idx + 1
        right = left + 1

        if left >= len(self.tree):
            return idx

        if s <= self.tree[left]:
            return self._retrieve(left, s)
        else:
            return self._retrieve(right, s - self.tree[left])

    def total(self):
        """
        Get total priority sum (root node value).

        Returns the sum of all priorities in the tree, which is stored
        at the root node for O(1) access.

        Returns:
            float: Total priority sum
                Zero if buffer empty
                Sum of all leaf priorities if buffer has experiences

        Usage:
            # Check if buffer has any priority
            if tree.total() > 0:
                # Safe to sample
                random_value = np.random.uniform(0, tree.total())
                experience = tree.get(random_value)

            # Calculate sampling probability
            experience_priority = tree.tree[leaf_idx]
            sampling_prob = experience_priority / tree.total()

        Complexity: O(1)
            Direct array access to root node

        Example:
            tree = SumTree(4)
            print(tree.total())  # 0.0 (empty)

            tree.add(10, exp1)
            tree.add(20, exp2)
            tree.add(30, exp3)
            print(tree.total())  # 60.0

        Notes:
            - Always up-to-date due to _propagate()
            - Used for proportional sampling
            - Used for importance sampling weight calculation
        """
        return self.tree[0]

    def add(self, priority, data):
        """
        Add new experience to buffer with given priority.

        Inserts experience at next available position (circular buffer)
        and sets its priority in the tree. Automatically overwrites
        oldest experience when buffer is full.

        Process:
            1. Calculate tree index for current write position
            2. Store experience data
            3. Update priority in tree (triggers propagation)
            4. Increment write index (circular)
            5. Update entry count (up to capacity)

        Args:
            priority (float): Priority value for this experience
                Typically: (|TD_error| + ε)^α × event_multiplier
                Range: [0, ∞) but usually [0.01, 100]
                Higher priority → sampled more frequently

            data: Experience tuple to store
                Typically: (state, action, reward, next_state, done)
                Can be any Python object
                Stored in data array at write_index

        Circular Buffer Behavior:
            - write_index wraps around at capacity
            - Oldest experiences overwritten when full
            - Maintains fixed memory footprint

        Example:
            tree = SumTree(capacity=3)

            # Add experiences
            tree.add(5.0, ("state1", 0, -1.0, "state2", False))
            tree.add(10.0, ("state2", 1, 0.5, "state3", False))
            tree.add(2.0, ("state3", 2, 1.0, "state4", True))
            # Buffer full: [exp1, exp2, exp3]

            # Add fourth experience (overwrites first)
            tree.add(8.0, ("state4", 0, -0.5, "state5", False))
            # Buffer now: [exp4, exp2, exp3]

        Priority Setting:
            High priority examples:
                - Large TD errors (bad predictions)
                - Safety violations (10x multiplier)
                - Pedestrian phases (5x multiplier)

            Low priority examples:
                - Small TD errors (good predictions)
                - Routine decisions (1x multiplier)

        Notes:
            - O(log n) complexity due to tree update
            - Automatically maintains tree sum property
            - Thread-unsafe (external synchronization needed for parallel updates)
            - Does not check for duplicate experiences
        """
        idx = self.write_index + self.capacity - 1
        self.data[self.write_index] = data
        self.update(idx, priority)

        self.write_index = (self.write_index + 1) % self.capacity
        if self.n_entries < self.capacity:
            self.n_entries += 1

    def update(self, idx, priority):
        """
        Update priority of existing experience in tree.

        Changes priority of a specific leaf node and propagates the
        change up the tree to maintain sum invariant. Used after training
        to update priorities based on new TD errors.

        Update Process:
            1. Calculate change: new_priority - old_priority
            2. Set new priority at leaf
            3. Propagate change to root

        Args:
            idx (int): Tree index of experience to update
                Range: [capacity-1, 2*capacity-2] (leaf nodes)
                Obtained from sample() method
                Not the same as data array index!

            priority (float): New priority value
                Typically: (|new_TD_error| + ε)^α × event_multiplier
                Reflects updated prediction error after training

        Why Update Priorities?
            After training on an experience:
                - TD error changes (hopefully decreases)
                - Priority should reflect new learning value
                - High error experiences remain high priority
                - Low error experiences become low priority

        Example:
            # Initial state
            tree.add(10.0, experience)  # High priority (bad prediction)

            # Sample and train
            idx, priority, exp = tree.get(random_value)
            # ... train on experience ...
            new_TD_error = 0.5  # Much better prediction now!

            # Update priority
            new_priority = (0.5 + 0.01) ** 0.6 = 0.68
            tree.update(idx, new_priority)  # Low priority now

        Complexity: O(log n)
            - One update operation at leaf
            - Propagation up to root

        Update Frequency:
            - After each training batch
            - For all sampled experiences
            - Updates reflect current learning state

        Notes:
            - Critical for adaptive prioritization
            - Prevents over-sampling of "learned" experiences
            - Enables continual re-prioritization
            - Must use tree index (not data index)
        """
        change = priority - self.tree[idx]
        self.tree[idx] = priority
        self._propagate(idx, change)

    def get(self, s):
        """
        Get experience by sampling with cumulative priority value.

        Retrieves experience whose cumulative priority range contains
        the given value s. Used by buffer's sample() method for
        proportional sampling.

        Args:
            s (float): Random value for proportional sampling
                Range: [0, total_priority]
                Typically: np.random.uniform(0, tree.total())

        Returns:
            tuple: (tree_idx, priority, experience_data)

            tree_idx (int): Tree index of selected leaf
                Range: [capacity-1, 2*capacity-2]
                Use for update() after training

            priority (float): Priority of selected experience
                Useful for importance sampling weight calculation

            experience_data: Stored experience tuple
                Typically: (state, action, reward, next_state, done)
                Ready for training

        Sampling Process:
            1. Call _retrieve() to traverse tree
            2. Get tree index of selected leaf
            3. Convert tree index to data index
            4. Return (tree_idx, priority, data)

        Example:
            tree = SumTree(4)
            tree.add(30, exp1)
            tree.add(30, exp2)
            tree.add(20, exp3)
            tree.add(20, exp4)
            # Total priority = 100

            # Sample experience
            s = np.random.uniform(0, 100)  # e.g., s = 65
            tree_idx, priority, experience = tree.get(s)

            # Result (for s=65):
            # tree_idx = 5 (leaf for exp3)
            # priority = 20
            # experience = exp3

        Sampling Distribution:
            P(exp_i) = priority_i / total_priority

            In example:
                P(exp1) = 30/100 = 30%
                P(exp2) = 30/100 = 30%
                P(exp3) = 20/100 = 20%
                P(exp4) = 20/100 = 20%

        Usage Pattern:
            # Sample batch
            for i in range(batch_size):
                s = np.random.uniform(0, tree.total())
                tree_idx, priority, experience = tree.get(s)
                batch.append(experience)
                indices.append(tree_idx)
                priorities.append(priority)

        Notes:
            - Implements proportional sampling
            - No explicit probability calculation
            - O(log n) complexity
            - Returns None if tree empty (no data at index)
        """
        idx = self._retrieve(0, s)
        data_idx = idx - self.capacity + 1
        return (idx, self.tree[idx], self.data[data_idx])


class PrioritizedReplayBuffer:
    """
    Prioritized Experience Replay Buffer for Deep Reinforcement Learning

    Stores experiences with priorities based on TD error and event importance.
    Samples experiences proportional to priority, emphasizing high-value learning
    opportunities. Implements importance sampling correction to remove bias.

    Key Features:
        1. Priority-based sampling: Important experiences sampled more often
        2. Traffic-specific multipliers: Safety, pedestrian, bus events prioritized
        3. Importance sampling: Corrects bias from non-uniform sampling
        4. Beta annealing: Gradually increases bias correction (0.4 → 1.0)
        5. SumTree backend: O(log n) efficient operations

    Priority Calculation:
        priority = ((|TD_error| + ε)^α) × event_multiplier

        Where:
            TD_error: Temporal Difference error (prediction error)
            ε = 0.01: Prevents zero priority
            α = 0.6: Prioritization exponent
            event_multiplier: Traffic-specific importance

    Event Multipliers (Traffic-Specific):
        safety_violation:  10x (critical - near collisions)
        sync_failure:      6x  (coordination failure)
        pedestrian_phase:  5x  (vulnerable road users)
        bus_conflict:      4x  (transit priority)
        sync_success:      3x  (positive coordination example)
        normal:            1x  (baseline)

    Importance Sampling Weights:
        w_i = (N · P(i))^(-β) / max_j((N · P(j))^(-β))

        Where:
            N = buffer size
            P(i) = sampling probability
            β = 0.4 → 1.0 (annealed)

    Beta Annealing Schedule:
        β_t = β_start + (1 - β_start) · (t / T)
        β_start = 0.4 (accept bias early)
        β_end = 1.0 (remove bias late)
        T = 50,000 frames

    Example Usage:
        # Initialize
        buffer = PrioritizedReplayBuffer(capacity=50000)

        # Store experience
        td_error = abs(q_target - q_current)
        buffer.add(state, action, reward, next_state, done,
                  td_error, event_type='sync_success')

        # Sample prioritized batch
        if len(buffer) >= batch_size:
            batch, indices, weights = buffer.sample(batch_size=32)

            # Train with importance sampling weights
            loss = (weights * td_errors**2).mean()

            # Update priorities after training
            new_errors = compute_new_td_errors(batch)
            buffer.update_priorities(indices, new_errors)

    Integration with DQN:
        1. Agent computes TD error when storing experience
        2. Agent classifies event type (sync, ped, safety, normal)
        3. Buffer assigns priority with multipliers
        4. Buffer samples high-priority experiences more often
        5. Agent trains with importance sampling weights
        6. Agent updates priorities based on new TD errors

    Comparison with Uniform Replay:
        Uniform:
            - All experiences sampled equally
            - Rare important events under-sampled
            - Slow learning on critical situations

        Prioritized:
            - Important experiences sampled frequently
            - Fast learning on critical situations
            - Requires importance sampling correction
            - ~2x faster convergence empirically

    Memory Usage:
        Capacity 50,000:
            - SumTree: ~12 MB
            - Experiences: ~10 MB (depends on state size)
            - Total: ~22 MB

    Attributes:
        tree (SumTree): Binary tree for efficient sampling
        capacity (int): Maximum buffer size (50,000)
        epsilon (float): Small constant for priority (0.01)
        alpha (float): Prioritization exponent (0.6)
        beta (float): Importance sampling exponent (0.4 → 1.0)
        beta_increment (float): Annealing step size
    """

    def __init__(self, capacity=DRLConfig.BUFFER_SIZE):
        """
        Initialize Prioritized Replay Buffer.

        Creates SumTree backend and sets hyperparameters for prioritization
        and importance sampling correction.

        Args:
            capacity (int, optional): Maximum buffer size
                Default: DRLConfig.BUFFER_SIZE (50,000)
                Range: 1,000 - 1,000,000 typical
                Larger = more diverse experiences but slower sampling

        Hyperparameters Set:
            epsilon (ε = 0.01):
                Small constant added to priorities
                Ensures all experiences can be sampled
                Prevents division by zero

            alpha (α = 0.6):
                Prioritization exponent
                0 = uniform sampling (no prioritization)
                1 = greedy sampling (only highest priority)
                0.6 = balanced (empirically optimal)

            beta (β_start = 0.4):
                Importance sampling correction exponent
                Starts at 0.4 (accept some bias)
                Anneals to 1.0 (full correction)

            beta_increment:
                Annealing step size
                (1.0 - 0.4) / 50,000 = 0.000012 per frame
                Reaches 1.0 after 50,000 samples

        Example:
            # Standard configuration
            buffer = PrioritizedReplayBuffer()  # 50K capacity

            # Custom capacity
            buffer = PrioritizedReplayBuffer(capacity=100000)

            # Check configuration
            print(f"Capacity: {buffer.capacity}")
            print(f"Alpha: {buffer.alpha}")
            print(f"Beta: {buffer.beta}")
        """
        self.tree = SumTree(capacity)
        self.capacity = capacity
        self.epsilon = DRLConfig.EPSILON_PER
        self.alpha = DRLConfig.ALPHA
        self.beta = DRLConfig.BETA_START
        self.beta_increment = (1.0 - DRLConfig.BETA_START) / DRLConfig.BETA_FRAMES

    def _get_priority(self, error, event_type="normal"):
        """
        Calculate priority with traffic-specific multipliers.

        Combines TD error magnitude with event type importance to compute
        final priority for experience. Higher priority experiences are
        sampled more frequently during training.

        Priority Formula:
            priority = ((|error| + ε)^α) × multiplier[event_type]

        Component Breakdown:
            |error|: Absolute TD error (prediction error)
            ε: Small constant (0.01) prevents zero priority
            α: Prioritization exponent (0.6) controls priority curve
            multiplier: Traffic-specific importance factor

        Args:
            error (float): TD error magnitude
                Typically: |Q_target - Q_current|
                Range: [0, ∞) but usually [0, 50]
                Large error = bad prediction = high priority

            event_type (str, optional): Event classification
                Default: 'normal'
                Options: 'safety_violation', 'sync_failure',
                        'pedestrian_phase', 'bus_conflict',
                        'sync_success', 'normal'

        Returns:
            float: Computed priority value
                Range: [0.01, ∞) but typically [0.1, 1000]
                Higher value = more frequent sampling

        Event Type Multipliers:
            'safety_violation': 10.0x
                Near-collisions, unsafe clearances
                Critical for safety learning
                Example: Red light violation, pedestrian conflict

            'sync_failure': 6.0x
                Failed coordination between intersections
                Important for learning sync timing
                Example: Missed green wave opportunity

            'pedestrian_phase': 5.0x
                Pedestrian phase activation
                Vulnerable road users priority
                Example: Phase 5 trigger with waiting pedestrians

            'bus_conflict': 4.0x
                Bus priority issues
                Transit efficiency critical
                Example: Bus delayed despite empty intersection

            'sync_success': 3.0x
                Successful coordination
                Learn from positive examples
                Example: Perfect green wave timing

            'normal': 1.0x
                Routine traffic control
                Baseline priority
                Example: Regular phase progression

        Example Calculations:
            # Safety violation with large error
            priority = self._get_priority(error=15.0, event_type='safety_violation')
            # = (15.0 + 0.01)^0.6 × 10.0 = 38.7 × 10.0 = 387

            # Normal decision with small error
            priority = self._get_priority(error=0.5, event_type='normal')
            # = (0.5 + 0.01)^0.6 × 1.0 = 0.68 × 1.0 = 0.68

            # Sampling ratio: 387 / 0.68 ≈ 569x more frequent!

        Priority Curve (α = 0.6):
            error=0.01 → priority=0.10 (minimum)
            error=0.1  → priority=0.32
            error=1.0  → priority=1.0
            error=10.0 → priority=3.98
            error=100.0 → priority=15.8

            Sublinear growth prevents extreme priorities

        Unknown Event Types:
            - Default to 1.0x multiplier (normal priority)
            - No error raised (robust to typos)
            - Logged warning recommended (not implemented)

        Notes:
            - Alpha=0.6 provides balanced prioritization
            - Epsilon ensures non-zero priority for all experiences
            - Multipliers hand-tuned for traffic control domain
            - Could be learned adaptively (future work)
        """
        priority = (abs(error) + self.epsilon) ** self.alpha

        # Traffic-specific priority multipliers
        multipliers = {
            "pedestrian_phase": 5.0,
            "bus_conflict": 4.0,
            "sync_success": 3.0,
            "sync_failure": 6.0,
            "safety_violation": 10.0,
            "normal": 1.0,
        }

        return priority * multipliers.get(event_type, 1.0)

    def add(
        self, state, action, reward, next_state, done, td_error, event_type="normal"
    ):
        """
        Add experience to buffer with computed priority.

        Stores transition with priority based on TD error and event type.
        High-priority experiences (large errors, important events) will be
        sampled more frequently during training.

        Storage Process:
            1. Calculate priority from TD error and event type
            2. Package experience as tuple
            3. Add to SumTree with priority
            4. Automatically overwrites oldest if buffer full

        Args:
            state (np.ndarray): Current traffic state
                Shape: (45,) for two-intersection system
                Normalized features in [0, 1]

            action (int): Action taken
                Range: [0, 2]
                0=Continue, 1=Skip, 2=Next

            reward (float): Reward received
                Typical range: [-2, 2]
                Clipped for stability

            next_state (np.ndarray): Resulting state
                Shape: (45,)
                State after action execution

            done (bool): Episode termination flag
                True if episode ended
                False if episode continues

            td_error (float): Temporal Difference error
                |Q_target - Q_current|
                Measures prediction error magnitude
                Used for priority calculation

            event_type (str, optional): Event classification
                Default: 'normal'
                Used for priority multiplier
                Options: see _get_priority() for full list

        Example:
            # Store routine decision
            buffer.add(
                state=current_state,
                action=0,  # Continue
                reward=-0.3,
                next_state=next_state,
                done=False,
                td_error=0.5,
                event_type='normal'
            )
            # Priority: (0.5 + 0.01)^0.6 × 1.0 = 0.68

            # Store safety violation
            buffer.add(
                state=current_state,
                action=2,  # Next phase
                reward=-10.0,
                next_state=next_state,
                done=False,
                td_error=15.0,
                event_type='safety_violation'
            )
            # Priority: (15.0 + 0.01)^0.6 × 10.0 = 387

        Priority Impact:
            Low priority (0.1-1.0):
                - Sampled every ~1000 batches
                - Small TD error, routine decision

            Medium priority (1.0-10.0):
                - Sampled every ~100 batches
                - Moderate error or sync events

            High priority (10.0-100.0):
                - Sampled every ~10 batches
                - Large error or safety events

            Very high priority (100+):
                - Sampled almost every batch
                - Critical safety violations

        Buffer Management:
            - Circular buffer (oldest overwritten when full)
            - Capacity: 50,000 experiences
            - No duplicate detection
            - Thread-unsafe (external sync needed)

        Notes:
            - TD error must be pre-computed by agent
            - Event type must match classifier output
            - Priority updated after training via update_priorities()
            - Experiences never deleted, only overwritten
        """
        priority = self._get_priority(td_error, event_type)
        experience = (state, action, reward, next_state, done)
        self.tree.add(priority, experience)

    def sample(self, batch_size):
        """
        Sample prioritized batch with importance sampling weights.

        Samples experiences proportional to priority and computes importance
        sampling weights to correct for non-uniform sampling bias. Returns
        experiences, indices, and weights for training.

        Sampling Algorithm:
            1. Divide total priority into batch_size segments
            2. For each segment:
                a. Sample random value in segment range
                b. Retrieve experience from SumTree
                c. Record index and priority
            3. Compute importance sampling weights
            4. Normalize weights by maximum
            5. Anneal beta toward 1.0

        Args:
            batch_size (int): Number of experiences to sample
                Typical: 32-64
                Your config: 32
                Larger batch = more stable gradients but slower

        Returns:
            tuple: (batch, indices, weights)

            batch (list): Sampled experiences
                Length: batch_size
                Format: [(s, a, r, s', done), ...]
                Ready for training

            indices (list): Tree indices of sampled experiences
                Length: batch_size
                Format: [tree_idx, ...]
                Used for update_priorities() after training

            weights (np.ndarray): Importance sampling weights
                Shape: (batch_size,)
                Range: [0, 1] (normalized)
                Multiply with loss for bias correction

        Importance Sampling Weights:
            For each sampled experience i:
                P(i) = priority_i / total_priority
                w_i = (N · P(i))^(-β)
                w_i = w_i / max_j(w_j)  # Normalize

            Where:
                N = current buffer size
                β = current beta value (annealed)

        Segment Sampling:
            Ensures coverage across priority range:
                Segment 0: [0, total/batch_size)
                Segment 1: [total/batch_size, 2*total/batch_size)
                ...
                Segment n-1: [(n-1)*total/batch_size, total)

        Example:
            buffer = PrioritizedReplayBuffer()
            # ... fill buffer with 1000 experiences ...

            if len(buffer) >= 32:
                batch, indices, weights = buffer.sample(32)

                # Unpack batch
                states, actions, rewards, next_states, dones = zip(*batch)

                # Convert to tensors
                states = torch.FloatTensor(states)
                actions = torch.LongTensor(actions)
                # ...

                # Compute loss with IS weights
                td_errors = targets - predictions
                loss = (weights * td_errors ** 2).mean()

                # Update priorities
                new_td_errors = td_errors.detach().numpy()
                buffer.update_priorities(indices, new_td_errors)

        Beta Annealing:
            Called every sample():
                β ← min(1.0, β + increment)

            Timeline (50K frames):
                Frame 0:     β = 0.4 (40% correction)
                Frame 10K:   β = 0.52 (52% correction)
                Frame 25K:   β = 0.7 (70% correction)
                Frame 50K:   β = 1.0 (100% correction)
                Frame 50K+:  β = 1.0 (saturated)

        Weight Interpretation:
            w_i ≈ 1.0: Experience sampled at natural frequency
            w_i < 1.0: Experience over-sampled, down-weight loss
            w_i = 0.5: Experience sampled 2x too often

        Sampling Distribution:
            High priority (p=100): Sampled often, small weight (w≈0.1)
            Medium priority (p=10): Sampled moderately, medium weight (w≈0.5)
            Low priority (p=1): Sampled rarely, large weight (w≈1.0)

        Notes:
            - Proportional sampling via SumTree (O(log n) per sample)
            - Importance sampling removes bias from prioritization
            - Beta annealing balances speed vs accuracy
            - Normalized weights ensure stable training
            - None experiences skipped (data integrity check)
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
        Update priorities for sampled experiences after training.

        After training on a batch, TD errors change as predictions improve.
        This method updates priorities in the tree to reflect new learning
        values, ensuring adaptive prioritization.

        Update Process:
            For each experience in batch:
                1. Compute new TD error (post-training)
                2. Calculate new priority
                3. Update in SumTree
                4. Propagate change to root

        Args:
            indices (list): Tree indices from sample()
                Length: batch_size
                Format: [tree_idx, ...]
                Must match order of errors

            errors (np.ndarray or list): New TD errors
                Length: batch_size
                Format: [|Q_target - Q_current|, ...]
                Absolute values (sign doesn't matter)

        Priority Recalculation:
            For each error:
                new_priority = (|error| + ε)^α × event_multiplier

            Note: Event type multiplier not reapplied (only TD error updated)
            Assumption: Event type doesn't change

        Example:
            # Sample and train
            batch, indices, weights = buffer.sample(32)

            # Training reduces TD errors
            # Before: errors = [15.0, 8.2, 12.1, ...]
            # After:  errors = [2.3, 1.1, 3.5, ...]

            # Compute new TD errors
            with torch.no_grad():
                targets = rewards + gamma * target_net(next_states).max(1)[0]
                predictions = policy_net(states).gather(1, actions)
                new_errors = abs(targets - predictions).numpy()

            # Update priorities
            buffer.update_priorities(indices, new_errors)

            # Result: Priorities decreased for improved predictions

        Priority Evolution Example:
            Experience lifecycle:
                Iteration 0:
                    TD_error = 15.0
                    priority = (15.0 + 0.01)^0.6 = 38.7
                    Sample frequently

                Iteration 10:
                    TD_error = 8.0 (learning!)
                    priority = (8.0 + 0.01)^0.6 = 22.8
                    Sample less frequently

                Iteration 50:
                    TD_error = 1.0 (learned well)
                    priority = (1.0 + 0.01)^0.6 = 1.0
                    Sample rarely

                Iteration 100:
                    TD_error = 0.1 (mastered)
                    priority = (0.1 + 0.01)^0.6 = 0.32
                    Sample very rarely

        Adaptive Learning:
            - High-error experiences stay high priority
            - Learned experiences automatically deprioritized
            - Buffer focuses on current learning frontier
            - No manual priority management needed

        Performance:
            - O(log n) per update (tree propagation)
            - Batch update: O(batch_size × log n)
            - For batch=32, n=50K: ~32 × 16 = 512 ops
            - Negligible compared to neural network forward/backward

        Notes:
            - Critical for adaptive prioritization
            - Must be called after every training step
            - Indices must match sampled batch order
            - Errors should be post-training TD errors
            - Event type multipliers not reapplied (could be future feature)
        """
        for idx, error in zip(indices, errors):
            priority = self._get_priority(error)
            self.tree.update(idx, priority)

    def __len__(self):
        """
        Get current number of stored experiences.

        Returns:
            int: Number of experiences in buffer
                Range: [0, capacity]
                Increases as experiences added
                Saturates at capacity (circular buffer)

        Usage:
            buffer = PrioritizedReplayBuffer(capacity=50000)

            # Check if ready to sample
            if len(buffer) >= 500:  # MIN_BUFFER_SIZE
                batch = buffer.sample(32)

            # Monitor fill progress
            print(f"Buffer: {len(buffer)}/{buffer.capacity}")
            # Output: Buffer: 12543/50000 (25% full)

        Example:
            buffer = PrioritizedReplayBuffer(capacity=100)
            assert len(buffer) == 0

            for i in range(150):
                buffer.add(state, action, reward, next_state, done, error)

            assert len(buffer) == 100  # Saturated at capacity

        Notes:
            - Does not count overwritten experiences
            - Maximum value is capacity
            - Used for sampling readiness check
            - O(1) operation
        """
        return self.tree.n_entries
