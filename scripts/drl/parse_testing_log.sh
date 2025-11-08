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
    buffer = ""
    traffic_buffer = ""
    scenario_name = ""
}

# Capture traffic config when scenario starts
/^Generating DEVELOPED control routes for scenario:/ {
    scenario_name = $NF
    traffic_buffer = "Scenario: " scenario_name "\n"
    next
}

# Capture traffic details
/^  (Cars|Bicycles|Pedestrians|Buses):/ && traffic_buffer != "" {
    traffic_buffer = traffic_buffer $0 "\n"
    next
}

# Start capturing from [ACTION SUMMARY]
/^\[ACTION SUMMARY\]/ {
    capturing = 1
    buffer = $0 "\n"
    next
}

# While capturing, accumulate everything
capturing == 1 {
    buffer = buffer $0 "\n"
    
    # Check if we hit the end of final safety summary
    if (/^================================================================================/ && prev_line ~ /Violation Rate:/) {
        capturing = 0
        scenario_num++
        
        # Print scenario header
        print "================================================================================"
        print "SCENARIO " scenario_num " - " scenario_name
        print "================================================================================"
        
        # Print traffic config
        if (traffic_buffer != "") {
            print "TRAFFIC CONFIG:"
            printf "%s", traffic_buffer
            print ""
        }
        
        # Print buffered content (Action Summary + Episode Summary + Final Safety)
        printf "%s", buffer
        print ""
        
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
' "$LOG_FILE"

echo ""
echo "========================================"
echo "Parsing complete!"
