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
    buffer = ""
    traffic_buffer = ""
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
