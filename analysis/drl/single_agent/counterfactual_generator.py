"""
Counterfactual Explanation Generation for DRL Agent

Generates minimal state perturbations that flip the agent's decision
from one action to another, revealing decision boundaries.

Optimization Problem:
    minimize: λ₁·||s' - s||₂² + λ₂·max(0, Q(s', a_orig) - Q(s', a_target))

Where:
    - First term: L2 distance penalty (prefer small changes)
    - Second term: Action flip constraint (ensure target action is chosen)
"""

import sys
import os

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

import torch
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from controls.ml_based.drl import DQNAgent
from controls.ml_based.drl.single_agent.config import DRLConfig


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
            max_iterations: Maximum optimization iterations
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
            "changed_indices": changed_indices,
            "original_action": original_action,
            "target_action": target_action,
            "final_action": final_action,
            "original_q_values": original_q_values.detach().cpu().numpy(),
            "final_q_values": final_q_values.detach().cpu().numpy(),
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

    def batch_generate(self, states, descriptions=None, output_dir=None):
        """
        Generate counterfactuals for multiple states.

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

    def find_states_with_action(self, states, actions, target_action, num_samples=100):
        """
        Find states where the agent selects target_action.

        Args:
            states: Array of states
            actions: Array of actions taken
            target_action: Target action index to find
            num_samples: Number of samples to return

        Returns:
            tuple: (sampled_states, sampled_indices)
        """
        matching_indices = np.where(actions == target_action)[0]

        if len(matching_indices) == 0:
            print(f"⚠️  No states found with action {target_action}")
            return None, None

        if len(matching_indices) > num_samples:
            sampled_indices = np.random.choice(
                matching_indices, num_samples, replace=False
            )
        else:
            sampled_indices = matching_indices

        return states[sampled_indices], sampled_indices

    def generate_counterfactual_aggressive(
        self,
        original_state,
        original_action,
        target_action,
        max_iterations=500,
        num_attempts=5,
        learning_rate=0.05,
    ):
        """
        Aggressive counterfactual generation with multiple attempts.
        Designed for difficult/rare transitions.

        Args:
            original_state: Original state (numpy array)
            original_action: Original action index
            target_action: Target action index
            max_iterations: Max optimization iterations per attempt
            num_attempts: Number of random initialization attempts
            learning_rate: Learning rate for optimization

        Returns:
            Best counterfactual found across all attempts
        """
        best_cf = None
        best_distance = float("inf")
        best_success = False

        for attempt in range(num_attempts):
            if attempt == 0:
                init_state = original_state.copy()
            else:
                noise = np.random.randn(*original_state.shape) * 0.1
                init_state = np.clip(original_state + noise, 0, 1)

            cf_state = torch.tensor(
                init_state, dtype=torch.float32, device=self.device, requires_grad=True
            )

            optimizer = optim.Adam([cf_state], lr=learning_rate)

            for iteration in range(max_iterations):
                optimizer.zero_grad()

                q_values = self.agent.policy_net(cf_state.unsqueeze(0))[0]
                predicted_action = q_values.argmax().item()

                target_q = q_values[target_action]
                other_q_max = torch.max(
                    torch.cat([q_values[:target_action], q_values[target_action + 1 :]])
                )

                action_loss = torch.relu(other_q_max - target_q + 0.5)
                distance = torch.norm(
                    cf_state - torch.tensor(original_state).to(self.device)
                )
                distance_loss = distance
                bounds_loss = torch.sum(torch.relu(-cf_state)) + torch.sum(
                    torch.relu(cf_state - 1)
                )

                total_loss = (
                    action_loss * 10.0 + distance_loss * 0.5 + bounds_loss * 5.0
                )

                total_loss.backward()
                optimizer.step()

                with torch.no_grad():
                    cf_state.clamp_(0, 1)

                if predicted_action == target_action:
                    current_distance = distance.item()
                    if current_distance < best_distance:
                        best_distance = current_distance
                        best_cf = {
                            "state": cf_state.detach().cpu().numpy(),
                            "iterations": iteration + 1,
                            "attempt": attempt + 1,
                            "distance": current_distance,
                        }
                        best_success = True
                    break

        if best_success:
            print(
                f"   ✅ Success after {best_cf['attempt']} attempts, "
                f"{best_cf['iterations']} iterations, distance: {best_cf['distance']:.3f}"
            )
        else:
            print(f"   Failed after {num_attempts} attempts")

        return best_cf if best_success else None

    def batch_generate_rare_transitions(
        self, states, actions, scenarios, output_dir=None
    ):
        """
        Generate counterfactuals for rare action transitions using enhanced optimization.

        Args:
            states: Array of state vectors
            actions: Array of action labels
            scenarios: Array of scenario names
            output_dir: Directory to save results (required)
        """
        if output_dir is None:
            raise ValueError("output_dir must be provided")

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        rare_transitions = [
            ("Continue", "Next"),
            ("Skip2P1", "Next"),
            ("Next", "Continue"),
            ("Next", "Skip2P1"),
        ]

        action_map = {"Continue": 0, "Skip2P1": 1, "Next": 2}

        results = []

        print("\n" + "=" * 80)
        print("ENHANCED COUNTERFACTUAL GENERATION FOR RARE TRANSITIONS")
        print("=" * 80)

        print(f"\n   Total states: {len(states):,}")
        print("   Action distribution:")
        for action_name, action_idx in action_map.items():
            count = np.sum(actions == action_idx)
            pct = count / len(actions) * 100
            print(f"      {action_name}: {count:,} ({pct:.1f}%)")

        for original_action_name, target_action_name in rare_transitions:
            print(f"\n{'=' * 80}")
            print(f"TRANSITION: {original_action_name} → {target_action_name}")
            print("=" * 80)

            original_action = action_map[original_action_name]
            target_action = action_map[target_action_name]

            sample_states, indices = self.find_states_with_action(
                states, actions, original_action, num_samples=10
            )

            if sample_states is None:
                continue

            print(f"   Found {len(sample_states)} sample states")

            successes = 0
            for i, (state, idx) in enumerate(zip(sample_states, indices)):
                scenario = scenarios[idx]
                print(
                    f"\n   Attempt {i + 1}/{len(sample_states)} (Scenario: {scenario}):"
                )

                cf_result = self.generate_counterfactual_aggressive(
                    state,
                    original_action,
                    target_action,
                    max_iterations=500,
                    num_attempts=5,
                    learning_rate=0.05,
                )

                if cf_result:
                    successes += 1

                    output_file = (
                        output_path
                        / f"cf_rare_{original_action_name}_to_{target_action_name}_{i + 1}.png"
                    )
                    self.visualize_counterfactual_enhanced(
                        state,
                        cf_result["state"],
                        original_action,
                        target_action,
                        output_file,
                    )

                    results.append(
                        {
                            "transition": f"{original_action_name} → {target_action_name}",
                            "scenario": scenario,
                            "distance": cf_result["distance"],
                            "iterations": cf_result["iterations"],
                            "attempts": cf_result["attempt"],
                        }
                    )

                    if successes >= 3:
                        break

            print(f"\n   ✅ Success rate: {successes}/{len(sample_states)}")

        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"   Total counterfactuals generated: {len(results)}")
        print(f"   Saved to: {output_dir}")

        if results:
            print("\n   Transition Success Summary:")
            for transition in rare_transitions:
                transition_str = f"{transition[0]} → {transition[1]}"
                count = sum(1 for r in results if r["transition"] == transition_str)
                print(f"      {transition_str}: {count} counterfactuals")

        print("\n✅ Enhanced counterfactual generation complete!")

    def visualize_counterfactual_enhanced(
        self,
        original_state,
        cf_state,
        original_action,
        target_action,
        output_path,
    ):
        """
        Visualize enhanced counterfactual changes.
        """
        changes = cf_state - original_state
        significant_changes = np.abs(changes) > 0.01

        fig, axes = plt.subplots(2, 1, figsize=(14, 10))

        x = np.arange(len(original_state))
        width = 0.35

        axes[0].bar(
            x - width / 2,
            original_state,
            width,
            label=f"Original ({self.action_names[original_action]})",
            alpha=0.7,
            color="#3498db",
        )
        axes[0].bar(
            x + width / 2,
            cf_state,
            width,
            label=f"Counterfactual ({self.action_names[target_action]})",
            alpha=0.7,
            color="#e74c3c",
        )

        axes[0].set_xlabel("Feature Index", fontsize=12)
        axes[0].set_ylabel("Feature Value", fontsize=12)
        axes[0].set_title(
            f"State Comparison: {self.action_names[original_action]} → "
            f"{self.action_names[target_action]}",
            fontsize=14,
            fontweight="bold",
        )
        axes[0].legend()
        axes[0].grid(axis="y", alpha=0.3)

        significant_indices = np.where(significant_changes)[0]
        if len(significant_indices) > 0:
            significant_changes_values = changes[significant_indices]
            colors = [
                "#27ae60" if c > 0 else "#e74c3c" for c in significant_changes_values
            ]

            axes[1].barh(
                significant_indices, significant_changes_values, color=colors, alpha=0.7
            )
            axes[1].set_xlabel("Change in Value (Δ)", fontsize=12)
            axes[1].set_ylabel("Feature Index", fontsize=12)
            axes[1].set_title(
                f"Significant Feature Changes (|Δ| > 0.01): {len(significant_indices)} features",
                fontsize=14,
                fontweight="bold",
            )
            axes[1].axvline(x=0, color="black", linestyle="-", linewidth=0.8)
            axes[1].grid(axis="x", alpha=0.3)

            for idx in significant_indices[:10]:
                axes[1].text(
                    changes[idx],
                    idx,
                    f" {self.feature_names[idx]}",
                    va="center",
                    fontsize=8,
                )

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"   💾 Saved: {output_path}")


def generate_test_states():
    """
    Generate test states for counterfactual analysis.

    Returns:
        tuple: (states, descriptions)
    """
    states = []
    descriptions = []

    """
    Scenario 1: Phase 1 with Moderate Vehicle Queue
    
    Traffic Situation:
        - Phase 1 active for 42s at TLS1, 30s at TLS2
        - Moderate vehicle queue in one direction at TLS1
        - Tests counterfactual: What minimal changes cause different action?
    
    Purpose:
        Generates counterfactuals to understand decision boundaries:
        - Continue vs Next transition threshold
        - Which features must change to flip action
        - Minimal perturbation analysis
    """
    p1_moderate_queue = np.zeros(32)
    p1_moderate_queue[0] = 1.0  # TLS1: Phase 1 active
    p1_moderate_queue[4] = 0.7  # TLS1: Phase duration = 42s (0.7 × 60)
    p1_moderate_queue[5:9] = [1.0, 0.0, 0.0, 0.0]  # TLS1: Vehicle queue in direction 1
    p1_moderate_queue[16] = 1.0  # TLS2: Phase 1 active
    p1_moderate_queue[20] = 0.5  # TLS2: Phase duration = 30s (0.5 × 60)
    states.append(p1_moderate_queue)
    descriptions.append("P1_Moderate_Queue")

    """
    Scenario 2: Phase 1 with Bus Present
    
    Traffic Situation:
        - Phase 1 active for 18s (early in cycle)
        - Bus detected at TLS1 with moderate waiting time
        - Buses travel on major arterial through lanes (P1)
    
    Purpose:
        Tests counterfactual for bus priority decisions:
        - Continue vs Skip2P1 decision boundary
        - How bus waiting time threshold affects action
        - Which feature changes flip to Skip2P1
    """
    p1_bus_present = np.zeros(32)
    p1_bus_present[0] = 1.0  # TLS1: Phase 1 active (buses use through lanes)
    p1_bus_present[4] = 0.3  # TLS1: Phase duration = 18s (0.3 × 60)
    p1_bus_present[13] = 1.0  # TLS1: Bus detected
    p1_bus_present[14] = 0.6  # TLS1: Moderate bus waiting time (normalized)
    p1_bus_present[16] = 1.0  # TLS2: Phase 1 active
    states.append(p1_bus_present)
    descriptions.append("P1_Bus_Present")

    """
    Scenario 3: Phase 1 Near Maximum Duration
    
    Traffic Situation:
        - Phase 1 active for 44s (at max_green limit for P1)
        - Mixed vehicle queues at both intersections
        - Critical decision point: extend or transition
    
    Purpose:
        Tests counterfactual near max_green threshold:
        - Continue vs Next when at duration limit
        - How queue distribution affects transition timing
        - Minimal changes that force Next action
    """
    p1_long_duration = np.zeros(32)
    p1_long_duration[0] = 1.0  # TLS1: Phase 1 active
    p1_long_duration[4] = 0.73  # TLS1: Phase duration = 44s (at P1 max_green)
    p1_long_duration[5:9] = [
        0.0,
        1.0,
        1.0,
        0.0,
    ]  # TLS1: Vehicle queues in directions 2&3
    p1_long_duration[16] = 1.0  # TLS2: Phase 1 active
    p1_long_duration[21:25] = [
        1.0,
        0.0,
        0.0,
        1.0,
    ]  # TLS2: Vehicle queues in directions 1&4
    states.append(p1_long_duration)
    descriptions.append("P1_Long_Duration")

    return states, descriptions


if __name__ == "__main__":
    MODEL_PATH = "models/training_20251103_163015/checkpoint_ep192.pth"

    generator = CounterfactualGenerator(MODEL_PATH)

    states, descriptions = generate_test_states()

    generator.batch_generate(states, descriptions)

    print("\n" + "=" * 80)
    print("✅ Counterfactual generation complete!")
    print("📊 Results saved to: images/2/counterfactuals/")
    print("=" * 80)
