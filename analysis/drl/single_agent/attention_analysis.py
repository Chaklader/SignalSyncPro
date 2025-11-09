"""
Attention-Based State Attribution Analysis

Computes attention weights showing which state features the DQN attends to
when making decisions. Uses gradient-based attention as a proxy since the
current DQN architecture doesn't have explicit attention layers.

Mathematical foundation:
    Attention weight α_i for feature i:

    α_i = softmax(|∇Q/∇s_i|) = exp(|∇Q/∇s_i|) / Σ_j exp(|∇Q/∇s_j|)

Where higher α_i indicates feature i receives more attention.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

from controls.ml_based.drl.agent import DQNAgent
from controls.ml_based.drl.config import DRLConfig


class AttentionAnalyzer:
    """
    Analyzes attention patterns in trained DQN agent.
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
            "Queue_Lengths": list(range(0, 8)),
            "Waiting_Times": list(range(8, 16)),
            "Phase_Info": list(range(16, 19)),
            "Bus_Info": list(range(19, 23)),
            "Detectors": list(range(23, 27)),
            "Ped_Demand": list(range(27, 29)),
            "Modal_Demand": list(range(29, 32)),
        }

    def compute_attention_weights(self, state):
        """
        Compute attention weights using gradient magnitudes.

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
            print(f"   {group_name:20s}: {group_attention * 100:5.2f}%")

        print("\n🎯 Top 10 Individual Features (Selected Action):")
        top_indices = np.argsort(attention)[-10:][::-1]

        feature_names = [
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

        for rank, idx in enumerate(top_indices, 1):
            print(
                f"   {rank:2d}. {feature_names[idx]:25s}: {attention[idx] * 100:5.2f}% (value: {state[idx]:.3f})"
            )

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

    def batch_analyze(self, states, descriptions=None, output_dir="results/attention"):
        """
        Analyze attention patterns for multiple states.

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

            self.analyze_decision(state, desc)

            output_file = (
                output_path / f"attention_{idx:03d}_{desc.replace(' ', '_')}.png"
            )
            self.visualize_attention_comparison(state, output_file, desc)

        print(f"\n✅ Batch analysis complete! Results saved to: {output_dir}")


def generate_test_states():
    """Generate representative test states."""
    states = []
    descriptions = []

    state = np.zeros(32)
    state[0] = 0.85
    state[8] = 0.6
    state[16] = 1
    state[17] = 0.25
    states.append(state)
    descriptions.append("Continue_High_Queue")

    state = np.zeros(32)
    state[19] = 1.0
    state[20] = 0.85
    state[16] = 2
    state[17] = 0.15
    states.append(state)
    descriptions.append("Skip2P1_Bus_Priority")

    state = np.zeros(32)
    state[0] = 0.4
    state[2] = 0.75
    state[16] = 1
    state[17] = 0.9
    states.append(state)
    descriptions.append("Next_Phase_Change")

    state = np.zeros(32)
    state[27] = 1.0
    state[28] = 1.0
    state[6] = 0.8
    state[16] = 3
    states.append(state)
    descriptions.append("Pedestrian_Demand")

    return states, descriptions


if __name__ == "__main__":
    MODEL_PATH = "models/training_20251103_163015/checkpoint_ep192.pth"

    analyzer = AttentionAnalyzer(MODEL_PATH)

    states, descriptions = generate_test_states()

    analyzer.batch_analyze(states, descriptions)

    print("\n" + "=" * 80)
    print("✅ Attention analysis complete!")
    print("📊 Results saved to: results/attention/")
    print("=" * 80)
