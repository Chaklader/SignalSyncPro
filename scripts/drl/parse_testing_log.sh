#!/bin/bash
# parse_testing_log.sh - Extract comprehensive XAI data from testing.log
# Includes Q-values, rewards, transitions, context, and decision analysis

if [ $# -eq 0 ]; then
    echo "Usage: $0 <testing_log_file>"
    echo "Example: $0 testing.log"
    echo ""
    echo "Extracts complete XAI analysis:"
    echo "  • Q-values with phase/duration context"
    echo "  • Decision context for non-Continue actions"
    echo "  • Q-value ranking changes (decision boundaries)"
    echo "  • Reward breakdown by scenario"
    echo "  • Phase transition patterns"
    echo "  • Blocked actions with context"
    echo "  • Exploitation decision sequences"
    echo "  • Bus assistance events"
    echo "  • Scenario summaries"
    exit 1
fi

LOG_FILE="$1"

if [ ! -f "$LOG_FILE" ]; then
    echo "Error: File '$LOG_FILE' not found!"
    exit 1
fi

echo "Parsing testing log with comprehensive XAI analysis: $LOG_FILE"
echo "================================================================"
echo ""

# Create output directory
OUTPUT_DIR="output/testing"
mkdir -p "$OUTPUT_DIR"

# Create output files with sequential naming
SUMMARY_FILE="${OUTPUT_DIR}/testing_data_summary.md"
QVALUES_FILE="${OUTPUT_DIR}/testing_data_1.csv"
CONTEXT_FILE="${OUTPUT_DIR}/testing_data_2.csv"
RANKING_FILE="${OUTPUT_DIR}/testing_data_3.csv"
REWARDS_FILE="${OUTPUT_DIR}/testing_data_4.csv"
TRANSITIONS_FILE="${OUTPUT_DIR}/testing_data_5.csv"
BLOCKED_FILE="${OUTPUT_DIR}/testing_data_6.csv"
SEQUENCES_FILE="${OUTPUT_DIR}/testing_data_7.csv"
BUS_FILE="${OUTPUT_DIR}/testing_data_8.csv"

# Initialize CSV files
echo "scenario,step,phase,duration,continue_q,skip2p1_q,next_q,selected_action,best_action,q_gap" > "$QVALUES_FILE"
echo "scenario,step,phase,duration,action,context_type,context_value" > "$CONTEXT_FILE"
echo "scenario,step,old_best,new_best,reason,phase_duration" > "$RANKING_FILE"
echo "scenario,reward_type,count,total_value,avg_value" > "$REWARDS_FILE"
echo "scenario,from_phase,to_phase,count,avg_duration" > "$TRANSITIONS_FILE"
echo "scenario,step,phase,duration,action,reason" > "$BLOCKED_FILE"
echo "scenario,sequence_num,decision_chain" > "$SEQUENCES_FILE"
echo "scenario,event_type,count,avg_wait,total_bonus_penalty" > "$BUS_FILE"

awk -v summary_file="$SUMMARY_FILE" \
    -v qvalues_file="$QVALUES_FILE" \
    -v context_file="$CONTEXT_FILE" \
    -v ranking_file="$RANKING_FILE" \
    -v rewards_file="$REWARDS_FILE" \
    -v transitions_file="$TRANSITIONS_FILE" \
    -v blocked_file="$BLOCKED_FILE" \
    -v sequences_file="$SEQUENCES_FILE" \
    -v bus_file="$BUS_FILE" '
BEGIN {
    scenario_num = 0
    capturing = 0
    buffer = ""
    traffic_buffer = ""
    scenario_name = ""
    
    # Tracking variables
    step_count = 0
    current_phase = "P1"
    current_duration = 0
    
    # Q-value tracking
    continue_q = 0
    skip2p1_q = 0
    next_q = 0
    prev_best_action = ""
    q_step = 0
    blocked_count_q = 0
    
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
    
    # Bus events
    delete bus_events
    delete bus_waits
}

# Capture scenario name
/Generating DEVELOPED control routes for scenario:/ {
    # Update to new scenario
    scenario_name = $NF
    traffic_buffer = "Scenario: " scenario_name "\n"
    
    # Reset tracking for new scenario
    step_count = 0
    current_phase = "P1"
    current_duration = 0
    blocked_count_q = 0
    prev_best_action = ""
    delete reward_counts
    delete reward_totals
    delete transition_counts
    delete transition_durations
    delete blocked_actions
    sequence_num = 0
    decision_chain = ""
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
        
        # Update current phase and duration for blocked action tracking
        current_phase = "P" to_phase
        current_duration = 0
    }
    next
}

# Track blocked actions with context
/^\[BLOCKED\].*Exploitation ACT: Cannot/ {
    step_count++
    current_duration++
    blocked_count_q++  # Also count for Q-value context
    
    phase = current_phase
    duration = current_duration
    action = "Unknown"
    reason = "Unknown"
    
    # Extract blocking info
    for (i = 1; i <= NF; i++) {
        if ($i ~ /^duration=/ && $i ~ /[0-9]+s/) {
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

# Track step number for Q-values
/\[SAFETY SUMMARY\] Step [0-9]+:/ || /\[PEDESTRIAN DEBUG\] Step [0-9]+:/ {
    for (i = 1; i <= NF; i++) {
        if ($i == "Step" && $(i+1) ~ /^[0-9]+:?$/) {
            gsub(/:/, "", $(i+1))
            q_step = $(i+1)
            break
        }
    }
    next
}

# Capture Q-values
/^  Q-values: Continue=/ {
    split($0, parts, ", ")
    for (i in parts) {
        if (parts[i] ~ /Continue=/) {
            split(parts[i], temp, "=")
            continue_q = temp[2]
        }
        else if (parts[i] ~ /Skip2P1=/) {
            split(parts[i], temp, "=")
            skip2p1_q = temp[2]
        }
        else if (parts[i] ~ /Next=/) {
            split(parts[i], temp, "=")
            next_q = temp[2]
        }
    }
    next
}

# Capture selected action and process Q-values
/^  Selected: [0-9]+/ {
    for (i = 1; i <= NF; i++) {
        if ($i == "Selected:" && $(i+1) ~ /^[0-9]+$/) {
            selected = $(i+1)
            break
        }
    }
    
    # Map action number to name
    if (selected == "0") action_name = "Continue"
    else if (selected == "1") action_name = "Skip2P1"
    else if (selected == "2") action_name = "Next"
    else action_name = "Unknown"
    
    # Find best action (highest Q-value)
    best_action = "Continue"
    best_q = continue_q
    if (skip2p1_q > best_q) {
        best_action = "Skip2P1"
        best_q = skip2p1_q
    }
    if (next_q > best_q) {
        best_action = "Next"
        best_q = next_q
    }
    
    # Calculate Q-gap (selected Q - worst Q)
    worst_q = continue_q
    if (skip2p1_q < worst_q) worst_q = skip2p1_q
    if (next_q < worst_q) worst_q = next_q
    
    selected_q = (selected == "0") ? continue_q : (selected == "1") ? skip2p1_q : next_q
    q_gap = selected_q - worst_q
    
    # Get phase number from current_phase
    phase_num = current_phase
    gsub(/P/, "", phase_num)
    
    # Print main Q-values to output file
    printf "%s,%d,P%s,%d,%.3f,%.3f,%.3f,%s,%s,%.3f\n", \
        scenario_name, q_step, phase_num, current_duration, \
        continue_q, skip2p1_q, next_q, \
        action_name, best_action, q_gap >> qvalues_file
    
    # For non-Continue decisions, capture state context
    if (action_name != "Continue") {
        printf "%s,%d,P%s,%d,%s,phase,P%s\n", \
            scenario_name, q_step, phase_num, current_duration, action_name, phase_num >> context_file
        printf "%s,%d,P%s,%d,%s,duration,%d\n", \
            scenario_name, q_step, phase_num, current_duration, action_name, current_duration >> context_file
        if (blocked_count_q > 0) {
            printf "%s,%d,P%s,%d,%s,blocked_count,%d\n", \
                scenario_name, q_step, phase_num, current_duration, action_name, blocked_count_q >> context_file
        }
    }
    
    # Track Q-ranking changes
    if (prev_best_action != "" && prev_best_action != best_action) {
        reason = sprintf("Q-values shifted: Continue=%.2f Skip2P1=%.2f Next=%.2f", \
            continue_q, skip2p1_q, next_q)
        printf "%s,%d,%s,%s,\"%s\",%d\n", \
            scenario_name, q_step, prev_best_action, best_action, reason, current_duration >> ranking_file
    }
    prev_best_action = best_action
    
    # Reset blocked counter after processing decision
    blocked_count_q = 0
    
    next
}

# NOTE: Blocked actions already tracked above for CSV.
# The blocked_count_q is incremented there as well via the same pattern.

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

# While capturing, accumulate everything except Pedestrian action and Results line
capturing == 1 {
    # Skip Pedestrian action line (Action 3)
    if ($0 ~ /^  Pedestrian \(3\):/) {
        prev_line = $0
        next
    }
    
    # Skip misleading "Results for..." line
    if ($0 ~ /^✓ Results for .* saved to:/) {
        prev_line = $0
        next
    }
    
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
        printf "%s,%s,%s,%d,%.1f\n", scenario_name, from_p, to_p, transition_counts[trans], avg_dur >> transitions_file
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
echo "================================================================"
echo "Parsing complete! All files saved to: $OUTPUT_DIR"
echo "================================================================"
echo ""
echo "Output files created:"
echo "  Summary:       testing_data_summary.md"
echo "  Q-values:      testing_data_1.csv (Q-values with phase/duration)"
echo "  Context:       testing_data_2.csv (Decision context for non-Continue)"
echo "  Ranking:       testing_data_3.csv (Q-value ranking changes)"
echo "  Rewards:       testing_data_4.csv (Reward breakdown by scenario)"
echo "  Transitions:   testing_data_5.csv (Phase transition patterns)"
echo "  Blocked:       testing_data_6.csv (Blocked actions with context)"
echo "  Sequences:     testing_data_7.csv (Decision sequences)"
echo "  Bus Events:    testing_data_8.csv (Bus assistance events)"
echo ""
echo "Total: 9 files (1 MD + 8 CSV)"
echo ""
