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
    in_action_dist = 0
    pending_print = 0
    buffer = ""
    traffic_buffer = ""
    initial_traffic_buffer = ""
    qvalue_buffer = ""
    qvalue_episode_num = 0
    action_dist_buffer = ""
    pending_episode_buffer = ""
    pending_episode_num = 0
    # Arrays to store Q-values by episode number
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

# Capture traffic config (Episode X - Generating RANDOM routes: or Episode X - Using TEST scenario:)
/^Episode [0-9]+ - (Generating|Using)/ {
    # If we have a pending episode to print, print it now with action dist and qvalues
    if (pending_print == 1) {
        print "================================================================================"
        print "EPISODE " pending_episode_num
        print "================================================================================"
        printf "%s", pending_episode_buffer
        
        # Print Q-value analysis if captured for pending episode
        if (qvalue_buffers[pending_episode_num] != "") {
            print "Q-VALUE ANALYSIS:"
            printf "%s", qvalue_buffers[pending_episode_num]
            print ""
            delete qvalue_buffers[pending_episode_num]
        }
        
        # Print action distribution that was captured after episode complete
        if (action_dist_buffer != "") {
            print "ACTION DISTRIBUTION:"
            printf "%s", action_dist_buffer
            print ""
            action_dist_buffer = ""
        }
        
        pending_print = 0
        pending_episode_buffer = ""
    }
    
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
/^\[Q-VALUE CHECK\] Episode [0-9]+ - / {
    in_qvalue = 1
    # Extract episode number this Q-value belongs to
    for (i=1; i<=NF; i++) {
        if ($i == "Episode") {
            qvalue_episode_num = $(i+1)
            break
        }
    }
    # Start Q-value buffer with separator line and header
    qvalue_buffer = "======================================================================\n" $0 "\n"
    next
}

# Capture Q-value section content
in_qvalue == 1 {
    qvalue_buffer = qvalue_buffer $0 "\n"
    
    # End of Q-value section (marked by the separator line after the summary)
    if (/^======================================================================/ && qvalue_buffer ~ /Best Action Distribution:/) {
        in_qvalue = 0
        # Store Q-value for the specific episode
        qvalue_buffers[qvalue_episode_num] = qvalue_buffer
        qvalue_buffer = ""
    }
    next
}

# Capture action distribution section (appears AFTER episode complete)
/^\[ACTION DISTRIBUTION\] Episode Summary:/ {
    in_action_dist = 1
    action_dist_buffer = $0 "\n"
    next
}

# Capture action distribution content
in_action_dist == 1 && /^  (Continue|Skip2P1|Next)/ {
    action_dist_buffer = action_dist_buffer $0 "\n"
    next
}

# End of action distribution (blank line after)
in_action_dist == 1 && /^$/ {
    in_action_dist = 0
    # Action dist captured for current pending episode
    # Dont clear buffer yet, will be printed with pending episode
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

# When we hit Episode X Complete, save to pending buffer (dont print yet)
/^Episode [0-9]+ Complete:/ {
    episode_num++
    pending_episode_num = episode_num
    pending_print = 1
    
    # Build pending episode buffer (will print when next episode starts)
    pending_episode_buffer = ""
    
    # Add traffic config if captured
    if (traffic_buffer != "") {
        pending_episode_buffer = pending_episode_buffer "TRAFFIC CONFIG:\n"
        pending_episode_buffer = pending_episode_buffer traffic_buffer
        pending_episode_buffer = pending_episode_buffer "\n"
        traffic_buffer = ""
    } else if (episode_num == 1 && initial_traffic_buffer != "") {
        # Use initial traffic config for Episode 1
        pending_episode_buffer = pending_episode_buffer "TRAFFIC CONFIG:\n"
        pending_episode_buffer = pending_episode_buffer initial_traffic_buffer
        pending_episode_buffer = pending_episode_buffer "\n"
        initial_traffic_buffer = ""
    }
    
    # Add buffered content (Phase Stats + Safety Summary)
    pending_episode_buffer = pending_episode_buffer buffer
    
    # Add Episode Complete line
    pending_episode_buffer = pending_episode_buffer $0 "\n"
    
    # Clear buffer and stop capturing
    buffer = ""
    capturing = 0
    
    # Now capture episode details
    in_episode = 1
    next
}

# Capture episode details (indented lines)
in_episode == 1 && /^  / {
    pending_episode_buffer = pending_episode_buffer $0 "\n"
    next
}

# End of episode block
in_episode == 1 && /^================================================================================/ {
    pending_episode_buffer = pending_episode_buffer $0 "\n\n"
    in_episode = 0
    next
}

# Print final pending episode at end of file
END {
    if (pending_print == 1) {
        print "================================================================================"
        print "EPISODE " pending_episode_num
        print "================================================================================"
        printf "%s", pending_episode_buffer
        
        # Print Q-value analysis if captured for pending episode
        if (qvalue_buffers[pending_episode_num] != "") {
            print "Q-VALUE ANALYSIS:"
            printf "%s", qvalue_buffers[pending_episode_num]
            print ""
        }
        
        # Print action distribution that was captured after episode complete
        if (action_dist_buffer != "") {
            print "ACTION DISTRIBUTION:"
            printf "%s", action_dist_buffer
            print ""
        }
    }
}
' "$LOG_FILE"

echo ""
echo "========================================"
echo "Parsing complete!"
