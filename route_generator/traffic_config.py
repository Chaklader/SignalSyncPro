"""
Traffic configuration for training and testing scenarios.

Provides traffic volume configurations for:
- Training: Random volumes (100-1000 vehicles/hour)
- Testing: 30 predefined scenarios (Pr_0-9, Bi_0-9, Pe_0-9)

Usage:
    from traffic_config import get_traffic_config

    # Training: random volumes
    config = get_traffic_config()

    # Testing: specific scenario
    config = get_traffic_config(scenario='Pr_5')
"""

import random


# ============================================================================
# Test Scenarios (30 scenarios for consistent evaluation)
# ============================================================================

BUS_INTERVAL = "every_15min"


def _generate_test_scenarios(lower, higher, control):
    """
    Generate 30 test scenarios programmatically.

    Args:
        lower: Minimum volume for varying mode (e.g., 100 for 2-intersection)
        higher: Maximum volume for varying mode (e.g., 1000 for 2-intersection)
        control: Control value for non-varying modes (e.g., 400 for 2-intersection)

    Returns:
        dict: 30 scenarios (Pr_0-9, Bi_0-9, Pe_0-9)
    """
    scenarios = {}
    step = (higher - lower) // 9

    for i in range(10):
        volume = lower + i * step
        scenarios[f"Pr_{i}"] = {
            "cars": volume,
            "bicycles": control,
            "pedestrians": control,
            "buses": BUS_INTERVAL,
        }
        scenarios[f"Bi_{i}"] = {
            "cars": control,
            "bicycles": volume,
            "pedestrians": control,
            "buses": BUS_INTERVAL,
        }
        scenarios[f"Pe_{i}"] = {
            "cars": control,
            "bicycles": control,
            "pedestrians": volume,
            "buses": BUS_INTERVAL,
        }

    return scenarios


TEST_SCENARIOS_TWO_INTERSECTIONS = _generate_test_scenarios(
    lower=100, higher=1000, control=400
)

TEST_SCENARIOS_FIVE_INTERSECTIONS = _generate_test_scenarios(
    lower=250, higher=2500, control=1000
)


# ============================================================================
# Traffic Configuration Functions
# ============================================================================


def get_traffic_config(scenario=None):
    """
    Get traffic configuration for training or testing.

    If scenario is None:
        Returns random traffic volumes for diverse learning:
        - Cars: 100-1000 per hour
        - Bicycles: 100-1000 per hour
        - Pedestrians: 100-1000 per hour
        - Buses: Every 15 minutes (constant)

    If scenario is specified:
        Returns predefined scenario configuration:
        - Must specify scenario name (e.g., 'Pr_5', 'Bi_3', 'Pe_7')
        - 30 scenarios total (Pr_0-9, Bi_0-9, Pe_0-9)

    Args:
        scenario (str, optional): Scenario name for specific test scenario
            Examples: 'Pr_0', 'Bi_5', 'Pe_9'
            If None, returns random traffic

    Returns:
        dict: Traffic configuration with keys:
            - 'cars': Cars per hour (int)
            - 'bicycles': Bicycles per hour (int)
            - 'pedestrians': Pedestrians per hour (int)
            - 'buses': Bus frequency (str: 'every_15min')
            - 'scenario_name': Scenario identifier (str)

    Examples:
        # Random volumes for training
        config = get_traffic_config()
        # {'cars': 573, 'bicycles': 821, 'pedestrians': 234,
        #  'buses': 'every_15min', 'scenario_name': 'training_random'}

        # Specific test scenario
        config = get_traffic_config(scenario='Pr_5')
        # {'cars': 600, 'bicycles': 400, 'pedestrians': 400,
        #  'buses': 'every_15min', 'scenario_name': 'Pr_5'}
    """
    if scenario is None:
        # Random traffic volumes for diverse learning
        return generate_random_traffic()
    else:
        # Predefined scenario
        return get_test_scenario(scenario)


def generate_random_traffic():
    """
    Generate random traffic volumes for training.

    Provides diverse traffic conditions to help agent learn robust policies.
    Each episode gets different random volumes.

    Returns:
        dict: Random traffic configuration
            - cars: 100-1000 per hour
            - bicycles: 100-1000 per hour
            - pedestrians: 100-1000 per hour
            - buses: Every 15 minutes (constant)

    Example:
        config = generate_random_traffic()
        print(config)
        # {'cars': 573, 'bicycles': 821, 'pedestrians': 234,
        #  'buses': 'every_15min', 'scenario_name': 'training_random'}
    """
    config = {
        "cars": random.randint(100, 1000),
        "bicycles": random.randint(100, 1000),
        "pedestrians": random.randint(100, 1000),
        "buses": "every_15min",
        "scenario_name": "training_random",
    }
    return config


def get_test_scenario(scenario_name, test_scenarios):
    """
    Get predefined test scenario configuration.

    Args:
        scenario_name (str): Scenario identifier (e.g., 'Pr_5', 'Bi_3', 'Pe_7')
        test_scenarios (dict): Scenarios dict (TEST_SCENARIOS_TWO_INTERSECTIONS
            or TEST_SCENARIOS_FIVE_INTERSECTIONS)

    Returns:
        dict: Test scenario configuration

    Raises:
        ValueError: If scenario_name not found
    """
    if scenario_name not in test_scenarios:
        valid_scenarios = list(test_scenarios.keys())
        raise ValueError(
            f"Invalid scenario: '{scenario_name}'. "
            f"Valid scenarios: {valid_scenarios[:5]}...{valid_scenarios[-5:]}"
        )

    config = test_scenarios[scenario_name].copy()
    config["scenario_name"] = scenario_name
    return config


def get_all_test_scenarios():
    """
    Get list of all test scenario names.

    Returns:
        list: All 30 scenario names

    Example:
        scenarios = get_all_test_scenarios()
        print(scenarios)
        # ['Pr_0', 'Pr_1', ..., 'Pe_9']
    """
    return list(TEST_SCENARIOS_TWO_INTERSECTIONS.keys())


def get_scenario_category(scenario_name):
    """
    Get category of a test scenario.

    Args:
        scenario_name (str): Scenario identifier

    Returns:
        str: Category ('Pr', 'Bi', or 'Pe')

    Example:
        category = get_scenario_category('Pr_5')
        print(category)  # 'Pr'
    """
    if scenario_name.startswith("Pr_"):
        return "Pr"
    elif scenario_name.startswith("Bi_"):
        return "Bi"
    elif scenario_name.startswith("Pe_"):
        return "Pe"
    else:
        return "Unknown"


def print_traffic_config(config):
    """
    Pretty print traffic configuration.

    Args:
        config (dict): Traffic configuration

    Example:
        config = get_traffic_config(scenario='Pr_5')
        print_traffic_config(config)
        # Output:
        # ======================================
        # Traffic Configuration: Pr_5
        # ======================================
        # Cars/hr:        600
        # Bicycles/hr:    400
        # Pedestrians/hr: 400
        # Buses:          Every 15 minutes
        # ======================================
    """
    print("=" * 50)
    print(f"Traffic Configuration: {config['scenario_name']}")
    print("=" * 50)
    print(f"Cars/hr:        {config['cars']}")
    print(f"Bicycles/hr:    {config['bicycles']}")
    print(f"Pedestrians/hr: {config['pedestrians']}")
    print("Buses:          Every 15 minutes")
    print("=" * 50)


# ============================================================================
# Export all functions
# ============================================================================

__all__ = [
    "TEST_SCENARIOS_TWO_INTERSECTIONS",
    "TEST_SCENARIOS_FIVE_INTERSECTIONS",
    "get_traffic_config",
    "generate_random_traffic",
    "get_test_scenario",
    "get_all_test_scenarios",
    "get_scenario_category",
    "print_traffic_config",
]
