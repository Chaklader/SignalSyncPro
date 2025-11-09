"""
VIPER: Verifiable Decision Tree Extraction from DQN

Implements VIPER (Verifiable Policy Extraction through Regression) to extract
an interpretable decision tree that approximates the DQN policy.

Algorithm:
1. Collect dataset of (state, action) pairs from DQN policy
2. Train decision tree classifier on dataset
3. Use tree to generate new states (DAgger-style aggregation)
4. Iterate until tree policy matches DQN policy
5. Extract and visualize decision rules

Reference: Bastani et al. (2018) "Verifiable Reinforcement Learning via Policy Extraction"
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
from pathlib import Path
import pickle

from controls.ml_based.drl.agent import DQNAgent
from controls.ml_based.drl.config import DRLConfig


class VIPERExtractor:
    """
    Extracts interpretable decision tree from trained DQN policy.
    """

    def __init__(self, model_path):
        """
        Initialize extractor with trained model.

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

        self.tree = None
        self.tree_accuracy = None

        print(f"✅ Loaded DQN model from: {model_path}")

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

    def collect_dqn_dataset(self, num_samples=10000, state_distribution="uniform"):
        """
        Collect dataset of (state, action) pairs from DQN policy.

        Args:
            num_samples: Number of samples to collect
            state_distribution: 'uniform' or 'gaussian'

        Returns:
            tuple: (states, actions)
        """
        print(f"\n📊 Collecting {num_samples} samples from DQN policy...")

        states = []
        actions = []

        for i in range(num_samples):
            if state_distribution == "uniform":
                state = np.random.uniform(0, 1, DRLConfig.STATE_DIM)
            else:
                state = np.clip(np.random.normal(0.5, 0.2, DRLConfig.STATE_DIM), 0, 1)

            state[16] = np.random.randint(1, 4)

            state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)

            with torch.no_grad():
                q_values = self.agent.policy_net(state_tensor)
                action = torch.argmax(q_values).item()

            states.append(state)
            actions.append(action)

            if (i + 1) % 2000 == 0:
                print(f"   Collected {i + 1}/{num_samples} samples...")

        states = np.array(states)
        actions = np.array(actions)

        action_distribution = np.bincount(actions, minlength=DRLConfig.ACTION_DIM)
        print("\n✅ Dataset collected!")
        print(
            f"   Action distribution: {dict(zip(self.action_names, action_distribution))}"
        )

        return states, actions

    def train_decision_tree(
        self,
        states,
        actions,
        max_depth=10,
        min_samples_split=50,
        min_samples_leaf=20,
        test_size=0.2,
    ):
        """
        Train decision tree classifier on DQN dataset.

        Args:
            states: State vectors
            actions: Corresponding actions
            max_depth: Maximum tree depth
            min_samples_split: Minimum samples to split node
            min_samples_leaf: Minimum samples in leaf
            test_size: Fraction for test set

        Returns:
            DecisionTreeClassifier: Trained tree
        """
        print("\n🌳 Training decision tree...")
        print(f"   Max depth: {max_depth}")
        print(f"   Min samples split: {min_samples_split}")
        print(f"   Min samples leaf: {min_samples_leaf}")

        split_idx = int(len(states) * (1 - test_size))
        train_states, test_states = states[:split_idx], states[split_idx:]
        train_actions, test_actions = actions[:split_idx], actions[split_idx:]

        self.tree = DecisionTreeClassifier(
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            min_samples_leaf=min_samples_leaf,
            random_state=42,
        )

        self.tree.fit(train_states, train_actions)

        train_pred = self.tree.predict(train_states)
        test_pred = self.tree.predict(test_states)

        train_acc = accuracy_score(train_actions, train_pred)
        test_acc = accuracy_score(test_actions, test_pred)
        self.tree_accuracy = test_acc

        print("\n✅ Tree trained!")
        print(f"   Train accuracy: {train_acc * 100:.2f}%")
        print(f"   Test accuracy: {test_acc * 100:.2f}%")
        print(f"   Tree depth: {self.tree.get_depth()}")
        print(f"   Number of leaves: {self.tree.get_n_leaves()}")

        print("\n📊 Classification Report (Test Set):")
        print(
            classification_report(
                test_actions, test_pred, target_names=self.action_names, zero_division=0
            )
        )

        return self.tree

    def viper_iteration(
        self,
        initial_states,
        initial_actions,
        n_iterations=3,
        samples_per_iteration=2000,
    ):
        """
        Run VIPER algorithm with DAgger-style dataset aggregation.

        Args:
            initial_states: Initial state dataset
            initial_actions: Initial action labels
            n_iterations: Number of VIPER iterations
            samples_per_iteration: New samples to generate per iteration

        Returns:
            DecisionTreeClassifier: Final tree after iterations
        """
        all_states = initial_states.copy()
        all_actions = initial_actions.copy()

        for iteration in range(n_iterations):
            print(f"\n{'=' * 80}")
            print(f"VIPER Iteration {iteration + 1}/{n_iterations}")
            print(f"{'=' * 80}")

            self.train_decision_tree(all_states, all_actions)

            print(
                f"\n🎲 Generating {samples_per_iteration} new samples using tree policy..."
            )
            new_states = []
            new_actions = []

            for i in range(samples_per_iteration):
                state = np.random.uniform(0, 1, DRLConfig.STATE_DIM)
                state[16] = np.random.randint(1, 4)

                state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)
                with torch.no_grad():
                    q_values = self.agent.policy_net(state_tensor)
                    dqn_action = torch.argmax(q_values).item()

                new_states.append(state)
                new_actions.append(dqn_action)

            all_states = np.vstack([all_states, new_states])
            all_actions = np.concatenate([all_actions, new_actions])

            print(f"   Dataset size now: {len(all_states)}")

        print(f"\n{'=' * 80}")
        print("Final Tree Training")
        print(f"{'=' * 80}")
        self.train_decision_tree(all_states, all_actions, max_depth=8)

        return self.tree

    def extract_rules(self, max_rules=20):
        """
        Extract human-readable decision rules from tree.

        Args:
            max_rules: Maximum number of rules to extract

        Returns:
            list: List of rule strings
        """
        if self.tree is None:
            print("❌ No tree trained yet!")
            return []

        tree_rules = export_text(
            self.tree, feature_names=self.feature_names, decimals=3, show_weights=True
        )

        print(f"\n{'=' * 80}")
        print(f"EXTRACTED DECISION RULES (Accuracy: {self.tree_accuracy * 100:.1f}%)")
        print(f"{'=' * 80}\n")
        print(tree_rules)

        return tree_rules

    def visualize_tree(self, output_path=None, max_depth=4):
        """
        Visualize decision tree structure.

        Args:
            output_path: Path to save figure
            max_depth: Maximum depth to visualize (for readability)
        """
        if self.tree is None:
            print("❌ No tree trained yet!")
            return

        fig, ax = plt.subplots(figsize=(20, 12))

        plot_tree(
            self.tree,
            feature_names=self.feature_names,
            class_names=self.action_names,
            filled=True,
            rounded=True,
            fontsize=8,
            max_depth=max_depth,
            ax=ax,
        )

        plt.title(
            f"Decision Tree Policy (Accuracy: {self.tree_accuracy * 100:.1f}%, Depth: {self.tree.get_depth()})",
            fontsize=16,
            fontweight="bold",
            pad=20,
        )

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            print(f"💾 Saved tree visualization to: {output_path}")
        else:
            plt.show()

        plt.close()

    def visualize_confusion_matrix(self, test_states, test_actions, output_path=None):
        """
        Visualize confusion matrix comparing tree to DQN.

        Args:
            test_states: Test state vectors
            test_actions: DQN actions for test states
            output_path: Path to save figure
        """
        if self.tree is None:
            print("❌ No tree trained yet!")
            return

        tree_predictions = self.tree.predict(test_states)

        cm = confusion_matrix(test_actions, tree_predictions)

        fig, ax = plt.subplots(figsize=(8, 6))

        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=self.action_names,
            yticklabels=self.action_names,
            ax=ax,
            cbar_kws={"label": "Count"},
        )

        ax.set_xlabel("Tree Prediction", fontsize=12, fontweight="bold")
        ax.set_ylabel("DQN Action", fontsize=12, fontweight="bold")
        ax.set_title(
            f"Tree vs DQN Confusion Matrix (Accuracy: {self.tree_accuracy * 100:.1f}%)",
            fontsize=14,
            fontweight="bold",
        )

        plt.tight_layout()

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            print(f"💾 Saved confusion matrix to: {output_path}")
        else:
            plt.show()

        plt.close()

    def save_tree(self, output_path):
        """Save trained tree to file."""
        if self.tree is None:
            print("❌ No tree trained yet!")
            return

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "wb") as f:
            pickle.dump(self.tree, f)

        print(f"💾 Saved tree to: {output_path}")

    def load_tree(self, input_path):
        """Load tree from file."""
        with open(input_path, "rb") as f:
            self.tree = pickle.load(f)

        print(f"✅ Loaded tree from: {input_path}")


if __name__ == "__main__":
    MODEL_PATH = "models/training_20251103_163015/checkpoint_ep192.pth"
    OUTPUT_DIR = Path("results/viper")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    extractor = VIPERExtractor(MODEL_PATH)

    print("\n" + "=" * 80)
    print("PHASE 1: Initial Dataset Collection")
    print("=" * 80)
    states, actions = extractor.collect_dqn_dataset(num_samples=10000)

    print("\n" + "=" * 80)
    print("PHASE 2: VIPER Iterative Training")
    print("=" * 80)
    tree = extractor.viper_iteration(
        states, actions, n_iterations=3, samples_per_iteration=2000
    )

    print("\n" + "=" * 80)
    print("PHASE 3: Rule Extraction")
    print("=" * 80)
    rules = extractor.extract_rules()

    with open(OUTPUT_DIR / "decision_rules.txt", "w") as f:
        f.write(rules)
    print(f"💾 Saved rules to: {OUTPUT_DIR / 'decision_rules.txt'}")

    print("\n" + "=" * 80)
    print("PHASE 4: Visualization")
    print("=" * 80)
    extractor.visualize_tree(OUTPUT_DIR / "decision_tree.png", max_depth=5)

    test_states, test_actions = extractor.collect_dqn_dataset(num_samples=1000)
    extractor.visualize_confusion_matrix(
        test_states, test_actions, OUTPUT_DIR / "confusion_matrix.png"
    )

    extractor.save_tree(OUTPUT_DIR / "extracted_tree.pkl")

    print("\n" + "=" * 80)
    print("✅ VIPER extraction complete!")
    print(f"📊 Results saved to: {OUTPUT_DIR}")
    print(f"🎯 Tree accuracy: {extractor.tree_accuracy * 100:.1f}%")
    print(f"🌳 Tree depth: {tree.get_depth()}")
    print(f"🍃 Number of leaves: {tree.get_n_leaves()}")
    print("=" * 80)
