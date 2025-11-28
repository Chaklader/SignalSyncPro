"""
Attention-Based State Attribution Analysis

Computes attention weights using gradient magnitudes to identify
which state features the agent focuses on for each action.

Mathematical Foundation:
    Attention weight α_i for feature i:

    α_i = softmax(|∇Q/∇s_i|) = exp(|∇Q/∇s_i|) / Σ_j exp(|∇Q/∇s_j|)

Where higher α_i indicates feature i receives more attention.
"""

import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

import torch
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

from controls.ml_based.drl import DQNAgent
from controls.ml_based.drl.single_agent.config import DRLConfig


class AttentionAnalyzer:
    """
    Analyzes attention patterns in trained DQN agent using gradient-based importance.

    Note: This computes pseudo-attention from gradient magnitudes, not actual
    attention weights from an attention mechanism. The gradients indicate which
    features most influence each action's Q-value.
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
        self.feature_groups = self._get_feature_groups()

        print(f"✅ Loaded model from: {model_path}")

    def _get_feature_groups(self):
        """
        Group features into semantic categories for analysis.
        """
        return {
            "TLS3_Phase_Encoding": list(range(0, 4)),
            "TLS3_Timing": [4, 15],
            "TLS3_Vehicle_Detectors": list(range(5, 9)),
            "TLS3_Bicycle_Detectors": list(range(9, 13)),
            "TLS3_Bus_Info": [13, 14],
            "TLS6_Phase_Encoding": list(range(16, 20)),
            "TLS6_Timing": [20, 31],
            "TLS6_Vehicle_Detectors": list(range(21, 25)),
            "TLS6_Bicycle_Detectors": list(range(25, 29)),
            "TLS6_Bus_Info": [29, 30],
        }

    def compute_attention_weights(self, state):
        """
        Compute attention weights using gradient magnitudes.

        This is computing pseudo-attention from gradient magnitudes,
        not extracting actual attention weights from the model.

        Args:
            state: State vector

        Returns:
            dict: Attention weights for each action
        """
        if isinstance(state, np.ndarray):
            state = torch.FloatTensor(state).to(self.device)

        state = state.unsqueeze(0) if state.dim() == 1 else state
        state.requires_grad = True

        q_values = self.agent.policy_net(state)

        attention_weights = {}
        for action_idx in range(DRLConfig.ACTION_DIM):
            if state.grad is not None:
                state.grad.zero_()

            q_values[0, action_idx].backward(retain_graph=True)

            gradients = state.grad[0].detach().cpu().numpy()
            abs_gradients = np.abs(gradients)

            attention = np.exp(abs_gradients) / np.sum(np.exp(abs_gradients))

            attention_weights[action_idx] = attention

        return attention_weights

    def get_q_values(self, state):
        """Get Q-values for state."""
        if isinstance(state, np.ndarray):
            state = torch.FloatTensor(state).to(self.device)

        state = state.unsqueeze(0) if state.dim() == 1 else state

        with torch.no_grad():
            q_values = self.agent.policy_net(state)

        return q_values[0].cpu().numpy()

    def analyze_decision(self, state, state_description=""):
        """
        Analyze attention patterns for a specific decision.

        Args:
            state: State vector
            state_description: Optional description
        """
        attention_weights = self.compute_attention_weights(state)
        q_values = self.get_q_values(state)
        selected_action = np.argmax(q_values)

        print(f"\n{'=' * 80}")
        print(f"ATTENTION ANALYSIS: {state_description}")
        print(f"{'=' * 80}")

        print("\n📊 Q-Values:")
        for idx, (action_name, q_val) in enumerate(zip(self.action_names, q_values)):
            marker = "🎯" if idx == selected_action else "  "
            print(f"{marker} {action_name}: {q_val:.4f}")

        print(
            f"\n🔍 Attention Distribution (Selected Action: {self.action_names[selected_action]}):"
        )

        attention = attention_weights[selected_action]

        for group_name, indices in self.feature_groups.items():
            group_attention = np.sum(attention[indices])
            print(f"   {group_name:25s}: {group_attention * 100:5.2f}%")

    def visualize_attention_comparison(
        self, state, output_path=None, state_description=""
    ):
        """
        Compare attention patterns across all actions.

        Args:
            state: State vector
            output_path: Path to save figure
            state_description: Description for title
        """
        attention_weights = self.compute_attention_weights(state)
        q_values = self.get_q_values(state)

        group_attention = {}
        for action_idx, action_name in enumerate(self.action_names):
            attention = attention_weights[action_idx]
            group_attention[action_name] = {
                group: np.sum(attention[indices])
                for group, indices in self.feature_groups.items()
            }

        df = pd.DataFrame(group_attention).T

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        df.plot(kind="bar", ax=ax1, width=0.8)
        ax1.set_title(
            f"Attention Distribution by Feature Group\n{state_description}",
            fontsize=12,
            fontweight="bold",
        )
        ax1.set_xlabel("Action", fontsize=11)
        ax1.set_ylabel("Attention Weight", fontsize=11)
        ax1.legend(title="Feature Groups", bbox_to_anchor=(1.05, 1), loc="upper left")
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0)
        ax1.grid(axis="y", alpha=0.3)

        colors = ["#d62728" if q < np.max(q_values) else "#2ca02c" for q in q_values]
        bars = ax2.bar(self.action_names, q_values, color=colors, alpha=0.7)
        ax2.set_title(f"Q-Values\n{state_description}", fontsize=12, fontweight="bold")
        ax2.set_xlabel("Action", fontsize=11)
        ax2.set_ylabel("Q-Value", fontsize=11)
        ax2.axhline(y=0, color="k", linestyle="--", alpha=0.3)
        ax2.grid(axis="y", alpha=0.3)

        for bar, q_val in zip(bars, q_values):
            height = bar.get_height()
            ax2.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"{q_val:.3f}",
                ha="center",
                va="bottom" if height > 0 else "top",
                fontsize=10,
                fontweight="bold",
            )

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            print(f"💾 Saved visualization to: {output_path}")
        else:
            plt.show()

        plt.close()

    def batch_analyze(self, states, descriptions=None, output_dir=None):
        """
        Analyze attention patterns for multiple states.

        Args:
            states: List of state vectors
            descriptions: Optional list of descriptions
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

            self.analyze_decision(state, desc)

            output_file = (
                output_path / f"attention_{idx:03d}_{desc.replace(' ', '_')}.png"
            )
            self.visualize_attention_comparison(state, output_file, desc)

        print(f"\n✅ Batch analysis complete! Results saved to: {output_dir}")


def generate_test_states():
    """
    Generate representative test states.

    TLS 1 (indices 0-15):
        [0-3]: Phase encoding (one-hot)
        [0] = 1.0 → Phase 1 (P1)
        [1] = 1.0 → Phase 2 (P2)
        [2] = 1.0 → Phase 3 (P3)
        [3] = 1.0 → Phase 4 (P4)
        [4]: Phase duration (0-1, normalized by 60s)
        [5-8]: Vehicle queue detectors (4 directions, binary 0/1)
        [9-12]: Bicycle queue detectors (4 directions, binary 0/1)
        [13]: Bus present (binary 0/1)
        [14]: Bus waiting time (0-1, normalized)
        [15]: Simulation time (0-1, normalized)

    TLS 2 (indices 16-31): Same structure
        [16-19]: Phase encoding (one-hot)
        [16] = 1.0 → Phase 1 (P1)
        [17] = 1.0 → Phase 2 (P2)
        [18] = 1.0 → Phase 3 (P3)
        [19] = 1.0 → Phase 4 (P4)
        [20]: Phase duration (0-1, normalized by 60s)
        [21-24]: Vehicle queue detectors (4 directions, binary 0/1)
        [25-28]: Bicycle queue detectors (4 directions, binary 0/1)
        [29]: Bus present (binary 0/1)
        [30]: Bus waiting time (0-1, normalized)
        [31]: Simulation time (0-1, normalized)
    """
    states = []
    descriptions = []

    """
    Scenario 1: High Vehicle Demand on Major Arterial (P1)
    
    Traffic Situation:
        - Phase 1 (major N-S through) active for 36s at TLS1, 24s at TLS2
        - Heavy vehicle queues on arterial (directions 1&2) at TLS1
        - Cross-street (directions 3&4) is clear
        - Represents asymmetric demand: 4x arterial vs 1x cross-street
    
    Purpose:
        Tests if model prioritizes high-demand arterial movements by:
        - Attending to vehicle queue features [5-8]
        - Balancing phase duration to serve demand
        - Deciding whether to Continue or transition to serve cross-street
    
    Real-world Context:
        Morning/evening rush hour on urban arterial with light cross-traffic
    """
    p1_high_vehicle_queue = np.zeros(32)
    p1_high_vehicle_queue[0] = 1.0  # TLS1: Phase 1 active (major through)
    p1_high_vehicle_queue[4] = 0.6  # TLS1: Phase duration = 36s (0.6 × 60)
    p1_high_vehicle_queue[5:9] = [
        1.0,
        1.0,
        0.0,
        0.0,
    ]  # TLS1: Heavy vehicle queue in directions 1&2
    p1_high_vehicle_queue[16] = 1.0  # TLS2: Phase 1 active
    p1_high_vehicle_queue[20] = 0.4  # TLS2: Phase duration = 24s (0.4 × 60)
    states.append(p1_high_vehicle_queue)
    descriptions.append("P1_High_Vehicle_Queue")

    """
    Scenario 2: Bus Priority During Phase 1
    
    Traffic Situation:
        - Phase 1 active for 30s at both intersections
        - Buses detected at both TLS1 and TLS2
        - High bus waiting times (0.85 and 0.9 normalized)
        - Buses travel on major arterial (N-S through lanes)
    
    Purpose:
        Tests if model recognizes bus priority conditions by:
        - Attending to bus presence features [13, 29]
        - Attending to bus waiting time features [14, 30]
        - Considering Skip2P1 action to expedite bus service
        - Balancing bus priority with general traffic demand
    
    Real-world Context:
        Bus approaching intersection during active green phase
        Evaluating whether to extend green or transition
    """
    p1_bus_waiting = np.zeros(32)
    p1_bus_waiting[0] = 1.0  # TLS1: Phase 1 active (major through)
    p1_bus_waiting[4] = 0.5  # TLS1: Phase duration = 30s
    p1_bus_waiting[13] = 1.0  # TLS1: Bus detected in priority lane
    p1_bus_waiting[14] = 0.85  # TLS1: High bus waiting time (normalized)
    p1_bus_waiting[16] = 1.0  # TLS2: Phase 1 active
    p1_bus_waiting[29] = 1.0  # TLS2: Bus detected
    p1_bus_waiting[30] = 0.9  # TLS2: High bus waiting time
    states.append(p1_bus_waiting)
    descriptions.append("P1_Bus_Waiting")

    """
    Scenario 3: Long Phase Duration with Spatial Queue Distribution
    
    Traffic Situation:
        - Phase 1 active for ~40s at TLS1 (90% of max_green=44s)
        - TLS1 has queues in directions 3&4 (cross-street)
        - TLS2 has queues in directions 1&2 (arterial)
        - Demonstrates spatially distributed demand across intersections
    
    Purpose:
        Tests if model handles complex spatial patterns by:
        - Recognizing long phase duration [4] = 0.9 (near maximum)
        - Attending to different queue locations at TLS1 vs TLS2
        - Deciding whether to Continue (risk hitting max_green)
        - Or transition to Next phase to serve waiting cross-street
    
    Real-world Context:
        Traffic wave propagation causing different queue patterns
        at adjacent intersections on same corridor
    """
    p1_long_duration_mixed_queue = np.zeros(32)
    p1_long_duration_mixed_queue[0] = 1.0
    p1_long_duration_mixed_queue[4] = 0.9
    p1_long_duration_mixed_queue[5:9] = [
        0.0,
        0.0,
        1.0,
        1.0,
    ]  # TLS1: Vehicle queue in directions 3&4
    p1_long_duration_mixed_queue[16] = 1.0  # TLS2: Phase 1 active
    p1_long_duration_mixed_queue[21:25] = [
        1.0,
        1.0,
        0.0,
        0.0,
    ]  # TLS2: Vehicle queue in directions 1&2
    states.append(p1_long_duration_mixed_queue)
    descriptions.append("P1_Long_Duration_Mixed_Queue")

    """
    Scenario 4: High Bicycle Demand on Minor Street (P3)
    
    Traffic Situation:
        - Phase 3 (minor E-W through) active for 18s
        - Heavy bicycle queues at all directions at TLS1
        - Partial bicycle queues at TLS2 (directions 1&2)
        - Represents vulnerable road user demand on cross-street
    
    Purpose:
        Tests if model recognizes multimodal equity by:
        - Attending to bicycle queue features [9-12, 25-28]
        - Differentiating bicycle demand from vehicle demand
        - Balancing minor phase timing for bicycle service
        - Avoiding premature transition that would strand cyclists
    
    Real-world Context:
        Bicycle commute period on residential cross-street
        connecting to major arterial, requiring adequate green time
    """
    p3_high_bicycle_demand = np.zeros(32)
    p3_high_bicycle_demand[2] = 1.0  # TLS1: Phase 3 active (minor through)
    p3_high_bicycle_demand[4] = 0.3  # TLS1: Phase duration = 18s
    p3_high_bicycle_demand[9:13] = [
        1.0,
        1.0,
        1.0,
        1.0,
    ]  # TLS1: Bicycle queue in all directions
    p3_high_bicycle_demand[18] = 1.0  # TLS2: Phase 3 active
    p3_high_bicycle_demand[25:29] = [
        1.0,
        1.0,
        0.0,
        0.0,
    ]  # TLS2: Bicycle queue in directions 1&2
    states.append(p3_high_bicycle_demand)
    descriptions.append("P3_High_Bicycle_Demand")

    return states, descriptions


if __name__ == "__main__":
    MODEL_PATH = "models/training_20251103_163015/checkpoint_ep192.pth"

    analyzer = AttentionAnalyzer(MODEL_PATH)

    states, descriptions = generate_test_states()

    analyzer.batch_analyze(states, descriptions)

    print("\n" + "=" * 80)
    print("✅ Attention analysis complete!")
    print("📊 Results saved to: images/2/attention/")
    print("=" * 80)
