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

<div align="center">
<img src="images/1/phase_structure.png" alt="Phase Structure Diagram" width="400" height=auto/>
<p align="center">figure: Four-phase signal control structure showing permitted movements and transitions. Yellow intervals separate conflicting phases to ensure safety.</p>
</div>

##### 1. Introduction

###### 1.1 Motivation and Background

###### 1.2 Limitations of Traditional Approaches

###### 1.3 Deep Reinforcement Learning for Traffic Control

###### 1.4 Research Contributions

---

##### 2. Related Work

###### 2.1 Traditional Traffic Signal Control

###### 2.2 Adaptive and Actuated Control Systems

###### 2.3 Deep Reinforcement Learning in Traffic Management

###### 2.4 Multi-Modal Intersection Control

###### 2.5 Experience Replay Mechanisms

###### 2.6 Research Gap and Positioning

---

##### 3. Problem Formulation

###### 3.1 Markov Decision Process Framework

###### 3.2 State Space Definition

###### 3.3 Action Space Definition

###### 3.4 Reward Function Overview

###### 3.5 Transition Dynamics

###### 3.6 Control Objective

---

##### 4. System Architecture

###### 4.1 Network Topology

###### 4.2 Intersection Configuration

###### 4.3 Phase Structure

###### 4.4 Detector Infrastructure

###### 4.5 Centralized Control Strategy

---

##### 5. Deep Q-Network Architecture

###### 5.1 Q-Function Approximation

###### 5.2 Network Architecture Design

###### 5.3 Action Selection Strategy

###### 5.4 Prioritized Experience Replay

###### 5.5 Double DQN Training Algorithm

---

##### 6. Multi-Objective Reward Function

###### 6.1 Reward Design Philosophy

###### 6.2 Environmental Feedback Components

###### 6.3 Meta-Level Guidance Components

###### 6.4 Safety and Constraint Enforcement

###### 6.5 Component Weighting and Tuning

---

##### 7. Training Methodology

###### 7.1 Training Data Generation

###### 7.2 Episode Structure and Procedure

###### 7.3 Hyperparameter Configuration

###### 7.4 Two-Phase Training Strategy

###### 7.5 Convergence Analysis

---

##### 8. Experimental Setup

###### 8.1 Simulation Environment (SUMO)

###### 8.2 Traffic Demand Generation

###### 8.3 Test Scenario Design

###### 8.4 Baseline Control Strategies

###### 8.5 Performance Metrics

---

##### 9. Results and Analysis

###### 9.1 Training Performance

###### 9.2 Waiting Time Analysis

###### 9.3 Modal Equity Evaluation

###### 9.4 Safety and Blocking Events

###### 9.5 Comparative Performance Analysis

###### 9.6 Scenario-Specific Insights

---

##### 10. Discussion

###### 10.1 Key Findings

###### 10.2 Trade-offs and Design Choices

###### 10.3 Scalability Considerations

###### 10.4 Practical Deployment Implications

###### 10.5 Limitations

---

##### 11. Conclusion

###### 11.1 Summary of Contributions

###### 11.2 Impact on Multi-Modal Traffic Control

###### 11.3 Future Research Directions

---

# References

---

# Appendices

###### Appendix A: Detailed Hyperparameters

###### Appendix B: Complete Test Results

###### Appendix C: Phase Timing Thresholds

###### Appendix D: Reward Component Specifications
