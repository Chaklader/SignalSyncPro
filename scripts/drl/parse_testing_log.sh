#!/bin/bash
# parse_testing_log.sh - Extract scenario summaries from testing.log

if [ $# -eq 0 ]; then
    echo "Usage: $0 <testing_log_file>"
    echo "Example: $0 testing.log"
    exit 1
fi

LOG_FILE="$1"

if [ ! -f "$LOG_FILE" ]; then
    echo "Error: File '$LOG_FILE' not found!"
    exit 1
fi

echo "Parsing testing log: $LOG_FILE"
echo "========================================"
echo ""

awk '
BEGIN {
    scenario_num = 0
    capturing = 0
    in_scenario_header = 0
    in_traffic = 0
    in_initial_traffic = 0
    buffer = ""
    traffic_buffer = ""
    initial_traffic_buffer = ""
    scenario_name = ""
}

# Capture initial traffic config (for first scenario)
/^Generating DEVELOPED control routes for scenario:/ {
    in_initial_traffic = 1
    scenario_name = $NF
    initial_traffic_buffer = "Scenario: " scenario_name "\n"
    next
}

# Capture initial traffic details
in_initial_traffic == 1 && /^  (Cars|Bicycles|Pedestrians|Buses):/ {
    # Remove "/hr" suffix from the line for consistency
    line = $0
    gsub(/\/hr$/, "", line)
    initial_traffic_buffer = initial_traffic_buffer line "\n"
    next
}

# End of initial traffic block
in_initial_traffic == 1 && /^✓ DEVELOPED control route generation complete/ {
    in_initial_traffic = 0
    next
}

# Capture scenario header (70 equals signs)
/^======================================================================$/ && in_scenario_header == 0 {
    in_scenario_header = 1
    next
}

# Capture scenario name
in_scenario_header == 1 && /^Scenario:/ {
    scenario_name = $2
    traffic_buffer = "Scenario: " scenario_name "\n"
    next
}

# Capture traffic config details
in_scenario_header == 1 && /^  (Cars|Bicycles|Pedestrians|Buses):/ {
    traffic_buffer = traffic_buffer $0 "\n"
    next
}

# End of scenario header
in_scenario_header == 1 && /^======================================================================$/ {
    in_scenario_header = 0
    next
}

# Start capturing from final Pedestrian Debug (Step 3600)
/^\[PEDESTRIAN DEBUG\] Step 3600:/ {
    capturing = 1
    buffer = $0 "\n"
    next
}

# While capturing, accumulate everything
capturing == 1 {
    buffer = buffer $0 "\n"
    
    # Check if we hit the end of final safety summary (the last separator line)
    if (/^================================================================================/ && prev_line ~ /Violation Rate:/) {
        capturing = 0
        scenario_num++
        
        # Print scenario header
        print "================================================================================"
        print "SCENARIO " scenario_num
        print "================================================================================"
        
        # Print traffic config if captured
        if (traffic_buffer != "") {
            print "TRAFFIC CONFIG:"
            printf "%s", traffic_buffer
            print ""
            traffic_buffer = ""
        } else if (scenario_num == 1 && initial_traffic_buffer != "") {
            # Use initial traffic config for first scenario
            print "TRAFFIC CONFIG:"
            printf "%s", initial_traffic_buffer
            print ""
            initial_traffic_buffer = ""
        }
        
        # Print buffered content (Pedestrian Debug + Safety Summary + Phase Stats + Final Safety)
        printf "%s", buffer
        print ""
        
        # Clear buffer
        buffer = ""
    }
    
    # Store previous line for checking
    prev_line = $0
    next
}

# Handle progress bar updates (skip them)
/^Testing scenarios:/ {
    next
}
' "$LOG_FILE"

echo ""
echo "========================================"
echo "Parsing complete!"
