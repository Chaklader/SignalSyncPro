#\!/bin/bash
# create_training_tables.sh - Generate analysis: training tables and CSV files

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

# Create output file
SUMMARY_FILE="${OUTPUT_DIR}/tables.md"

awk -v summary_file="$SUMMARY_FILE" '
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
    episode_complete[episode_num] = 1  # Mark episode as complete
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
        } else if ($i == "Epsilon:") {
            table_metrics[episode_num, "epsilon"] = $(i+1)
        }
    }
    next
}

# Parse episode summary statistics (only if episode not yet complete to avoid overwrites)
/^  Total actions attempted: / {
    if (!episode_complete[episode_num]) {
        table_metrics[episode_num, "total_actions"] = $4
    }
    next
}

/^  Phase changes executed: / {
    if (!episode_complete[episode_num]) {
        table_metrics[episode_num, "phase_changes"] = $4
    }
    next
}

/^  Phase change rate: / {
    if (!episode_complete[episode_num]) {
        table_metrics[episode_num, "phase_change_rate"] = $4
    }
    next
}

/^  Actions blocked/ {
    if (!episode_complete[episode_num]) {
        table_metrics[episode_num, "blocked_count"] = $4
    }
    next
}

/^  Block rate: / {
    if (!episode_complete[episode_num]) {
        table_metrics[episode_num, "block_rate"] = $3
    }
    next
}

# Parse ACTION DISTRIBUTION (format: "  Continue    : 1159/3600 ( 32.2%)")
# NOTE: ACTION DISTRIBUTION for episode N is logged at the start of episode N+1
# So we store it for (episode_num - 1)
/^\[ACTION DISTRIBUTION\] Episode Summary:/ {
    in_action_dist = 1
    action_dist_ep = episode_num - 1  # Store for previous episode
    next
}

in_action_dist == 1 && /^  Continue/ {
    split($3, parts, "/")
    count = parts[1]
    pct = $5
    gsub(/[()%]/, "", pct)
    gsub(/^ +| +$/, "", pct)
    table_actions[action_dist_ep, "continue"] = count " (" pct "%)"
    next
}

in_action_dist == 1 && /^  Skip2P1/ {
    split($3, parts, "/")
    count = parts[1]
    pct = $5
    gsub(/[()%]/, "", pct)
    gsub(/^ +| +$/, "", pct)
    table_actions[action_dist_ep, "skip2p1"] = count " (" pct "%)"
    next
}

in_action_dist == 1 && /^  Next/ {
    split($3, parts, "/")
    count = parts[1]
    pct = $5
    gsub(/[()%]/, "", pct)
    gsub(/^ +| +$/, "", pct)
    table_actions[action_dist_ep, "next"] = count " (" pct "%)"
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
    count = parts[1]
    # Handle both formats: "( 63.8%)" (field 5) and "(100.0%)" (field 4)
    pct = (NF == 5) ? $5 : $4
    gsub(/[()%]/, "", pct)
    gsub(/^ +| +$/, "", pct)
    table_qvalues[episode_num, "best_continue"] = count " (" pct "%)"
    next
}

in_best_action == 1 && /^    Skip2P1/ {
    split($3, parts, "/")
    count = parts[1]
    # Handle both formats: "( 63.8%)" (field 5) and "(100.0%)" (field 4)
    pct = (NF == 5) ? $5 : $4
    gsub(/[()%]/, "", pct)
    gsub(/^ +| +$/, "", pct)
    table_qvalues[episode_num, "best_skip2p1"] = count " (" pct "%)"
    next
}

in_best_action == 1 && /^    Next/ {
    split($3, parts, "/")
    count = parts[1]
    # Handle both formats: "( 63.8%)" (field 5) and "(100.0%)" (field 4)
    pct = (NF == 5) ? $5 : $4
    gsub(/[()%]/, "", pct)
    gsub(/^ +| +$/, "", pct)
    table_qvalues[episode_num, "best_next"] = count " (" pct "%)"
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

# Parse exploitation decisions with phase transitions
/^\[PHASE CHANGE\].*Exploitation ACT:/ {
    exploit_count[episode_num]++
    
    # Extract phase transition (e.g., "P2 → P1")
    trans_found = 0
    for (i = 1; i <= NF; i++) {
        if ($i ~ /^P[0-9]+$/ && $(i+1) == "→" && $(i+2) ~ /^P[0-9]+$/) {
            trans = $i "→" $(i+2)
            table_phase_trans[episode_num, trans]++
            trans_found = 1
        }
        # Extract duration (appears later in the line)
        if (trans_found && $i == "Duration:" && $(i+1) ~ /^[0-9]+s$/) {
            duration_val = $(i+1)
            gsub(/s/, "", duration_val)
            table_phase_trans[episode_num, trans "_dur"] += duration_val
            break
        }
    }
    next
}

# Parse reward events with detailed breakdown
/^\[EARLY CHANGE\].*penalty:/ {
    reward_event_count[episode_num]++
    # Extract penalty value (e.g., "-0.750")
    for (i = 1; i <= NF; i++) {
        if ($i == "penalty:" && $(i+1) ~ /^-/) {
            val = $(i+1)
            gsub(/^-/, "", val)
            table_reward_events[episode_num, "early_change_count"]++
            table_reward_events[episode_num, "early_change_total"] += val
            break
        }
    }
    next
}

/^\[CONTINUE SPAM\].*penalty:/ {
    reward_event_count[episode_num]++
    for (i = 1; i <= NF; i++) {
        if ($i == "penalty:" && $(i+1) ~ /^-/) {
            val = $(i+1)
            gsub(/^-/, "", val)
            table_reward_events[episode_num, "continue_spam_count"]++
            table_reward_events[episode_num, "continue_spam_total"] += val
            break
        }
    }
    next
}

/^\[STABILITY BONUS\].*bonus:/ {
    reward_event_count[episode_num]++
    for (i = 1; i <= NF; i++) {
        if ($i == "bonus:" && $(i+1) ~ /^\+/) {
            val = $(i+1)
            gsub(/^\+/, "", val)
            table_reward_events[episode_num, "stability_bonus_count"]++
            table_reward_events[episode_num, "stability_bonus_total"] += val
            break
        }
    }
    next
}

/^\[NEXT BONUS\].*bonus:/ {
    reward_event_count[episode_num]++
    for (i = 1; i <= NF; i++) {
        if ($i == "bonus:" && $(i+1) ~ /^\+/) {
            val = $(i+1)
            gsub(/^\+/, "", val)
            table_reward_events[episode_num, "next_bonus_count"]++
            table_reward_events[episode_num, "next_bonus_total"] += val
            break
        }
    }
    next
}

/^\[SKIP2P1 BONUS\].*bonus:/ {
    reward_event_count[episode_num]++
    for (i = 1; i <= NF; i++) {
        if ($i == "bonus:" && $(i+1) ~ /^\+/) {
            val = $(i+1)
            gsub(/^\+/, "", val)
            table_reward_events[episode_num, "skip2p1_bonus_count"]++
            table_reward_events[episode_num, "skip2p1_bonus_total"] += val
            break
        }
    }
    next
}

/^\[BUS (PENALTY|EXCELLENT)\]/ {
    reward_event_count[episode_num]++
    # Handle both penalty and bonus
    for (i = 1; i <= NF; i++) {
        if ($i == "penalty:" && $(i+1) ~ /^-/) {
            val = $(i+1)
            gsub(/^-/, "", val)
            table_reward_events[episode_num, "bus_penalty_count"]++
            table_reward_events[episode_num, "bus_penalty_total"] += val
            break
        } else if ($i == "bonus:" && $(i+1) ~ /^\+/) {
            val = $(i+1)
            gsub(/^\+/, "", val)
            table_reward_events[episode_num, "bus_excellent_count"]++
            table_reward_events[episode_num, "bus_excellent_total"] += val
            break
        }
    }
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
    # Generate markdown tables
    split(episode_list, episodes, ",")
    n_episodes = 0
    for (i in episodes) n_episodes++
    
    print "# Analysis: Training Tables" > summary_file
    print "" >> summary_file
    print "##### Table 1: Episode Metrics & Traffic Configuration" >> summary_file
    print "" >> summary_file
    print "| Episode | Cars | Bikes | Peds | Buses | Total Actions | Phase Changes | Block Rate | Total Reward | Loss | Epsilon |" >> summary_file
    print "|---------|------|-------|------|-------|---------------|---------------|------------|--------------|------|---------|" >> summary_file
    
    for (i = 1; i <= n_episodes; i++) {
        ep = episodes[i]
        # Combine phase changes with rate
        phase_str = table_metrics[ep, "phase_changes"] " (" table_metrics[ep, "phase_change_rate"] ")"
        # Combine blocked count with rate
        block_str = table_metrics[ep, "blocked_count"] " (" table_metrics[ep, "block_rate"] ")"
        
        printf "| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |\n", \
            ep, \
            table_traffic[ep, "cars"], \
            table_traffic[ep, "bikes"], \
            table_traffic[ep, "peds"], \
            table_traffic[ep, "buses"], \
            table_metrics[ep, "total_actions"], \
            phase_str, \
            block_str, \
            table_metrics[ep, "reward"], \
            table_metrics[ep, "loss"], \
            table_metrics[ep, "epsilon"] >> summary_file
    }
    print "" >> summary_file
    print "---" >> summary_file
    print "" >> summary_file
    
    print "##### Table 2: Actual Action Execution (ε-greedy)" >> summary_file
    print "" >> summary_file
    print "| Episode | Continue | Skip2P1 | Next |" >> summary_file
    print "|---------|----------|---------|------|" >> summary_file
    
    for (i = 1; i <= n_episodes; i++) {
        ep = episodes[i]
        printf "| %s | %s | %s | %s |\n", \
            ep, \
            table_actions[ep, "continue"], \
            table_actions[ep, "skip2p1"], \
            table_actions[ep, "next"] >> summary_file
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
    print "---" >> summary_file
    print "" >> summary_file
    
    # Table 5: Phase Transition Patterns (Exploitation Decisions)
    print "##### Table 5: Phase Transition Patterns (Exploitation Decisions)" >> summary_file
    print "" >> summary_file
    print "*Note: Shows count and average duration for each phase transition type.*" >> summary_file
    print "" >> summary_file
    print "| Episode | P1→P2 | P2→P1 | P2→P3 | P3→P1 | P3→P4 | P4→P1 |" >> summary_file
    print "|---------|-------|-------|-------|-------|-------|-------|" >> summary_file
    
    for (i = 1; i <= n_episodes; i++) {
        ep = episodes[i]
        printf "| %s | %s | %s | %s | %s | %s | %s |\n", \
            ep, \
            format_phase_trans(ep, "P1→P2"), \
            format_phase_trans(ep, "P2→P1"), \
            format_phase_trans(ep, "P2→P3"), \
            format_phase_trans(ep, "P3→P1"), \
            format_phase_trans(ep, "P3→P4"), \
            format_phase_trans(ep, "P4→P1") >> summary_file
    }
    print "" >> summary_file
    print "---" >> summary_file
    print "" >> summary_file
    
    # Table 6: Reward Event Breakdown
    print "##### Table 6: Reward Event Breakdown" >> summary_file
    print "" >> summary_file
    print "*Note: Count and total value for each reward event type. Format: count (total value).*" >> summary_file
    print "" >> summary_file
    print "| Episode | Early Change Penalty | Continue Spam | Stability Bonus | Next Bonus | Skip2P1 Bonus | Bus Penalty | Bus Excellent |" >> summary_file
    print "|---------|---------------------|---------------|-----------------|------------|---------------|-------------|---------------|" >> summary_file
    
    for (i = 1; i <= n_episodes; i++) {
        ep = episodes[i]
        printf "| %s | %s | %s | %s | %s | %s | %s | %s |\n", \
            ep, \
            format_reward_event(ep, "early_change"), \
            format_reward_event(ep, "continue_spam"), \
            format_reward_event(ep, "stability_bonus"), \
            format_reward_event(ep, "next_bonus"), \
            format_reward_event(ep, "skip2p1_bonus"), \
            format_reward_event(ep, "bus_penalty"), \
            format_reward_event(ep, "bus_excellent") >> summary_file
    }
    print "" >> summary_file
}

# Helper functions (must be inside awk script)
function format_phase_trans(ep, trans) {
    # Clean up episode number
    gsub(/^[ \t]+|[ \t]+$/, "", ep)
    
    count = table_phase_trans[ep, trans]
    dur_total = table_phase_trans[ep, trans "_dur"]
    if (count == "" || count == 0) {
        return "-"
    } else {
        avg_dur = (count > 0 && dur_total > 0) ? (dur_total / count) : 0
        return sprintf("%d (%.1fs)", count, avg_dur)
    }
}

function format_other_trans(ep) {
    # Count any transitions not in the main 6
    other = 0
    for (key in table_phase_trans) {
        split(key, parts, SUBSEP)
        if (parts[1] == ep && parts[2] !~ /_dur$/ && 
            parts[2] != "P1→P2" && parts[2] != "P2→P1" && 
            parts[2] != "P2→P3" && parts[2] != "P3→P1" && 
            parts[2] != "P3→P4" && parts[2] != "P4→P1") {
            other += table_phase_trans[ep, parts[2]]
        }
    }
    return (other > 0) ? other : "-"
}

function format_reward_event(ep, event_type) {
    count = table_reward_events[ep, event_type "_count"]
    total = table_reward_events[ep, event_type "_total"]
    if (count == "" || count == 0) {
        return "-"
    } else {
        return sprintf("%d (%.2f)", count, total)
    }
}
' "$LOG_FILE"

echo ""
echo "================================================================"
echo "Parsing complete! File saved to: $OUTPUT_DIR"
echo "================================================================"
echo ""
echo "Output file created:"
echo "  tables.md (6 training summary tables)"
echo ""
