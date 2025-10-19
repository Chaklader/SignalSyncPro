"""
Dynamic route generation for training and testing.
Wraps existing route generation scripts with configurable traffic volumes.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants.constants import (
    SIMULATION_LIMIT_TRAIN,
    STRAIGHT_TRAFFIC_RATIO,
    TURN_RATIO,
)
from common.utils import calculate_traffic_load
import random


def generate_car_routes_developed(cars_per_hour):
    """Generate private car routes for DEVELOPED control with specified volume."""

    # Calculate traffic loads for horizontal (main) and vertical (minor) roads
    major_hourly_traffic_load, minor_hourly_traffic_load = calculate_traffic_load(cars_per_hour)

    # Calculate loads for all routes (same logic as privateCarRouteFile.py)
    ac_load = TURN_RATIO * major_hourly_traffic_load
    ad_load = TURN_RATIO * major_hourly_traffic_load
    ae_load = STRAIGHT_TRAFFIC_RATIO * TURN_RATIO * major_hourly_traffic_load
    af_load = STRAIGHT_TRAFFIC_RATIO * TURN_RATIO * major_hourly_traffic_load
    ab_load = STRAIGHT_TRAFFIC_RATIO * STRAIGHT_TRAFFIC_RATIO * major_hourly_traffic_load

    bf_load = TURN_RATIO * major_hourly_traffic_load
    be_load = TURN_RATIO * major_hourly_traffic_load
    ba_load = STRAIGHT_TRAFFIC_RATIO * STRAIGHT_TRAFFIC_RATIO * major_hourly_traffic_load
    bd_load = STRAIGHT_TRAFFIC_RATIO * TURN_RATIO * major_hourly_traffic_load
    bc_load = STRAIGHT_TRAFFIC_RATIO * TURN_RATIO * major_hourly_traffic_load

    dc_load = STRAIGHT_TRAFFIC_RATIO * minor_hourly_traffic_load
    da_load = TURN_RATIO * minor_hourly_traffic_load
    db_load = STRAIGHT_TRAFFIC_RATIO * TURN_RATIO * minor_hourly_traffic_load
    df_load = TURN_RATIO * TURN_RATIO * minor_hourly_traffic_load
    de_load = TURN_RATIO * TURN_RATIO * minor_hourly_traffic_load

    ca_load = TURN_RATIO * minor_hourly_traffic_load
    cd_load = STRAIGHT_TRAFFIC_RATIO * minor_hourly_traffic_load
    cf_load = TURN_RATIO * TURN_RATIO * minor_hourly_traffic_load
    ce_load = TURN_RATIO * TURN_RATIO * minor_hourly_traffic_load
    cb_load = STRAIGHT_TRAFFIC_RATIO * TURN_RATIO * minor_hourly_traffic_load

    fb_load = TURN_RATIO * minor_hourly_traffic_load
    fe_load = STRAIGHT_TRAFFIC_RATIO * minor_hourly_traffic_load
    fd_load = TURN_RATIO * TURN_RATIO * minor_hourly_traffic_load
    fc_load = TURN_RATIO * TURN_RATIO * minor_hourly_traffic_load
    fa_load = STRAIGHT_TRAFFIC_RATIO * TURN_RATIO * minor_hourly_traffic_load

    eb_load = TURN_RATIO * minor_hourly_traffic_load
    ef_load = STRAIGHT_TRAFFIC_RATIO * minor_hourly_traffic_load
    ed_load = TURN_RATIO * TURN_RATIO * minor_hourly_traffic_load
    ec_load = TURN_RATIO * TURN_RATIO * minor_hourly_traffic_load
    ea_load = STRAIGHT_TRAFFIC_RATIO * TURN_RATIO * minor_hourly_traffic_load

    # Generate route file
    routes = open("infrastructure/developed/common/routes/privateCar.rou.xml", "w")
    print(
        """<routes>
        
            <vType id="Volkswagen" accel="2.3" decel="4.5" sigma="0.5" length="4.0" maxSpeed="60" color="124,252,0" vClass="private" emissionClass="P_7_7"/>  
        
            <route id="1" edges="a_1 1_2 2_3 3_10 10_9 9_c"/>
            <route id="2" edges="a_1 1_2 2_3 3_11 11_12 12_d"/>
            <route id="3" edges="a_1 1_2 2_3 3_4 4_5 5_6 6_14 14_13 13_e"/>
            <route id="4" edges="a_1 1_2 2_3 3_4 4_5 5_6 6_15 15_16 16_f"/>
            <route id="5" edges="a_1 1_2 2_3 3_4 4_5 5_6 6_7 7_8 8_b"/>

            <route id="6" edges="b_8 8_7 7_6 6_15 15_16 16_f"/>
            <route id="7" edges="b_8 8_7 7_6 6_14 14_13 13_e"/>
            <route id="8" edges="b_8 8_7 7_6 6_5 5_4 4_3 3_2 2_1 1_a"/>
            <route id="9" edges="b_8 8_7 7_6 6_5 5_4 4_3 3_11 11_12 12_d"/> 
            <route id="10" edges="b_8 8_7 7_6 6_5 5_4 4_3 3_10 10_9 9_c"/>
            
            <route id="11" edges="d_12 12_11 11_3 3_10 10_9 9_c"/>
            <route id="12" edges="d_12 12_11 11_3  3_2 2_1 1_a "/>
            <route id="13" edges="d_12 12_11 11_3 3_4 4_5 5_6 6_7 7_8 8_b"/>
            <route id="14" edges="d_12 12_11 11_3  3_4 4_5 5_6 6_15 15_16 16_f"/> 
            <route id="15" edges="d_12 12_11 11_3 3_4 4_5 5_6 6_14 14_13 13_e"/>
            
            <route id="16" edges="c_9 9_10 10_3 3_2 2_1 1_a"/>
            <route id="17" edges="c_9 9_10 10_3 3_11 11_12 12_d"/>
            <route id="18" edges="c_9 9_10 10_3 3_4 4_5 5_6 6_15 15_16 16_f"/>
            <route id="19" edges="c_9 9_10 10_3 3_4 4_5 5_6 6_14 14_13 13_e"/> 
            <route id="20" edges="c_9 9_10 10_3 3_4 4_5 5_6 6_7 7_8 8_b"/>
            
            <route id="21" edges="f_16 16_15 15_6 6_7 7_8 8_b"/>
            <route id="22" edges="f_16 16_15 15_6 6_14 14_13 13_e"/>
            <route id="23" edges="f_16 16_15 15_6 6_5 5_4 4_3 3_11 11_12 12_d"/>
            <route id="24" edges="f_16 16_15 15_6 6_5 5_4 4_3 3_10 10_9 9_c"/> 
            <route id="25" edges="f_16 16_15 15_6 6_5 5_4 4_3 3_2 2_1 1_a"/>
            
            <route id="26" edges="e_13 13_14 14_6 6_7 7_8 8_b"/>
            <route id="27" edges="e_13 13_14 14_6 6_15 15_16 16_f"/>
            <route id="28" edges="e_13 13_14 14_6 6_5 5_4 4_3 3_11 11_12 12_d"/>
            <route id="29" edges="e_13 13_14 14_6 6_5 5_4 4_3 3_10 10_9 9_c"/> 
            <route id="30" edges="e_13 13_14 14_6 6_5 5_4 4_3 3_2 2_1 1_a"/>	
                        
        """,
        file=routes,
    )

    veh_nr = 0  # Cars start at 0
    loads = [
        ac_load,
        ad_load,
        ae_load,
        af_load,
        ab_load,
        bf_load,
        be_load,
        ba_load,
        bd_load,
        bc_load,
        dc_load,
        da_load,
        db_load,
        df_load,
        de_load,
        ca_load,
        cd_load,
        cf_load,
        ce_load,
        cb_load,
        fb_load,
        fe_load,
        fd_load,
        fc_load,
        fa_load,
        eb_load,
        ef_load,
        ed_load,
        ec_load,
        ea_load,
    ]

    for loop_number in range(SIMULATION_LIMIT_TRAIN):
        for route_id, load in enumerate(loads, 1):
            if random.uniform(0, 1) < load:
                print(
                    f'    <vehicle id="{veh_nr}" type="Volkswagen" route="{route_id}" depart="{loop_number}" departLane="free" departSpeed="random" />',
                    file=routes,
                )
                veh_nr += 1

    print("</routes>", file=routes)
    routes.close()


def generate_bicycle_routes_developed(bikes_per_hour):
    """Generate bicycle routes for DEVELOPED control with specified volume."""

    # Calculate traffic loads for horizontal (main) and vertical (minor) roads
    major_hourly_traffic_load, minor_hourly_traffic_load = calculate_traffic_load(bikes_per_hour)

    ac_load = TURN_RATIO * major_hourly_traffic_load
    ad_load = TURN_RATIO * major_hourly_traffic_load
    ae_load = STRAIGHT_TRAFFIC_RATIO * TURN_RATIO * major_hourly_traffic_load
    af_load = STRAIGHT_TRAFFIC_RATIO * TURN_RATIO * major_hourly_traffic_load
    ab_load = STRAIGHT_TRAFFIC_RATIO * STRAIGHT_TRAFFIC_RATIO * major_hourly_traffic_load

    bf_load = TURN_RATIO * major_hourly_traffic_load
    be_load = TURN_RATIO * major_hourly_traffic_load
    ba_load = STRAIGHT_TRAFFIC_RATIO * STRAIGHT_TRAFFIC_RATIO * major_hourly_traffic_load
    bd_load = STRAIGHT_TRAFFIC_RATIO * TURN_RATIO * major_hourly_traffic_load
    bc_load = STRAIGHT_TRAFFIC_RATIO * TURN_RATIO * major_hourly_traffic_load

    dc_load = STRAIGHT_TRAFFIC_RATIO * minor_hourly_traffic_load
    da_load = TURN_RATIO * minor_hourly_traffic_load
    db_load = STRAIGHT_TRAFFIC_RATIO * TURN_RATIO * minor_hourly_traffic_load
    df_load = TURN_RATIO * TURN_RATIO * minor_hourly_traffic_load
    de_load = TURN_RATIO * TURN_RATIO * minor_hourly_traffic_load

    ca_load = TURN_RATIO * minor_hourly_traffic_load
    cd_load = STRAIGHT_TRAFFIC_RATIO * minor_hourly_traffic_load
    cf_load = TURN_RATIO * TURN_RATIO * minor_hourly_traffic_load
    ce_load = TURN_RATIO * TURN_RATIO * minor_hourly_traffic_load
    cb_load = STRAIGHT_TRAFFIC_RATIO * TURN_RATIO * minor_hourly_traffic_load

    fb_load = TURN_RATIO * minor_hourly_traffic_load
    fe_load = STRAIGHT_TRAFFIC_RATIO * minor_hourly_traffic_load
    fd_load = TURN_RATIO * TURN_RATIO * minor_hourly_traffic_load
    fc_load = TURN_RATIO * TURN_RATIO * minor_hourly_traffic_load
    fa_load = STRAIGHT_TRAFFIC_RATIO * TURN_RATIO * minor_hourly_traffic_load

    eb_load = TURN_RATIO * minor_hourly_traffic_load
    ef_load = STRAIGHT_TRAFFIC_RATIO * minor_hourly_traffic_load
    ed_load = TURN_RATIO * TURN_RATIO * minor_hourly_traffic_load
    ec_load = TURN_RATIO * TURN_RATIO * minor_hourly_traffic_load
    ea_load = STRAIGHT_TRAFFIC_RATIO * TURN_RATIO * minor_hourly_traffic_load

    routes = open("infrastructure/developed/common/routes/bicycle.rou.xml", "w")
    print(
        """<routes>
        
            <vType id="Raleigh" accel="0.8" decel="1.5" sigma="0.5" length="1.6" maxSpeed="5.8" color="255,255,0" guiShape="bicycle" vClass="bicycle" emissionClass="zero"/>  
        
            <route id="l" edges="a_3 3_c"/>
            <route id="ll" edges="a_3 3_d"/>
            <route id="lll" edges="a_3 3_6 6_e"/>
            <route id="lV" edges="a_3 3_6 6_f"/>
            <route id="V" edges="a_3 3_6 6_b"/>

            <route id="Vl" edges="b_6 6_f"/>
            <route id="Vll" edges="b_6 6_e"/>
            <route id="Vlll" edges="b_6 6_3 3_a"/>
            <route id="lX" edges="b_6 6_3 3_d"/> 
            <route id="X" edges="b_6 6_3 3_c"/>
            
            
            <route id="Xl" edges="d_3 3_c"/>
            <route id="Xll" edges="d_3 3_a "/>
            <route id="Xlll" edges="d_3 3_6 6_b"/>
            <route id="XlV" edges="d_3 3_6 6_f"/> 
            <route id="XV" edges="d_3 3_6 6_e"/>
            
            <route id="XVl" edges="c_3 3_a"/>
            <route id="XVll" edges="c_3 3_d"/>
            <route id="XVlll" edges="c_3 3_6 6_f"/>
            <route id="XlX" edges="c_3 3_6 6_e"/> 
            <route id="XX" edges="c_3 3_6 6_b"/>
            
            <route id="XXl" edges="f_6 6_b"/>
            <route id="XXll" edges="f_6 6_e"/>
            <route id="XXlll" edges="f_6 6_3 3_d"/>
            <route id="XXlV" edges="f_6 6_3 3_c"/> 
            <route id="XXV" edges="f_6 6_3 3_a"/>
            
            <route id="XXVl"  edges="e_6 6_b"/>
            <route id="XXVll" edges="e_6 6_f"/>
            <route id="XXVlll" edges="e_6 6_3 3_d"/>
            <route id="XXlX" edges="e_6 6_3 3_c"/> 
            <route id="XXX" edges="e_6 6_3 3_a"/>	
                        
        """,
        file=routes,
    )

    veh_nr = 400000  # Bicycles start at 400000 (to avoid conflicts with cars)
    loads = [
        ac_load,
        ad_load,
        ae_load,
        af_load,
        ab_load,
        bf_load,
        be_load,
        ba_load,
        bd_load,
        bc_load,
        dc_load,
        da_load,
        db_load,
        df_load,
        de_load,
        ca_load,
        cd_load,
        cf_load,
        ce_load,
        cb_load,
        fb_load,
        fe_load,
        fd_load,
        fc_load,
        fa_load,
        eb_load,
        ef_load,
        ed_load,
        ec_load,
        ea_load,
    ]

    # Roman numeral route IDs matching old_routes
    route_ids = [
        "l",
        "ll",
        "lll",
        "lV",
        "V",
        "Vl",
        "Vll",
        "Vlll",
        "lX",
        "X",
        "Xl",
        "Xll",
        "Xlll",
        "XlV",
        "XV",
        "XVl",
        "XVll",
        "XVlll",
        "XlX",
        "XX",
        "XXl",
        "XXll",
        "XXlll",
        "XXlV",
        "XXV",
        "XXVl",
        "XXVll",
        "XXVlll",
        "XXlX",
        "XXX",
    ]

    for loop_number in range(SIMULATION_LIMIT_TRAIN):
        for route_id, load in zip(route_ids, loads):
            if random.uniform(0, 1) < load:
                print(
                    f'    <vehicle id="{veh_nr}" type="Raleigh" route="{route_id}" depart="{loop_number}" departLane="free" departSpeed="random" />',
                    file=routes,
                )
                veh_nr += 1

    print("</routes>", file=routes)
    routes.close()


def generate_pedestrian_routes_developed(peds_per_hour):
    """Generate pedestrian routes for DEVELOPED control with specified volume."""

    # Calculate pedestrian loads for horizontal (main) and vertical (minor) crossings
    ped_we, ped_sn = calculate_traffic_load(peds_per_hour)
    ped_ew = ped_we  # East-West same as West-East
    ped_ns = ped_sn  # North-South same as South-North

    routes = open("infrastructure/developed/common/routes/pedestrian.rou.xml", "w")
    print(
        """<routes>

            <vType id="Berliner" accel="0.5" decel="1.0" sigma="0.5" length="0.5" maxSpeed="1.5" minGap="1.0" color="255,165,0" guiShape="pedestrian"  width ="0.5" vClass="pedestrian"/>  

            <route id="a" edges="a_3 3_6"/>
            <route id="c" edges="6_3 3_a"/>
            <route id="e" edges="c_3 3_d"/>
            <route id="g" edges="d_3 3_c"/>
            <route id="i" edges="3_6 6_b"/>
            <route id="k" edges="b_6 6_3"/>
            <route id="m" edges="e_6 6_f"/>
            <route id="o" edges="f_6 6_e"/>
                        
        """,
        file=routes,
    )

    veh_nr = 800000  # Pedestrians start at 800000 (to avoid conflicts)
    ped_loads = [ped_we, ped_ew, ped_sn, ped_ns, ped_we, ped_ew, ped_sn, ped_ns]
    route_ids = ["a", "c", "e", "g", "i", "k", "m", "o"]

    for loop_number in range(SIMULATION_LIMIT_TRAIN):
        for route_id, load in zip(route_ids, ped_loads):
            if random.uniform(0, 1) < load:
                print(
                    f'    <person id="{veh_nr}" depart="{loop_number}" departPos="random">',
                    file=routes,
                )
                print(f'        <walk route="{route_id}"/>', file=routes)
                print("    </person>", file=routes)
                veh_nr += 1

    print("</routes>", file=routes)
    routes.close()


def generate_bus_routes(buses_per_hour=4):
    """
    Generate bus routes with specified volume.

    NOTE: Bus routes are IDENTICAL for both developed and reference control.
    Buses run on fixed schedules with bus stops.
    Default: 4 buses/hour = 1 bus every 15 minutes (900 seconds)

    Args:
        buses_per_hour: Number of buses per hour, or 'every_15min' for fixed schedule
    """
    routes = open("infrastructure/developed/common/routes/bus.rou.xml", "w")
    print(
        """<routes>

    <vType id="bus" accel="2.6" decel="4.5" sigma="0.5" length="12" minGap="3" maxSpeed="70" color="1,0,0" guiShape="bus/city" vClass="bus" emissionClass="HDV_12_12"/>
""",
        file=routes,
    )

    # Handle string values like 'every_15min'
    if isinstance(buses_per_hour, str):
        bus_interval = 900  # Default: every 15 minutes
    else:
        # Calculate bus interval (seconds between buses)
        bus_interval = 3600 / buses_per_hour if buses_per_hour > 0 else 900

    bus_id = 0
    depart_time = 0

    # Generate buses for simulation duration
    while depart_time < SIMULATION_LIMIT_TRAIN:
        # Bus from a to b (eastbound)
        print(
            f"""    <vehicle id="bus_{bus_id}" depart="{depart_time}" departPos="0" departLane="best" arrivalPos="-1" type="bus" >
        <route edges="a_1 1_2 2_3 3_4 4_5 5_6 6_7 7_8 8_b"/>
        <stop busStop="Stop#1" duration="20"/>
        <stop busStop="Stop#2" duration="20"/>
    </vehicle>""",
            file=routes,
        )
        bus_id += 1

        # Bus from b to a (westbound)
        print(
            f"""    <vehicle id="bus_{bus_id}" depart="{depart_time}" departPos="0" departLane="best" arrivalPos="-1" type="bus" >
        <route edges="b_8 8_7 7_6 6_5 5_4 4_3 3_2 2_1 1_a"/>
        <stop busStop="Stop#3" duration="20"/>
        <stop busStop="Stop#4" duration="20"/>
    </vehicle>
""",
            file=routes,
        )
        bus_id += 1

        depart_time += bus_interval

    print("</routes>", file=routes)
    routes.close()


def generate_all_routes_developed(traffic_config):
    """
    Generate all route files for DEVELOPED control based on traffic configuration.

    Args:
        traffic_config (dict): Traffic configuration from traffic_config.py
            Keys: 'cars', 'bicycles', 'pedestrians', 'buses', 'scenario_name'

    Example:
        config = get_traffic_config()
        generate_all_routes_developed(config)
    """
    print(
        f"Generating DEVELOPED control routes for scenario: {traffic_config['scenario_name']}"
    )
    print(f"  Cars: {traffic_config['cars']}/hr")
    print(f"  Bicycles: {traffic_config['bicycles']}/hr")
    print(f"  Pedestrians: {traffic_config['pedestrians']}/hr")
    print(f"  Buses: {traffic_config.get('buses', 4)}/hr")

    # Create routes directory if it doesn't exist
    import os

    routes_dir = "infrastructure/developed/common/routes"
    os.makedirs(routes_dir, exist_ok=True)

    generate_car_routes_developed(traffic_config["cars"])
    generate_bicycle_routes_developed(traffic_config["bicycles"])
    generate_pedestrian_routes_developed(traffic_config["pedestrians"])
    generate_bus_routes(traffic_config.get("buses", 4))

    print("✓ DEVELOPED control route generation complete\n")
