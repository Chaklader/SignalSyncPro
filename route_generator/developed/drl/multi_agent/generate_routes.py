"""
Dynamic route generation for multi-agent DRL training and testing.
Generates routes for 5 TLS network with 12 entry/exit points.

Network topology:
                    c              e              g              i              k
                    │              │              │              │              │
   a────1────2────[3]────4────5──[6]────7───20─[17]───21───22─[18]───23───24─[19]───25────8────b
                    │              │              │              │              │
                    d              f              h              j              l

   x=-1100        x=0          x=1000         x=2000         x=3000         x=4000        x=5100
   (Entry)      TLS-1          TLS-2          TLS-3          TLS-4          TLS-5         (Exit)
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)
sys.path.insert(0, PROJECT_ROOT)

from constants.constants import (  # noqa: E402
    STRAIGHT_TRAFFIC_RATIO,
    TURN_RATIO,
)
from common.utils import calculate_traffic_load  # noqa: E402
import random  # noqa: E402


ROUTES_DIR = "infrastructure/developed/drl/multi_agent/routes"


def generate_car_routes(cars_per_hour, simulation_limit):
    """Generate private car routes for multi-agent 5-TLS network."""

    major_hourly_traffic_load, minor_hourly_traffic_load = calculate_traffic_load(
        cars_per_hour
    )

    # Traffic loads for different route types
    # Major (horizontal) traffic
    straight_major = STRAIGHT_TRAFFIC_RATIO * major_hourly_traffic_load
    turn_major = TURN_RATIO * major_hourly_traffic_load

    # Minor (vertical) traffic
    straight_minor = STRAIGHT_TRAFFIC_RATIO * minor_hourly_traffic_load
    turn_minor = TURN_RATIO * minor_hourly_traffic_load

    routes = open(f"{ROUTES_DIR}/privateCar.rou.xml", "w")
    print(
        """<routes>
        
    <vType id="Volkswagen" accel="2.3" decel="4.5" sigma="0.5" length="4.0" maxSpeed="60" color="124,252,0" vClass="private" emissionClass="HBEFA3/PC_G_EU4"/>  

    <!-- ========================================== -->
    <!-- HORIZONTAL ROUTES: West to East (from a)  -->
    <!-- ========================================== -->

    <!--  Horizontal Arterial - 5 Intersections @ 1km spacing -->
    <!-- 


                        c              e              g              i              k
                        │              │              │              │              │
                        9             13             26             30             34
                        │              │              │              │              │
                    10             14             27             31             35
                        │              │              │              │              │
    a────1────2────[3]────4────5──[6]────7───20─[17]───21───22─[18]───23───24─[19]───25────8────b
                        │              │              │              │              │
                    11             15             28             32             36
                        │              │              │              │              │
                    12             16             29             33             37
                        │              │              │              │              │
                        d              f              h              j              l


    x=-1100        x=0          x=1000         x=2000         x=3000         x=4000        x=5100
    (Entry)      TLS-1          TLS-2          TLS-3          TLS-4          TLS-5         (Exit)

    -->
    
    <!-- a to b (full through) -->
    <route id="1" edges="a_1 1_2 2_3 3_4 4_5 5_6 6_7 7_20 20_17 17_21 21_22 22_18 18_23 23_24 24_19 19_25 25_8 8_b"/>
    
    <!-- a to vertical exits at TLS-1 -->
    <route id="2" edges="a_1 1_2 2_3 3_10 10_9 9_c"/>
    <route id="3" edges="a_1 1_2 2_3 3_11 11_12 12_d"/>
    
    <!-- a to vertical exits at TLS-2 -->
    <route id="4" edges="a_1 1_2 2_3 3_4 4_5 5_6 6_14 14_13 13_e"/>
    <route id="5" edges="a_1 1_2 2_3 3_4 4_5 5_6 6_15 15_16 16_f"/>
    
    <!-- a to vertical exits at TLS-3 -->
    <route id="6" edges="a_1 1_2 2_3 3_4 4_5 5_6 6_7 7_20 20_17 17_27 27_26 26_g"/>
    <route id="7" edges="a_1 1_2 2_3 3_4 4_5 5_6 6_7 7_20 20_17 17_28 28_29 29_h"/>
    
    <!-- a to vertical exits at TLS-4 -->
    <route id="8" edges="a_1 1_2 2_3 3_4 4_5 5_6 6_7 7_20 20_17 17_21 21_22 22_18 18_31 31_30 30_i"/>
    <route id="9" edges="a_1 1_2 2_3 3_4 4_5 5_6 6_7 7_20 20_17 17_21 21_22 22_18 18_32 32_33 33_j"/>
    
    <!-- a to vertical exits at TLS-5 -->
    <route id="10" edges="a_1 1_2 2_3 3_4 4_5 5_6 6_7 7_20 20_17 17_21 21_22 22_18 18_23 23_24 24_19 19_35 35_34 34_k"/>
    <route id="11" edges="a_1 1_2 2_3 3_4 4_5 5_6 6_7 7_20 20_17 17_21 21_22 22_18 18_23 23_24 24_19 19_36 36_37 37_l"/>

    <!-- ========================================== -->
    <!-- HORIZONTAL ROUTES: East to West (from b)  -->
    <!-- ========================================== -->
    
    <!-- b to a (full through) -->
    <route id="12" edges="b_8 8_25 25_19 19_24 24_23 23_18 18_22 22_21 21_17 17_20 20_7 7_6 6_5 5_4 4_3 3_2 2_1 1_a"/>
    
    <!-- b to vertical exits at TLS-5 -->
    <route id="13" edges="b_8 8_25 25_19 19_35 35_34 34_k"/>
    <route id="14" edges="b_8 8_25 25_19 19_36 36_37 37_l"/>
    
    <!-- b to vertical exits at TLS-4 -->
    <route id="15" edges="b_8 8_25 25_19 19_24 24_23 23_18 18_31 31_30 30_i"/>
    <route id="16" edges="b_8 8_25 25_19 19_24 24_23 23_18 18_32 32_33 33_j"/>
    
    <!-- b to vertical exits at TLS-3 -->
    <route id="17" edges="b_8 8_25 25_19 19_24 24_23 23_18 18_22 22_21 21_17 17_27 27_26 26_g"/>
    <route id="18" edges="b_8 8_25 25_19 19_24 24_23 23_18 18_22 22_21 21_17 17_28 28_29 29_h"/>
    
    <!-- b to vertical exits at TLS-2 -->
    <route id="19" edges="b_8 8_25 25_19 19_24 24_23 23_18 18_22 22_21 21_17 17_20 20_7 7_6 6_14 14_13 13_e"/>
    <route id="20" edges="b_8 8_25 25_19 19_24 24_23 23_18 18_22 22_21 21_17 17_20 20_7 7_6 6_15 15_16 16_f"/>
    
    <!-- b to vertical exits at TLS-1 -->
    <route id="21" edges="b_8 8_25 25_19 19_24 24_23 23_18 18_22 22_21 21_17 17_20 20_7 7_6 6_5 5_4 4_3 3_10 10_9 9_c"/>
    <route id="22" edges="b_8 8_25 25_19 19_24 24_23 23_18 18_22 22_21 21_17 17_20 20_7 7_6 6_5 5_4 4_3 3_11 11_12 12_d"/>

    <!-- ========================================== -->
    <!-- VERTICAL ROUTES @ TLS-1: c and d          -->
    <!-- ========================================== -->
    
    <!-- From c (south entry) -->
    <route id="23" edges="c_9 9_10 10_3 3_11 11_12 12_d"/>
    <route id="24" edges="c_9 9_10 10_3 3_2 2_1 1_a"/>
    <route id="25" edges="c_9 9_10 10_3 3_4 4_5 5_6 6_7 7_20 20_17 17_21 21_22 22_18 18_23 23_24 24_19 19_25 25_8 8_b"/>
    
    <!-- From d (north entry) -->
    <route id="26" edges="d_12 12_11 11_3 3_10 10_9 9_c"/>
    <route id="27" edges="d_12 12_11 11_3 3_2 2_1 1_a"/>
    <route id="28" edges="d_12 12_11 11_3 3_4 4_5 5_6 6_7 7_20 20_17 17_21 21_22 22_18 18_23 23_24 24_19 19_25 25_8 8_b"/>

    <!-- ========================================== -->
    <!-- VERTICAL ROUTES @ TLS-2: e and f          -->
    <!-- ========================================== -->
    
    <!-- From e (south entry) -->
    <route id="29" edges="e_13 13_14 14_6 6_15 15_16 16_f"/>
    <route id="30" edges="e_13 13_14 14_6 6_5 5_4 4_3 3_2 2_1 1_a"/>
    <route id="31" edges="e_13 13_14 14_6 6_7 7_20 20_17 17_21 21_22 22_18 18_23 23_24 24_19 19_25 25_8 8_b"/>
    
    <!-- From f (north entry) -->
    <route id="32" edges="f_16 16_15 15_6 6_14 14_13 13_e"/>
    <route id="33" edges="f_16 16_15 15_6 6_5 5_4 4_3 3_2 2_1 1_a"/>
    <route id="34" edges="f_16 16_15 15_6 6_7 7_20 20_17 17_21 21_22 22_18 18_23 23_24 24_19 19_25 25_8 8_b"/>

    <!-- ========================================== -->
    <!-- VERTICAL ROUTES @ TLS-3: g and h          -->
    <!-- ========================================== -->
    
    <!-- From g (south entry) -->
    <route id="35" edges="g_26 26_27 27_17 17_28 28_29 29_h"/>
    <route id="36" edges="g_26 26_27 27_17 17_20 20_7 7_6 6_5 5_4 4_3 3_2 2_1 1_a"/>
    <route id="37" edges="g_26 26_27 27_17 17_21 21_22 22_18 18_23 23_24 24_19 19_25 25_8 8_b"/>
    
    <!-- From h (north entry) -->
    <route id="38" edges="h_29 29_28 28_17 17_27 27_26 26_g"/>
    <route id="39" edges="h_29 29_28 28_17 17_20 20_7 7_6 6_5 5_4 4_3 3_2 2_1 1_a"/>
    <route id="40" edges="h_29 29_28 28_17 17_21 21_22 22_18 18_23 23_24 24_19 19_25 25_8 8_b"/>

    <!-- ========================================== -->
    <!-- VERTICAL ROUTES @ TLS-4: i and j          -->
    <!-- ========================================== -->
    
    <!-- From i (south entry) -->
    <route id="41" edges="i_30 30_31 31_18 18_32 32_33 33_j"/>
    <route id="42" edges="i_30 30_31 31_18 18_22 22_21 21_17 17_20 20_7 7_6 6_5 5_4 4_3 3_2 2_1 1_a"/>
    <route id="43" edges="i_30 30_31 31_18 18_23 23_24 24_19 19_25 25_8 8_b"/>
    
    <!-- From j (north entry) -->
    <route id="44" edges="j_33 33_32 32_18 18_31 31_30 30_i"/>
    <route id="45" edges="j_33 33_32 32_18 18_22 22_21 21_17 17_20 20_7 7_6 6_5 5_4 4_3 3_2 2_1 1_a"/>
    <route id="46" edges="j_33 33_32 32_18 18_23 23_24 24_19 19_25 25_8 8_b"/>

    <!-- ========================================== -->
    <!-- VERTICAL ROUTES @ TLS-5: k and l          -->
    <!-- ========================================== -->
    
    <!-- From k (south entry) -->
    <route id="47" edges="k_34 34_35 35_19 19_36 36_37 37_l"/>
    <route id="48" edges="k_34 34_35 35_19 19_24 24_23 23_18 18_22 22_21 21_17 17_20 20_7 7_6 6_5 5_4 4_3 3_2 2_1 1_a"/>
    <route id="49" edges="k_34 34_35 35_19 19_25 25_8 8_b"/>
    
    <!-- From l (north entry) -->
    <route id="50" edges="l_37 37_36 36_19 19_35 35_34 34_k"/>
    <route id="51" edges="l_37 37_36 36_19 19_24 24_23 23_18 18_22 22_21 21_17 17_20 20_7 7_6 6_5 5_4 4_3 3_2 2_1 1_a"/>
    <route id="52" edges="l_37 37_36 36_19 19_25 25_8 8_b"/>

        """,
        file=routes,
    )

    veh_nr = 0

    # Define loads for each route
    # Routes 1-11: From a (major horizontal)
    # Routes 12-22: From b (major horizontal)
    # Routes 23-52: From vertical entries (minor)

    loads = [
        # From a (horizontal entry - major traffic)
        straight_major * STRAIGHT_TRAFFIC_RATIO,  # 1: a->b through
        turn_major,  # 2: a->c
        turn_major,  # 3: a->d
        straight_major * turn_major,  # 4: a->e
        straight_major * turn_major,  # 5: a->f
        straight_major * turn_major,  # 6: a->g
        straight_major * turn_major,  # 7: a->h
        straight_major * turn_major,  # 8: a->i
        straight_major * turn_major,  # 9: a->j
        straight_major * turn_major,  # 10: a->k
        straight_major * turn_major,  # 11: a->l
        # From b (horizontal entry - major traffic)
        straight_major * STRAIGHT_TRAFFIC_RATIO,  # 12: b->a through
        turn_major,  # 13: b->k
        turn_major,  # 14: b->l
        straight_major * turn_major,  # 15: b->i
        straight_major * turn_major,  # 16: b->j
        straight_major * turn_major,  # 17: b->g
        straight_major * turn_major,  # 18: b->h
        straight_major * turn_major,  # 19: b->e
        straight_major * turn_major,  # 20: b->f
        straight_major * turn_major,  # 21: b->c
        straight_major * turn_major,  # 22: b->d
        # From c (vertical entry - minor traffic)
        straight_minor,  # 23: c->d through
        turn_minor,  # 24: c->a
        turn_minor * STRAIGHT_TRAFFIC_RATIO,  # 25: c->b
        # From d (vertical entry - minor traffic)
        straight_minor,  # 26: d->c through
        turn_minor,  # 27: d->a
        turn_minor * STRAIGHT_TRAFFIC_RATIO,  # 28: d->b
        # From e (vertical entry - minor traffic)
        straight_minor,  # 29: e->f through
        turn_minor,  # 30: e->a
        turn_minor * STRAIGHT_TRAFFIC_RATIO,  # 31: e->b
        # From f (vertical entry - minor traffic)
        straight_minor,  # 32: f->e through
        turn_minor,  # 33: f->a
        turn_minor * STRAIGHT_TRAFFIC_RATIO,  # 34: f->b
        # From g (vertical entry - minor traffic)
        straight_minor,  # 35: g->h through
        turn_minor,  # 36: g->a
        turn_minor * STRAIGHT_TRAFFIC_RATIO,  # 37: g->b
        # From h (vertical entry - minor traffic)
        straight_minor,  # 38: h->g through
        turn_minor,  # 39: h->a
        turn_minor * STRAIGHT_TRAFFIC_RATIO,  # 40: h->b
        # From i (vertical entry - minor traffic)
        straight_minor,  # 41: i->j through
        turn_minor,  # 42: i->a
        turn_minor * STRAIGHT_TRAFFIC_RATIO,  # 43: i->b
        # From j (vertical entry - minor traffic)
        straight_minor,  # 44: j->i through
        turn_minor,  # 45: j->a
        turn_minor * STRAIGHT_TRAFFIC_RATIO,  # 46: j->b
        # From k (vertical entry - minor traffic)
        straight_minor,  # 47: k->l through
        turn_minor,  # 48: k->a
        turn_minor * STRAIGHT_TRAFFIC_RATIO,  # 49: k->b
        # From l (vertical entry - minor traffic)
        straight_minor,  # 50: l->k through
        turn_minor,  # 51: l->a
        turn_minor * STRAIGHT_TRAFFIC_RATIO,  # 52: l->b
    ]

    for loop_number in range(simulation_limit):
        for route_id, load in enumerate(loads, 1):
            if random.uniform(0, 1) < load:
                print(
                    f'    <vehicle id="{veh_nr}" type="Volkswagen" route="{route_id}" depart="{loop_number}" departLane="free" departSpeed="random" />',
                    file=routes,
                )
                veh_nr += 1

    print("</routes>", file=routes)
    routes.close()
    return veh_nr


def generate_bicycle_routes(bikes_per_hour, simulation_limit):
    """Generate bicycle routes for multi-agent 5-TLS network using dedicated bike edges."""

    major_hourly_traffic_load, minor_hourly_traffic_load = calculate_traffic_load(
        bikes_per_hour
    )

    straight_major = STRAIGHT_TRAFFIC_RATIO * major_hourly_traffic_load
    turn_major = TURN_RATIO * major_hourly_traffic_load
    straight_minor = STRAIGHT_TRAFFIC_RATIO * minor_hourly_traffic_load
    turn_minor = TURN_RATIO * minor_hourly_traffic_load

    routes = open(f"{ROUTES_DIR}/bicycle.rou.xml", "w")
    print(
        """<routes>
        
    <vType id="Raleigh" accel="0.8" decel="1.5" sigma="0.5" length="1.6" maxSpeed="5.8" color="255,255,0" guiShape="bicycle" vClass="bicycle" emissionClass="zero"/>  

    <!-- ========================================== -->
    <!-- HORIZONTAL BICYCLE: West to East          -->
    <!-- ========================================== -->
    
    <!-- From a to exits -->
    <route id="ab" edges="a_3 3_6 6_17 17_18 18_19 19_b"/>
    <route id="ac" edges="a_3 3_c"/>
    <route id="ad" edges="a_3 3_d"/>
    <route id="ae" edges="a_3 3_6 6_e"/>
    <route id="af" edges="a_3 3_6 6_f"/>
    <route id="ag" edges="a_3 3_6 6_17 17_g"/>
    <route id="ah" edges="a_3 3_6 6_17 17_h"/>
    <route id="ai" edges="a_3 3_6 6_17 17_18 18_i"/>
    <route id="aj" edges="a_3 3_6 6_17 17_18 18_j"/>
    <route id="ak" edges="a_3 3_6 6_17 17_18 18_19 19_k"/>
    <route id="al" edges="a_3 3_6 6_17 17_18 18_19 19_l"/>

    <!-- ========================================== -->
    <!-- HORIZONTAL BICYCLE: East to West          -->
    <!-- ========================================== -->
    
    <!-- From b to exits -->
    <route id="ba" edges="b_19 19_18 18_17 17_6 6_3 3_a"/>
    <route id="bk" edges="b_19 19_k"/>
    <route id="bl" edges="b_19 19_l"/>
    <route id="bi" edges="b_19 19_18 18_i"/>
    <route id="bj" edges="b_19 19_18 18_j"/>
    <route id="bg" edges="b_19 19_18 18_17 17_g"/>
    <route id="bh" edges="b_19 19_18 18_17 17_h"/>
    <route id="be" edges="b_19 19_18 18_17 17_6 6_e"/>
    <route id="bf" edges="b_19 19_18 18_17 17_6 6_f"/>
    <route id="bc" edges="b_19 19_18 18_17 17_6 6_3 3_c"/>
    <route id="bd" edges="b_19 19_18 18_17 17_6 6_3 3_d"/>

    <!-- ========================================== -->
    <!-- VERTICAL BICYCLE @ TLS-1                  -->
    <!-- ========================================== -->
    
    <route id="cd" edges="c_3 3_d"/>
    <route id="ca" edges="c_3 3_a"/>
    <route id="cb" edges="c_3 3_6 6_17 17_18 18_19 19_b"/>
    
    <route id="dc" edges="d_3 3_c"/>
    <route id="da" edges="d_3 3_a"/>
    <route id="db" edges="d_3 3_6 6_17 17_18 18_19 19_b"/>

    <!-- ========================================== -->
    <!-- VERTICAL BICYCLE @ TLS-2                  -->
    <!-- ========================================== -->
    
    <route id="ef" edges="e_6 6_f"/>
    <route id="ea" edges="e_6 6_3 3_a"/>
    <route id="eb" edges="e_6 6_17 17_18 18_19 19_b"/>
    
    <route id="fe" edges="f_6 6_e"/>
    <route id="fa" edges="f_6 6_3 3_a"/>
    <route id="fb" edges="f_6 6_17 17_18 18_19 19_b"/>

    <!-- ========================================== -->
    <!-- VERTICAL BICYCLE @ TLS-3                  -->
    <!-- ========================================== -->
    
    <route id="gh" edges="g_17 17_h"/>
    <route id="ga" edges="g_17 17_6 6_3 3_a"/>
    <route id="gb" edges="g_17 17_18 18_19 19_b"/>
    
    <route id="hg" edges="h_17 17_g"/>
    <route id="ha" edges="h_17 17_6 6_3 3_a"/>
    <route id="hb" edges="h_17 17_18 18_19 19_b"/>

    <!-- ========================================== -->
    <!-- VERTICAL BICYCLE @ TLS-4                  -->
    <!-- ========================================== -->
    
    <route id="ij" edges="i_18 18_j"/>
    <route id="ia" edges="i_18 18_17 17_6 6_3 3_a"/>
    <route id="ib" edges="i_18 18_19 19_b"/>
    
    <route id="ji" edges="j_18 18_i"/>
    <route id="ja" edges="j_18 18_17 17_6 6_3 3_a"/>
    <route id="jb" edges="j_18 18_19 19_b"/>

    <!-- ========================================== -->
    <!-- VERTICAL BICYCLE @ TLS-5                  -->
    <!-- ========================================== -->
    
    <route id="kl" edges="k_19 19_l"/>
    <route id="ka" edges="k_19 19_18 18_17 17_6 6_3 3_a"/>
    <route id="kb" edges="k_19 19_b"/>
    
    <route id="lk" edges="l_19 19_k"/>
    <route id="la" edges="l_19 19_18 18_17 17_6 6_3 3_a"/>
    <route id="lb" edges="l_19 19_b"/>

        """,
        file=routes,
    )

    veh_nr = 400000  # Bicycles start at 400000

    # Route IDs and corresponding loads
    route_ids = [
        # From a (horizontal)
        "ab",
        "ac",
        "ad",
        "ae",
        "af",
        "ag",
        "ah",
        "ai",
        "aj",
        "ak",
        "al",
        # From b (horizontal)
        "ba",
        "bk",
        "bl",
        "bi",
        "bj",
        "bg",
        "bh",
        "be",
        "bf",
        "bc",
        "bd",
        # From c
        "cd",
        "ca",
        "cb",
        # From d
        "dc",
        "da",
        "db",
        # From e
        "ef",
        "ea",
        "eb",
        # From f
        "fe",
        "fa",
        "fb",
        # From g
        "gh",
        "ga",
        "gb",
        # From h
        "hg",
        "ha",
        "hb",
        # From i
        "ij",
        "ia",
        "ib",
        # From j
        "ji",
        "ja",
        "jb",
        # From k
        "kl",
        "ka",
        "kb",
        # From l
        "lk",
        "la",
        "lb",
    ]

    loads = [
        # From a
        straight_major * STRAIGHT_TRAFFIC_RATIO,  # ab
        turn_major,
        turn_major,  # ac, ad
        straight_major * turn_major,
        straight_major * turn_major,  # ae, af
        straight_major * turn_major,
        straight_major * turn_major,  # ag, ah
        straight_major * turn_major,
        straight_major * turn_major,  # ai, aj
        straight_major * turn_major,
        straight_major * turn_major,  # ak, al
        # From b
        straight_major * STRAIGHT_TRAFFIC_RATIO,  # ba
        turn_major,
        turn_major,  # bk, bl
        straight_major * turn_major,
        straight_major * turn_major,  # bi, bj
        straight_major * turn_major,
        straight_major * turn_major,  # bg, bh
        straight_major * turn_major,
        straight_major * turn_major,  # be, bf
        straight_major * turn_major,
        straight_major * turn_major,  # bc, bd
        # From c
        straight_minor,
        turn_minor,
        turn_minor * STRAIGHT_TRAFFIC_RATIO,
        # From d
        straight_minor,
        turn_minor,
        turn_minor * STRAIGHT_TRAFFIC_RATIO,
        # From e
        straight_minor,
        turn_minor,
        turn_minor * STRAIGHT_TRAFFIC_RATIO,
        # From f
        straight_minor,
        turn_minor,
        turn_minor * STRAIGHT_TRAFFIC_RATIO,
        # From g
        straight_minor,
        turn_minor,
        turn_minor * STRAIGHT_TRAFFIC_RATIO,
        # From h
        straight_minor,
        turn_minor,
        turn_minor * STRAIGHT_TRAFFIC_RATIO,
        # From i
        straight_minor,
        turn_minor,
        turn_minor * STRAIGHT_TRAFFIC_RATIO,
        # From j
        straight_minor,
        turn_minor,
        turn_minor * STRAIGHT_TRAFFIC_RATIO,
        # From k
        straight_minor,
        turn_minor,
        turn_minor * STRAIGHT_TRAFFIC_RATIO,
        # From l
        straight_minor,
        turn_minor,
        turn_minor * STRAIGHT_TRAFFIC_RATIO,
    ]

    for loop_number in range(simulation_limit):
        for route_id, load in zip(route_ids, loads):
            if random.uniform(0, 1) < load:
                print(
                    f'    <vehicle id="{veh_nr}" type="Raleigh" route="{route_id}" depart="{loop_number}" departLane="free" departSpeed="random" />',
                    file=routes,
                )
                veh_nr += 1

    print("</routes>", file=routes)
    routes.close()
    return veh_nr - 400000


def generate_pedestrian_routes(peds_per_hour, simulation_limit):
    """Generate pedestrian routes for multi-agent 5-TLS network."""

    ped_we, ped_sn = calculate_traffic_load(peds_per_hour)
    ped_ew = ped_we
    ped_ns = ped_sn

    routes = open(f"{ROUTES_DIR}/pedestrian.rou.xml", "w")
    print(
        """<routes>

    <vType id="Berliner" accel="0.5" decel="1.0" sigma="0.5" length="0.5" maxSpeed="1.5" minGap="1.0" color="255,165,0" guiShape="pedestrian" width="0.5" vClass="pedestrian"/>  

    <!-- Horizontal pedestrian routes (through the corridor) -->
    <!--  Horizontal Arterial - 5 Intersections @ 1km spacing -->
    <!-- 


                    c              e              g              i              k
                    │              │              │              │              │
                    9             13             26             30             34
                    │              │              │              │              │
                   10             14             27             31             35
                    │              │              │              │              │
   a────1────2────[3]────4────5──[6]────7───20─[17]───21───22─[18]───23───24─[19]───25────8────b
                    │              │              │              │              │
                   11             15             28             32             36
                    │              │              │              │              │
                   12             16             29             33             37
                    │              │              │              │              │
                    d              f              h              j              l


   x=-1100        x=0          x=1000         x=2000         x=3000         x=4000        x=5100
   (Entry)      TLS-1          TLS-2          TLS-3          TLS-4          TLS-5         (Exit)

    -->

    <route id="we1" edges="a_3 3_6"/>
    <route id="we2" edges="3_6 6_17"/>
    <route id="we3" edges="6_17 17_18"/>
    <route id="we4" edges="17_18 18_19"/>
    <route id="we5" edges="18_19 19_b"/>
    
    <route id="ew1" edges="b_19 19_18"/>
    <route id="ew2" edges="19_18 18_17"/>
    <route id="ew3" edges="18_17 17_6"/>
    <route id="ew4" edges="17_6 6_3"/>
    <route id="ew5" edges="6_3 3_a"/>
    
    <!-- Vertical pedestrian routes (crossing at each TLS) -->
    <route id="sn1" edges="c_3 3_d"/>
    <route id="ns1" edges="d_3 3_c"/>
    <route id="sn2" edges="e_6 6_f"/>
    <route id="ns2" edges="f_6 6_e"/>
    <route id="sn3" edges="g_17 17_h"/>
    <route id="ns3" edges="h_17 17_g"/>
    <route id="sn4" edges="i_18 18_j"/>
    <route id="ns4" edges="j_18 18_i"/>
    <route id="sn5" edges="k_19 19_l"/>
    <route id="ns5" edges="l_19 19_k"/>
                    
        """,
        file=routes,
    )

    veh_nr = 800000  # Pedestrians start at 800000

    # Route IDs and loads
    route_ids = [
        "we1",
        "we2",
        "we3",
        "we4",
        "we5",  # West to East segments
        "ew1",
        "ew2",
        "ew3",
        "ew4",
        "ew5",  # East to West segments
        "sn1",
        "ns1",  # TLS-1 vertical
        "sn2",
        "ns2",  # TLS-2 vertical
        "sn3",
        "ns3",  # TLS-3 vertical
        "sn4",
        "ns4",  # TLS-4 vertical
        "sn5",
        "ns5",  # TLS-5 vertical
    ]

    ped_loads = [
        ped_we,
        ped_we,
        ped_we,
        ped_we,
        ped_we,  # W->E
        ped_ew,
        ped_ew,
        ped_ew,
        ped_ew,
        ped_ew,  # E->W
        ped_sn,
        ped_ns,  # TLS-1
        ped_sn,
        ped_ns,  # TLS-2
        ped_sn,
        ped_ns,  # TLS-3
        ped_sn,
        ped_ns,  # TLS-4
        ped_sn,
        ped_ns,  # TLS-5
    ]

    for loop_number in range(simulation_limit):
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
    return veh_nr - 800000


def generate_bus_routes(buses_per_hour, simulation_limit):
    """
    Generate bus routes for multi-agent 5-TLS network.

    Buses run on the horizontal arterial (through road) only.
    10 bus stops: 5 eastbound + 5 westbound
    """
    routes = open(f"{ROUTES_DIR}/bus.rou.xml", "w")
    print(
        """<routes>

    <vType id="bus" accel="2.6" decel="4.5" sigma="0.5" length="12" minGap="3" maxSpeed="70" color="1,0,0" guiShape="bus" vClass="bus" emissionClass="HBEFA3/Bus"/>
""",
        file=routes,
    )

    # Handle string values like 'every_15min'
    if isinstance(buses_per_hour, str):
        bus_interval = 900  # Default: every 15 minutes
    else:
        bus_interval = 3600 / buses_per_hour if buses_per_hour > 0 else 900

    bus_id = 0
    depart_time = 0

    while depart_time < simulation_limit:
        # Eastbound bus (a -> b)
        print(
            f"""    <vehicle id="bus_{bus_id}" depart="{depart_time}" departPos="0" departLane="best" arrivalPos="-1" type="bus">
        <route edges="a_1 1_2 2_3 3_4 4_5 5_6 6_7 7_20 20_17 17_21 21_22 22_18 18_23 23_24 24_19 19_25 25_8 8_b"/>
        <stop busStop="Stop#1" duration="20"/>
        <stop busStop="Stop#2" duration="20"/>
        <stop busStop="Stop#3" duration="20"/>
        <stop busStop="Stop#4" duration="20"/>
        <stop busStop="Stop#5" duration="20"/>
    </vehicle>""",
            file=routes,
        )
        bus_id += 1

        # Westbound bus (b -> a)
        print(
            f"""    <vehicle id="bus_{bus_id}" depart="{depart_time}" departPos="0" departLane="best" arrivalPos="-1" type="bus">
        <route edges="b_8 8_25 25_19 19_24 24_23 23_18 18_22 22_21 21_17 17_20 20_7 7_6 6_5 5_4 4_3 3_2 2_1 1_a"/>
        <stop busStop="Stop#6" duration="20"/>
        <stop busStop="Stop#7" duration="20"/>
        <stop busStop="Stop#8" duration="20"/>
        <stop busStop="Stop#9" duration="20"/>
        <stop busStop="Stop#10" duration="20"/>
    </vehicle>
""",
            file=routes,
        )
        bus_id += 1

        depart_time += bus_interval

    print("</routes>", file=routes)
    routes.close()
    return bus_id


def generate_all_routes(traffic_config, simulation_limit):
    """
    Generate all route files for multi-agent 5-TLS network.

    Args:
        traffic_config (dict): Traffic configuration with keys:
            'cars', 'bicycles', 'pedestrians', 'buses', 'scenario_name'
        simulation_limit (int): Simulation duration in seconds

    Example:
        config = {'cars': 400, 'bicycles': 200, 'pedestrians': 100, 'buses': 4, 'scenario_name': 'test'}
        generate_all_routes(config, simulation_limit=3600)
    """
    print(f"\n{'=' * 60}")
    print(
        f"Generating MULTI-AGENT routes for scenario: {traffic_config.get('scenario_name', 'unknown')}"
    )
    print(f"{'=' * 60}")
    print(f"  Cars: {traffic_config['cars']}/hr")
    print(f"  Bicycles: {traffic_config['bicycles']}/hr")
    print(f"  Pedestrians: {traffic_config['pedestrians']}/hr")
    print(f"  Buses: {traffic_config.get('buses', 4)}/hr")
    print(f"  Simulation duration: {simulation_limit}s")

    # Create routes directory if it doesn't exist
    os.makedirs(ROUTES_DIR, exist_ok=True)

    car_count = generate_car_routes(traffic_config["cars"], simulation_limit)
    bike_count = generate_bicycle_routes(traffic_config["bicycles"], simulation_limit)
    ped_count = generate_pedestrian_routes(
        traffic_config["pedestrians"], simulation_limit
    )
    bus_count = generate_bus_routes(traffic_config.get("buses", 4), simulation_limit)

    print("\n✓ Multi-agent route generation complete")
    print(
        f"  Generated: {car_count} cars, {bike_count} bicycles, {ped_count} pedestrians, {bus_count} buses"
    )
    print(f"  Output: {ROUTES_DIR}/")
    print()


if __name__ == "__main__":
    # Example usage
    test_config = {
        "cars": 400,
        "bicycles": 200,
        "pedestrians": 100,
        "buses": 4,
        "scenario_name": "Multi-Agent Test",
    }
    generate_all_routes(test_config, simulation_limit=3600)
