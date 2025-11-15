#!/usr/bin/env python3
"""
Verification script to ensure state collection is working correctly
before running the full 1-day testing.

Runs a quick test with 1 scenario to verify:
1. States are collected during testing
2. States are saved to file correctly
3. VIPER can load and use the states
4. Action distribution looks correct

Run this BEFORE the full 30-scenario testing!
"""

import sys
import os
from pathlib import Path
import numpy as np

project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from run.testing import test_drl  # noqa: E402
from analysis.drl.single_agent.viper_extraction import VIPERExtractor  # noqa: E402


def print_section(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def verify_state_collection():
    """Run verification tests."""

    print_section("STATE COLLECTION VERIFICATION")
    print("This script verifies state collection is working correctly.")
    print("Estimated time: 5-10 minutes (1 test scenario)")
    print("\nPress Ctrl+C to cancel, or wait 5 seconds to continue...")

    import time

    try:
        time.sleep(5)
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(0)

    print_section("TEST 1: Running Pr_0 Scenario with State Collection")

    model_path = "models/training_20251103_163015/checkpoint_ep192.pth"

    if not Path(model_path).exists():
        print(f"❌ Model not found: {model_path}")
        print(
            "\nPlease update the model_path in this script to point to your trained model."
        )
        return False

    scenarios = {"Pr": [0]}

    print(f"Running test with model: {model_path}")
    print("Scenario: Pr_0 (low car traffic)\n")

    try:
        test_drl.test_drl_agent(model_path, scenarios=scenarios)
    except Exception as e:
        print(f"\n❌ Testing failed: {e}")
        return False

    print_section("TEST 2: Verifying States File Created")

    results_dir = Path("results")
    states_files = list(results_dir.glob("test_states_*.npz"))

    if not states_files:
        print("❌ No test_states_*.npz file found in results/")
        print("\nLikely causes:")
        print("  1. save_states_for_analysis=False in TestLogger")
        print("  2. logger.save_collected_states() not called")
        return False

    latest_states_file = max(states_files, key=os.path.getmtime)
    print(f"✅ States file found: {latest_states_file}")

    file_size_mb = latest_states_file.stat().st_size / (1024 * 1024)
    print(f"   File size: {file_size_mb:.2f} MB")

    print_section("TEST 3: Verifying File Contents")

    try:
        data = np.load(latest_states_file)

        required_keys = ["states", "actions", "scenarios"]
        for key in required_keys:
            if key not in data:
                print(f"❌ Missing key '{key}' in states file")
                return False

        states = data["states"]
        actions = data["actions"]
        scenarios = data["scenarios"]

        print("✅ File structure correct")
        print(f"   Keys: {list(data.keys())}")
        print(f"\n   States shape: {states.shape}")
        print(f"   Actions shape: {actions.shape}")
        print(f"   Scenarios: {np.unique(scenarios)}")

        expected_min = 9900
        expected_max = 10100

        if len(states) < expected_min:
            print(f"\n⚠️  Warning: Only {len(states)} states collected")
            print(f"   Expected: {expected_min}-{expected_max} for 1 scenario")
            print("   Sampling may not be working correctly")
        elif len(states) > expected_max:
            print(f"\n⚠️  Warning: {len(states)} states collected")
            print(f"   Expected: {expected_min}-{expected_max} for 1 scenario")
            print("   May be sampling too frequently")
        else:
            print(f"\n✅ State count looks good: {len(states)} states")

        if states.shape[1] != 32:
            print(f"\n❌ Incorrect state dimension: {states.shape[1]} (expected 32)")
            return False

        print("✅ State dimension correct: 32 features")

        unique_actions, counts = np.unique(actions, return_counts=True)
        action_names = {0: "Continue", 1: "Skip2P1", 2: "Next"}

        print("\n   Action distribution:")
        for action_id, count in zip(unique_actions, counts):
            percentage = (count / len(actions)) * 100
            name = action_names.get(action_id, f"Action_{action_id}")
            print(f"     {name:10s}: {count:4d} ({percentage:5.1f}%)")

        continue_pct = (
            counts[unique_actions == 0][0] / len(actions) * 100
            if 0 in unique_actions
            else 0
        )

        if continue_pct < 60:
            print(f"\n⚠️  Warning: Continue action only {continue_pct:.1f}%")
            print("   Expected: >60% for low-traffic scenario (Pr_0)")
        else:
            print("\n✅ Action distribution looks reasonable")

    except Exception as e:
        print(f"❌ Error reading states file: {e}")
        return False

    print_section("TEST 4: Verifying VIPER Can Load States")

    try:
        extractor = VIPERExtractor(model_path)

        print("Loading states into VIPER...")
        loaded_states, loaded_actions = extractor.collect_dqn_dataset(
            num_samples=None, states_file=str(latest_states_file)
        )

        print("\n✅ VIPER successfully loaded states")
        print(f"   Loaded: {len(loaded_states)} states")
        print(
            f"   Action distribution matches file: {np.array_equal(loaded_actions, actions)}"
        )

    except Exception as e:
        print(f"❌ VIPER failed to load states: {e}")
        import traceback

        traceback.print_exc()
        return False

    print_section("VERIFICATION SUMMARY")

    print("✅ All tests passed!")
    print("\n📋 Verification checklist:")
    print("   ✅ State collection enabled in testing")
    print("   ✅ States saved to file correctly")
    print("   ✅ File structure and contents valid")
    print("   ✅ VIPER can load and use states")
    print("   ✅ Action distribution looks reasonable")

    print("\n" + "=" * 70)
    print("  READY FOR FULL 30-SCENARIO TESTING!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Run full testing (1 day):")
    print(f"   python run/testing/test_drl.py --model {model_path}")
    print("\n2. After testing completes, run analysis:")
    print("   bash scripts/drl/single_agent/analyze/run_all_analysis.sh")
    print("\n3. Analysis will automatically use the collected states")

    print(f"\n\n💾 Verification states file: {latest_states_file}")
    print("   You can delete this file or keep it for reference.")
    print("   (The full testing will create a new, larger states file)")

    return True


if __name__ == "__main__":
    success = verify_state_collection()
    sys.exit(0 if success else 1)
