import random
from constants import (
    simulationLimit,
    numberOfPrivateCarPerHour,
    minorToMajorTrafficRatio,
    straightTrafficRatio,
    turnRatio,
)


# d        f
# |        |
# |        |
# |        |
# a ------------------------------ b
# |        |
# |        |
# |        |
# c        e


# ----------------------
# |  |a   |b   |c   |d   |e   |f   |
# ----------------------
# |a |0.00|0.64|0.10|0.10|0.08|0.08|
# ----------------------
# |b |  |  |  |  |  |  |
# ----------------------
# |c |  |  |  |  |  |  |
# ----------------------
# |d |  |  |  |  |  |  |
# ----------------------
# |e |  |  |  |  |  |  |
# ----------------------
# |f |  |  |  |  |  |  |
# ----------------------


for trafficLoad in [numberOfPrivateCarPerHour]:
    tHorLoad = float(trafficLoad) / 3600

    acLoad = turnRatio * tHorLoad  # 1
    adLoad = turnRatio * tHorLoad  # 2
    aeLoad = straightTrafficRatio * turnRatio * tHorLoad  # 3
    afLoad = straightTrafficRatio * turnRatio * tHorLoad  # 4
    abLoad = straightTrafficRatio * straightTrafficRatio * tHorLoad  # 5 WE

    bfLoad = turnRatio * tHorLoad  # 6
    beLoad = turnRatio * tHorLoad  # 7
    baLoad = straightTrafficRatio * straightTrafficRatio * tHorLoad  # 8
    bdLoad = straightTrafficRatio * turnRatio * tHorLoad  # 9
    bcLoad = straightTrafficRatio * turnRatio * tHorLoad  # 10

    for trafficLoad in [numberOfPrivateCarPerHour]:
        tVerLoad = minorToMajorTrafficRatio * float(trafficLoad) / 3600

        dcLoad = straightTrafficRatio * tVerLoad  # 11
        daLoad = turnRatio * tVerLoad  # 12
        dbLoad = straightTrafficRatio * turnRatio * tVerLoad  # 13
        dfLoad = turnRatio * turnRatio * tVerLoad  # 14
        deLoad = turnRatio * turnRatio * tVerLoad  # 15

        caLoad = turnRatio * tVerLoad  # 16
        cdLoad = straightTrafficRatio * tVerLoad  # 17 SN
        cfLoad = turnRatio * turnRatio * tVerLoad  # 18
        ceLoad = turnRatio * turnRatio * tVerLoad  # 19
        cbLoad = straightTrafficRatio * turnRatio * tVerLoad  # 20

        fbLoad = turnRatio * tVerLoad  # 21
        feLoad = straightTrafficRatio * tVerLoad  # 22
        fdLoad = turnRatio * turnRatio * tVerLoad  # 23
        fcLoad = turnRatio * turnRatio * tVerLoad  # 24
        faLoad = straightTrafficRatio * turnRatio * tVerLoad  # 25

        ebLoad = turnRatio * tVerLoad  # 26
        efLoad = straightTrafficRatio * tVerLoad  # 27
        edLoad = turnRatio * turnRatio * tVerLoad  # 28
        ecLoad = turnRatio * turnRatio * tVerLoad  # 29
        eaLoad = straightTrafficRatio * turnRatio * tVerLoad  # 30

        # acLoad adLoad aeLoad afLoad abLoad
        # bfLoad beLoad baLoad  bdLoad bcLoad
        # dcLoad daLoad dbLoad dfLoad deLoad
        # caLoad cdLoad cfLoad ceLoad cbLoad
        # fbLoad feLoad fdLoad fcLoad faLoad
        # ebLoad  efLoad edLoad ecLoad eaLoad

        routes = open(
            "../infrastructure/developed/common/routes/privateCar.rou.xml", "w"
        )
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

        lastVeh = 0
        vehNr = 0

        for loopNumber in range(simulationLimit):
            if random.uniform(0, 1) < acLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="1" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < adLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="2" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < aeLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="3" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < afLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="4" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < abLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="5" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1

            if random.uniform(0, 1) < bfLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="6" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < beLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="7" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < baLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="8" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < bdLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="9" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < bcLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="10" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1

            if random.uniform(0, 1) < dcLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="11" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < daLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="12" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < dbLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="13" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < dfLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="14" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < deLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="15" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1

            if random.uniform(0, 1) < caLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="16" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < cdLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="17" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < cfLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="18" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < ceLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="19" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < cbLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="20" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1

            if random.uniform(0, 1) < fbLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="21" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < feLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="22" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < fdLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="23" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < fcLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="24" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < faLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="25" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1

            if random.uniform(0, 1) < ebLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="26" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < efLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="27" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < edLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="28" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < ecLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="29" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1
            if random.uniform(0, 1) < eaLoad:
                print(
                    '    <vehicle id="%i" type="Volkswagen" route="30" depart="%i" departLane="free" departSpeed="random" />'
                    % (vehNr, loopNumber),
                    file=routes,
                )
                vehNr += 1

        print("</routes>", file=routes)
        routes.close()
