import random 
from constants import simulationLimit , numberOfBiCyclePerHour, minorToMajorTrafficRatio, straightTrafficRatio, turnRatio


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

# may be reduce bicycle left turns 

# pWE, pSN  
for trafficLoad in [numberOfBiCyclePerHour]: 

    tHorLoad = float(trafficLoad)/3600 
    
    acLoad = turnRatio*tHorLoad   #1 
    adLoad = turnRatio*tHorLoad   #2 
    aeLoad = straightTrafficRatio*turnRatio*tHorLoad  #3
    afLoad = straightTrafficRatio*turnRatio*tHorLoad  #4
    abLoad = straightTrafficRatio*straightTrafficRatio*tHorLoad  #5 WE 
    
    
    bfLoad = turnRatio*tHorLoad   #6
    beLoad = turnRatio*tHorLoad   #7
    baLoad = straightTrafficRatio*straightTrafficRatio*tHorLoad  #8
    bdLoad = straightTrafficRatio*turnRatio*tHorLoad  #9
    bcLoad = straightTrafficRatio*turnRatio*tHorLoad  #10
    
    
    for trafficLoad in [numberOfBiCyclePerHour]:
    
        tVerLoad = minorToMajorTrafficRatio*float(trafficLoad)/3600
    
        dcLoad = straightTrafficRatio*tVerLoad   #11
        daLoad = turnRatio*tVerLoad   #12
        dbLoad = straightTrafficRatio*turnRatio*tVerLoad  #13
        dfLoad = turnRatio*turnRatio*tVerLoad  #14
        deLoad = turnRatio*turnRatio*tVerLoad  #15
        

        caLoad = turnRatio*tVerLoad   #16
        cdLoad = straightTrafficRatio*tVerLoad   #17 SN 
        cfLoad = turnRatio*turnRatio*tVerLoad  #18
        ceLoad = turnRatio*turnRatio*tVerLoad  #19
        cbLoad = straightTrafficRatio*turnRatio*tVerLoad  #20
        
        fbLoad = turnRatio*tVerLoad   #21
        feLoad = straightTrafficRatio*tVerLoad   #22
        fdLoad = turnRatio*turnRatio*tVerLoad  #23
        fcLoad = turnRatio*turnRatio*tVerLoad  #24
        faLoad = straightTrafficRatio*turnRatio*tVerLoad  #25
        
        
        ebLoad = turnRatio*tVerLoad   #26
        efLoad = straightTrafficRatio*tVerLoad   #27
        edLoad = turnRatio*turnRatio*tVerLoad  #28
        ecLoad = turnRatio*turnRatio*tVerLoad  #29
        eaLoad = straightTrafficRatio*turnRatio*tVerLoad  #30


        # acLoad adLoad aeLoad afLoad abLoad 
        # bfLoad beLoad baLoad  bdLoad bcLoad
        # dcLoad daLoad dbLoad dfLoad deLoad 
        # caLoad cdLoad cfLoad ceLoad cbLoad
        # fbLoad feLoad fdLoad fcLoad faLoad   
        # ebLoad  efLoad edLoad ecLoad eaLoad
        
        

        # max 5.6 m/s = 20 km/hour 
        
        routes = open("../infrastructure/developed/routes/bicycle.rou.xml", "w")
        print("""<routes>
        
            <vType id="Raleigh" accel="2.0" decel="3.0" sigma="0.5" length="2.5" maxSpeed="5.6" color="0,255,255" guiShape="bicycle" width ="1.0" vClass="bicycle"/>  
        
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
                        
        """, file=routes)

        bikeNr = 400000    # max car = 3,00,000
       
        for loopNumber in range(simulationLimit):
        
            if random.uniform(0,1) < acLoad: 
                print('    <vehicle id="%i" type="Raleigh" route="l" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr = bikeNr + 1
            if random.uniform(0,1) < adLoad:
                print('    <vehicle id="%i" type="Raleigh" route="ll" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
            if random.uniform(0,1) < aeLoad:
                print('    <vehicle id="%i" type="Raleigh" route="lll" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1  

            # creating deadlock 
            
            if random.uniform(0,1) < afLoad:
                print('    <vehicle id="%i" type="Raleigh" route="lV" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
                
            if random.uniform(0, 1) <  abLoad:
                print('    <vehicle id="%i" type="Raleigh" route="V" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
                
                
            if random.uniform(0,1) < bfLoad: # Poisson distribution
                print('    <vehicle id="%i" type="Raleigh" route="Vl" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1       
            if random.uniform(0,1) < beLoad:
                print('    <vehicle id="%i" type="Raleigh" route="Vll" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
            if random.uniform(0,1) <  baLoad:
                print('    <vehicle id="%i" type="Raleigh" route="Vlll" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
            if random.uniform(0,1) < bdLoad:
                print('    <vehicle id="%i" type="Raleigh" route="lX" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
            if random.uniform(0, 1) < bcLoad:
                print('    <vehicle id="%i" type="Raleigh" route="X" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
          

                
            if random.uniform(0,1) < dcLoad: # Poisson distribution
                print('    <vehicle id="%i" type="Raleigh" route="Xl" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
            if random.uniform(0,1) <  daLoad:
                print('    <vehicle id="%i" type="Raleigh" route="Xll" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
            if random.uniform(0,1) < dbLoad:
                print('    <vehicle id="%i" type="Raleigh" route="Xlll" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
                
            # these bicycle making dead lock 
            
            if random.uniform(0,1) <  dfLoad:
                print('    <vehicle id="%i" type="Raleigh" route="XlV" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
                
            if random.uniform(0,1) <  deLoad:
                print('    <vehicle id="%i" type="Raleigh" route="XV" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
 
            
            if random.uniform(0,1) < caLoad: # Poisson distribution
                print('    <vehicle id="%i" type="Raleigh" route="XVl" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
            if random.uniform(0,1) <  cdLoad:
                print('    <vehicle id="%i" type="Raleigh" route="XVll" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
            if random.uniform(0,1) <  cfLoad:
                print('    <vehicle id="%i" type="Raleigh" route="XVlll" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
            if random.uniform(0,1) <  ceLoad:
                print('    <vehicle id="%i" type="Raleigh" route="XlX" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
            if random.uniform(0,1) <  cbLoad:
                print('    <vehicle id="%i" type="Raleigh" route="XX" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
             
             

            if random.uniform(0,1) < fbLoad: # Poisson distribution
                print('    <vehicle id="%i" type="Raleigh" route="XXl" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
            if random.uniform(0,1) <  feLoad:
                print('    <vehicle id="%i" type="Raleigh" route="XXll" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
            if random.uniform(0,1) <  fdLoad:
                print('    <vehicle id="%i" type="Raleigh" route="XXlll" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
            if random.uniform(0,1) <  fcLoad:
                print('    <vehicle id="%i" type="Raleigh" route="XXlV" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
            if random.uniform(0,1) <  faLoad:
                print('    <vehicle id="%i" type="Raleigh" route="XXV" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
            
            
            if random.uniform(0,1) < ebLoad: # Poisson distribution
                print('    <vehicle id="%i" type="Raleigh" route="XXVl" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
            if random.uniform(0,1) <   efLoad:
                print('    <vehicle id="%i" type="Raleigh" route="XXVll" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
            if random.uniform(0,1) <  edLoad:
                print('    <vehicle id="%i" type="Raleigh" route="XXVlll" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
            if random.uniform(0,1) <  ecLoad:
                print('    <vehicle id="%i" type="Raleigh" route="XXlX" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
            if random.uniform(0,1) <  eaLoad:
                print('    <vehicle id="%i" type="Raleigh" route="XXX" depart="%i" departLane="free" departSpeed="random" />' % (bikeNr, loopNumber), file=routes)
                bikeNr += 1
     

               
        print("</routes>", file=routes)
        routes.close()
