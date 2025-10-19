"""
Deep Q-Network Architecture for Traffic Signal Control

This module implements the neural network that approximates the Q-function for
Deep Q-Learning. The network maps traffic states to action-value estimates.

===================================================================================
MATHEMATICAL FOUNDATIONS
===================================================================================

1. Q-FUNCTION APPROXIMATION
----------------------------
The network learns a function approximator:

    Q(s, a; θ) ≈ Q*(s, a)

Where:
    s = state (45-dimensional traffic conditions)
    a = action (4 possible signal control decisions)
    θ = network parameters (weights and biases)
    Q*(s, a) = optimal action-value function

Instead of storing Q-values in a table (infeasible with continuous states),
the neural network generalizes across similar states.

2. NETWORK ARCHITECTURE
------------------------
Progressive dimensionality transformation:

    Input Layer:      45 dimensions (state features)
                      ↓
    Hidden Layer 1:   Linear(45 → 256) + ReLU
                      ↓
    Hidden Layer 2:   Linear(256 → 256) + ReLU
                      ↓
    Hidden Layer 3:   Linear(256 → 128) + ReLU
                      ↓
    Output Layer:     Linear(128 → 4) (no activation)
                      ↓
    Output:           4 Q-values (one per action)

3. ACTIVATION FUNCTIONS
------------------------
ReLU (Rectified Linear Unit):
    ReLU(x) = max(0, x)

Properties:
    - Non-linear: enables learning complex patterns
    - Sparse activation: only positive values pass through
    - No vanishing gradient problem (unlike sigmoid/tanh)
    - Computationally efficient

Why no activation on output layer?
    - Q-values can be any real number (positive or negative)
    - Rewards can be negative (penalties) or positive (bonuses)
    - Linear output allows unrestricted value estimation

4. FORWARD PASS MATHEMATICS
----------------------------
Given state s ∈ ℝ⁴⁵, the network computes:

    h₁ = ReLU(W₁·s + b₁)           [256 neurons]
    h₂ = ReLU(W₂·h₁ + b₂)          [256 neurons]
    h₃ = ReLU(W₃·h₂ + b₃)          [128 neurons]
    Q = W₄·h₃ + b₄                 [4 outputs]

Total parameters:
    Layer 1: (45 × 256) + 256 = 11,776
    Layer 2: (256 × 256) + 256 = 65,792
    Layer 3: (256 × 128) + 128 = 32,896
    Output:  (128 × 4) + 4 = 516
    ─────────────────────────────────
    Total:                      110,980 parameters

5. BATCH PROCESSING
--------------------
The network processes multiple samples simultaneously:

    Input:  [batch_size, 45]  e.g., [32, 45]  (32 traffic states)
    Output: [batch_size, 4]   e.g., [32, 4]   (32 sets of Q-values)

Example for batch_size=3:
    States = [[s₀_features],     ← State 0 (45 values)
              [s₁_features],     ← State 1 (45 values)
              [s₂_features]]     ← State 2 (45 values)
    
    Q-values = [[Q(s₀,a₀), Q(s₀,a₁), Q(s₀,a₂), Q(s₀,a₃)],  ← 4 Q-values for state 0
                [Q(s₁,a₀), Q(s₁,a₁), Q(s₁,a₂), Q(s₁,a₃)],  ← 4 Q-values for state 1
                [Q(s₂,a₀), Q(s₂,a₁), Q(s₂,a₂), Q(s₂,a₃)]]  ← 4 Q-values for state 2

6. DESIGN RATIONALE
--------------------
Architecture choices and their purposes:

Initial Expansion (45 → 256):
    - Allows network to learn rich feature representations
    - Captures complex traffic patterns and interactions
    - Creates abstract feature space for signal timing decisions

Constant Width (256 → 256):
    - Maintains representational capacity
    - Enables deep hierarchical feature learning
    - Processes complex temporal and spatial patterns

Gradual Compression (256 → 128 → 4):
    - Funnels information toward action values
    - Forces network to extract most relevant features
    - Final layer maps features to action-specific values

Why not wider/deeper?
    - Too wide: overfitting, slow training, memory constraints
    - Too narrow: underfitting, can't learn complex patterns
    - Too deep: vanishing gradients, harder to train
    - Current design: empirically balanced for traffic control

7. COMPARISON WITH TABULAR Q-LEARNING
---------------------------------------
Tabular Q-Learning (IMPOSSIBLE for traffic):
    State space: 10⁴⁵ possible states (continuous features)
    Storage: 10⁴⁵ × 4 = 4×10⁴⁵ Q-values
    Memory required: More than atoms in universe!

Neural Network Approximation:
    Parameters: 110,980 (manageable)
    Memory: ~440 KB (4 bytes per float)
    Generalization: Similar states → similar Q-values
    
Example of generalization:
    Seen state:    [queue=5, phase=1, sync=10, ...]
    Q-values:      [2.5, 4.1, 3.2, 1.8]
    
    New state:     [queue=5.2, phase=1, sync=9.8, ...]  ← Never seen before
    Q-values:      [2.4, 4.0, 3.1, 1.7]  ← Generalized from similar states!

===================================================================================
STATE SPACE FOR TRAFFIC CONTROL (45 dimensions)
===================================================================================

Input features per intersection:
    1. Phase Encoding (one-hot):        5 dimensions [Phase 1-5]
    2. Phase Duration:                  1 dimension  [seconds active]
    3. Vehicle Queues (4 directions):   4 dimensions [vehicles waiting]
    4. Bicycle Queues (4 directions):   4 dimensions [bicycles waiting]
    5. Pedestrian Demand:               1 dimension  [pedestrians waiting]
    6. Bus Presence:                    1 dimension  [binary: bus detected]
    7. Detector Occupancy:              Multiple dimensions
    8. Sync Timer:                      1 dimension  [coordination countdown]
    9. Time of Day:                     1 dimension  [normalized 0-1]

Total: ~45 dimensions (exact count depends on detector configuration)

===================================================================================
ACTION SPACE (4 discrete actions)
===================================================================================

Output Q-values correspond to:
    Q(s, a₀): Continue current phase
    Q(s, a₁): Skip to Phase 1 (major arterial through)
    Q(s, a₂): Progress to next phase in sequence
    Q(s, a₃): Activate pedestrian priority phase

Action selection:
    a* = argmax_a Q(s, a; θ)  ← Choose action with highest Q-value

===================================================================================
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from drl.config import DRLConfig


class DQN(nn.Module):
    """
    Deep Q-Network for Multimodal Traffic Signal Control
    
    A feedforward neural network that maps traffic states to Q-values for
    each possible signal control action. Uses a progressive architecture
    that expands, maintains, then compresses information flow.
    
    Architecture:
        Input → Dense(256) → ReLU → Dense(256) → ReLU → Dense(128) → ReLU → Dense(4)
        
        Dimensions: 45 → 256 → 256 → 128 → 4
        
    Layers:
        - Input: 45-dimensional traffic state vector
        - Hidden 1: 256 neurons with ReLU activation
        - Hidden 2: 256 neurons with ReLU activation  
        - Hidden 3: 128 neurons with ReLU activation
        - Output: 4 Q-values (no activation, can be any real number)
        
    Parameters:
        - Total trainable parameters: ~110,980
        - Memory footprint: ~440 KB (32-bit floats)
        
    Properties:
        - Universal function approximator (can learn any continuous Q-function)
        - Generalizes across similar traffic states
        - Efficient parallel processing via batch operations
        - Compatible with GPU acceleration
        
    Input/Output Specifications:
        Input shape:  [batch_size, 45] or [1, 45] for single state
        Output shape: [batch_size, 4] or [1, 4] for single state
        
        Example:
            state = torch.randn(32, 45)  # Batch of 32 traffic states
            q_values = model(state)      # Shape: [32, 4]
            best_actions = q_values.argmax(dim=1)  # Shape: [32]
            
    Usage:
        # Single state (inference)
        state = torch.FloatTensor(state_vector).unsqueeze(0)  # [1, 45]
        q_values = model(state)  # [1, 4]
        action = q_values.argmax().item()  # int
        
        # Batch processing (training)
        states = torch.FloatTensor(state_batch)  # [batch_size, 45]
        q_values = model(states)  # [batch_size, 4]
        
    Mathematical Operation:
        For state s ∈ ℝ⁴⁵, computes Q(s, a; θ) for all actions a ∈ {0,1,2,3}
        
        Q(s, ·; θ) = f_θ(s) where f_θ is this neural network
    """
    
    def __init__(self, state_dim, action_dim, hidden_layers=None):
        """
        Initialize Deep Q-Network with specified architecture.
        
        Constructs a feedforward neural network with configurable hidden layers.
        Each hidden layer uses ReLU activation. The output layer has no activation
        to allow Q-values to be any real number (positive or negative).
        
        Args:
            state_dim (int): Dimension of state space
                - For traffic control: 45 (queue lengths, phase info, detectors, etc.)
                - Must match the state representation from environment
                
            action_dim (int): Number of discrete actions
                - For traffic control: 4 (Continue, Skip to Phase 1, Next, Pedestrian)
                - Network outputs one Q-value per action
                
            hidden_layers (list of int, optional): Hidden layer sizes
                - Default: [256, 256, 128] from DRLConfig.HIDDEN_LAYERS
                - Example custom: [512, 512, 256] for larger capacity
                - Example minimal: [128, 64] for faster training
                
        Network Construction:
            The network is built dynamically based on hidden_layers specification:
            
            For hidden_layers = [256, 256, 128]:
                Layer 0: Linear(45 → 256)  + ReLU
                Layer 1: Linear(256 → 256) + ReLU
                Layer 2: Linear(256 → 128) + ReLU
                Layer 3: Linear(128 → 4)   (no activation)
                
        Example Configurations:
            # Standard (default)
            model = DQN(45, 4)  # Uses [256, 256, 128]
            
            # Larger network
            model = DQN(45, 4, hidden_layers=[512, 512, 256])
            
            # Smaller network (faster, less capacity)
            model = DQN(45, 4, hidden_layers=[128, 64])
            
            # Very deep network
            model = DQN(45, 4, hidden_layers=[256, 256, 256, 128, 128])
            
        Layer-by-Layer Breakdown:
            Input dimension: state_dim (45)
            ↓
            For each h in hidden_layers:
                Add Linear(input_dim → h)
                Add ReLU activation
                input_dim = h  # Update for next layer
            ↓
            Add Linear(final_hidden → action_dim)  # Output layer
            ↓
            Output dimension: action_dim (4)
            
        Parameter Initialization:
            PyTorch automatically initializes weights using Kaiming initialization
            (suitable for ReLU networks) with uniform distribution.
        """
        super(DQN, self).__init__()
        
        # Use default hidden layers from config if not specified
        if hidden_layers is None:
            hidden_layers = DRLConfig.HIDDEN_LAYERS
        
        # Build network layers dynamically
        layers = []
        input_dim = state_dim  # Start with state dimension (45)
        
        # Create hidden layers with ReLU activations
        for hidden_dim in hidden_layers:
            # Linear transformation: y = Wx + b
            layers.append(nn.Linear(input_dim, hidden_dim))
            # ReLU activation: y = max(0, x)
            layers.append(nn.ReLU())
            # Next layer's input is this layer's output
            input_dim = hidden_dim
        
        # Output layer (no activation - Q-values can be any real number)
        layers.append(nn.Linear(input_dim, action_dim))
        
        # Combine all layers into sequential container
        # Sequential executes layers in order during forward pass
        self.network = nn.Sequential(*layers)
    
    def forward(self, state):
        """
        Forward propagation through the Q-network.
        
        Computes Q-values for all actions given the current state(s).
        Supports both single states and batched states for efficient training.
        
        Args:
            state (torch.Tensor): Traffic state(s)
                Shape: [batch_size, state_dim] or [state_dim]
                Dtype: torch.float32
                
                Single state example:
                    state = torch.FloatTensor([queue_lengths, phase_info, ...])
                    state.shape = [45]
                    
                Batch example:
                    states = torch.FloatTensor([[state_0], [state_1], ...])
                    states.shape = [32, 45]
                
        Returns:
            torch.Tensor: Q-values for each action
                Shape: [batch_size, action_dim] or [action_dim]
                Dtype: torch.float32
                
                Each row contains Q-values for one state:
                    [[Q(s₀,a₀), Q(s₀,a₁), Q(s₀,a₂), Q(s₀,a₃)],
                     [Q(s₁,a₀), Q(s₁,a₁), Q(s₁,a₂), Q(s₁,a₃)],
                     ...]
                
        Computation Graph:
            state [batch, 45]
            ↓ Linear(45→256) + ReLU
            h₁ [batch, 256]
            ↓ Linear(256→256) + ReLU
            h₂ [batch, 256]
            ↓ Linear(256→128) + ReLU
            h₃ [batch, 128]
            ↓ Linear(128→4)
            Q-values [batch, 4]
            
        Mathematical Operations:
            h₁ = ReLU(W₁·state + b₁)
            h₂ = ReLU(W₂·h₁ + b₂)
            h₃ = ReLU(W₃·h₂ + b₃)
            Q = W₄·h₃ + b₄
            
            Where Wᵢ are weight matrices and bᵢ are bias vectors
            
        Example Usage:
            # Single state inference
            >>> state = torch.randn(1, 45)  # One traffic state
            >>> q_values = model(state)
            >>> q_values.shape
            torch.Size([1, 4])
            >>> best_action = q_values.argmax(dim=1).item()
            >>> print(f"Best action: {best_action}")
            Best action: 2
            
            # Batch training
            >>> states = torch.randn(32, 45)  # Batch of 32 states
            >>> q_values = model(states)
            >>> q_values.shape
            torch.Size([32, 4])
            >>> best_actions = q_values.argmax(dim=1)
            >>> best_actions.shape
            torch.Size([32])
            
            # Examining Q-values
            >>> state = torch.randn(1, 45)
            >>> q_values = model(state)
            >>> print(q_values)
            tensor([[ 2.3, -1.5,  4.2,  0.8]])  # Q-values for 4 actions
            >>> # Action 2 has highest Q-value (4.2), so it's the best choice
            
        Gradient Computation:
            During training (.train() mode):
                - Gradients computed for backpropagation
                - Dropout active (if added in future)
                - Batch normalization in training mode (if added)
                
            During inference (.eval() mode):
                - No gradient computation (use with torch.no_grad())
                - Dropout disabled (if added)
                - Batch normalization in inference mode (if added)
                
        Performance Characteristics:
            - Forward pass time: ~0.1-0.5ms on GPU (batch_size=32)
            - Memory: ~440 KB for model weights
            - FLOPs per sample: ~110K multiply-add operations
            
        Numerical Stability:
            - ReLU prevents vanishing gradients
            - No activation on output allows full range of Q-values
            - Gradient clipping in agent prevents exploding gradients
            - Clipping Q-values in agent prevents extreme outputs
        """
        return self.network(state)