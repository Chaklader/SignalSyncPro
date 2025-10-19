





1. How to I run testing? 

2. How many 3600s episods I need to run for training?

3. Update the traffic data for training and testing 

4. Description of the control strategy 

5. Refactor the codebase and include the reference control 

6. Both reference and previous developed control will need to generate route before we start the simulation. So, we need to have a reset method similar to the DRL control 

7. Need to generate the same format of traffic data output from the DRL simulation 

8. **1. Block Rate: NO Learning**: The agent needs to learn that **continuing current phase** is often better than **changing immediately at 5s**.How to I fix it? 




Need to FIX 

**Warning: Emission classes should always use the model as a prefix, please recheck 'P_7_7'. Starting with SUMO 1.24 this will be an error.**
**Warning: Emission classes should always use the model as a prefix, please recheck 'HDV_12_12'. Starting with SUMO 1.24 this will be an error.**
**Warning: The shape 'bus/city' for vType 'bus' is deprecated, use 'bus' instead.**