#\!/bin/bash
# create_training_tables.sh - Generate training analysis tables and CSV files

if [ $# -eq 0 ]; then
    echo "Usage: $0 <training_log_file>"
    echo "Example: $0 training.log"
    exit 1
fi

LOG_FILE="$1"

if [ \! -f "$LOG_FILE" ]; then
    echo "Error: File '$LOG_FILE' not found\!"
    exit 1
fi

echo "================================================================"
echo "Parsing training log: $LOG_FILE"
echo "================================================================"
echo ""

# Create output directory
OUTPUT_DIR="output/training"
mkdir -p "$OUTPUT_DIR"

# Create output files
SUMMARY_FILE="${OUTPUT_DIR}/tables.md"
EPISODE_METRICS_FILE="${OUTPUT_DIR}/training_data_1.csv"
ACTION_EXEC_FILE="${OUTPUT_DIR}/training_data_2.csv"
QVALUE_ANALYSIS_FILE="${OUTPUT_DIR}/training_data_3.csv"
REWARD_BREAKDOWN_FILE="${OUTPUT_DIR}/training_data_4.csv"
TRANSITIONS_FILE="${OUTPUT_DIR}/training_data_5.csv"

# Initialize CSV files
echo "episode,cars,bikes,peds,buses,total_actions,phase_changes,block_rate,reward,loss,epsilon" > "$EPISODE_METRICS_FILE"
echo "episode,continue,continue_pct,skip2p1,skip2p1_pct,next,next_pct" > "$ACTION_EXEC_FILE"
echo "episode,avg_continue_q,avg_skip2p1_q,avg_next_q,q_spread,best_continue,best_skip2p1,best_next" > "$QVALUE_ANALYSIS_FILE"
echo "episode,waiting,flow,co2,equity,safety,blocked,bus_assist,next_bonus,skip2p1_bonus,stability" > "$REWARD_BREAKDOWN_FILE"
echo "episode,transition,count,avg_duration" > "$TRANSITIONS_FILE"

awk -v metrics_file="$EPISODE_METRICS_FILE" \
    -v action_exec_file="$ACTION_EXEC_FILE" \
    -v qvalue_file="$QVALUE_ANALYSIS_FILE" \
    -v reward_file="$REWARD_BREAKDOWN_FILE" \
    -v transition_file="$TRANSITIONS_FILE" \
    -v summary_file="$SUMMARY_FILE" '
BEGIN {
    episode_num = 0
    episode_list = ""
    
    # Storage arrays for table generation
    delete table_traffic
    delete table_metrics  
    delete table_actions
    delete table_qvalues
    delete table_rewards
    delete table_transitions_count
    delete exploit_count
    delete reward_event_count
}

# Parse Episode number from "Episode X Complete:"
/^Episode [0-9]+ Complete:/ {
    episode_num = $2
    episode_list = episode_list (episode_list ? "," : "") episode_num
    next
}

# Parse traffic config - extract episode number early
/^Episode [0-9]+ - (Generating|Using)/ {
    episode_num = $2
    next
}

/^  Cars: / {
    split($2, parts, "/")
    table_traffic[episode_num, "cars"] = parts[1]
    next
}

/^  Bicycles: / {
    split($2, parts, "/")
    table_traffic[episode_num, "bikes"] = parts[1]
    next
}

/^  Pedestrians: / {
    split($2, parts, "/")
    table_traffic[episode_num, "peds"] = parts[1]
    next
}

/^  Buses: / {
    bus_val = $2
    # Normalize bus frequency text
    if (bus_val ~ /every_15min/) {
        bus_val = "1/15 minutes"
    }
    table_traffic[episode_num, "buses"] = bus_val
    next
}

# Parse episode summary metrics (format: "Reward: X | Loss: Y | Steps: Z | Epsilon: W")
/^  Reward: .* \| Loss: .* \| Steps: .* \| Epsilon: / {
    for (i = 1; i <= NF; i++) {
        if ($i == "Reward:") {
            table_metrics[episode_num, "reward"] = $(i+1)
        } else if ($i == "Loss:") {
            table_metrics[episode_num, "loss"] = $(i+1)
        } else if ($i == "Steps:") {
            table_metrics[episode_num, "total_actions"] = $(i+1)
        } else if ($i == "Epsilon:") {
            table_metrics[episode_num, "epsilon"] = $(i+1)
        }
    }
    next
}

# Parse phase changes from [EPISODE SUMMARY] section
/^  Phase changes executed: / {
    table_metrics[episode_num, "phase_changes"] = $4
    next
}

/^  Block rate: / {
    table_metrics[episode_num, "block_rate"] = $3
    next
}

# Parse ACTION DISTRIBUTION (format: "  Continue    : 1159/3600 ( 32.2%)")
/^\[ACTION DISTRIBUTION\] Episode Summary:/ {
    in_action_dist = 1
    next
}

in_action_dist == 1 && /^  Continue/ {
    split($3, parts, "/")
    table_actions[episode_num, "continue"] = parts[1]
    pct = $5
    gsub(/[()%]/, "", pct)
    gsub(/^ +| +$/, "", pct)  # Remove leading/trailing spaces
    table_actions[episode_num, "continue_pct"] = pct
    next
}

in_action_dist == 1 && /^  Skip2P1/ {
    split($3, parts, "/")
    table_actions[episode_num, "skip2p1"] = parts[1]
    pct = $5
    gsub(/[()%]/, "", pct)
    gsub(/^ +| +$/, "", pct)
    table_actions[episode_num, "skip2p1_pct"] = pct
    next
}

in_action_dist == 1 && /^  Next/ {
    split($3, parts, "/")
    table_actions[episode_num, "next"] = parts[1]
    pct = $5
    gsub(/[()%]/, "", pct)
    gsub(/^ +| +$/, "", pct)
    table_actions[episode_num, "next_pct"] = pct
    in_action_dist = 0
    next
}

# Parse Q-VALUE CHECK
/^\[Q-VALUE CHECK\] Episode [0-9]+ - / {
    in_qvalue = 1
    next
}

in_qvalue == 1 && /^    Avg Continue Q-value: / {
    table_qvalues[episode_num, "avg_continue_q"] = $4
    next
}

in_qvalue == 1 && /^    Avg Skip2P1 Q-value: / {
    table_qvalues[episode_num, "avg_skip2p1_q"] = $4
    next
}

in_qvalue == 1 && /^    Avg Next Q-value: / {
    table_qvalues[episode_num, "avg_next_q"] = $4
    next
}

in_qvalue == 1 && /^    Q-value Spread: / {
    table_qvalues[episode_num, "q_spread"] = $3
    next
}

in_qvalue == 1 && /^  Best Action Distribution:/ {
    in_best_action = 1
    next
}

in_best_action == 1 && /^    Continue/ {
    split($3, parts, "/")
    table_qvalues[episode_num, "best_continue"] = parts[1]
    next
}

in_best_action == 1 && /^    Skip2P1/ {
    split($3, parts, "/")
    table_qvalues[episode_num, "best_skip2p1"] = parts[1]
    next
}

in_best_action == 1 && /^    Next/ {
    split($3, parts, "/")
    table_qvalues[episode_num, "best_next"] = parts[1]
    in_best_action = 0
    in_qvalue = 0
    next
}

# Parse reward components (format: "    Component:    +value")
/^    Waiting:/ {
    table_rewards[episode_num, "waiting"] = $2
    next
}

/^    Flow:/ {
    table_rewards[episode_num, "flow"] = $2
    next
}

/^    CO2:/ {
    table_rewards[episode_num, "co2"] = $2
    next
}

/^    Equity:/ {
    table_rewards[episode_num, "equity"] = $2
    next
}

/^    Safety:/ {
    table_rewards[episode_num, "safety"] = $2
    next
}

/^    Blocked:/ {
    table_rewards[episode_num, "blocked"] = $2
    next
}

/^    Bus Assistance:/ {
    table_rewards[episode_num, "bus_assist"] = $3
    next
}

/^    Next Bonus:/ {
    table_rewards[episode_num, "next_bonus"] = $3
    next
}

/^    Skip2P1 Effect:/ {
    table_rewards[episode_num, "skip2p1_bonus"] = $3
    next
}

/^    Stability:/ {
    table_rewards[episode_num, "stability"] = $2
    next
}

# Count exploitation decisions
/^\[PHASE CHANGE\].*Exploitation ACT:/ {
    exploit_count[episode_num]++
    next
}

# Count reward events
/^\[(EARLY CHANGE|SKIP2P1|CONTINUE|NEXT BONUS|BUS|STABILITY)\]/ {
    reward_event_count[episode_num]++
    next
}

# Parse phase transitions  
/^  P[0-9] → P[0-9]: / {
    trans = $1 " " $2 " " $3
    gsub(/:/, "", trans)
    split($4, parts, " ")
    count = parts[1]
    split($7, dur, "s")
    avg_dur = dur[1]
    
    table_transitions_count[episode_num, trans] = count
    table_transitions_count[episode_num, trans "_dur"] = avg_dur
    next
}

END {
    # Generate CSV files
    split(episode_list, episodes, ",")
    n_episodes = 0
    for (i in episodes) n_episodes++
    
    # Write Episode Metrics CSV
    for (i = 1; i <= n_episodes; i++) {
        ep = episodes[i]
        printf "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n", \
            ep, \
            table_traffic[ep, "cars"], \
            table_traffic[ep, "bikes"], \
            table_traffic[ep, "peds"], \
            table_traffic[ep, "buses"], \
            table_metrics[ep, "total_actions"], \
            table_metrics[ep, "phase_changes"], \
            table_metrics[ep, "block_rate"], \
            table_metrics[ep, "reward"], \
            table_metrics[ep, "loss"], \
            table_metrics[ep, "epsilon"] >> metrics_file
    }
    
    # Write Action Execution CSV
    for (i = 1; i <= n_episodes; i++) {
        ep = episodes[i]
        printf "%s,%s,%s,%s,%s,%s,%s\n", \
            ep, \
            table_actions[ep, "continue"], \
            table_actions[ep, "continue_pct"], \
            table_actions[ep, "skip2p1"], \
            table_actions[ep, "skip2p1_pct"], \
            table_actions[ep, "next"], \
            table_actions[ep, "next_pct"] >> action_exec_file
    }
    
    # Write Q-value Analysis CSV
    for (i = 1; i <= n_episodes; i++) {
        ep = episodes[i]
        printf "%s,%s,%s,%s,%s,%s,%s,%s\n", \
            ep, \
            table_qvalues[ep, "avg_continue_q"], \
            table_qvalues[ep, "avg_skip2p1_q"], \
            table_qvalues[ep, "avg_next_q"], \
            table_qvalues[ep, "q_spread"], \
            table_qvalues[ep, "best_continue"], \
            table_qvalues[ep, "best_skip2p1"], \
            table_qvalues[ep, "best_next"] >> qvalue_file
    }
    
    # Write Reward Breakdown CSV
    for (i = 1; i <= n_episodes; i++) {
        ep = episodes[i]
        printf "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n", \
            ep, \
            table_rewards[ep, "waiting"], \
            table_rewards[ep, "flow"], \
            table_rewards[ep, "co2"], \
            table_rewards[ep, "equity"], \
            table_rewards[ep, "safety"], \
            table_rewards[ep, "blocked"], \
            table_rewards[ep, "bus_assist"], \
            table_rewards[ep, "next_bonus"], \
            table_rewards[ep, "skip2p1_bonus"], \
            table_rewards[ep, "stability"] >> reward_file
    }
    
    # Generate markdown tables
    print "# Training Analysis Tables" > summary_file
    print "" >> summary_file
    print "##### Table 1: Episode Metrics & Traffic Configuration" >> summary_file
    print "" >> summary_file
    print "| Episode | Cars | Bikes | Peds | Buses | Total Actions | Phase Changes | Block Rate | Reward | Loss | Epsilon |" >> summary_file
    print "|---------|------|-------|------|-------|---------------|---------------|------------|--------|------|---------|" >> summary_file
    
    for (i = 1; i <= n_episodes; i++) {
        ep = episodes[i]
        printf "| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |\n", \
            ep, \
            table_traffic[ep, "cars"], \
            table_traffic[ep, "bikes"], \
            table_traffic[ep, "peds"], \
            table_traffic[ep, "buses"], \
            table_metrics[ep, "total_actions"], \
            table_metrics[ep, "phase_changes"], \
            table_metrics[ep, "block_rate"], \
            table_metrics[ep, "reward"], \
            table_metrics[ep, "loss"], \
            table_metrics[ep, "epsilon"] >> summary_file
    }
    print "" >> summary_file
    print "---" >> summary_file
    print "" >> summary_file
    
    print "##### Table 2: Actual Action Execution (ε-greedy)" >> summary_file
    print "" >> summary_file
    print "| Episode | Continue | Continue % | Skip2P1 | Skip2P1 % | Next | Next % |" >> summary_file
    print "|---------|----------|------------|---------|-----------|------|--------|" >> summary_file
    
    for (i = 1; i <= n_episodes; i++) {
        ep = episodes[i]
        printf "| %s | %s | %s%% | %s | %s%% | %s | %s%% |\n", \
            ep, \
            table_actions[ep, "continue"], \
            table_actions[ep, "continue_pct"], \
            table_actions[ep, "skip2p1"], \
            table_actions[ep, "skip2p1_pct"], \
            table_actions[ep, "next"], \
            table_actions[ep, "next_pct"] >> summary_file
    }
    print "" >> summary_file


    
    print "---" >> summary_file
    print "" >> summary_file
    
    print "##### Table 3: Learned Policy (Best Action from Q-values)" >> summary_file
    print "" >> summary_file
    print "| Episode | Avg Continue Q | Avg Skip2P1 Q | Avg Next Q | Q-Spread | Best Continue | Best Skip2P1 | Best Next |" >> summary_file
    print "|---------|----------------|---------------|------------|----------|---------------|--------------|-----------|" >> summary_file
    
    for (i = 1; i <= n_episodes; i++) {
        ep = episodes[i]
        printf "| %s | %s | %s | %s | %s | %s | %s | %s |\n", \
            ep, \
            table_qvalues[ep, "avg_continue_q"], \
            table_qvalues[ep, "avg_skip2p1_q"], \
            table_qvalues[ep, "avg_next_q"], \
            table_qvalues[ep, "q_spread"], \
            table_qvalues[ep, "best_continue"], \
            table_qvalues[ep, "best_skip2p1"], \
            table_qvalues[ep, "best_next"] >> summary_file
    }
    print "" >> summary_file
    print "---" >> summary_file
    print "" >> summary_file
    
    print "##### Table 4: Exploitation & Reward Event Summary" >> summary_file
    print "" >> summary_file
    print "*Note: Counts of agent exploitation decisions and reward events per episode.*" >> summary_file
    print "" >> summary_file
    print "| Episode | Exploitation Decisions | Reward Events |" >> summary_file
    print "|---------|----------------------|---------------|" >> summary_file
    
    for (i = 1; i <= n_episodes; i++) {
        ep = episodes[i]
        exp_cnt = exploit_count[ep] ? exploit_count[ep] : 0
        rew_cnt = reward_event_count[ep] ? reward_event_count[ep] : 0
        printf "| %s | %s | %s |\n", ep, exp_cnt, rew_cnt >> summary_file
    }
    print "" >> summary_file
}
' "$LOG_FILE"

echo ""
echo "================================================================"
echo "Parsing complete\! All files saved to: $OUTPUT_DIR"
echo "================================================================"
echo ""
echo "Output files created:"
echo "  Tables:        tables.md (4 training summary tables)"
echo "  Metrics:       training_data_1.csv (Episode metrics & config)"
echo "  Actions:       training_data_2.csv (Action execution distribution)"
echo "  Q-values:      training_data_3.csv (Q-value analysis)"
echo "  Rewards:       training_data_4.csv (Reward component breakdown)"
echo "  Transitions:   training_data_5.csv (Phase transition patterns)"
echo ""
echo "Total: 6 files (1 MD + 5 CSV)"
echo ""
