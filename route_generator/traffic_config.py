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

TEST_SCENARIOS = {
    # Pr scenarios: Varying car volumes (100-1000), constant bikes/peds (400)
    "Pr_0": {"cars": 100, "bicycles": 400, "pedestrians": 400, "buses": "every_15min"},
    "Pr_1": {"cars": 200, "bicycles": 400, "pedestrians": 400, "buses": "every_15min"},
    "Pr_2": {"cars": 300, "bicycles": 400, "pedestrians": 400, "buses": "every_15min"},
    "Pr_3": {"cars": 400, "bicycles": 400, "pedestrians": 400, "buses": "every_15min"},
    "Pr_4": {"cars": 500, "bicycles": 400, "pedestrians": 400, "buses": "every_15min"},
    "Pr_5": {"cars": 600, "bicycles": 400, "pedestrians": 400, "buses": "every_15min"},
    "Pr_6": {"cars": 700, "bicycles": 400, "pedestrians": 400, "buses": "every_15min"},
    "Pr_7": {"cars": 800, "bicycles": 400, "pedestrians": 400, "buses": "every_15min"},
    "Pr_8": {"cars": 900, "bicycles": 400, "pedestrians": 400, "buses": "every_15min"},
    "Pr_9": {"cars": 1000, "bicycles": 400, "pedestrians": 400, "buses": "every_15min"},
    # Bi scenarios: Varying bicycle volumes (100-1000), constant cars/peds (400)
    "Bi_0": {"cars": 400, "bicycles": 100, "pedestrians": 400, "buses": "every_15min"},
    "Bi_1": {"cars": 400, "bicycles": 200, "pedestrians": 400, "buses": "every_15min"},
    "Bi_2": {"cars": 400, "bicycles": 300, "pedestrians": 400, "buses": "every_15min"},
    "Bi_3": {"cars": 400, "bicycles": 400, "pedestrians": 400, "buses": "every_15min"},
    "Bi_4": {"cars": 400, "bicycles": 500, "pedestrians": 400, "buses": "every_15min"},
    "Bi_5": {"cars": 400, "bicycles": 600, "pedestrians": 400, "buses": "every_15min"},
    "Bi_6": {"cars": 400, "bicycles": 700, "pedestrians": 400, "buses": "every_15min"},
    "Bi_7": {"cars": 400, "bicycles": 800, "pedestrians": 400, "buses": "every_15min"},
    "Bi_8": {"cars": 400, "bicycles": 900, "pedestrians": 400, "buses": "every_15min"},
    "Bi_9": {"cars": 400, "bicycles": 1000, "pedestrians": 400, "buses": "every_15min"},
    # Pe scenarios: Varying pedestrian volumes (100-1000), constant cars/bikes (400)
    "Pe_0": {"cars": 400, "bicycles": 400, "pedestrians": 100, "buses": "every_15min"},
    "Pe_1": {"cars": 400, "bicycles": 400, "pedestrians": 200, "buses": "every_15min"},
    "Pe_2": {"cars": 400, "bicycles": 400, "pedestrians": 300, "buses": "every_15min"},
    "Pe_3": {"cars": 400, "bicycles": 400, "pedestrians": 400, "buses": "every_15min"},
    "Pe_4": {"cars": 400, "bicycles": 400, "pedestrians": 500, "buses": "every_15min"},
    "Pe_5": {"cars": 400, "bicycles": 400, "pedestrians": 600, "buses": "every_15min"},
    "Pe_6": {"cars": 400, "bicycles": 400, "pedestrians": 700, "buses": "every_15min"},
    "Pe_7": {"cars": 400, "bicycles": 400, "pedestrians": 800, "buses": "every_15min"},
    "Pe_8": {"cars": 400, "bicycles": 400, "pedestrians": 900, "buses": "every_15min"},
    "Pe_9": {"cars": 400, "bicycles": 400, "pedestrians": 1000, "buses": "every_15min"},
}


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


def get_test_scenario(scenario_name):
    """
    Get predefined test scenario configuration.

    30 scenarios organized in 3 categories:
    - Pr_0 to Pr_9: Varying car volumes (100-1000)
    - Bi_0 to Bi_9: Varying bicycle volumes (100-1000)
    - Pe_0 to Pe_9: Varying pedestrian volumes (100-1000)

    Args:
        scenario_name (str): Scenario identifier
            Valid: 'Pr_0' through 'Pr_9', 'Bi_0' through 'Bi_9',
                   'Pe_0' through 'Pe_9'

    Returns:
        dict: Test scenario configuration

    Raises:
        ValueError: If scenario_name not found

    Example:
        config = get_test_scenario('Pr_5')
        print(config)
        # {'cars': 600, 'bicycles': 400, 'pedestrians': 400,
        #  'buses': 'every_15min', 'scenario_name': 'Pr_5'}
    """
    if scenario_name not in TEST_SCENARIOS:
        valid_scenarios = list(TEST_SCENARIOS.keys())
        raise ValueError(
            f"Invalid scenario: '{scenario_name}'. "
            f"Valid scenarios: {valid_scenarios[:5]}...{valid_scenarios[-5:]}"
        )

    config = TEST_SCENARIOS[scenario_name].copy()
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
    return list(TEST_SCENARIOS.keys())


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
    "TEST_SCENARIOS",
    "get_traffic_config",
    "generate_random_traffic",
    "get_test_scenario",
    "get_all_test_scenarios",
    "get_scenario_category",
    "print_traffic_config",
]
