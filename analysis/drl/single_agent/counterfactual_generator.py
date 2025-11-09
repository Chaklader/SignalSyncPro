"""
Counterfactual Explanation Generation

Generates counterfactual states that would change the agent's action decision.
Uses gradient-based optimization to find minimal perturbations.

Mathematical foundation:
    Find s' such that:
    - argmax_a Q(s', a) = a_target (desired action)
    - ||s' - s||_2 is minimized (minimal change)

Optimization problem:
    minimize: λ₁·||s' - s||₂² + λ₂·max(0, Q(s', a_orig) - Q(s', a_target))

Where:
    - First term: L2 distance penalty (prefer small changes)
    - Second term: Action flip constraint (ensure target action is chosen)
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from controls.ml_based.drl.agent import DQNAgent
from controls.ml_based.drl.config import DRLConfig


class CounterfactualGenerator:
    """
    Generates counterfactual explanations for DQN decisions.
    """

    def __init__(self, model_path):
        """
        Initialize generator with trained model.

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

    def _get_feature_names(self):
        """Get human-readable feature names."""
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

    def generate_counterfactual(
        self,
        original_state,
        target_action,
        learning_rate=0.01,
        max_iterations=1000,
        lambda_distance=1.0,
        lambda_action=10.0,
        convergence_threshold=0.01,
    ):
        """
        Generate counterfactual state for target action.

        Args:
            original_state: Original state vector
            target_action: Desired action index (0=Continue, 1=Skip2P1, 2=Next)
            learning_rate: Optimization learning rate
            max_iterations: Maximum optimization steps
            lambda_distance: Weight for L2 distance penalty
            lambda_action: Weight for action flip constraint
            convergence_threshold: Stop if change < threshold

        Returns:
            dict: Results including counterfactual state, changes, and metrics
        """
        if isinstance(original_state, np.ndarray):
            original_state_tensor = torch.FloatTensor(original_state).to(self.device)
        else:
            original_state_tensor = original_state.clone().to(self.device)

        original_q_values = self.agent.policy_net(original_state_tensor.unsqueeze(0))[0]
        original_action = torch.argmax(original_q_values).item()

        if original_action == target_action:
            return {
                "success": False,
                "message": f"Original state already selects target action {self.action_names[target_action]}",
            }

        counterfactual_state = (
            original_state_tensor.clone().detach().requires_grad_(True)
        )
        optimizer = torch.optim.Adam([counterfactual_state], lr=learning_rate)

        best_state = None
        best_loss = float("inf")
        prev_loss = float("inf")

        for iteration in range(max_iterations):
            optimizer.zero_grad()

            q_values = self.agent.policy_net(counterfactual_state.unsqueeze(0))[0]

            distance_loss = lambda_distance * torch.sum(
                (counterfactual_state - original_state_tensor) ** 2
            )

            action_loss = lambda_action * torch.relu(
                q_values[original_action] - q_values[target_action]
            )

            total_loss = distance_loss + action_loss

            total_loss.backward()
            optimizer.step()

            with torch.no_grad():
                counterfactual_state.clamp_(0, 1)

            if total_loss.item() < best_loss:
                best_loss = total_loss.item()
                best_state = counterfactual_state.clone()

            if (
                iteration > 0
                and abs(prev_loss - total_loss.item()) < convergence_threshold
            ):
                print(f"   ✓ Converged at iteration {iteration}")
                break

            prev_loss = total_loss.item()

        if best_state is None:
            best_state = counterfactual_state

        final_q_values = self.agent.policy_net(best_state.unsqueeze(0))[0]
        final_action = torch.argmax(final_q_values).item()

        counterfactual_np = best_state.detach().cpu().numpy()
        original_np = original_state_tensor.cpu().numpy()

        delta = counterfactual_np - original_np
        changed_indices = np.where(np.abs(delta) > 0.01)[0]

        return {
            "success": final_action == target_action,
            "original_state": original_np,
            "counterfactual_state": counterfactual_np,
            "delta": delta,
            "original_action": original_action,
            "target_action": target_action,
            "final_action": final_action,
            "original_q_values": original_q_values.detach().cpu().numpy(),
            "final_q_values": final_q_values.detach().cpu().numpy(),
            "changed_indices": changed_indices,
            "num_changed_features": len(changed_indices),
            "l2_distance": np.linalg.norm(delta),
            "iterations": iteration + 1,
            "final_loss": best_loss,
        }

    def explain_counterfactual(self, result):
        """
        Print human-readable explanation of counterfactual.

        Args:
            result: Result dict from generate_counterfactual
        """
        if not result.get("success", False):
            print(f"❌ {result.get('message', 'Failed to generate counterfactual')}")
            return

        print(f"\n{'=' * 80}")
        print("COUNTERFACTUAL EXPLANATION")
        print(f"{'=' * 80}")

        print("\n📊 Original Decision:")
        print(f"   Action: {self.action_names[result['original_action']]}")
        print(f"   Q-values: {result['original_q_values']}")

        print("\n🎯 Target Decision:")
        print(f"   Action: {self.action_names[result['target_action']]}")

        print("\n✨ Counterfactual Decision:")
        print(f"   Action: {self.action_names[result['final_action']]}")
        print(f"   Q-values: {result['final_q_values']}")

        print("\n📏 Changes Required:")
        print(f"   Features changed: {result['num_changed_features']}")
        print(f"   L2 distance: {result['l2_distance']:.4f}")
        print(f"   Optimization iterations: {result['iterations']}")

        print("\n🔍 Feature Changes (|Δ| > 0.01):")
        for idx in result["changed_indices"]:
            original_val = result["original_state"][idx]
            new_val = result["counterfactual_state"][idx]
            delta_val = result["delta"][idx]
            print(
                f"   {self.feature_names[idx]:25s}: {original_val:.3f} → {new_val:.3f} (Δ = {delta_val:+.3f})"
            )

    def visualize_counterfactual(self, result, output_path=None):
        """
        Create visualization of counterfactual changes.

        Args:
            result: Result dict from generate_counterfactual
            output_path: Path to save figure
        """
        if not result.get("success", False):
            print("❌ Cannot visualize failed counterfactual")
            return

        changed_indices = result["changed_indices"]
        changed_names = [self.feature_names[i] for i in changed_indices]
        original_vals = [result["original_state"][i] for i in changed_indices]
        cf_vals = [result["counterfactual_state"][i] for i in changed_indices]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        x = np.arange(len(changed_names))
        width = 0.35

        ax1.bar(
            x - width / 2,
            original_vals,
            width,
            label="Original",
            alpha=0.8,
            color="#d62728",
        )
        ax1.bar(
            x + width / 2,
            cf_vals,
            width,
            label="Counterfactual",
            alpha=0.8,
            color="#2ca02c",
        )

        ax1.set_xlabel("Feature", fontsize=11)
        ax1.set_ylabel("Value", fontsize=11)
        ax1.set_title("Feature Value Comparison", fontsize=12, fontweight="bold")
        ax1.set_xticks(x)
        ax1.set_xticklabels(changed_names, rotation=45, ha="right")
        ax1.legend()
        ax1.grid(axis="y", alpha=0.3)

        q_comparison = np.array([result["original_q_values"], result["final_q_values"]])

        im = ax2.imshow(q_comparison, cmap="RdYlGn", aspect="auto")
        ax2.set_xticks(range(len(self.action_names)))
        ax2.set_xticklabels(self.action_names)
        ax2.set_yticks([0, 1])
        ax2.set_yticklabels(["Original", "Counterfactual"])
        ax2.set_title("Q-Value Comparison", fontsize=12, fontweight="bold")

        for i in range(2):
            for j in range(len(self.action_names)):
                ax2.text(
                    j,
                    i,
                    f"{q_comparison[i, j]:.3f}",
                    ha="center",
                    va="center",
                    color="black",
                    fontweight="bold",
                )

        plt.colorbar(im, ax=ax2, label="Q-Value")

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            print(f"💾 Saved visualization to: {output_path}")
        else:
            plt.show()

        plt.close()

    def batch_generate(
        self, states, descriptions=None, output_dir="results/counterfactuals"
    ):
        """
        Generate counterfactuals for multiple states.

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

            original_q = self.agent.policy_net(
                torch.FloatTensor(state).unsqueeze(0).to(self.device)
            )[0]
            original_action = torch.argmax(original_q).item()

            for target_action in range(DRLConfig.ACTION_DIM):
                if target_action == original_action:
                    continue

                print(
                    f"\n   Generating: {self.action_names[original_action]} → {self.action_names[target_action]}"
                )

                result = self.generate_counterfactual(state, target_action)
                self.explain_counterfactual(result)

                if result.get("success", False):
                    output_file = (
                        output_path
                        / f"cf_{idx:03d}_{desc}_to_{self.action_names[target_action]}.png"
                    )
                    self.visualize_counterfactual(result, output_file)

        print(f"\n✅ Batch generation complete! Results saved to: {output_dir}")


def generate_test_states():
    """Generate test states for counterfactual analysis."""
    states = []
    descriptions = []

    state = np.zeros(32)
    state[0] = 0.7
    state[8] = 0.5
    state[16] = 1
    state[17] = 0.3
    states.append(state)
    descriptions.append("Moderate_Queue")

    state = np.zeros(32)
    state[2] = 0.6
    state[10] = 0.4
    state[16] = 2
    state[17] = 0.2
    states.append(state)
    descriptions.append("P2_Active")

    state = np.zeros(32)
    state[0] = 0.3
    state[2] = 0.8
    state[16] = 1
    state[17] = 0.8
    states.append(state)
    descriptions.append("Long_Duration")

    return states, descriptions


if __name__ == "__main__":
    MODEL_PATH = "models/training_20251103_163015/checkpoint_ep192.pth"

    generator = CounterfactualGenerator(MODEL_PATH)

    states, descriptions = generate_test_states()

    generator.batch_generate(states, descriptions)

    print("\n" + "=" * 80)
    print("✅ Counterfactual generation complete!")
    print("📊 Results saved to: results/counterfactuals/")
    print("=" * 80)
