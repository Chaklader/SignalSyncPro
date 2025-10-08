import random 
from constants import simulationLimit , numberOfPedestrianPerHour, minorToMajorTrafficRatio


for pedWE in [numberOfPedestrianPerHour]: 

    pedWE = float(pedWE)/3600  
    pedEW = pedWE  

    for pedSN in [numberOfPedestrianPerHour]: 

        pedSN = minorToMajorTrafficRatio*float(pedSN)/3600  
        pedNS = pedSN  

        
        
        # <route id="b" edges="a_3 3_d"/>
        # <route id="d" edges="6_3 3_c"/>
        # <route id="f" edges="c_3 3_a"/>
        # <route id="h" edges="d_3 3_6"/>
        # <route id="j" edges="3_6 6_f"/>
        # <route id="!" edges="b_6 6_e"/>
        # <route id="n" edges="e_6 6_3"/>
        # <route id="p" edges="f_6 6_b"/>
		
        routes = open("pedestrian.rou.xml", "w")
        print("""<routes>


            <vType id="Berliner" accel="0.5" decel="1.0" sigma="0.5" length="0.5" maxSpeed="1.5" minGap="1.0" color="255,165,0" guiShape="pedestrian"  width ="0.5" vClass="pedestrian"/>  

            
            <route id="a" edges="a_3 3_6"/>

            <route id="c" edges="6_3 3_a"/>
            
            <route id="e" edges="c_3 3_d"/>

            <route id="g" edges="d_3 3_c"/>

            <route id="i" edges="3_6 6_b"/>
 
            
            <route id="k" edges="b_6 6_3"/>
                        
            <route id="m" edges="e_6 6_f"/>
           
            <route id="o" edges="f_6 6_e"/>
                        
        """, file=routes)        
          

        pedNr = 800000 # max bicycle = 7,00,000 (=4,00,000 + 3,00,000)
        

        for loopNumber in range(simulationLimit):

            if random.uniform(0,1) < pedWE:         
                print('    <vehicle id="%i" type="Berliner" route="a" depart="%i" departLane="free" departSpeed="random" />' % (pedNr, loopNumber), file=routes)
                pedNr = pedNr + 1

            if random.uniform(0,1) < pedEW:        
                print('    <vehicle id="%i" type="Berliner" route="c" depart="%i" departLane="free" departSpeed="random" />' % (pedNr, loopNumber), file=routes)
                pedNr = pedNr + 1
 
            if random.uniform(0,1) < pedSN:           
                print('    <vehicle id="%i" type="Berliner" route="e" depart="%i" departLane="free" departSpeed="random" />' % (pedNr, loopNumber), file=routes)
                pedNr = pedNr + 1
  
            if random.uniform(0,1) < pedNS:            
                print('    <vehicle id="%i" type="Berliner" route="g" depart="%i" departLane="free" departSpeed="random" />' % (pedNr, loopNumber), file=routes)
                pedNr = pedNr + 1
  
            if random.uniform(0,1) < pedWE:          
                print('    <vehicle id="%i" type="Berliner" route="i" depart="%i" departLane="free" departSpeed="random" />' % (pedNr, loopNumber), file=routes)
                pedNr = pedNr + 1
            if random.uniform(0,1) < pedEW:        
                print('    <vehicle id="%i" type="Berliner" route="k" depart="%i" departLane="free" departSpeed="random" />' % (pedNr, loopNumber), file=routes)
                pedNr = pedNr + 1
    
            if random.uniform(0,1) < pedSN:            
                print('    <vehicle id="%i" type="Berliner" route="m" depart="%i" departLane="free" departSpeed="random" />' % (pedNr, loopNumber), file=routes)
                pedNr = pedNr + 1
   
            if random.uniform(0,1) < pedNS:          
                print('    <vehicle id="%i" type="Berliner" route="o" depart="%i" departLane="free" departSpeed="random" />' % (pedNr, loopNumber), file=routes)
                pedNr = pedNr + 1
            
            
            # diagonal traffic volume 
            
            # if (current_phase == pedestrian priority phase for certain node)
            
            # then generate these traffic volumen 
            
            # if random.uniform(0,1) < pedSN:            
                # print >> routes, '    <vehicle id="%i" type="Berliner" route="n" depart="%i" departLane="free" departSpeed="random" />' % (pedNr, loopNumber), file=routes)
                # pedNr = pedNr + 1
             
			# '!' is used 
            # if random.uniform(0,1) < pedEW:            
                # print >> routes, '    <vehicle id="%i" type="Berliner" route="!" depart="%i" departLane="free" departSpeed="random" />' % (pedNr, loopNumber), file=routes)
                # pedNr = pedNr + 1
            
            # if random.uniform(0,1) < pedWE:         
                # print >> routes, '    <vehicle id="%i" type="Berliner" route="j" depart="%i" departLane="free" departSpeed="random" />' % (pedNr,loopNumber)
                # pedNr = pedNr + 1
                
            # if random.uniform(0,1) < pedNS:             
                # print >> routes, '    <vehicle id="%i" type="Berliner" route="h" depart="%i" departLane="free" departSpeed="random" />' % (pedNr, loopNumber), file=routes)
                # pedNr = pedNr + 1
                
            # if random.uniform(0,1) < pedSN:           
                # print >> routes, '    <vehicle id="%i" type="Berliner" route="f" depart="%i" departLane="free" departSpeed="random" />' % (pedNr, loopNumber), file=routes)
                # pedNr = pedNr + 1
                
            # if random.uniform(0,1) < pedEW:         
                # print >> routes, '    <vehicle id="%i" type="Berliner" route="d" depart="%i" departLane="free" departSpeed="random" />' % (pedNr, loopNumber), file=routes)
                # pedNr = pedNr + 1
                
            # if random.uniform(0,1) < pedWE:             
                # print >> routes, '    <vehicle id="%i" type="Berliner" route="b" depart="%i" departLane="free" departSpeed="random" />' % (pedNr,loopNumber)
                # pedNr = pedNr + 1
                
            # if random.uniform(0,1) < pedWE:             
                # print >> routes, '    <vehicle id="%i" type="Berliner" route="b" depart="%i" departLane="free" departSpeed="random" />' % (pedNr,loopNumber)
                # pedNr = pedNr + 1            
                
            # if random.uniform(0,1) < pedNS:             
                # print >> routes, '    <vehicle id="%i" type="Berliner" route="p" depart="%i" departLane="free" departSpeed="random" />' % (pedNr, loopNumber), file=routes)
                # pedNr = pedNr + 1
                       
                
        print("</routes>", file=routes)
        routes.close()
