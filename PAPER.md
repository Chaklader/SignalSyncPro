# Deep Reinforcement Learning with Prioritized Experience Replay for Adaptive Multi-Modal Traffic Signal Control

Multimodal urban intersections require balancing the needs of vehicles, bicycles, pedestrians, and public transit.
Current traffic signal control systems either prioritize vehicles (Reference Control) or use fixed rule-based logic for
multimodal coordination (Developed Control).

We propose a Deep Q-Network (DQN) with Prioritized Experience Replay (PER) that learns optimal signal control policies
for multimodal intersections. The PER mechanism prioritizes learning from rare but critical events such as pedestrian
exclusive phase activation, bus priority conflicts, and synchronization failures.

We evaluate our approach on 27 traffic scenarios using SUMO simulation, comparing against two baselines: a conventional
vehicle-centric control (Reference) and a rule-based multimodal control (Developed). Results show that DRL-PER achieves:

- 60-85% reduction in bicycle waiting time vs. Reference
- 15-25% improvement over rule-based control (Developed)
- 82% synchronization success rate (vs. 60% for rule-based)
- Better handling of rare events through prioritized learning

Our approach demonstrates that combining deep reinforcement learning with prioritized experience replay enables adaptive
multimodal coordination that outperforms both conventional and rule-based approaches.





