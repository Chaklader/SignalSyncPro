"""
Master script to run all explainability and safety analyses for Paper 2.

Executes all 5 analysis scripts in sequence:
1. Saliency Analysis (Section 4.4)
2. Attention Analysis (Section 4.1)
3. Counterfactual Generation (Section 4.2)
4. VIPER Decision Tree Extraction (Section 4.3)
5. Safety Analysis (Section 5)

Total runtime: ~20 minutes
"""

import sys
from pathlib import Path
import time
import os

project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from analysis.drl.single_agent.saliency_analysis import (  # noqa: E402
    SaliencyAnalyzer,
    generate_synthetic_states,
)
from analysis.drl.single_agent.attention_analysis import (  # noqa: E402
    AttentionAnalyzer,
    generate_test_states,
)
from analysis.drl.single_agent.counterfactual_generator import (  # noqa: E402
    CounterfactualGenerator,
    generate_test_states as gen_cf_states,
)
from analysis.drl.single_agent.viper_extraction import VIPERExtractor  # noqa: E402
from analysis.drl.single_agent.safety_analysis import SafetyAnalyzer  # noqa: E402


def print_section(title):
    """Print formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def find_latest_states_file():
    """
    Find the most recent test_states_*.npz file in results directory.

    Returns:
        str: Path to states file, or None if not found
    """
    results_dir = Path("results")
    if not results_dir.exists():
        return None

    states_files = list(results_dir.glob("test_states_*.npz"))
    if not states_files:
        return None

    # Return most recent file
    latest_file = max(states_files, key=os.path.getmtime)
    return str(latest_file)


def run_all_analyses(model_path, states_file=None):
    """
    Run all explainability and safety analyses.

    Args:
        model_path: Path to trained model checkpoint
        states_file: Path to saved test states file (optional, auto-detects if None)
    """
    if states_file is None:
        states_file = find_latest_states_file()
        if states_file:
            print(f"\n🔍 Auto-detected states file: {states_file}")
        else:
            print("\n⚠️  No test states file found - will use synthetic states")
            print("   Run testing with state collection first for accurate results!")
    else:
        print(f"\n📂 Using provided states file: {states_file}")
    start_time = time.time()

    print("\n" + "=" * 80)
    print("  COMPREHENSIVE EXPLAINABILITY & SAFETY ANALYSIS")
    print("  Paper 2: Section 4 (Explainability) + Section 5 (Safety)")
    print("=" * 80)
    print(f"\nModel: {model_path}")
    print("Estimated runtime: ~20 minutes")
    print("\nStarting analysis...\n")

    try:
        print_section("ANALYSIS 1/5: Saliency Maps (Section 4.4)")
        analyzer_saliency = SaliencyAnalyzer(model_path)
        states_saliency, desc_saliency = generate_synthetic_states()
        analyzer_saliency.batch_analyze(states_saliency, desc_saliency)
        print("✅ Saliency analysis complete!")

    except Exception as e:
        print(f"❌ Saliency analysis failed: {e}")

    try:
        print_section("ANALYSIS 2/5: Attention Patterns (Section 4.1)")
        analyzer_attention = AttentionAnalyzer(model_path)
        states_attention, desc_attention = generate_test_states()
        analyzer_attention.batch_analyze(states_attention, desc_attention)
        print("✅ Attention analysis complete!")

    except Exception as e:
        print(f"❌ Attention analysis failed: {e}")

    try:
        print_section("ANALYSIS 3/5: Counterfactual Explanations (Section 4.2)")
        generator = CounterfactualGenerator(model_path)
        states_cf, desc_cf = gen_cf_states()
        generator.batch_generate(states_cf, desc_cf)
        print("✅ Counterfactual generation complete!")

    except Exception as e:
        print(f"❌ Counterfactual generation failed: {e}")

    try:
        print_section("ANALYSIS 4/5: Decision Tree Extraction (Section 4.3)")
        print("Note: This analysis takes ~10 minutes")

        extractor = VIPERExtractor(model_path)

        print("\n[Phase 1/4] Collecting initial dataset...")
        states_viper, actions_viper = extractor.collect_dqn_dataset(
            num_samples=None if states_file else 10000, states_file=states_file
        )

        print("\n[Phase 2/4] Running VIPER iterations...")
        tree = extractor.viper_iteration(
            states_viper, actions_viper, n_iterations=3, samples_per_iteration=2000
        )

        print("\n[Phase 3/4] Extracting decision rules...")
        rules = extractor.extract_rules()

        output_dir = Path("images/2/viper")
        output_dir.mkdir(parents=True, exist_ok=True)

        with open(output_dir / "decision_rules.txt", "w") as f:
            f.write(rules)

        print("\n[Phase 4/4] Creating visualizations...")
        extractor.visualize_tree(output_dir / "decision_tree.png", max_depth=5)

        test_states_viper, test_actions_viper = extractor.collect_dqn_dataset(
            num_samples=10000, states_file=states_file
        )
        extractor.visualize_confusion_matrix(
            test_states_viper, test_actions_viper, output_dir / "confusion_matrix.png"
        )

        extractor.save_tree(output_dir / "extracted_tree.pkl")

        print("✅ VIPER extraction complete!")
        print(f"   Tree accuracy: {extractor.tree_accuracy * 100:.1f}%")
        print(f"   Tree depth: {tree.get_depth()}")
        print(f"   Number of leaves: {tree.get_n_leaves()}")

    except Exception as e:
        print(f"❌ VIPER extraction failed: {e}")

    try:
        print_section("ANALYSIS 5/5: Safety Analysis (Section 5)")

        analyzer_safety = SafetyAnalyzer()

        print("[Phase 1/5] Operational safety metrics...")
        analyzer_safety.analyze_operational_safety()

        print("\n[Phase 2/5] Edge case identification...")
        analyzer_safety.identify_edge_cases()

        print("\n[Phase 3/5] Decision pattern analysis...")
        analyzer_safety.analyze_decision_patterns()

        print("\n[Phase 4/5] Safe region characterization...")
        analyzer_safety.characterize_safe_regions()

        print("\n[Phase 5/5] Generating visualizations and report...")
        analyzer_safety.visualize_safety_metrics()
        analyzer_safety.generate_safety_report()

        print("✅ Safety analysis complete!")

    except Exception as e:
        print(f"❌ Safety analysis failed: {e}")

    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)

    print("\n" + "=" * 80)
    print("  ANALYSIS COMPLETE!")
    print("=" * 80)
    print(f"\n⏱️  Total runtime: {minutes}m {seconds}s")
    print("\n📊 Results saved to:")
    print("   - images/2/saliency/")
    print("   - images/2/attention/")
    print("   - images/2/counterfactuals/")
    print("   - images/2/viper/")
    print("   - images/2/safety/")
    print("\n📝 Key files for Paper 2:")
    print("   Section 4.1: images/2/attention/*.png")
    print("   Section 4.2: images/2/counterfactuals/*.png")
    print("   Section 4.3: images/2/viper/decision_tree.png, decision_rules.txt")
    print("   Section 4.4: images/2/saliency/*.png")
    print("   Section 5:   images/2/safety/safety_report.txt, *.png")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Run all explainability and safety analyses"
    )
    parser.add_argument(
        "model_path", type=str, help="Path to trained model checkpoint (.pth file)"
    )
    parser.add_argument(
        "--states-file",
        type=str,
        default=None,
        help="Path to test states file (.npz). If not provided, auto-detects latest file.",
    )
    args = parser.parse_args()

    model_path = args.model_path

    if not Path(model_path).exists():
        print(f"❌ Model not found: {model_path}")
        print("Please provide a valid path to the model checkpoint.")
        sys.exit(1)

    run_all_analyses(model_path, states_file=args.states_file)
