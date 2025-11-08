#!/bin/bash
# parse_testing_log.sh - Extract comprehensive XAI data from testing.log

if [ $# -eq 0 ]; then
    echo "Usage: $0 <testing_log_file>"
    echo "Example: $0 testing.log"
    echo ""
    echo "Extracts scenario summaries + XAI analysis:"
    echo "  • Reward breakdown by scenario"
    echo "  • Phase transition patterns"
    echo "  • Blocked actions with context"
    echo "  • Exploitation decision sequences"
    echo "  • Exploration vs Exploitation outcomes"
    echo "  • Bus assistance events"
    echo "  • Safety-performance tradeoff"
    exit 1
fi

LOG_FILE="$1"

if [ ! -f "$LOG_FILE" ]; then
    echo "Error: File '$LOG_FILE' not found!"
    exit 1
fi

echo "Parsing testing log with XAI analysis: $LOG_FILE"
echo "========================================"
echo ""

# Create output files
BASE="${LOG_FILE%.log}"
SUMMARY_FILE="${BASE}_summary.md"
REWARDS_FILE="${BASE}_reward_breakdown.csv"
TRANSITIONS_FILE="${BASE}_phase_transitions.csv"
BLOCKED_FILE="${BASE}_blocked_context.csv"
SEQUENCES_FILE="${BASE}_decision_sequences.csv"
COMPARE_FILE="${BASE}_explore_vs_exploit.csv"
BUS_FILE="${BASE}_bus_events.csv"

# Initialize CSV files
echo "scenario,reward_type,count,total_value,avg_value" > "$REWARDS_FILE"
echo "scenario,from_phase,to_phase,action,count,avg_duration" > "$TRANSITIONS_FILE"
echo "scenario,step,phase,duration,action,reason" > "$BLOCKED_FILE"
echo "scenario,sequence_num,decision_chain" > "$SEQUENCES_FILE"
echo "scenario,decision_type,total_actions,avg_reward,safety_violations" > "$COMPARE_FILE"
echo "scenario,event_type,count,avg_wait,total_bonus_penalty" > "$BUS_FILE"

awk -v summary_file="$SUMMARY_FILE" \
    -v rewards_file="$REWARDS_FILE" \
    -v transitions_file="$TRANSITIONS_FILE" \
    -v blocked_file="$BLOCKED_FILE" \
    -v sequences_file="$SEQUENCES_FILE" \
    -v compare_file="$COMPARE_FILE" \
    -v bus_file="$BUS_FILE" '
BEGIN {
    scenario_num = 0
    capturing = 0
    buffer = ""
    traffic_buffer = ""
    scenario_name = ""
    
    # Tracking variables
    step_count = 0
    
    # Reward tracking
    delete reward_counts
    delete reward_totals
    
    # Phase transition tracking
    delete transition_counts
    delete transition_durations
    
    # Blocked actions
    delete blocked_actions
    
    # Decision sequences
    sequence_num = 0
    decision_chain = ""
    
    # Exploration vs Exploitation
    exploit_actions = 0
    explore_actions = 0
    
    # Bus events
    delete bus_events
    delete bus_waits
}

# Capture scenario name
/^Generating DEVELOPED control routes for scenario:/ {
    # Save previous scenario data if exists
    if (scenario_name != "") {
        save_scenario_analysis()
    }
    
    scenario_name = $NF
    traffic_buffer = "Scenario: " scenario_name "\n"
    
    # Reset tracking
    step_count = 0
    delete reward_counts
    delete reward_totals
    delete transition_counts
    delete transition_durations
    delete blocked_actions
    sequence_num = 0
    decision_chain = ""
    exploit_actions = 0
    explore_actions = 0
    delete bus_events
    delete bus_waits
    
    next
}

# Capture traffic details
/^  (Cars|Bicycles|Pedestrians|Buses):/ && traffic_buffer != "" {
    traffic_buffer = traffic_buffer $0 "\n"
    next
}

# Track reward events
/^\[SKIP2P1 BONUS\].*bonus:/ {
    for (i = 1; i <= NF; i++) {
        if ($i == "bonus:" && $(i+1) ~ /^\+/) {
            value = $(i+1)
            gsub(/^\+/, "", value)
            reward_counts["skip2p1_bonus"]++
            reward_totals["skip2p1_bonus"] += value
            break
        }
    }
    next
}

/^\[STABILITY BONUS\].*bonus:/ {
    for (i = 1; i <= NF; i++) {
        if ($i == "bonus:" && $(i+1) ~ /^\+/) {
            value = $(i+1)
            gsub(/^\+/, "", value)
            reward_counts["stability_bonus"]++
            reward_totals["stability_bonus"] += value
            break
        }
    }
    next
}

/^\[NEXT BONUS\].*bonus:/ {
    for (i = 1; i <= NF; i++) {
        if ($i == "bonus:" && $(i+1) ~ /^\+/) {
            value = $(i+1)
            gsub(/^\+/, "", value)
            reward_counts["next_bonus"]++
            reward_totals["next_bonus"] += value
            break
        }
    }
    next
}

/^\[BUS PENALTY\].*penalty:/ {
    for (i = 1; i <= NF; i++) {
        if ($i == "penalty:" && $(i+1) ~ /^-/) {
            value = $(i+1)
            gsub(/^-/, "", value)
            reward_counts["bus_penalty"]++
            reward_totals["bus_penalty"] += value
            break
        }
    }
    next
}

/^\[EARLY CHANGE\].*penalty:/ {
    for (i = 1; i <= NF; i++) {
        if ($i == "penalty:" && $(i+1) ~ /^-/) {
            value = $(i+1)
            gsub(/^-/, "", value)
            reward_counts["early_change_penalty"]++
            reward_totals["early_change_penalty"] += value
            break
        }
    }
    next
}

/^\[CONTINUE SPAM\].*penalty:/ {
    for (i = 1; i <= NF; i++) {
        if ($i == "penalty:" && $(i+1) ~ /^-/) {
            value = $(i+1)
            gsub(/^-/, "", value)
            reward_counts["continue_spam_penalty"]++
            reward_totals["continue_spam_penalty"] += value
            break
        }
    }
    next
}

# Track phase transitions
/^\[PHASE CHANGE\].*Exploitation ACT:/ {
    # Extract phases and duration using field iteration
    from_phase = ""
    to_phase = ""
    duration = 0
    
    for (i = 1; i <= NF; i++) {
        if ($i ~ /^P[0-9]+$/ && $(i+1) == "→") {
            from_phase = $i
            gsub(/P/, "", from_phase)
        }
        else if ($(i-1) == "→" && $i ~ /^P[0-9]+$/) {
            to_phase = $i
            gsub(/P/, "", to_phase)
        }
        else if ($i == "Duration:" && $(i+1) ~ /^[0-9]+s$/) {
            duration = $(i+1)
            gsub(/s/, "", duration)
        }
    }
    
    if (from_phase != "" && to_phase != "") {
        key = "P" from_phase "_to_P" to_phase
        transition_counts[key]++
        transition_durations[key] += duration
        
        # Add to decision chain
        if (decision_chain != "") decision_chain = decision_chain " → "
        decision_chain = decision_chain "P" from_phase "→P" to_phase "(" duration "s)"
        
        # Track exploitation
        exploit_actions++
    }
    next
}

# Track blocked actions with context
/^\[BLOCKED\].*Exploitation ACT: Cannot/ {
    step_count++
    
    phase = "Unknown"
    duration = "Unknown"
    action = "Unknown"
    reason = "Unknown"
    
    # Extract phase
    for (i = 1; i <= NF; i++) {
        if ($i == "Phase" && $(i+1) ~ /^[0-9]+$/) {
            phase = "P" $(i+1)
        }
        else if ($i ~ /^duration=/ && $i ~ /[0-9]+s/) {
            duration = $i
            gsub(/duration=/, "", duration)
            gsub(/s/, "", duration)
        }
        else if ($i ~ /^MIN_GREEN=/ && $i ~ /[0-9]+s/) {
            reason = $i
            gsub(/\)/, "", reason)
        }
    }
    
    # Determine action type
    if ($0 ~ /skip to P1/) action = "Skip2P1"
    else if ($0 ~ /advance phase/) action = "Next"
    
    printf "%s,%d,%s,%s,%s,%s\n", scenario_name, step_count, phase, duration, action, reason >> blocked_file
    next
}

# Track bus events
/^\[SKIP2P1 BONUS\].*wait=/ {
    wait_time = 0
    bonus_value = 0
    
    for (i = 1; i <= NF; i++) {
        if ($i ~ /^wait=/ && $i ~ /[0-9.]+s/) {
            wait_time = $i
            gsub(/wait=/, "", wait_time)
            gsub(/s,?/, "", wait_time)
        }
        else if ($i == "bonus:" && $(i+1) ~ /^\+/) {
            bonus_value = $(i+1)
            gsub(/^\+/, "", bonus_value)
        }
    }
    
    if (wait_time > 0 && bonus_value > 0) {
        bus_events["skip2p1_bonus"]++
        bus_waits["skip2p1_bonus"] += wait_time
        bus_events["skip2p1_bonus_value"] += bonus_value
    }
    next
}

/^\[BUS EXCELLENT\].*waiting/ {
    wait_time = 0
    bonus_value = 0
    
    for (i = 1; i <= NF; i++) {
        if ($i == "waiting" && $(i+1) ~ /^[0-9.]+s/) {
            wait_time = $(i+1)
            gsub(/s/, "", wait_time)
        }
        else if ($i == "bonus:" && $(i+1) ~ /^\+/) {
            bonus_value = $(i+1)
            gsub(/^\+/, "", bonus_value)
        }
    }
    
    if (wait_time > 0 && bonus_value > 0) {
        bus_events["bus_excellent"]++
        bus_waits["bus_excellent"] += wait_time
        bus_events["bus_excellent_value"] += bonus_value
    }
    next
}

/^\[BUS PENALTY\].*waiting/ {
    wait_time = 0
    penalty_value = 0
    
    for (i = 1; i <= NF; i++) {
        if ($i == "waiting" && $(i+1) ~ /^[0-9.]+s/) {
            wait_time = $(i+1)
            gsub(/s/, "", wait_time)
        }
        else if ($i == "penalty:" && $(i+1) ~ /^-/) {
            penalty_value = $(i+1)
            gsub(/^-/, "", penalty_value)
        }
    }
    
    if (wait_time > 0 && penalty_value > 0) {
        bus_events["bus_penalty"]++
        bus_waits["bus_penalty"] += wait_time
        bus_events["bus_penalty_value"] += penalty_value
    }
    next
}

# Track exploration actions
/^\[PHASE CHANGE\].*Exploration/ {
    explore_actions++
    next
}

# Start capturing from [ACTION SUMMARY]
/^\[ACTION SUMMARY\]/ {
    capturing = 1
    buffer = $0 "\n"
    
    # Save decision sequence if any
    if (decision_chain != "") {
        sequence_num++
        printf "%s,%d,\"%s\"\n", scenario_name, sequence_num, decision_chain >> sequences_file
        decision_chain = ""
    }
    
    next
}

# While capturing, accumulate everything
capturing == 1 {
    buffer = buffer $0 "\n"
    
    # Check if we hit the end of final safety summary
    if (/^================================================================================/ && prev_line ~ /Violation Rate:/) {
        capturing = 0
        scenario_num++
        
        # Save all analysis data
        save_scenario_analysis()
        
        # Print to summary file
        print "================================================================================" >> summary_file
        print "SCENARIO " scenario_num " - " scenario_name >> summary_file
        print "================================================================================" >> summary_file
        print "" >> summary_file
        
        if (traffic_buffer != "") {
            print "TRAFFIC CONFIG:" >> summary_file
            printf "%s", traffic_buffer >> summary_file
            print "" >> summary_file
        }
        
        printf "%s", buffer >> summary_file
        print "" >> summary_file
        
        # Print XAI analysis
        print_xai_analysis()
        
        # Clear buffers
        buffer = ""
        traffic_buffer = ""
    }
    
    # Store previous line for checking
    prev_line = $0
    next
}

# Skip progress bar updates
/^Testing scenarios:/ {
    next
}

function save_scenario_analysis() {
    # Save reward breakdown
    for (r_type in reward_counts) {
        avg = reward_totals[r_type] / reward_counts[r_type]
        printf "%s,%s,%d,%.3f,%.3f\n", scenario_name, r_type, reward_counts[r_type], reward_totals[r_type], avg >> rewards_file
    }
    
    # Save phase transitions
    for (trans in transition_counts) {
        split(trans, parts, "_to_")
        from_p = parts[1]
        to_p = parts[2]
        avg_dur = transition_durations[trans] / transition_counts[trans]
        printf "%s,%s,%s,Exploitation,%d,%.1f\n", scenario_name, from_p, to_p, transition_counts[trans], avg_dur >> transitions_file
    }
    
    # Save exploration vs exploitation comparison
    total_actions = exploit_actions + explore_actions
    if (total_actions > 0) {
        printf "%s,Exploitation,%d,NA,NA\n", scenario_name, exploit_actions >> compare_file
        printf "%s,Exploration,%d,NA,NA\n", scenario_name, explore_actions >> compare_file
    }
    
    # Save bus events
    for (event in bus_events) {
        if (event !~ /_value$/) {
            count = bus_events[event]
            avg_wait = (count > 0) ? bus_waits[event] / count : 0
            value = bus_events[event "_value"]
            printf "%s,%s,%d,%.1f,%.3f\n", scenario_name, event, count, avg_wait, value >> bus_file
        }
    }
}

function print_xai_analysis() {
    print "=== XAI ANALYSIS ===" >> summary_file
    print "" >> summary_file
    
    # Reward breakdown
    if (length(reward_counts) > 0) {
        print "REWARD BREAKDOWN:" >> summary_file
        for (r_type in reward_counts) {
            avg = reward_totals[r_type] / reward_counts[r_type]
            printf "  %s: %d events, Total: %.2f, Avg: %.3f\n", r_type, reward_counts[r_type], reward_totals[r_type], avg >> summary_file
        }
        print "" >> summary_file
    }
    
    # Phase transition patterns
    if (length(transition_counts) > 0) {
        print "PHASE TRANSITION PATTERNS:" >> summary_file
        for (trans in transition_counts) {
            split(trans, parts, "_to_")
            avg_dur = transition_durations[trans] / transition_counts[trans]
            printf "  %s → %s: %d times, Avg duration: %.1fs\n", parts[1], parts[2], transition_counts[trans], avg_dur >> summary_file
        }
        print "" >> summary_file
    }
    
    # Exploration vs exploitation
    total_actions = exploit_actions + explore_actions
    if (total_actions > 0) {
        exploit_pct = (exploit_actions / total_actions) * 100
        explore_pct = (explore_actions / total_actions) * 100
        print "EXPLORATION VS EXPLOITATION:" >> summary_file
        printf "  Exploitation: %d actions (%.1f%%)\n", exploit_actions, exploit_pct >> summary_file
        printf "  Exploration: %d actions (%.1f%%)\n", explore_actions, explore_pct >> summary_file
        print "" >> summary_file
    }
    
    # Bus assistance
    if (length(bus_events) > 0) {
        print "BUS ASSISTANCE SUMMARY:" >> summary_file
        for (event in bus_events) {
            if (event !~ /_value$/) {
                count = bus_events[event]
                avg_wait = (count > 0) ? bus_waits[event] / count : 0
                value = bus_events[event "_value"]
                printf "  %s: %d events, Avg wait: %.1fs, Total value: %.2f\n", event, count, avg_wait, value >> summary_file
            }
        }
        print "" >> summary_file
    }
    
    print "===================" >> summary_file
    print "" >> summary_file
}
' "$LOG_FILE"

echo ""
echo "========================================"
echo "Parsing complete!"
echo ""
echo "Output files created:"
echo "  1. $SUMMARY_FILE - Scenario summaries with XAI analysis"
echo "  2. $REWARDS_FILE - Reward breakdown by scenario"
echo "  3. $TRANSITIONS_FILE - Phase transition patterns"
echo "  4. $BLOCKED_FILE - Blocked actions with context"
echo "  5. $SEQUENCES_FILE - Exploitation decision sequences"
echo "  6. $COMPARE_FILE - Exploration vs Exploitation comparison"
echo "  7. $BUS_FILE - Bus assistance events"
echo ""
