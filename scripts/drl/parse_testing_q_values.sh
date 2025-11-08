#!/bin/bash
# parse_q_values.sh - Extract Q-values and decision context from testing.log
# Usage: ./parse_q_values.sh <testing_log_file>

if [ $# -eq 0 ]; then
    echo "Usage: $0 <testing_log_file>"
    echo "Example: $0 testing.log"
    echo ""
    echo "This script extracts Q-values with state context for XAI analysis."
    echo "Includes: Q-values, phase, duration, ranking changes, and decision context."
    exit 1
fi

LOG_FILE="$1"

if [ ! -f "$LOG_FILE" ]; then
    echo "Error: File '$LOG_FILE' not found!"
    exit 1
fi

echo "Extracting Q-values and decision context from: $LOG_FILE"
echo "=========================================="
echo ""

# Create output CSV files
OUTPUT_FILE="${LOG_FILE%.log}_q_values.csv"
CONTEXT_FILE="${LOG_FILE%.log}_decision_context.csv"
RANKING_FILE="${LOG_FILE%.log}_q_ranking_changes.csv"

echo "scenario,step,phase,duration,continue_q,skip2p1_q,next_q,selected_action,best_action,q_gap" > "$OUTPUT_FILE"
echo "scenario,step,phase,duration,action,context_type,context_value" > "$CONTEXT_FILE"
echo "scenario,step,old_best,new_best,reason,phase_duration" > "$RANKING_FILE"

awk -v output_file="$OUTPUT_FILE" -v context_file="$CONTEXT_FILE" -v ranking_file="$RANKING_FILE" '
BEGIN {
    scenario = "Unknown"
    step = 0
    current_phase = 1  # Start in P1
    phase_duration = 0
    prev_best_action = ""
    bus_wait = 0
    blocked_count = 0
}

# Capture scenario name
/Generating DEVELOPED control routes for scenario:/ {
    scenario = $NF
    step = 0
    current_phase = 1
    phase_duration = 0
    prev_best_action = ""
    next
}

# Track phase changes and capture duration
/\[PHASE CHANGE\].*Exploitation ACT:/ {
    for (i = 1; i <= NF; i++) {
        if ($(i-1) == "→" && $i ~ /^P[0-9]+$/) {
            current_phase = $i
            gsub(/P/, "", current_phase)
        }
        else if ($i == "Duration:" && $(i+1) ~ /^[0-9]+s$/) {
            phase_duration = $(i+1)
            gsub(/s/, "", phase_duration)
        }
    }
    next
}

# Track CONTINUE SPAM for duration estimation
/\[CONTINUE SPAM\].*Phase/ {
    for (i = 1; i <= NF; i++) {
        if ($i == "Phase" && $(i+1) ~ /^[0-9]+:/) {
            current_phase = $(i+1)
            gsub(/:/, "", current_phase)
        }
    }
    next
}

# Track MAX_GREEN FORCED changes
/\[MAX_GREEN FORCED\].*Phase/ {
    for (i = 1; i <= NF; i++) {
        if ($(i-1) == "→" && $i ~ /^P[0-9]+$/) {
            current_phase = $i
            gsub(/P/, "", current_phase)
        }
    }
    next
}

# Track blocked actions
/\[BLOCKED\].*Exploitation ACT:/ {
    blocked_count++
    next
}

# Track bus events
/\[SKIP2P1 BONUS\].*wait=/ {
    for (i = 1; i <= NF; i++) {
        if ($i ~ /^wait=/ && $i ~ /[0-9.]+s/) {
            bus_wait = $i
            gsub(/wait=/, "", bus_wait)
            gsub(/s,?/, "", bus_wait)
        }
    }
    next
}

/\[BUS PENALTY\].*waiting/ {
    for (i = 1; i <= NF; i++) {
        if ($i == "waiting" && $(i+1) ~ /^[0-9.]+s/) {
            bus_wait = $(i+1)
            gsub(/s/, "", bus_wait)
        }
    }
    next
}

# Capture step number
/\[SAFETY SUMMARY\] Step [0-9]+:/ || /\[PEDESTRIAN DEBUG\] Step [0-9]+:/ {
    for (i = 1; i <= NF; i++) {
        if ($i == "Step" && $(i+1) ~ /^[0-9]+:?$/) {
            gsub(/:/, "", $(i+1))
            step = $(i+1)
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

# Capture selected action and process
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
    
    # Print main Q-values to output file
    printf "%s,%d,P%d,%d,%.3f,%.3f,%.3f,%s,%s,%.3f\n", \
        scenario, step, current_phase, phase_duration, \
        continue_q, skip2p1_q, next_q, \
        action_name, best_action, q_gap >> output_file
    
    # For non-Continue decisions, capture state context
    if (action_name != "Continue") {
        printf "%s,%d,P%d,%d,%s,phase,P%d\n", \
            scenario, step, current_phase, phase_duration, action_name, current_phase >> context_file
        printf "%s,%d,P%d,%d,%s,duration,%d\n", \
            scenario, step, current_phase, phase_duration, action_name, phase_duration >> context_file
        if (bus_wait > 0) {
            printf "%s,%d,P%d,%d,%s,bus_wait,%.1f\n", \
                scenario, step, current_phase, phase_duration, action_name, bus_wait >> context_file
        }
        if (blocked_count > 0) {
            printf "%s,%d,P%d,%d,%s,blocked_count,%d\n", \
                scenario, step, current_phase, phase_duration, action_name, blocked_count >> context_file
        }
    }
    
    # Track Q-ranking changes
    if (prev_best_action != "" && prev_best_action != best_action) {
        reason = sprintf("Q-values shifted: Continue=%.2f Skip2P1=%.2f Next=%.2f", \
            continue_q, skip2p1_q, next_q)
        printf "%s,%d,%s,%s,\"%s\",%d\n", \
            scenario, step, prev_best_action, best_action, reason, phase_duration >> ranking_file
    }
    
    prev_best_action = best_action
    blocked_count = 0
    bus_wait = 0
    selected = ""
    next
}
' "$LOG_FILE"

# Count Q-values extracted
Q_COUNT=$(tail -n +2 "$OUTPUT_FILE" | wc -l | tr -d ' ')

echo ""
echo "=========================================="
echo "Extraction complete!"
echo "Total Q-values extracted: $Q_COUNT"
echo ""
echo "Output files:"
echo "  1. $OUTPUT_FILE - All Q-values with phase and duration"
echo "  2. $CONTEXT_FILE - State context for non-Continue decisions"
echo "  3. $RANKING_FILE - Q-value ranking changes (decision boundaries)"
echo ""
echo "CSV columns (Q-values):"
echo "  - scenario, step, phase, duration, continue_q, skip2p1_q, next_q"
echo "  - selected_action, best_action (highest Q), q_gap (selected - worst)"
echo ""

# Count decision contexts
CONTEXT_COUNT=$(tail -n +2 "$CONTEXT_FILE" | wc -l | tr -d ' ')
RANKING_COUNT=$(tail -n +2 "$RANKING_FILE" | wc -l | tr -d ' ')

echo "Decision contexts captured: $CONTEXT_COUNT (for non-Continue actions)"
echo "Q-ranking changes detected: $RANKING_COUNT (action preference flips)"
echo ""

# Show Q-ranking changes
if [ $RANKING_COUNT -gt 0 ]; then
    echo "=========================================="
    echo "Q-VALUE RANKING CHANGES (First 10)"
    echo "=========================================="
    echo ""
    head -11 "$RANKING_FILE" | column -t -s','
    echo ""
fi

# Show decision context examples
if [ $CONTEXT_COUNT -gt 0 ]; then
    echo "=========================================="
    echo "DECISION CONTEXT EXAMPLES (First 10)"
    echo "=========================================="
    echo ""
    head -11 "$CONTEXT_FILE" | column -t -s','
    echo ""
fi

echo "=========================================="
echo "Analysis complete! Use these files for:"
echo "  • Attention mechanisms (which features matter?)"
echo "  • Counterfactual explanations (decision boundaries)"
echo "  • State-action pattern analysis"
echo "=========================================="
echo ""
