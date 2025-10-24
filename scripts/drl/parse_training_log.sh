#!/bin/bash
# parse_training_log.sh - Extract episode summaries from training.log

if [ $# -eq 0 ]; then
    echo "Usage: $0 <training_log_file>"
    echo "Example: $0 training.log"
    exit 1
fi

LOG_FILE="$1"

if [ ! -f "$LOG_FILE" ]; then
    echo "Error: File '$LOG_FILE' not found!"
    exit 1
fi

echo "Parsing training log: $LOG_FILE"
echo "========================================"
echo ""

 awk '
BEGIN {
    episode_num = 0
    capturing = 0
    in_episode = 0
    in_traffic = 0
    in_initial_traffic = 0
    in_qvalue = 0
    buffer = ""
    traffic_buffer = ""
    initial_traffic_buffer = ""
    qvalue_buffer = ""
}

# Capture initial traffic config (for Episode 1)
/^Generating DEVELOPED control routes for scenario:/ {
    in_initial_traffic = 1
    initial_traffic_buffer = "Episode 1 - Generating routes (initial):\n"
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

# Capture traffic config (Episode X - Generating routes:)
/^Episode [0-9]+ - Generating routes:/ {
    in_traffic = 1
    traffic_buffer = $0 "\n"
    next
}

# Capture traffic details (Cars, Bicycles, Pedestrians, Buses)
in_traffic == 1 && /^  (Cars|Bicycles|Pedestrians|Buses):/ {
    traffic_buffer = traffic_buffer $0 "\n"
    next
}

# End of traffic block
in_traffic == 1 && /^======================================================================/ {
    in_traffic = 0
    next
}

# Capture Q-value analysis section
/^\[Q-VALUE CHECK\] Episode [0-9]+ - Pedestrian Q-value Analysis/ {
    in_qvalue = 1
    qvalue_buffer = $0 "\n"
    next
}

# Capture Q-value section content
in_qvalue == 1 {
    qvalue_buffer = qvalue_buffer $0 "\n"
    
    # End of Q-value section (marked by the separator line after the summary)
    if (/^======================================================================/ && qvalue_buffer ~ /Best Action Distribution:/) {
        in_qvalue = 0
    }
    next
}

# Start capturing from Phase Change Statistics
/^\[EPISODE SUMMARY\] Phase Change Statistics:/ {
    capturing = 1
    buffer = $0 "\n"
    next
}

# While capturing, accumulate everything (including Safety Summary)
capturing == 1 && !/^Episode [0-9]+ Complete:/ {
    buffer = buffer $0 "\n"
    next
}

# When we hit Episode X Complete, print everything
/^Episode [0-9]+ Complete:/ {
    episode_num++
    
    # Print episode header
    print "================================================================================"
    print "EPISODE " episode_num
    print "================================================================================"
    
    # Print traffic config if captured
    if (traffic_buffer != "") {
        print "TRAFFIC CONFIG:"
        printf "%s", traffic_buffer
        print ""
        traffic_buffer = ""
    } else if (episode_num == 1 && initial_traffic_buffer != "") {
        # Use initial traffic config for Episode 1
        print "TRAFFIC CONFIG:"
        printf "%s", initial_traffic_buffer
        print ""
        initial_traffic_buffer = ""
    }
    
    # Print Q-value analysis if captured
    if (qvalue_buffer != "") {
        print "Q-VALUE ANALYSIS:"
        printf "%s", qvalue_buffer
        print ""
        qvalue_buffer = ""
    }
    
    # Print buffered content (Phase Stats + Safety Summary)
    printf "%s", buffer
    
    # Print Episode Complete line
    print $0
    
    # Clear buffer and stop capturing
    buffer = ""
    capturing = 0
    
    # Now capture episode details
    in_episode = 1
    next
}

# Capture episode details (indented lines)
in_episode == 1 && /^  / {
    print $0
    next
}

# End of episode block
in_episode == 1 && /^================================================================================/ {
    print $0
    print ""
    in_episode = 0
    next
}
' "$LOG_FILE"

echo ""
echo "========================================"
echo "Parsing complete!"
