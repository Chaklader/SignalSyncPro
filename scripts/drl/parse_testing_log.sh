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
SUMMARY_FILE="${OUTPUT_DIR}/tables.md"
QVALUES_FILE="${OUTPUT_DIR}/testing_data_1.csv"
CONTEXT_FILE="${OUTPUT_DIR}/testing_data_2.csv"
SEQUENCES_FILE="${OUTPUT_DIR}/testing_data_3.csv"

# Initialize CSV files
echo "scenario,step,phase,continue_q,skip2p1_q,next_q,selected_action,q_gap" > "$QVALUES_FILE"
echo "scenario,step_window,action,phase,duration,blocked_count" > "$CONTEXT_FILE"
echo "scenario,sequence_num,decision_chain" > "$SEQUENCES_FILE"

awk -v summary_file="$SUMMARY_FILE" \
    -v qvalues_file="$QVALUES_FILE" \
    -v context_file="$CONTEXT_FILE" \
    -v sequences_file="$SEQUENCES_FILE" '
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
    
    # Arrays for storing table data across all scenarios
    delete scenarios
    scenario_order = ""
    delete table_traffic
    delete table_actions
    delete table_phase_metrics
    delete table_safety
    delete table_rewards
    delete table_transitions
    delete table_bus
    
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

# Track blocked actions count for Q-value context
/^\[BLOCKED\].*Exploitation ACT: Cannot/ {
    blocked_count_q++
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
    printf "%s,%d,P%s,%.3f,%.3f,%.3f,%s,%.3f\n", \
        scenario_name, q_step, phase_num, \
        continue_q, skip2p1_q, next_q, \
        action_name, q_gap >> qvalues_file
    
    # For non-Continue decisions, capture state context in wide format
    if (action_name != "Continue") {
        # Calculate step window (e.g., 100-199, 2500-2599)
        window_start = q_step
        window_end = q_step + 99
        step_window = sprintf("%d-%d", window_start, window_end)
        
        # Use NA for blocked_count if 0
        blocked_display = (blocked_count_q > 0) ? blocked_count_q : "NA"
        
        # Output one row: scenario, step_window, action, phase, duration, blocked_count
        printf "%s,%s,%s,P%s,%d,%s\n", \
            scenario_name, step_window, action_name, phase_num, current_duration, blocked_display >> context_file
    }
    
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
        
        # Parse and store table data
        print_xai_analysis()
        
        # Save all analysis data to CSV files
        save_scenario_analysis()
        
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
    # Add to scenario order
    if (scenario_order == "") {
        scenario_order = scenario_name
    } else {
        scenario_order = scenario_order "," scenario_name
    }
    
    # Store reward breakdown for tables
    for (r_type in reward_counts) {
        table_rewards[scenario_name, r_type, "count"] = reward_counts[r_type]
        table_rewards[scenario_name, r_type, "total"] = reward_totals[r_type]
    }
    
    # Store phase transition patterns for tables
    for (trans in transition_counts) {
        avg_dur = transition_durations[trans] / transition_counts[trans]
        table_transitions[scenario_name, trans, "count"] = transition_counts[trans]
        table_transitions[scenario_name, trans, "avg_dur"] = avg_dur
    }
    
    # Store bus events for tables
    for (event in bus_events) {
        if (event !~ /_value$/) {
            count = bus_events[event]
            avg_wait = (count > 0) ? bus_waits[event] / count : 0
            value = bus_events[event "_value"]
            table_bus[scenario_name, event, "count"] = count
            table_bus[scenario_name, event, "avg_wait"] = avg_wait
            table_bus[scenario_name, event, "value"] = value
        }
    }
}

function print_xai_analysis() {
    # Parse traffic config from traffic_buffer
    split(traffic_buffer, traffic_lines, "\n")
    for (i in traffic_lines) {
        line = traffic_lines[i]
        if (line ~ /Cars:/) {
            split(line, parts, ": ")
            table_traffic[scenario_name, "cars"] = parts[2]
        } else if (line ~ /Bicycles:/) {
            split(line, parts, ": ")
            table_traffic[scenario_name, "bicycles"] = parts[2]
        } else if (line ~ /Pedestrians:/) {
            split(line, parts, ": ")
            table_traffic[scenario_name, "pedestrians"] = parts[2]
        } else if (line ~ /Buses:/) {
            split(line, parts, ": ")
            bus_val = parts[2]
            # Normalize bus frequency text
            if (bus_val ~ /every_15min/) {
                bus_val = "1/15 minutes"
            }
            table_traffic[scenario_name, "buses"] = bus_val
        }
    }
    
    # Parse action summary and phase metrics from buffer
    split(buffer, lines, "\n")
    for (i in lines) {
        line = lines[i]
        if (line ~ /Total actions:/) {
            split(line, parts, ": ")
            table_actions[scenario_name, "total"] = parts[2]
        } else if (line ~ /Continue \(0\):/) {
            split(line, parts, ": ")
            split(parts[2], vals, " ")
            table_actions[scenario_name, "continue"] = vals[1]
            gsub(/[()%]/, "", vals[2])
            table_actions[scenario_name, "continue_pct"] = vals[2]
        } else if (line ~ /Skip to P1 \(1\):/) {
            split(line, parts, ": ")
            split(parts[2], vals, " ")
            table_actions[scenario_name, "skip2p1"] = vals[1]
            gsub(/[()%]/, "", vals[2])
            table_actions[scenario_name, "skip2p1_pct"] = vals[2]
        } else if (line ~ /Next Phase \(2\):/) {
            split(line, parts, ": ")
            split(parts[2], vals, " ")
            table_actions[scenario_name, "next"] = vals[1]
            gsub(/[()%]/, "", vals[2])
            table_actions[scenario_name, "next_pct"] = vals[2]
        } else if (line ~ /Total actions attempted:/) {
            split(line, parts, ": ")
            table_phase_metrics[scenario_name, "attempted"] = parts[2]
        } else if (line ~ /Phase changes executed:/) {
            split(line, parts, ": ")
            table_phase_metrics[scenario_name, "executed"] = parts[2]
        } else if (line ~ /Actions blocked/) {
            split(line, parts, ": ")
            table_phase_metrics[scenario_name, "blocked"] = parts[2]
        } else if (line ~ /Phase change rate:/) {
            split(line, parts, ": ")
            table_phase_metrics[scenario_name, "change_rate"] = parts[2]
        } else if (line ~ /Block rate:/) {
            split(line, parts, ": ")
            table_phase_metrics[scenario_name, "block_rate"] = parts[2]
        } else if (line ~ /TOTAL SAFETY VIOLATIONS:/) {
            split(line, parts, ": ")
            gsub(/^[ \t]+/, "", parts[2])
            table_safety[scenario_name, "violations"] = parts[2]
        } else if (line ~ /Violation Rate:/) {
            split(line, parts, ": ")
            gsub(/^[ \t]+/, "", parts[2])
            table_safety[scenario_name, "violation_rate"] = parts[2]
        }
    }
}

END {
    # Generate 5 clean markdown tables
    
    # Header
    print "# XAI Data Tables for Traffic Signal Control Analysis" > summary_file
    print "" >> summary_file
    
    # Split scenario_order into array
    split(scenario_order, scenario_list, ",")
    n_scenarios = 0
    for (i in scenario_list) n_scenarios++
    
    # TABLE 1: Traffic Configuration & Action Distribution
    print "##### Table 1: Traffic Configuration & Action Distribution" >> summary_file
    print "" >> summary_file
    print "| Scenario | Cars (veh/hr) | Bicycles (veh/hr) | Pedestrians (veh/hr) | Buses | Total Actions | Continue | Skip to P1 | Next |" >> summary_file
    print "|----------|---------------|-------------------|---------------------|-------|---------------|----------|------------|------|" >> summary_file
    
    for (i = 1; i <= n_scenarios; i++) {
        sc = scenario_list[i]
        printf "| %s | %s | %s | %s | %s | %s | %s (%s%%) | %s (%s%%) | %s (%s%%) |\n", \
            sc, \
            table_traffic[sc, "cars"], \
            table_traffic[sc, "bicycles"], \
            table_traffic[sc, "pedestrians"], \
            table_traffic[sc, "buses"], \
            table_actions[sc, "total"], \
            table_actions[sc, "continue"], table_actions[sc, "continue_pct"], \
            table_actions[sc, "skip2p1"], table_actions[sc, "skip2p1_pct"], \
            table_actions[sc, "next"], table_actions[sc, "next_pct"] >> summary_file
    }
    print "" >> summary_file
    print "---" >> summary_file
    print "" >> summary_file
    
    # TABLE 2: Phase Change & Safety Metrics
    print "##### Table 2: Phase Change & Safety Metrics" >> summary_file
    print "" >> summary_file
    print "| Scenario | Actions Attempted | Phase Changes | Actions Blocked | Phase Change Rate | Block Rate | Total Safety Violations | Violation Rate |" >> summary_file
    print "|----------|-------------------|---------------|-----------------|-------------------|------------|------------------------|----------------|" >> summary_file
    
    for (i = 1; i <= n_scenarios; i++) {
        sc = scenario_list[i]
        printf "| %s | %s | %s | %s | %s | %s | %s | %s |\n", \
            sc, \
            table_phase_metrics[sc, "attempted"], \
            table_phase_metrics[sc, "executed"], \
            table_phase_metrics[sc, "blocked"], \
            table_phase_metrics[sc, "change_rate"], \
            table_phase_metrics[sc, "block_rate"], \
            table_safety[sc, "violations"], \
            table_safety[sc, "violation_rate"] >> summary_file
    }
    print "" >> summary_file
    print "---" >> summary_file
    print "" >> summary_file
    
    # TABLE 3: Reward Breakdown (Events & Total Values)
    print "##### Table 3: Reward Breakdown (Events & Total Values)" >> summary_file
    print "" >> summary_file
    print "*Note: Values in parentheses show total reward contribution.*" >> summary_file
    print "" >> summary_file
    print "| Scenario | Continue Spam Penalty | Next Bonus | Skip2P1 Bonus | Stability Bonus | Early Change Penalty | Bus Penalty |" >> summary_file
    print "|----------|----------------------|------------|---------------|-----------------|----------------------|-------------|" >> summary_file
    
    for (i = 1; i <= n_scenarios; i++) {
        sc = scenario_list[i]
        printf "| %s | %s | %s | %s | %s | %s | %s |\n", \
            sc, \
            format_reward(sc, "continue_spam_penalty"), \
            format_reward(sc, "next_bonus"), \
            format_reward(sc, "skip2p1_bonus"), \
            format_reward(sc, "stability_bonus"), \
            format_reward(sc, "early_change_penalty"), \
            format_reward(sc, "bus_penalty") >> summary_file
    }
    print "" >> summary_file
    print "---" >> summary_file
    print "" >> summary_file
    
    # TABLE 4: Phase Transition Patterns
    print "##### Table 4: Phase Transition Patterns" >> summary_file
    print "" >> summary_file
    print "| Scenario | P1→P2 (times, avg duration) | P2→P1 (times, avg duration) | P2→P3 (times, avg duration) | P3→P1 (times, avg duration) | P3→P4 (times, avg duration) | P4→P1 (times, avg duration) |" >> summary_file
    print "|----------|----------------------------|----------------------------|----------------------------|----------------------------|----------------------------|----------------------------|" >> summary_file
    
    for (i = 1; i <= n_scenarios; i++) {
        sc = scenario_list[i]
        printf "| %s | %s | %s | %s | %s | %s | %s |\n", \
            sc, \
            format_transition(sc, "P1_to_P2"), \
            format_transition(sc, "P2_to_P1"), \
            format_transition(sc, "P2_to_P3"), \
            format_transition(sc, "P3_to_P1"), \
            format_transition(sc, "P3_to_P4"), \
            format_transition(sc, "P4_to_P1") >> summary_file
    }
    print "" >> summary_file
    print "---" >> summary_file
    print "" >> summary_file
    
    # TABLE 5: Bus Assistance Summary
    print "##### Table 5: Bus Assistance Summary" >> summary_file
    print "" >> summary_file
    print "| Scenario | Bus Excellent Events | Avg Wait (s) | Total Value |" >> summary_file
    print "|----------|---------------------|--------------|-------------|" >> summary_file
    
    for (i = 1; i <= n_scenarios; i++) {
        sc = scenario_list[i]
        count = table_bus[sc, "bus_excellent", "count"]
        wait = table_bus[sc, "bus_excellent", "avg_wait"]
        value = table_bus[sc, "bus_excellent", "value"]
        if (count == "") count = "0"
        if (wait == "") wait = "0.0"
        if (value == "") value = "0.00"
        printf "| %s | %s | %s | %s |\n", sc, count, wait, value >> summary_file
    }
    print "" >> summary_file
}

function format_reward(sc, r_type) {
    count = table_rewards[sc, r_type, "count"]
    total = table_rewards[sc, r_type, "total"]
    if (count == "" || count == 0) {
        return "-"
    } else {
        return sprintf("%d events (%.2f)", count, total)
    }
}

function format_transition(sc, trans) {
    count = table_transitions[sc, trans, "count"]
    avg_dur = table_transitions[sc, trans, "avg_dur"]
    if (count == "" || count == 0) {
        return "-"
    } else {
        return sprintf("%d (%.1fs)", count, avg_dur)
    }
}
' "$LOG_FILE"

echo ""
echo "================================================================"
echo "Parsing complete! All files saved to: $OUTPUT_DIR"
echo "================================================================"
echo ""
echo "Output files created:"
echo "  Tables:        tables.md (5 XAI summary tables)"
echo "  Q-values:      testing_data_1.csv (Detailed Q-values by step)"
echo "  Context:       testing_data_2.csv (Decision context for non-Continue)"
echo "  Sequences:     testing_data_3.csv (Decision sequences)"
echo ""
echo "Total: 4 files (1 MD + 3 CSV)"
echo ""
