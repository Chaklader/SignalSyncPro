"""
Saliency Analysis for DRL Traffic Signal Controller

Computes gradient-based saliency maps to identify which state features
most influence the agent's Q-value predictions for each action.

Mathematical Foundation:
    Saliency for action a: ∇_s Q(s, a)

Where high magnitude |∇_i Q(s, a)| indicates feature i is critical for action a.
"""

import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

import torch
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from controls.ml_based.drl.agent import DQNAgent
from controls.ml_based.drl.config import DRLConfig


class SaliencyAnalyzer:
    """
    Computes and visualizes saliency maps for trained DQN agent.
    """

    def __init__(self, model_path):
        """
        Initialize analyzer with trained model.

        Args:
            model_path: Path to trained model checkpoint (.pth file)
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.agent = DQNAgent(
            state_dim=DRLConfig.STATE_DIM,
            action_dim=DRLConfig.ACTION_DIM,
            device=self.device,
        )
        self.agent.load(model_path)
        self.agent.set_eval_mode()

        self.action_names = ["Continue", "Skip2P1", "Next"]
        self.feature_names = self._get_feature_names()

        print(f"✅ Loaded model from: {model_path}")
        print(
            f"📊 State dim: {DRLConfig.STATE_DIM}, Action dim: {DRLConfig.ACTION_DIM}"
        )

    def _get_feature_names(self):
        """
        Get human-readable names for all 32 state features.
        """
        tls3_features = [
            "TLS3_Phase_P1",
            "TLS3_Phase_P2",
            "TLS3_Phase_P3",
            "TLS3_Phase_P4",
            "TLS3_Phase_Duration",
            "TLS3_Vehicle_Det1",
            "TLS3_Vehicle_Det2",
            "TLS3_Vehicle_Det3",
            "TLS3_Vehicle_Det4",
            "TLS3_Bicycle_Det1",
            "TLS3_Bicycle_Det2",
            "TLS3_Bicycle_Det3",
            "TLS3_Bicycle_Det4",
            "TLS3_Bus_Present",
            "TLS3_Bus_Wait",
            "TLS3_Sim_Time",
        ]

        tls6_features = [
            "TLS6_Phase_P1",
            "TLS6_Phase_P2",
            "TLS6_Phase_P3",
            "TLS6_Phase_P4",
            "TLS6_Phase_Duration",
            "TLS6_Vehicle_Det1",
            "TLS6_Vehicle_Det2",
            "TLS6_Vehicle_Det3",
            "TLS6_Vehicle_Det4",
            "TLS6_Bicycle_Det1",
            "TLS6_Bicycle_Det2",
            "TLS6_Bicycle_Det3",
            "TLS6_Bicycle_Det4",
            "TLS6_Bus_Present",
            "TLS6_Bus_Wait",
            "TLS6_Sim_Time",
        ]

        return tls3_features + tls6_features

    def compute_saliency(self, state):
        """
        Compute saliency maps for all actions given a state.

        Args:
            state: State vector (numpy array or tensor)

        Returns:
            dict: Saliency maps for each action {action_idx: gradient_vector}
        """
        if isinstance(state, np.ndarray):
            state = torch.FloatTensor(state).to(self.device)

        state = state.unsqueeze(0) if state.dim() == 1 else state
        state.requires_grad = True

        q_values = self.agent.policy_net(state)

        saliency_maps = {}
        for action_idx in range(DRLConfig.ACTION_DIM):
            if state.grad is not None:
                state.grad.zero_()

            q_values[0, action_idx].backward(retain_graph=True)

            saliency_maps[action_idx] = state.grad[0].detach().cpu().numpy()

        return saliency_maps

    def analyze_state(self, state, state_description=""):
        """
        Analyze saliency for a single state and print findings.

        Args:
            state: State vector
            state_description: Optional description of the state
        """
        saliency_maps = self.compute_saliency(state)

        print(f"\n{'=' * 80}")
        print(f"SALIENCY ANALYSIS: {state_description}")
        print(f"{'=' * 80}")

        for action_idx, action_name in enumerate(self.action_names):
            saliency = saliency_maps[action_idx]
            abs_saliency = np.abs(saliency)

            top_indices = np.argsort(abs_saliency)[-5:][::-1]

            print(f"\n🎯 {action_name}:")
            print("   Top 5 influential features:")
            for rank, idx in enumerate(top_indices, 1):
                print(f"   {rank}. {self.feature_names[idx]}: {saliency[idx]:+.4f}")

    def visualize_saliency(self, state, output_path=None, state_description=""):
        """
        Create heatmap visualization of saliency maps.

        Args:
            state: State vector
            output_path: Path to save figure (optional)
            state_description: Description for title
        """
        saliency_maps = self.compute_saliency(state)

        saliency_matrix = np.array(
            [saliency_maps[i] for i in range(DRLConfig.ACTION_DIM)]
        )

        fig, ax = plt.subplots(figsize=(14, 6))

        sns.heatmap(
            saliency_matrix,
            cmap="RdBu_r",
            center=0,
            xticklabels=self.feature_names,
            yticklabels=self.action_names,
            cbar_kws={"label": "Gradient Magnitude"},
            ax=ax,
        )

        plt.title(f"Saliency Map: {state_description}", fontsize=14, fontweight="bold")
        plt.xlabel("State Features", fontsize=12)
        plt.ylabel("Actions", fontsize=12)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            print(f"💾 Saved visualization to: {output_path}")
        else:
            plt.show()

        plt.close()

    def batch_analyze(self, states, descriptions=None, output_dir=None):
        """
        Analyze multiple states and save results.

        Args:
            states: List of state vectors
            descriptions: Optional list of state descriptions
            output_dir: Directory to save results (required)
        """
        if output_dir is None:
            raise ValueError("output_dir must be provided")

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        if descriptions is None:
            descriptions = [f"State_{i}" for i in range(len(states))]

        for idx, (state, desc) in enumerate(zip(states, descriptions)):
            print(f"\n{'=' * 80}")
            print(f"Processing: {desc} ({idx + 1}/{len(states)})")

            self.analyze_state(state, desc)

            output_file = (
                output_path / f"saliency_{idx:03d}_{desc.replace(' ', '_')}.png"
            )
            self.visualize_saliency(state, output_file, desc)

        print(f"\n✅ Batch analysis complete! Results saved to: {output_dir}")


def generate_synthetic_states():
    """
    Generate representative synthetic states for saliency analysis.

    Returns:
        tuple: (states, descriptions)
    """
    states = []
    descriptions = []

    """
    Scenario 1: Phase 1 with High Vehicle Demand
    
    Traffic Situation:
        - Phase 1 (major through) active for 30s at TLS1, 18s at TLS2
        - Heavy vehicle queues on arterial (directions 1&2)
        - Tests feature importance during typical arterial operation
    
    Purpose:
        Identifies which features drive Continue vs Next decisions:
        - Vehicle queue detectors [5-8]
        - Phase duration [4]
        - Phase encoding [0-3]
    
    Expected Saliency:
        High importance on vehicle queue and phase duration features
    """
    p1_active_high_vehicle_queue = np.zeros(32)
    p1_active_high_vehicle_queue[0] = 1.0  # TLS1: Phase 1 active
    p1_active_high_vehicle_queue[4] = 0.5  # TLS1: Phase duration = 30s (0.5 × 60)
    p1_active_high_vehicle_queue[5:9] = [
        1.0,
        1.0,
        0.0,
        0.0,
    ]  # TLS1: Vehicle queues in directions 1&2
    p1_active_high_vehicle_queue[16] = 1.0  # TLS2: Phase 1 active
    p1_active_high_vehicle_queue[20] = 0.3  # TLS2: Phase duration = 18s (0.3 × 60)
    states.append(p1_active_high_vehicle_queue)
    descriptions.append("P1_Active_High_Vehicle_Queue")

    """
    Scenario 2: Phase 1 with Bus Priority
    
    Traffic Situation:
        - Phase 1 active for 12s (early in cycle)
        - Buses detected at TLS1 with high waiting time (0.9)
        - Buses travel on major arterial through lanes (P1)
    
    Purpose:
        Identifies which bus-related features are most important:
        - Bus presence [13, 29]
        - Bus waiting time [14, 30]
        - Whether model uses these for Skip2P1 decisions
    
    Expected Saliency:
        High importance on bus presence and waiting time features
    """
    p1_active_bus_priority = np.zeros(32)
    p1_active_bus_priority[0] = 1.0  # TLS1: Phase 1 active
    p1_active_bus_priority[4] = 0.2  # TLS1: Phase duration = 12s (0.2 × 60)
    p1_active_bus_priority[13] = 1.0  # TLS1: Bus detected
    p1_active_bus_priority[14] = 0.9  # TLS1: High bus waiting time (normalized)
    p1_active_bus_priority[16] = 1.0  # TLS2: Phase 1 active
    p1_active_bus_priority[29] = 1.0  # TLS2: Bus detected (16+13=29)
    states.append(p1_active_bus_priority)
    descriptions.append("P1_Active_Bus_Priority")

    """
    Scenario 3: Phase 3 with Mixed Bicycle Demand
    
    Traffic Situation:
        - Phase 3 (minor through) active for 36s
        - Bicycle queues at 3 directions at TLS1
        - Mixed bicycle queues at TLS2 (directions 1,3,4)
    
    Purpose:
        Tests bicycle feature importance:
        - Bicycle queue detectors [9-12, 25-28]
        - Whether model differentiates bicycle vs vehicle demand
        - Minor phase timing decisions
    
    Expected Saliency:
        High importance on bicycle queue features for multimodal decisions
    """
    p3_active_mixed_bicycle_demand = np.zeros(32)
    p3_active_mixed_bicycle_demand[2] = 1.0  # TLS1: Phase 3 active (minor through)
    p3_active_mixed_bicycle_demand[4] = 0.6  # TLS1: Phase duration = 36s (0.6 × 60)
    p3_active_mixed_bicycle_demand[9:13] = [
        1.0,
        1.0,
        1.0,
        0.0,
    ]  # TLS1: Bicycle queues in 3 directions
    p3_active_mixed_bicycle_demand[18] = 1.0  # TLS2: Phase 3 active (16+2=18)
    p3_active_mixed_bicycle_demand[25:29] = [
        1.0,
        0.0,
        1.0,
        1.0,
    ]  # TLS2: Bicycle queues in directions 1,3,4
    states.append(p3_active_mixed_bicycle_demand)
    descriptions.append("P3_Active_Mixed_Bicycle_Demand")

    """
    Scenario 4: Phase 4 Near Maximum Duration
    
    Traffic Situation:
        - Phase 4 (minor left turn) active for 12s (at max_green limit)
        - Vehicle queues on cross-street at TLS1 (directions 3&4)
        - Vehicle queues on arterial at TLS2 (directions 1&2)
    
    Purpose:
        Tests duration-based decision making:
        - Phase duration [4] at maximum (0.2 = 12s for P4)
        - Whether model recognizes need to transition
        - Spatial queue distribution across intersections
    
    Expected Saliency:
        High importance on phase duration and queue location features
    """
    p4_active_long_duration = np.zeros(32)
    p4_active_long_duration[3] = 1.0  # TLS1: Phase 4 active (minor left)
    p4_active_long_duration[4] = 0.2  # TLS1: Phase duration = 12s (at P4 max_green)
    p4_active_long_duration[5:9] = [
        0.0,
        0.0,
        1.0,
        1.0,
    ]  # TLS1: Vehicle queues in directions 3&4
    p4_active_long_duration[19] = 1.0  # TLS2: Phase 4 active (16+3=19)
    p4_active_long_duration[21:25] = [
        1.0,
        1.0,
        0.0,
        0.0,
    ]  # TLS2: Vehicle queues in directions 1&2
    states.append(p4_active_long_duration)
    descriptions.append("P4_Active_Long_Duration")

    """
    Scenario 5: Heavy Congestion All Modes
    
    Traffic Situation:
        - Phase 1 active for 9s (early in cycle)
        - All vehicle queues present (all 4 directions)
        - All bicycle queues present (all 4 directions)
        - Represents peak congestion scenario
    
    Purpose:
        Tests feature importance under congestion:
        - Which mode gets priority (vehicles vs bicycles)
        - How model handles competing demands
        - Whether phase extension or transition is preferred
    
    Expected Saliency:
        Distributed importance across vehicle and bicycle features
    """
    p1_heavy_congestion_all_modes = np.zeros(32)
    p1_heavy_congestion_all_modes[0] = 1.0  # TLS1: Phase 1 active
    p1_heavy_congestion_all_modes[4] = 0.15  # TLS1: Phase duration = 9s (0.15 × 60)
    p1_heavy_congestion_all_modes[5:9] = [
        1.0,
        1.0,
        1.0,
        1.0,
    ]  # TLS1: All vehicle queues
    p1_heavy_congestion_all_modes[9:13] = [
        1.0,
        1.0,
        1.0,
        1.0,
    ]  # TLS1: All bicycle queues
    p1_heavy_congestion_all_modes[16] = 1.0  # TLS2: Phase 1 active
    p1_heavy_congestion_all_modes[21:25] = [
        1.0,
        1.0,
        1.0,
        1.0,
    ]  # TLS2: All vehicle queues
    states.append(p1_heavy_congestion_all_modes)
    descriptions.append("P1_Heavy_Congestion_All_Modes")

    return states, descriptions


if __name__ == "__main__":
    MODEL_PATH = "models/training_20251103_163015/checkpoint_ep192.pth"

    analyzer = SaliencyAnalyzer(MODEL_PATH)

    states, descriptions = generate_synthetic_states()

    analyzer.batch_analyze(states, descriptions)

    print("\n" + "=" * 80)
    print("✅ Saliency analysis complete!")
    print("📊 Results saved to: images/2/saliency/")
    print("=" * 80)
