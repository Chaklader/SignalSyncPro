# MSc Thesis Results - Traffic Signal Control Comparison

## Test Scenario Definitions

All 30 test scenarios use consistent bus frequency (every 15 minutes) with varying volumes for cars, bicycles, and
pedestrians.

### Pr Scenarios (Varying Private Car Volumes)

Constant: 400 bicycles/hr, 400 pedestrians/hr

| Scenario | Cars/hr | Bicycles/hr | Pedestrians/hr | Buses       |
| -------- | ------- | ----------- | -------------- | ----------- |
| Pr_0     | 100     | 400         | 400            | every_15min |
| Pr_1     | 200     | 400         | 400            | every_15min |
| Pr_2     | 300     | 400         | 400            | every_15min |
| Pr_3     | 400     | 400         | 400            | every_15min |
| Pr_4     | 500     | 400         | 400            | every_15min |
| Pr_5     | 600     | 400         | 400            | every_15min |
| Pr_6     | 700     | 400         | 400            | every_15min |
| Pr_7     | 800     | 400         | 400            | every_15min |
| Pr_8     | 900     | 400         | 400            | every_15min |
| Pr_9     | 1000    | 400         | 400            | every_15min |

### Bi Scenarios (Varying Bicycle Volumes)

Constant: 400 cars/hr, 400 pedestrians/hr

| Scenario | Cars/hr | Bicycles/hr | Pedestrians/hr | Buses       |
| -------- | ------- | ----------- | -------------- | ----------- |
| Bi_0     | 400     | 100         | 400            | every_15min |
| Bi_1     | 400     | 200         | 400            | every_15min |
| Bi_2     | 400     | 300         | 400            | every_15min |
| Bi_3     | 400     | 400         | 400            | every_15min |
| Bi_4     | 400     | 500         | 400            | every_15min |
| Bi_5     | 400     | 600         | 400            | every_15min |
| Bi_6     | 400     | 700         | 400            | every_15min |
| Bi_7     | 400     | 800         | 400            | every_15min |
| Bi_8     | 400     | 900         | 400            | every_15min |
| Bi_9     | 400     | 1000        | 400            | every_15min |

### Pe Scenarios (Varying Pedestrian Volumes)

Constant: 400 cars/hr, 400 bicycles/hr

| Scenario | Cars/hr | Bicycles/hr | Pedestrians/hr | Buses       |
| -------- | ------- | ----------- | -------------- | ----------- |
| Pe_0     | 400     | 400         | 100            | every_15min |
| Pe_1     | 400     | 400         | 200            | every_15min |
| Pe_2     | 400     | 400         | 300            | every_15min |
| Pe_3     | 400     | 400         | 400            | every_15min |
| Pe_4     | 400     | 400         | 500            | every_15min |
| Pe_5     | 400     | 400         | 600            | every_15min |
| Pe_6     | 400     | 400         | 700            | every_15min |
| Pe_7     | 400     | 400         | 800            | every_15min |
| Pe_8     | 400     | 400         | 900            | every_15min |
| Pe_9     | 400     | 400         | 1000           | every_15min |

---

## Table 1: Average Waiting Time for Private Cars (seconds)

| Scenario name | Reference control (seconds) | Developed control (seconds) |
| ------------- | --------------------------- | --------------------------- |
| Pr_0          | 19                          | 29                          |
| Pr_1          | 24                          | 31                          |
| Pr_2          | 23                          | 32                          |
| Pr_3          | 21                          | 37                          |
| Pr_4          | 22                          | 35                          |
| Pr_5          | 23                          | 38                          |
| Pr_6          | 24                          | 40                          |
| Pr_7          | 26                          | 42                          |
| Pr_8          | 26                          | 42                          |
| Pr_9          | 26                          | 48                          |
| Bi_0          | 22                          | 33                          |
| Bi_1          | 22                          | 32                          |
| Bi_2          | 22                          | 32                          |
| Bi_3          | 21                          | 37                          |
| Bi_4          | 22                          | 36                          |
| Bi_5          | 21                          | 38                          |
| Bi_6          | 21                          | 40                          |
| Bi_7          | 21                          | 40                          |
| Bi_8          | 22                          | 41                          |
| Bi_9          | 23                          | 43                          |
| Pe_0          | 22                          | 27                          |
| Pe_1          | 22                          | 30                          |
| Pe_2          | 22                          | 34                          |
| Pe_3          | 21                          | 37                          |
| Pe_4          | 23                          | 35                          |
| Pe_5          | 21                          | 36                          |
| Pe_6          | 21                          | 38                          |
| Pe_7          | 22                          | 38                          |
| Pe_8          | 21                          | 39                          |
| Pe_9          | 21                          | 36                          |

---

## Table 2: Average Waiting Time for Bicycles (seconds)

| Scenario name | Reference control (seconds) | Developed control (seconds) |
| ------------- | --------------------------- | --------------------------- |
| Pr_0          | 316                         | 32                          |
| Pr_1          | 348                         | 31                          |
| Pr_2          | 232                         | 31                          |
| Pr_3          | 158                         | 33                          |
| Pr_4          | 64                          | 31                          |
| Pr_5          | 54                          | 32                          |
| Pr_6          | 48                          | 35                          |
| Pr_7          | 48                          | 35                          |
| Pr_8          | 40                          | 35                          |
| Pr_9          | 37                          | 38                          |
| Bi_0          | 25                          | 29                          |
| Bi_1          | 34                          | 28                          |
| Bi_2          | 48                          | 31                          |
| Bi_3          | 158                         | 33                          |
| Bi_4          | 267                         | 35                          |
| Bi_5          | 369                         | 40                          |
| Bi_6          | 507                         | 55                          |
| Bi_7          | 647                         | 66                          |
| Bi_8          | 598                         | 122                         |
| Bi_9          | 667                         | 205                         |
| Pe_0          | 116                         | 25                          |
| Pe_1          | 108                         | 28                          |
| Pe_2          | 152                         | 31                          |
| Pe_3          | 158                         | 33                          |
| Pe_4          | 102                         | 33                          |
| Pe_5          | 113                         | 33                          |
| Pe_6          | 93                          | 35                          |
| Pe_7          | 94                          | 35                          |
| Pe_8          | 88                          | 35                          |
| Pe_9          | 123                         | 34                          |

---

## Table 3: Average Waiting Time for Pedestrians (seconds)

| Scenario name | Reference control (seconds) | Developed control (seconds) |
| ------------- | --------------------------- | --------------------------- |
| Pr_0          | 129                         | 11                          |
| Pr_1          | 69                          | 11                          |
| Pr_2          | 25                          | 11                          |
| Pr_3          | 14                          | 12                          |
| Pr_4          | 13                          | 12                          |
| Pr_5          | 13                          | 13                          |
| Pr_6          | 12                          | 12                          |
| Pr_7          | 12                          | 13                          |
| Pr_8          | 12                          | 14                          |
| Pr_9          | 12                          | 14                          |
| Bi_0          | 12                          | 10                          |
| Bi_1          | 14                          | 11                          |
| Bi_2          | 13                          |                             |
| Bi_3          | 14                          | 12                          |
| Bi_4          | 13                          | 12                          |
| Bi_5          | 15                          | 13                          |
| Bi_6          | 15                          | 13                          |
| Bi_7          | 15                          | 15                          |
| Bi_8          | 17                          | 17                          |
| Bi_9          | 17                          | 15                          |
| Pe_0          | 9                           | 10                          |
| Pe_1          | 9                           | 9                           |
| Pe_2          | 11                          | 11                          |
| Pe_3          | 14                          | 12                          |
| Pe_4          | 48                          | 13                          |
| Pe_5          | 87                          | 17                          |
| Pe_6          | 94                          | 22                          |
| Pe_7          | 105                         | 30                          |
| Pe_8          | 111                         | 35                          |
| Pe_9          | 126                         | 47                          |

---

## Table 4: Average Waiting Time for Buses (seconds)

| Scenario name | Reference control (seconds) | Developed control (seconds) |
| ------------- | --------------------------- | --------------------------- |
| Pr_0          | 26                          | 9                           |
| Pr_1          | 28                          | 12                          |
| Pr_2          | 26                          | 11                          |
| Pr_3          | 26                          | 12                          |
| Pr_4          | 22                          | 24                          |
| Pr_5          | 32                          | 18                          |
| Pr_6          | 21                          | 14                          |
| Pr_7          | 21                          | 21                          |
| Pr_8          | 20                          | 32                          |
| Pr_9          | 24                          | 27                          |
| Bi_0          | 24                          | 14                          |
| Bi_1          | 23                          | 18                          |
| Bi_2          | 23                          | 16                          |
| Bi_3          | 26                          | 12                          |
| Bi_4          | 24                          | 14                          |
| Bi_5          | 27                          | 13                          |
| Bi_6          | 31                          | 17                          |
| Bi_7          | 19                          | 16                          |
| Bi_8          | 22                          | 15                          |
| Bi_9          | 24                          | 17                          |
| Pe_0          | 31                          | 7                           |
| Pe_1          | 21                          | 10                          |
| Pe_2          | 21                          | 12                          |
| Pe_3          | 26                          | 12                          |
| Pe_4          | 22                          | 18                          |
| Pe_5          | 30                          | 17                          |
| Pe_6          | 28                          | 17                          |
| Pe_7          | 29                          | 25                          |
| Pe_8          | 29                          | 17                          |
| Pe_9          | 22                          | 11                          |

---

## Table 5: Total CO₂ Emission (kg)

NOTE: This emission data is for whole simulation (10000s) while our test provides hourly emission data. So, be careful
and intentional when you make comparison.

| Scenario name | Reference control (kg) per 10000s | Developed control (kg) per 10000s |
| ------------- | --------------------------------- | --------------------------------- |
| Pr_0          | 286                               | 292                               |
| Pr_1          | 517                               | 528                               |
| Pr_2          | 749                               | 728                               |
| Pr_3          | 891                               | 964                               |
| Pr_4          | 1080                              | 1073                              |
| Pr_5          | 1241                              | 1299                              |
| Pr_6          | 1404                              | 1427                              |
| Pr_7          | 1557                              | 1595                              |
| Pr_8          | 1678                              | 1743                              |
| Pr_9          | 1804                              | 1941                              |
| Bi_0          | 919                               | 918                               |
| Bi_1          | 923                               | 916                               |
| Bi_2          | 917                               | 921                               |
| Bi_3          | 891                               | 964                               |
| Bi_4          | 926                               | 969                               |
| Bi_5          | 877                               | 917                               |
| Bi_6          | 885                               | 916                               |
| Bi_7          | 857                               | 895                               |
| Bi_8          | 883                               | 900                               |
| Bi_9          | 875                               | 933                               |
| Pe_0          | 904                               | 892                               |
| Pe_1          | 924                               | 930                               |
| Pe_2          | 885                               | 909                               |
| Pe_3          | 891                               | 964                               |
| Pe_4          | 911                               | 911                               |
| Pe_5          | 922                               | 928                               |
| Pe_6          | 877                               | 937                               |
| Pe_7          | 867                               | 915                               |
| Pe_8          | 888                               | 920                               |
| Pe_9          | 889                               | 970                               |

---

**Source:** Institute of Transportation, TU München **Author:** Chaklader Asfak Arefe, July, 2013

---

## Table 6: DRL Agent Test Results - Average Waiting Times (seconds)

| Scenario | Car Wait (s) | Bicycle Wait (s) | Pedestrian Wait (s) | Bus Wait (s) | Safety Violations |
| -------- | ------------ | ---------------- | ------------------- | ------------ | ----------------- |
| Pr_0     | 17.63        | 13.70            | 4.79                | 2.09         | 0                 |
| Pr_1     | 24.29        | 15.04            | 3.00                | 1.94         | 0                 |
| Pr_2     | 33.96        | 19.94            | 5.72                | 2.04         | 0                 |
| Pr_3     | 37.83        | 21.18            | 3.22                | 1.84         | 0                 |
| Pr_4     | 51.07        | 22.40            | 2.76                | 12.08        | 0                 |
| Pr_5     | 50.83        | 23.92            | 4.86                | 10.30        | 0                 |
| Pr_6     | 48.94        | 20.34            | 2.08                | 12.79        | 0                 |
| Pr_7     | 46.55        | 14.86            | 1.16                | 10.87        | 0                 |
| Pr_8     | 44.81        | 13.46            | 0.92                | 14.54        | 0                 |
| Pr_9     | 45.88        | 17.14            | 1.73                | 13.47        | 0                 |
| Bi_0     | 40.14        | 7.05             | 2.01                | 2.31         | 0                 |
| Bi_1     | 45.72        | 9.16             | 1.48                | 2.00         | 0                 |
| Bi_2     | 45.71        | 13.98            | 3.07                | 2.63         | 0                 |
| Bi_3     | 43.86        | 25.49            | 5.21                | 3.25         | 0                 |
| Bi_4     | 49.48        | 32.48            | 2.29                | 3.87         | 0                 |
| Bi_5     | 36.28        | 28.51            | 2.21                | 1.41         | 0                 |
| Bi_6     | 48.98        | 43.05            | 5.21                | 2.42         | 0                 |
| Bi_7     | 42.14        | 39.49            | 2.91                | 2.68         | 0                 |
| Bi_8     | 45.80        | 45.33            | 1.87                | 2.26         | 0                 |
| Bi_9     | 45.55        | 42.40            | 3.82                | 1.69         | 0                 |
| Pe_0     | 40.74        | 17.60            | 1.47                | 3.35         | 0                 |
| Pe_1     | 39.59        | 19.58            | 2.02                | 2.67         | 0                 |
| Pe_2     | 37.45        | 20.70            | 2.25                | 2.73         | 0                 |
| Pe_3     | 41.02        | 22.96            | 2.60                | 2.42         | 0                 |
| Pe_4     | 52.57        | 23.97            | 2.18                | 1.20         | 0                 |
| Pe_5     | 47.86        | 21.39            | 2.92                | 2.12         | 0                 |
| Pe_6     | 45.21        | 24.23            | 4.44                | 2.17         | 0                 |
| Pe_7     | 42.36        | 20.14            | 3.13                | 2.77         | 0                 |
| Pe_8     | 42.23        | 18.97            | 4.84                | 3.47         | 0                 |
| Pe_9     | 49.94        | 23.97            | 3.99                | 4.60         | 0                 |

**Test Date:** November 4, 2025 | **Model:** DRL (DQN) Agent trained for 100 episodes | **Test Duration:** 10,000s per
scenario

---

---

# Training Results

---

---

# Testing Results

## Table 1: Comparison of Phase Transition Behavior Across Traffic Scenarios

| Scenario Group | Scenarios | Total Trans. | Avg. Trans./Scenario | Phases Used |
|----------------|-----------|--------------|----------------------|-------------|
| Private Cars (Pr) | 10 | 6,019 | 601.9 | P1, P2, P3, P4 |
| Bicycles (Bi) | 10 | 5,171 | 517.1 | P1, P2, P3, P4 |
| Pedestrians (Pe) | 10 | 5,217 | 521.7 | P1, P2, P3, P4 |
| **Total** | **30** | **16,407** | **546.9** | -- |

---

## Table 2: Phase Transition Statistics for Private Car Scenarios

| Transition Type | Count | % | Duration (seconds) |||||
|-----------------|-------|---|----|------|-----|-----|
| | | | Min | Mean | Max | Std |
| P1→P2 | 1,819 | 30.2 | 8 | 24.1 | 41 | 11.8 |
| P2→P3 | 1,384 | 23.0 | 3 | 3.3 | 7 | 0.7 |
| P4→P1 | 1,004 | 16.7 | 2 | 2.0 | 2 | 0.0 |
| P3→P4 | 1,003 | 16.7 | 5 | 5.2 | 22 | 1.7 |
| P2→P1 | 431 | 7.2 | 3 | 3.2 | 6 | 0.5 |
| P3→P1 | 378 | 6.3 | 6 | 17.7 | 23 | 2.3 |
| **Total** | **6,019** | **100.0** | -- | **10.6** | -- | -- |

---

## Table 3: Phase Transition Statistics for Bicycle Scenarios

| Transition Type | Count | % | Duration (seconds) |||||
|-----------------|-------|---|----|------|-----|-----|
| | | | Min | Mean | Max | Std |
| P1→P2 | 1,618 | 31.3 | 8 | 30.7 | 40 | 8.0 |
| P2→P3 | 1,181 | 22.8 | 3 | 3.3 | 7 | 0.6 |
| P4→P1 | 770 | 14.9 | 2 | 2.0 | 2 | 0.0 |
| P3→P4 | 761 | 14.7 | 5 | 5.6 | 22 | 2.5 |
| P2→P1 | 434 | 8.4 | 3 | 3.1 | 7 | 0.5 |
| P3→P1 | 407 | 7.9 | 6 | 19.5 | 23 | 1.8 |
| **Total** | **5,171** | **100.0** | -- | **13.3** | -- | -- |

---

## Table 4: Phase Transition Statistics for Pedestrian Scenarios

| Transition Type | Count | % | Duration (seconds) |||||
|-----------------|-------|---|----|------|-----|-----|
| | | | Min | Mean | Max | Std |
| P1→P2 | 1,642 | 31.5 | 8 | 29.8 | 40 | 8.2 |
| P2→P3 | 1,200 | 23.0 | 3 | 3.3 | 7 | 0.6 |
| P4→P1 | 747 | 14.3 | 2 | 2.0 | 2 | 0.0 |
| P3→P4 | 740 | 14.2 | 5 | 5.7 | 23 | 2.7 |
| P3→P1 | 449 | 8.6 | 6 | 18.9 | 23 | 1.8 |
| P2→P1 | 439 | 8.4 | 3 | 3.1 | 6 | 0.4 |
| **Total** | **5,217** | **100.0** | -- | **13.1** | -- | -- |

---

## Table 5: Consolidated Phase Transition Statistics Across All Scenarios

| Transition Type | Private Cars || Bicycles || Pedestrians ||
|-----------------|--------|----------|--------|----------|--------|----------|
| | Count | Mean (s) | Count | Mean (s) | Count | Mean (s) |
| P1→P2 | 1,819 | 24.1 | 1,618 | 30.7 | 1,642 | 29.8 |
| P2→P3 | 1,384 | 3.3 | 1,181 | 3.3 | 1,200 | 3.3 |
| P2→P1 | 431 | 3.2 | 434 | 3.1 | 439 | 3.1 |
| P3→P4 | 1,003 | 5.2 | 761 | 5.6 | 740 | 5.7 |
| P3→P1 | 378 | 17.7 | 407 | 19.5 | 449 | 18.9 |
| P4→P1 | 1,004 | 2.0 | 770 | 2.0 | 747 | 2.0 |
| **Total** | **6,019** | **10.6** | **5,171** | **13.3** | **5,217** | **13.1** |

---

## Analysis Summary

The DRL agent's phase transition behavior was analyzed across 30 evaluation scenarios comprising 10 private car scenarios (Pr_0-Pr_9), 10 bicycle scenarios (Bi_0-Bi_9), and 10 pedestrian scenarios (Pe_0-Pe_9). As shown in **Table 1**, the agent generated **16,407 total phase transitions**, with private car scenarios exhibiting the highest transition frequency (6,019 transitions, 601.9 per scenario on average) compared to bicycle (5,171 transitions, 517.1 per scenario) and pedestrian scenarios (5,217 transitions, 521.7 per scenario).

All three scenario groups utilized the complete four-phase structure (P1: North-South, P2: East-West, P3: Bicycle phase, P4: Pedestrian phase), demonstrating the agent's capability to activate all available phases based on traffic demands. The consolidated transition statistics in **Table 5** reveal distinct patterns across scenario types.

### Key Findings:

**P1→P2 Transition (North-South to East-West)**
- Most frequent transition across all scenarios: 30.2% (Pr), 31.3% (Bi), 31.5% (Pe)
- Significantly shorter mean duration in private car scenarios (24.1s) vs bicycle (30.7s) and pedestrian (29.8s)
- **Interpretation:** Agent adapts phase timing based on traffic composition

**P2→P3 Transition (East-West to Bicycle phase)**
- Consistent short durations across all scenarios (3.3s mean)
- **Interpretation:** Rapid phase advancement behavior

**P4→P1 Transition (Pedestrian to North-South)**
- Constant 2.0s duration with zero variance
- **Interpretation:** Minimum transition time enforced by yellow phase constraint

**P3→P1 Transition (Bicycle phase directly to North-South)**
- Moderate frequency: 6.3-8.6% of transitions
- Substantially longer mean durations (17.7-19.5s)
- **Interpretation:** Agent occasionally maintains bicycle phase for extended periods before returning to primary North-South phase

### Adaptation Patterns:

**High Variability Transitions:**
- P1→P2: std 8.0-11.8s → Responsive adjustments to traffic conditions

**Low Variability Transitions:**
- P2→P3 and P2→P1: std 0.4-0.7s → Deterministic switching behavior for secondary phases

---
