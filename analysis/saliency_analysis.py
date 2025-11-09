"""
Saliency Analysis for DQN Traffic Signal Controller

Computes per-action saliency maps (gradients) to identify which state features
most influence Q-value predictions for each action.

Mathematical foundation:
    Saliency for action a: g^(a) = ∇_s Q(s, a)

Where:
    - s: State vector (32 dimensions)
    - Q(s, a): Q-value for state s and action a
    - g^(a): Gradient vector showing sensitivity of Q(s,a) to each state feature

High magnitude gradient |g_i^(a)| indicates feature i is critical for action a.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
        return [
            "Queue_P1_Major",
            "Queue_P1_Minor",
            "Queue_P2_Major",
            "Queue_P2_Minor",
            "Queue_P3_Left",
            "Queue_P3_Right",
            "Queue_P4_Ped",
            "Queue_P4_Special",
            "Wait_P1_Major",
            "Wait_P1_Minor",
            "Wait_P2_Major",
            "Wait_P2_Minor",
            "Wait_P3_Left",
            "Wait_P3_Right",
            "Wait_P4_Ped",
            "Wait_P4_Special",
            "Phase_ID",
            "Phase_Duration",
            "Time_Since_Last_Change",
            "Bus_Present_TLS3",
            "Bus_Wait_TLS3",
            "Bus_Present_TLS6",
            "Bus_Wait_TLS6",
            "Detector_1",
            "Detector_2",
            "Detector_3",
            "Detector_4",
            "Ped_Demand_TLS3",
            "Ped_Demand_TLS6",
            "Modal_Demand_Car",
            "Modal_Demand_Bike",
            "Modal_Demand_Ped",
        ]

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
            state_description: Description for plot title
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

    def batch_analyze(self, states, descriptions=None, output_dir="results/saliency"):
        """
        Analyze multiple states and save results.

        Args:
            states: List of state vectors
            descriptions: Optional list of descriptions
            output_dir: Directory to save results
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        if descriptions is None:
            descriptions = [f"State_{i}" for i in range(len(states))]

        for idx, (state, desc) in enumerate(zip(states, descriptions)):
            print(f"\n{'=' * 80}")
            print(f"Processing: {desc} ({idx + 1}/{len(states)})")
            print(f"{'=' * 80}")

            self.analyze_state(state, desc)

            output_file = (
                output_path / f"saliency_{idx:03d}_{desc.replace(' ', '_')}.png"
            )
            self.visualize_saliency(state, output_file, desc)

        print(f"\n✅ Batch analysis complete! Results saved to: {output_dir}")


def load_test_states(scenario_name):
    """
    Load test states from saved test logs.

    Args:
        scenario_name: Name of test scenario (e.g., "Pr_0", "Bi_5")

    Returns:
        list: List of state vectors from test episode
    """
    log_path = Path(f"logs/testing/{scenario_name}_states.npy")

    if log_path.exists():
        states = np.load(log_path)
        print(f"✅ Loaded {len(states)} states from {scenario_name}")
        return states
    else:
        print(f"⚠️  No saved states found for {scenario_name}")
        return None


def generate_synthetic_states():
    """
    Generate representative synthetic states for analysis.

    Returns:
        tuple: (states, descriptions)
    """
    states = []
    descriptions = []

    state = np.zeros(32)
    state[0] = 0.8
    state[8] = 0.5
    state[16] = 1
    state[17] = 0.3
    states.append(state)
    descriptions.append("High_Major_Queue_P1")

    state = np.zeros(32)
    state[19] = 1.0
    state[20] = 0.9
    state[16] = 2
    state[17] = 0.2
    states.append(state)
    descriptions.append("Bus_Waiting_P2")

    state = np.zeros(32)
    state[27] = 1.0
    state[28] = 1.0
    state[16] = 3
    state[17] = 0.4
    states.append(state)
    descriptions.append("High_Ped_Demand")

    state = np.zeros(32)
    state[0] = 0.3
    state[2] = 0.7
    state[16] = 1
    state[17] = 0.8
    states.append(state)
    descriptions.append("Long_Phase_Duration")

    state = np.zeros(32)
    state[0] = 0.9
    state[1] = 0.9
    state[8] = 0.8
    state[9] = 0.8
    state[16] = 1
    state[17] = 0.1
    states.append(state)
    descriptions.append("Congestion_All_Approaches")

    return states, descriptions


if __name__ == "__main__":
    MODEL_PATH = "models/training_20251103_163015/checkpoint_ep192.pth"

    analyzer = SaliencyAnalyzer(MODEL_PATH)

    states, descriptions = generate_synthetic_states()

    analyzer.batch_analyze(states, descriptions)

    print("\n" + "=" * 80)
    print("✅ Saliency analysis complete!")
    print("📊 Results saved to: results/saliency/")
    print("=" * 80)
