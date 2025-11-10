# Deep Reinforcement Learning with Prioritized Experience Replay for Adaptive Multi-Modal Traffic Signal Control

**Abstract**

Urban traffic signal control systems face increasing complexity as cities prioritize multi-modal transportation
infrastructure serving private vehicles, bicycles, pedestrians, and public transit. Traditional approaches either
optimize for vehicular throughput at the expense of other modes (Reference Control) or rely on fixed rule-based
heuristics for modal coordination (Developed Control), both proving inadequate for dynamic, high-density urban
environments. This paper presents a Deep Q-Network (DQN) architecture augmented with Prioritized Experience Replay (PER)
that learns adaptive signal control policies for multi-modal intersections through reinforcement learning. The PER
mechanism addresses the challenge of rare but critical traffic events—such as bus priority conflicts, signal
synchronization opportunities, and extreme traffic volume conditions—by preferentially sampling high-temporal-difference
experiences during training, accelerating convergence and improving policy quality. Our agent operates on a
32-dimensional state space capturing queue lengths, phase states, waiting times, and modal demands across a
two-intersection corridor network with four signal phases (major through, major left, minor through, minor left),
selecting from three actions: Continue current phase, Skip to Phase 1 (arterial coordination), or advance to Next Phase.
Training employed a two-phase methodology over 200 episodes with progressive reward function recalibration to achieve
target action distribution ratios (85% Continue, 2.5% Skip, 12.5% Next) while maintaining multi-modal service equity.
Extensive evaluation across 30 systematically designed traffic scenarios (varying private car, bicycle, and pedestrian
volumes from 100-1000/hour) using SUMO simulation demonstrates that DRL-PER achieves transformational improvements for
vulnerable road users: 88.6% reduction in bicycle waiting times (from 208.5s to 23.8s), 93.6% reduction in pedestrian
waiting times (from 48.4s to 3.1s), and 83.3% reduction in bus waiting times (from 25.2s to 4.2s) compared to Reference
Control. Compared to the rule-based Developed Control, the agent achieves 50.5% improvement for bicycles, 81.8% for
pedestrians, and 74.1% for buses. This multi-modal optimization comes with a trade-off of 20.0% higher private car
waiting times (43.8s vs 36.5s) compared to Developed Control, reflecting the agent's learned priority for vulnerable
road users and public transit. Our results validate that combining deep reinforcement learning with prioritized
experience replay enables adaptive, equity-focused traffic signal coordination that fundamentally rebalances urban
intersection priorities toward sustainable and inclusive mobility.

**Keywords:** Deep Reinforcement Learning, Traffic Signal Control, Multi-Modal Transportation, Prioritized Experience
Replay, DQN, Adaptive Control, Urban Mobility

---

---

---

---
