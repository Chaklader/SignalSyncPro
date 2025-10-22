#!/bin/bash
# parse_q_values.sh - Extract Q-values from testing.log
# Usage: ./parse_q_values.sh <testing_log_file>

if [ $# -eq 0 ]; then
    echo "Usage: $0 <testing_log_file>"
    echo "Example: $0 testing.log"
    echo ""
    echo "This script extracts all Q-value logs from the testing log file."
    echo "Output includes: scenario, step, phase, Q-values, and selected action."
    exit 1
fi

LOG_FILE="$1"

if [ ! -f "$LOG_FILE" ]; then
    echo "Error: File '$LOG_FILE' not found!"
    exit 1
fi

echo "Extracting Q-values from: $LOG_FILE"
echo "=========================================="
echo ""

# Create output CSV file
OUTPUT_FILE="${LOG_FILE%.log}_q_values.csv"
echo "scenario,step,phase,continue_q,skip2p1_q,next_q,ped_q,selected_action" > "$OUTPUT_FILE"

awk '
BEGIN {
    scenario = "Unknown"
    step = 0
    current_phase = "Unknown"
    q_line = ""
    selected = ""
}

# Capture scenario name
/Generating DEVELOPED control routes for scenario:/ {
    scenario = $NF
    step = 0
    next
}

# Track current phase from phase change logs
/\[PHASE CHANGE\] TLS 3: Phase/ {
    # Extract the destination phase (after arrow symbol)
    # Split on spaces and get the number after the arrow
    for (i = 1; i <= NF; i++) {
        if ($i ~ /^[0-9]+$/ && $(i-1) !~ /Phase/) {
            current_phase = $i
            break
        }
    }
    next
}

# Track MAX_GREEN forced changes
/\[MAX_GREEN FORCED\] TLS 3: Phase/ {
    # Extract the destination phase (after arrow symbol)
    for (i = 1; i <= NF; i++) {
        if ($i ~ /^[0-9]+$/ && $(i-1) !~ /Phase/) {
            current_phase = $i
            break
        }
    }
    next
}

# Capture step number from Pedestrian Debug or Safety Summary
/\[PEDESTRIAN DEBUG\] Step [0-9]+:/ {
    # Extract step number - the field after Step
    for (i = 1; i <= NF; i++) {
        if ($i == "Step" && $(i+1) ~ /^[0-9]+:?$/) {
            gsub(/:/, "", $(i+1))
            step = $(i+1)
            break
        }
    }
    next
}

/\[SAFETY SUMMARY\] Step [0-9]+:/ {
    # Extract step number - the field after Step
    for (i = 1; i <= NF; i++) {
        if ($i == "Step" && $(i+1) ~ /^[0-9]+:?$/) {
            gsub(/:/, "", $(i+1))
            step = $(i+1)
            break
        }
    }
    next
}

# Capture Q-values line
/^  Q-values: Continue=/ {
    q_line = $0
    # Extract Q-values by splitting on commas and equals
    split(q_line, parts, ", ")
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
        else if (parts[i] ~ /Ped=/) {
            split(parts[i], temp, "=")
            ped_q = temp[2]
        }
    }
    next
}

# Capture selected action
/^  Selected: [0-9]+/ {
    # Extract the number after "Selected:"
    for (i = 1; i <= NF; i++) {
        if ($i == "Selected:" && $(i+1) ~ /^[0-9]+$/) {
            selected = $(i+1)
            break
        }
    }
    if (selected == "") {
        # Try without colon
        for (i = 1; i <= NF; i++) {
            if ($i ~ /^[0-9]+$/ && $(i-1) == "Selected:") {
                selected = $i
                break
            }
        }
    }
    
    # Map action number to name
    if (selected == "0") action_name = "Continue"
    else if (selected == "1") action_name = "Skip2P1"
    else if (selected == "2") action_name = "Next"
    else if (selected == "3") action_name = "Pedestrian"
    else action_name = "Unknown"
    
    # Print to CSV
    if (q_line != "") {
        printf "%s,%d,%s,%.3f,%.3f,%.3f,%.3f,%s\n", \
            scenario, step, current_phase, \
            continue_q, skip2p1_q, next_q, ped_q, \
            action_name
    }
    
    # Reset for next Q-value
    q_line = ""
    selected = ""
    next
}
' "$LOG_FILE" >> "$OUTPUT_FILE"

# Count Q-values extracted
Q_COUNT=$(tail -n +2 "$OUTPUT_FILE" | wc -l | tr -d ' ')

echo ""
echo "=========================================="
echo "Extraction complete!"
echo "Total Q-values extracted: $Q_COUNT"
echo "Output saved to: $OUTPUT_FILE"
echo ""
echo "CSV columns:"
echo "  - scenario: Test scenario name (e.g., Pr_0, Bi_1)"
echo "  - step: Simulation step number"
echo "  - phase: Current traffic signal phase"
echo "  - continue_q: Q-value for Continue action"
echo "  - skip2p1_q: Q-value for Skip to P1 action"
echo "  - next_q: Q-value for Next Phase action"
echo "  - ped_q: Q-value for Pedestrian action"
echo "  - selected_action: Action chosen by agent"
echo ""

# Show summary by scenario
echo "=========================================="
echo "Q-Values Summary by Scenario"
echo "=========================================="
echo ""

# Get unique scenarios and show count for each
awk -F',' '
NR>1 {
    scenarios[$1]++
}
END {
    for (s in scenarios) {
        print s ": " scenarios[s] " Q-values"
    }
}' "$OUTPUT_FILE" | sort

echo ""
echo "=========================================="
echo "All Q-Values (grouped by scenario)"
echo "=========================================="
echo ""

# Show all Q-values grouped by scenario
awk -F',' '
BEGIN {
    print "SCENARIO | STEP  | PHASE | CONTINUE | SKIP2P1 | NEXT    | PED     | SELECTED"
    print "---------|-------|-------|----------|---------|---------|---------|-------------"
}
NR>1 {
    printf "%-8s | %-5s | %-5s | %-8s | %-7s | %-7s | %-7s | %s\n", 
           $1, $2, $3, $4, $5, $6, $7, $8
}' "$OUTPUT_FILE" | sort -t'|' -k1,1 -k2,2n

echo ""
