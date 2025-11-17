"""
Bicycle Wait Time Spike Analysis

Analyzes why bicycle wait times spike in Bi_6, Bi_7, Bi_8, Bi_9 scenarios
by comparing them with good-performing bicycle scenarios (Bi_0-5).

Investigates:
1. Decision patterns (Continue/Skip2P1/Next usage)
2. Phase duration distributions
3. Detector activation patterns
4. Q-value characteristics
5. Blocking event frequency
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import glob

ACTION_NAMES = ["Continue", "Skip2P1", "Next"]

GOOD_SCENARIOS = ["Bi_0", "Bi_1", "Bi_2", "Bi_3", "Bi_4", "Bi_5"]
BAD_SCENARIOS = ["Bi_6", "Bi_7", "Bi_8", "Bi_9"]


class BicycleSpikeAnalyzer:
    """Analyze bicycle wait time spikes in problematic scenarios."""

    def __init__(
        self,
        states_file,
        test_results_csv,
        qvalue_csv,
        blocking_csv,
        output_dir,
    ):
        self.states = None
        self.actions = None
        self.scenarios = None
        self.test_results = None
        self.qvalue_data = None
        self.blocking_data = None
        self.output_dir = output_dir
        self.states_file = states_file
        self.test_results_csv = test_results_csv
        self.qvalue_csv = qvalue_csv
        self.blocking_csv = blocking_csv

    def load_data(self):
        """Load all necessary data."""
        print("\n📂 Loading data...")

        if not self.states_file:
            raise ValueError("states_file is required")

        data = np.load(self.states_file)
        self.states = data["states"]
        self.actions = data["actions"]
        self.scenarios = data["scenarios"]
        print(f"   ✅ States: {len(self.states):,} samples (from {self.states_file})")

        test_files = glob.glob(self.test_results_csv)
        if not test_files:
            raise FileNotFoundError(
                f"No test results CSV found: {self.test_results_csv}"
            )
        latest_test_file = sorted(test_files)[-1]
        self.test_results = pd.read_csv(latest_test_file)
        print(
            f"   ✅ Test results: {len(self.test_results)} scenarios (from {latest_test_file})"
        )

        self.qvalue_data = pd.read_csv(self.qvalue_csv)
        print(f"   ✅ Q-values: {len(self.qvalue_data):,} records")

        self.blocking_data = pd.read_csv(self.blocking_csv)
        print(f"   ✅ Blocking events: {len(self.blocking_data):,} records")

    def filter_scenarios(self, scenario_list):
        """Filter states by scenario list."""
        mask = np.isin(self.scenarios, scenario_list)
        return self.states[mask], self.actions[mask], self.scenarios[mask]

    def analyze_action_distribution(self):
        """Compare action distributions between good and bad scenarios."""
        print("\n" + "=" * 80)
        print("ACTION DISTRIBUTION ANALYSIS")
        print("=" * 80)

        results = {}

        for group_name, scenario_list in [
            ("Good (Bi_0-5)", GOOD_SCENARIOS),
            ("Bad (Bi_6-9)", BAD_SCENARIOS),
        ]:
            _, actions, _ = self.filter_scenarios(scenario_list)

            distribution = {}
            for action_idx, action_name in enumerate(ACTION_NAMES):
                count = np.sum(actions == action_idx)
                pct = count / len(actions) * 100
                distribution[action_name] = {"count": count, "percent": pct}

            results[group_name] = distribution

            print(f"\n{group_name}:")
            for action_name, stats in distribution.items():
                print(
                    f"   {action_name:10s}: {stats['count']:6d} ({stats['percent']:5.1f}%)"
                )

        # Visualization
        fig, ax = plt.subplots(figsize=(10, 6))

        groups = list(results.keys())
        x = np.arange(len(ACTION_NAMES))
        width = 0.35

        for i, group in enumerate(groups):
            percentages = [results[group][action]["percent"] for action in ACTION_NAMES]
            ax.bar(x + i * width, percentages, width, label=group, alpha=0.8)

        ax.set_xlabel("Action", fontsize=12, fontweight="bold")
        ax.set_ylabel("Percentage (%)", fontsize=12, fontweight="bold")
        ax.set_title(
            "Action Distribution: Good vs Bad Bicycle Scenarios",
            fontsize=14,
            fontweight="bold",
        )
        ax.set_xticks(x + width / 2)
        ax.set_xticklabels(ACTION_NAMES)
        ax.legend()
        ax.grid(axis="y", alpha=0.3)

        output_path = Path(self.output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        plt.savefig(
            output_path / "action_distribution.png", dpi=300, bbox_inches="tight"
        )
        plt.close()

        print(f"\n   💾 Saved: {output_path / 'action_distribution.png'}")

        return results

    def analyze_phase_durations(self):
        """Analyze phase duration patterns."""
        print("\n" + "=" * 80)
        print("PHASE DURATION ANALYSIS")
        print("=" * 80)

        # Phase duration is at index 4 (TLS3) and 20 (TLS6)
        duration_indices = [4, 20]

        results = {}

        for group_name, scenario_list in [
            ("Good (Bi_0-5)", GOOD_SCENARIOS),
            ("Bad (Bi_6-9)", BAD_SCENARIOS),
        ]:
            states, _, _ = self.filter_scenarios(scenario_list)

            # Get phase durations (normalized 0-1, multiply by MAX_GREEN=60 for actual)
            tls3_durations = states[:, duration_indices[0]] * 60
            tls6_durations = states[:, duration_indices[1]] * 60

            results[group_name] = {
                "TLS3_mean": np.mean(tls3_durations),
                "TLS3_std": np.std(tls3_durations),
                "TLS3_max": np.max(tls3_durations),
                "TLS6_mean": np.mean(tls6_durations),
                "TLS6_std": np.std(tls6_durations),
                "TLS6_max": np.max(tls6_durations),
            }

            print(f"\n{group_name}:")
            print(
                f"   TLS3 Duration: {results[group_name]['TLS3_mean']:.1f}s ± "
                f"{results[group_name]['TLS3_std']:.1f}s (max: {results[group_name]['TLS3_max']:.1f}s)"
            )
            print(
                f"   TLS6 Duration: {results[group_name]['TLS6_mean']:.1f}s ± "
                f"{results[group_name]['TLS6_std']:.1f}s (max: {results[group_name]['TLS6_max']:.1f}s)"
            )

        # Visualization
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        for tls_idx, (tls_name, dur_idx) in enumerate(
            [("TLS3", duration_indices[0]), ("TLS6", duration_indices[1])]
        ):
            good_states, _, _ = self.filter_scenarios(GOOD_SCENARIOS)
            bad_states, _, _ = self.filter_scenarios(BAD_SCENARIOS)

            good_dur = good_states[:, dur_idx] * 60
            bad_dur = bad_states[:, dur_idx] * 60

            axes[tls_idx].hist(
                good_dur, bins=30, alpha=0.6, label="Good (Bi_0-5)", color="#27ae60"
            )
            axes[tls_idx].hist(
                bad_dur, bins=30, alpha=0.6, label="Bad (Bi_6-9)", color="#e74c3c"
            )

            axes[tls_idx].set_xlabel("Phase Duration (seconds)", fontsize=11)
            axes[tls_idx].set_ylabel("Frequency", fontsize=11)
            axes[tls_idx].set_title(
                f"{tls_name} Phase Duration Distribution",
                fontsize=12,
                fontweight="bold",
            )
            axes[tls_idx].legend()
            axes[tls_idx].grid(axis="y", alpha=0.3)

        plt.tight_layout()
        output_path = Path(self.output_dir)
        plt.savefig(output_path / "phase_durations.png", dpi=300, bbox_inches="tight")
        plt.close()

        print(f"\n   💾 Saved: {output_path / 'phase_durations.png'}")

        return results

    def analyze_detector_patterns(self):
        """Analyze bicycle detector activation patterns."""
        print("\n" + "=" * 80)
        print("BICYCLE DETECTOR ANALYSIS")
        print("=" * 80)

        # Bicycle detector indices: TLS3 [9-12], TLS6 [25-28]
        bike_detector_indices = {
            "TLS3_Bike1": 9,
            "TLS3_Bike2": 10,
            "TLS3_Bike3": 11,
            "TLS3_Bike4": 12,
            "TLS6_Bike1": 25,
            "TLS6_Bike2": 26,
            "TLS6_Bike3": 27,
            "TLS6_Bike4": 28,
        }

        results = {}

        for group_name, scenario_list in [
            ("Good", GOOD_SCENARIOS),
            ("Bad", BAD_SCENARIOS),
        ]:
            states, _, _ = self.filter_scenarios(scenario_list)

            detector_stats = {}
            for name, idx in bike_detector_indices.items():
                activation_rate = np.mean(states[:, idx] > 0.5) * 100
                avg_value = np.mean(states[:, idx])
                detector_stats[name] = {
                    "activation_rate": activation_rate,
                    "avg_value": avg_value,
                }

            results[group_name] = detector_stats

            print(f"\n{group_name} Scenarios:")
            for name, stats in detector_stats.items():
                print(
                    f"   {name}: Activation {stats['activation_rate']:.1f}%, "
                    f"Avg {stats['avg_value']:.3f}"
                )

        # Visualization
        fig, ax = plt.subplots(figsize=(12, 6))

        detector_names = list(bike_detector_indices.keys())
        x = np.arange(len(detector_names))
        width = 0.35

        good_rates = [
            results["Good"][name]["activation_rate"] for name in detector_names
        ]
        bad_rates = [results["Bad"][name]["activation_rate"] for name in detector_names]

        ax.bar(
            x - width / 2,
            good_rates,
            width,
            label="Good (Bi_0-5)",
            color="#27ae60",
            alpha=0.8,
        )
        ax.bar(
            x + width / 2,
            bad_rates,
            width,
            label="Bad (Bi_6-9)",
            color="#e74c3c",
            alpha=0.8,
        )

        ax.set_xlabel("Bicycle Detector", fontsize=12, fontweight="bold")
        ax.set_ylabel("Activation Rate (%)", fontsize=12, fontweight="bold")
        ax.set_title(
            "Bicycle Detector Activation: Good vs Bad Scenarios",
            fontsize=14,
            fontweight="bold",
        )
        ax.set_xticks(x)
        ax.set_xticklabels(detector_names, rotation=45, ha="right")
        ax.legend()
        ax.grid(axis="y", alpha=0.3)

        plt.tight_layout()
        output_path = Path(self.output_dir)
        plt.savefig(output_path / "bicycle_detectors.png", dpi=300, bbox_inches="tight")
        plt.close()

        print(f"\n   💾 Saved: {output_path / 'bicycle_detectors.png'}")

        return results

    def analyze_qvalues(self):
        """Analyze Q-value patterns."""
        print("\n" + "=" * 80)
        print("Q-VALUE ANALYSIS")
        print("=" * 80)

        results = {}

        for group_name, scenario_list in [
            ("Good", GOOD_SCENARIOS),
            ("Bad", BAD_SCENARIOS),
        ]:
            group_data = self.qvalue_data[
                self.qvalue_data["scenario"].isin(scenario_list)
            ]

            q_stats = {
                "continue_mean": group_data["continue_q"].mean(),
                "skip2p1_mean": group_data["skip2p1_q"].mean(),
                "next_mean": group_data["next_q"].mean(),
                "q_gap_mean": group_data["q_gap"].mean(),
                "q_gap_std": group_data["q_gap"].std(),
            }

            results[group_name] = q_stats

            print(f"\n{group_name} Scenarios:")
            print(f"   Continue Q: {q_stats['continue_mean']:.3f}")
            print(f"   Skip2P1 Q:  {q_stats['skip2p1_mean']:.3f}")
            print(f"   Next Q:     {q_stats['next_mean']:.3f}")
            print(
                f"   Q-Gap:      {q_stats['q_gap_mean']:.3f} ± {q_stats['q_gap_std']:.3f}"
            )

        # Visualization
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Q-values comparison
        actions = ["Continue", "Skip2P1", "Next"]
        good_q = [
            results["Good"]["continue_mean"],
            results["Good"]["skip2p1_mean"],
            results["Good"]["next_mean"],
        ]
        bad_q = [
            results["Bad"]["continue_mean"],
            results["Bad"]["skip2p1_mean"],
            results["Bad"]["next_mean"],
        ]

        x = np.arange(len(actions))
        width = 0.35

        axes[0].bar(
            x - width / 2,
            good_q,
            width,
            label="Good (Bi_0-5)",
            color="#27ae60",
            alpha=0.8,
        )
        axes[0].bar(
            x + width / 2,
            bad_q,
            width,
            label="Bad (Bi_6-9)",
            color="#e74c3c",
            alpha=0.8,
        )
        axes[0].set_xlabel("Action", fontsize=11, fontweight="bold")
        axes[0].set_ylabel("Mean Q-Value", fontsize=11, fontweight="bold")
        axes[0].set_title("Mean Q-Values Comparison", fontsize=12, fontweight="bold")
        axes[0].set_xticks(x)
        axes[0].set_xticklabels(actions)
        axes[0].legend()
        axes[0].grid(axis="y", alpha=0.3)
        axes[0].axhline(y=0, color="black", linestyle="-", linewidth=0.8)

        # Q-gap distributions
        good_gaps = self.qvalue_data[self.qvalue_data["scenario"].isin(GOOD_SCENARIOS)][
            "q_gap"
        ]
        bad_gaps = self.qvalue_data[self.qvalue_data["scenario"].isin(BAD_SCENARIOS)][
            "q_gap"
        ]

        axes[1].hist(
            good_gaps, bins=30, alpha=0.6, label="Good (Bi_0-5)", color="#27ae60"
        )
        axes[1].hist(
            bad_gaps, bins=30, alpha=0.6, label="Bad (Bi_6-9)", color="#e74c3c"
        )
        axes[1].set_xlabel("Q-Gap", fontsize=11, fontweight="bold")
        axes[1].set_ylabel("Frequency", fontsize=11, fontweight="bold")
        axes[1].set_title("Q-Gap Distribution", fontsize=12, fontweight="bold")
        axes[1].legend()
        axes[1].grid(axis="y", alpha=0.3)

        plt.tight_layout()
        output_path = Path(self.output_dir)
        plt.savefig(output_path / "qvalue_analysis.png", dpi=300, bbox_inches="tight")
        plt.close()

        print(f"\n   💾 Saved: {output_path / 'qvalue_analysis.png'}")

        return results

    def analyze_blocking_events(self):
        """Analyze blocking event frequency."""
        print("\n" + "=" * 80)
        print("BLOCKING EVENTS ANALYSIS")
        print("=" * 80)

        results = {}

        for group_name, scenario_list in [
            ("Good", GOOD_SCENARIOS),
            ("Bad", BAD_SCENARIOS),
        ]:
            group_data = self.blocking_data[
                self.blocking_data["scenario"].isin(scenario_list)
            ]

            total_blocks = group_data["blocked_count"].sum()
            blocks_per_scenario = total_blocks / len(scenario_list)

            action_blocks = group_data.groupby("action")["blocked_count"].sum()

            results[group_name] = {
                "total_blocks": total_blocks,
                "blocks_per_scenario": blocks_per_scenario,
                "action_blocks": action_blocks.to_dict(),
            }

            print(f"\n{group_name} Scenarios:")
            print(f"   Total blocks: {total_blocks}")
            print(f"   Blocks per scenario: {blocks_per_scenario:.1f}")
            print("   Blocks by action:")
            for action, count in action_blocks.items():
                print(f"      {action}: {count}")

        # Visualization
        fig, ax = plt.subplots(figsize=(10, 6))

        groups = ["Good (Bi_0-5)", "Bad (Bi_6-9)"]
        blocks = [
            results["Good"]["blocks_per_scenario"],
            results["Bad"]["blocks_per_scenario"],
        ]
        colors = ["#27ae60", "#e74c3c"]

        ax.bar(groups, blocks, color=colors, alpha=0.8)
        ax.set_ylabel("Blocks per Scenario", fontsize=12, fontweight="bold")
        ax.set_title(
            "Blocking Events: Good vs Bad Bicycle Scenarios",
            fontsize=14,
            fontweight="bold",
        )
        ax.grid(axis="y", alpha=0.3)

        # Annotate values
        for i, (group, value) in enumerate(zip(groups, blocks)):
            ax.text(
                i,
                value,
                f"{value:.1f}",
                ha="center",
                va="bottom",
                fontsize=12,
                fontweight="bold",
            )

        plt.tight_layout()
        output_path = Path(self.output_dir)
        plt.savefig(output_path / "blocking_events.png", dpi=300, bbox_inches="tight")
        plt.close()

        print(f"\n   💾 Saved: {output_path / 'blocking_events.png'}")

        return results

    def generate_summary_report(self, all_results):
        """Generate comprehensive summary report."""
        print("\n" + "=" * 80)
        print("GENERATING SUMMARY REPORT")
        print("=" * 80)

        output_path = Path(self.output_dir)
        report_path = output_path / "bicycle_spike_analysis_report.txt"

        with open(report_path, "w") as f:
            f.write("=" * 80 + "\n")
            f.write("BICYCLE WAIT TIME SPIKE ANALYSIS REPORT\n")
            f.write("Why do Bi_6, Bi_7, Bi_8, Bi_9 have high bicycle wait times?\n")
            f.write("=" * 80 + "\n\n")

            # Test results comparison
            f.write("1. WAIT TIME COMPARISON\n")
            f.write("-" * 80 + "\n")
            good_scenarios_data = self.test_results[
                self.test_results["scenario"].isin(GOOD_SCENARIOS)
            ]
            bad_scenarios_data = self.test_results[
                self.test_results["scenario"].isin(BAD_SCENARIOS)
            ]

            f.write("Good Scenarios (Bi_0-5):\n")
            f.write(
                f"   Bicycle wait: {good_scenarios_data['avg_waiting_time_bicycle'].mean():.2f}s ± "
                f"{good_scenarios_data['avg_waiting_time_bicycle'].std():.2f}s\n"
            )
            f.write("Bad Scenarios (Bi_6-9):\n")
            f.write(
                f"   Bicycle wait: {bad_scenarios_data['avg_waiting_time_bicycle'].mean():.2f}s ± "
                f"{bad_scenarios_data['avg_waiting_time_bicycle'].std():.2f}s\n\n"
            )

            # Key findings
            f.write("2. KEY FINDINGS\n")
            f.write("-" * 80 + "\n\n")

            # Action distribution
            action_results = all_results["actions"]
            f.write("A. Action Distribution:\n")
            for action in ACTION_NAMES:
                good_pct = action_results["Good (Bi_0-5)"][action]["percent"]
                bad_pct = action_results["Bad (Bi_6-9)"][action]["percent"]
                diff = bad_pct - good_pct
                f.write(
                    f"   {action:10s}: Good {good_pct:5.1f}% vs Bad {bad_pct:5.1f}% (Δ {diff:+5.1f}%)\n"
                )

            f.write("\n")

            # Phase durations
            duration_results = all_results["durations"]
            f.write("B. Phase Durations:\n")
            f.write(
                f"   TLS3: Good {duration_results['Good (Bi_0-5)']['TLS3_mean']:.1f}s vs "
                f"Bad {duration_results['Bad (Bi_6-9)']['TLS3_mean']:.1f}s\n"
            )
            f.write(
                f"   TLS6: Good {duration_results['Good (Bi_0-5)']['TLS6_mean']:.1f}s vs "
                f"Bad {duration_results['Bad (Bi_6-9)']['TLS6_mean']:.1f}s\n\n"
            )

            # Q-values
            qvalue_results = all_results["qvalues"]
            f.write("C. Q-Values:\n")
            f.write(
                f"   Continue: Good {qvalue_results['Good']['continue_mean']:.3f} vs "
                f"Bad {qvalue_results['Bad']['continue_mean']:.3f}\n"
            )
            f.write(
                f"   Q-Gap:    Good {qvalue_results['Good']['q_gap_mean']:.3f} vs "
                f"Bad {qvalue_results['Bad']['q_gap_mean']:.3f}\n\n"
            )

            # Blocking
            blocking_results = all_results["blocking"]
            f.write("D. Blocking Events:\n")
            f.write(
                f"   Good: {blocking_results['Good']['blocks_per_scenario']:.1f} blocks/scenario\n"
            )
            f.write(
                f"   Bad:  {blocking_results['Bad']['blocks_per_scenario']:.1f} blocks/scenario\n\n"
            )

            # Conclusions
            f.write("3. CONCLUSIONS\n")
            f.write("-" * 80 + "\n")
            f.write(
                "Based on the analysis, the high bicycle wait times in Bi_6-9 scenarios are\n"
            )
            f.write("likely caused by:\n\n")

            # Determine root causes
            conclusions = []

            # Check Continue usage
            good_continue = action_results["Good (Bi_0-5)"]["Continue"]["percent"]
            bad_continue = action_results["Bad (Bi_6-9)"]["Continue"]["percent"]
            if bad_continue > good_continue + 5:
                conclusions.append(
                    f"   • EXCESSIVE CONTINUE: {bad_continue:.1f}% vs {good_continue:.1f}% in good scenarios\n"
                    "     → Agent stays in current phase too long, ignoring bicycle demand\n"
                )

            # Check Next usage
            good_next = action_results["Good (Bi_0-5)"]["Next"]["percent"]
            bad_next = action_results["Bad (Bi_6-9)"]["Next"]["percent"]
            if bad_next < good_next - 5:
                conclusions.append(
                    f"   • LOW NEXT USAGE: {bad_next:.1f}% vs {good_next:.1f}% in good scenarios\n"
                    "     → Insufficient phase cycling to reach bicycle phases\n"
                )

            # Check blocking
            if (
                blocking_results["Bad"]["blocks_per_scenario"]
                > blocking_results["Good"]["blocks_per_scenario"] * 1.5
            ):
                conclusions.append(
                    f"   • HIGH BLOCKING: {blocking_results['Bad']['blocks_per_scenario']:.1f} vs "
                    f"{blocking_results['Good']['blocks_per_scenario']:.1f} blocks/scenario\n"
                    "     → Actions frequently blocked, limiting adaptability\n"
                )

            # Check bicycle detector activation (CRITICAL)
            detector_names = [
                "TLS3_Bike1",
                "TLS3_Bike2",
                "TLS3_Bike3",
                "TLS3_Bike4",
                "TLS6_Bike1",
                "TLS6_Bike2",
                "TLS6_Bike3",
                "TLS6_Bike4",
            ]
            good_avg_activation = sum(
                all_results["detectors"]["Good"][name]["activation_rate"]
                for name in detector_names
            ) / len(detector_names)
            bad_avg_activation = sum(
                all_results["detectors"]["Bad"][name]["activation_rate"]
                for name in detector_names
            ) / len(detector_names)

            if bad_avg_activation > good_avg_activation * 2.0:
                conclusions.append(
                    f"   • HIGH BICYCLE DEMAND: {bad_avg_activation:.1f}% vs {good_avg_activation:.1f}% detector activation\n"
                    f"     → Scenarios have {bad_avg_activation / good_avg_activation:.1f}x more bicycles detected\n"
                    "     → This is a traffic scenario characteristic, not an agent failure\n"
                )

            if conclusions:
                for conclusion in conclusions:
                    f.write(conclusion + "\n")
            else:
                f.write("   • Analysis inconclusive - further investigation needed\n\n")

            f.write("\n" + "=" * 80 + "\n")

        print(f"   💾 Saved report: {report_path}")


def main():
    """Main analysis pipeline."""
    print("\n" + "=" * 80)
    print("BICYCLE WAIT TIME SPIKE ANALYSIS")
    print("Comparing Bi_0-5 (Good) vs Bi_6-9 (Bad)")
    print("=" * 80)

    analyzer = BicycleSpikeAnalyzer(
        states_file="results/test_states_20251115_202404.npz",
        test_results_csv="results/drl_test_results_*.csv",
        qvalue_csv="output/testing/testing_data_1.csv",
        blocking_csv="output/testing/testing_data_2.csv",
    )

    analyzer.load_data()

    print("\n[Phase 1/5] Analyzing action distribution...")
    action_results = analyzer.analyze_action_distribution()

    print("\n[Phase 2/5] Analyzing phase durations...")
    duration_results = analyzer.analyze_phase_durations()

    print("\n[Phase 3/5] Analyzing detector patterns...")
    detector_results = analyzer.analyze_detector_patterns()

    print("\n[Phase 4/5] Analyzing Q-values...")
    qvalue_results = analyzer.analyze_qvalues()

    print("\n[Phase 5/5] Analyzing blocking events...")
    blocking_results = analyzer.analyze_blocking_events()

    print("\n[Generating Summary Report...]")
    all_results = {
        "actions": action_results,
        "durations": duration_results,
        "detectors": detector_results,
        "qvalues": qvalue_results,
        "blocking": blocking_results,
    }
    analyzer.generate_summary_report(all_results)

    print("\n" + "=" * 80)
    print("Analysis complete!")
    print(f"Results saved to: {analyzer.output_dir}")
    print("=" * 80)


if __name__ == "__main__":
    main()
