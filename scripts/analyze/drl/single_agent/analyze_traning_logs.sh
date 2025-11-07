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
    # Arrays to store Q-values and action distributions by episode number
    # Arrays to store exploitation decisions and penalties
    exploit_decision_buffer = ""
    exploit_penalty_buffer = ""
    # Buffer to store reward events (bonuses and penalties)
    reward_events_buffer = ""
}

/^Generating DEVELOPED control routes for scenario:/ {
    in_initial_traffic = 1
    initial_traffic_buffer = "Episode 1 - Generating routes (initial):\n"
    next
}

in_initial_traffic == 1 && /^  (Cars|Bicycles|Pedestrians|Buses):/ {
    line = $0
    gsub(/\/hr$/, "", line)
    initial_traffic_buffer = initial_traffic_buffer line "\n"
    next
}

in_initial_traffic == 1 && /^✓ DEVELOPED control route generation complete/ {
    in_initial_traffic = 0
    next
}

/^Episode [0-9]+ - (Generating|Using)/ {
    in_traffic = 1
    traffic_buffer = $0 "\n"
    next
}

in_traffic == 1 && /^  (Cars|Bicycles|Pedestrians|Buses):/ {
    traffic_buffer = traffic_buffer $0 "\n"
    next
}

in_traffic == 1 && /^======================================================================/ {
    in_traffic = 0
    next
}

/^\[Q-VALUE CHECK\] Episode [0-9]+ - / {
    in_qvalue = 1
    for (i=1; i<=NF; i++) {
        if ($i == "Episode") {
            qvalue_episode_num = $(i+1)
            break
        }
    }
    qvalue_buffer = "======================================================================\n" $0 "\n"
    next
}

in_qvalue == 1 {
    qvalue_buffer = qvalue_buffer $0 "\n"
    
    if (/^======================================================================/ && qvalue_buffer ~ /Best Action Distribution:/) {
        in_qvalue = 0
        qvalue_buffers[qvalue_episode_num] = qvalue_buffer
        qvalue_buffer = ""
    }
    next
}

/^\[ACTION DISTRIBUTION\] Episode Summary:/ {
    in_action_dist = 1
    action_dist_buffer = $0 "\n"
    next
}

in_action_dist == 1 && /^  (Continue|Skip2P1|Next)/ {
    action_dist_buffer = action_dist_buffer $0 "\n"
    next
}

# Capture Exploitation ACT phase changes (actual decisions)
/^\[PHASE CHANGE\].*Exploitation ACT:/ {
    exploit_decision_buffer = exploit_decision_buffer $0 "\n"
    next
}

# Capture Exploitation ACT blocked actions (penalties)
/^\[BLOCKED\].*Exploitation ACT:/ {
    exploit_penalty_buffer = exploit_penalty_buffer $0 "\n"
    next
}

# Capture reward event types (bonuses and penalties)
/^\[(EARLY CHANGE|SKIP2P1 BONUS|SKIP2P1 EFFECTIVE|CONTINUE UNDERUSED|ACTION 2 OVERUSED|STABILITY BONUS|CONTINUE SPAM|NEXT BONUS|BLOCKED - BUS WAIT|BUS PENALTY|BUS EXCELLENT|MAX_GREEN FORCED)\]/ {
    reward_events_buffer = reward_events_buffer $0 "\n"
    next
}

# End of action distribution (blank line after)
in_action_dist == 1 && /^$/ {
    in_action_dist = 0
    action_dist_buffers[episode_num] = action_dist_buffer
    action_dist_buffer = ""
    
    if (pending_print == 1) {
        print "================================================================================"
        print "EPISODE " pending_episode_num
        print "================================================================================"
        printf "%s", pending_episode_buffer
        
        if (qvalue_buffers[pending_episode_num] != "") {
            print "Q-VALUE ANALYSIS:"
            printf "%s", qvalue_buffers[pending_episode_num]
            print ""
            delete qvalue_buffers[pending_episode_num]
        }
        
        if (action_dist_buffers[pending_episode_num] != "") {
            print "ACTION DISTRIBUTION:"
            printf "%s", action_dist_buffers[pending_episode_num]
            print ""
            delete action_dist_buffers[pending_episode_num]
        }
        
        # Print exploitation decisions
        if (exploit_decision_buffer != "") {
            print "EXPLOITATION DECISIONS - Agent Actual Choices:"
            printf "%s", exploit_decision_buffer
            print ""
        }
        
        # Print exploitation penalties
        if (exploit_penalty_buffer != "") {
            print "PENALTY EVENTS - Blocked Actions:"
            printf "%s", exploit_penalty_buffer
            print ""
        }
        
        # Print reward events
        if (reward_events_buffer != "") {
            print "REWARD EVENTS - Bonuses and Penalties:"
            printf "%s", reward_events_buffer
            print ""
        }
        
        # Reset buffers for next episode
        exploit_decision_buffer = ""
        exploit_penalty_buffer = ""
        reward_events_buffer = ""
        
        pending_print = 0
        pending_episode_buffer = ""
    }
    next
}

/^\[EPISODE SUMMARY\] Phase Change Statistics:/ {
    capturing = 1
    buffer = $0 "\n"
    next
}

capturing == 1 && !/^Episode [0-9]+ Complete:/ {
    buffer = buffer $0 "\n"
    next
}

/^Episode [0-9]+ Complete:/ {
    episode_num++
    pending_episode_num = episode_num
    pending_print = 1
    
    pending_episode_buffer = ""
    
    if (traffic_buffer != "") {
        pending_episode_buffer = pending_episode_buffer "TRAFFIC CONFIG:\n"
        pending_episode_buffer = pending_episode_buffer traffic_buffer
        pending_episode_buffer = pending_episode_buffer "\n"
        traffic_buffer = ""
    } else if (episode_num == 1 && initial_traffic_buffer != "") {
        pending_episode_buffer = pending_episode_buffer "TRAFFIC CONFIG:\n"
        pending_episode_buffer = pending_episode_buffer initial_traffic_buffer
        pending_episode_buffer = pending_episode_buffer "\n"
        initial_traffic_buffer = ""
    }
    
    pending_episode_buffer = pending_episode_buffer buffer
    pending_episode_buffer = pending_episode_buffer $0 "\n"
    
    buffer = ""
    capturing = 0
    in_episode = 1
    next
}

in_episode == 1 && /^  / {
    pending_episode_buffer = pending_episode_buffer $0 "\n"
    next
}

in_episode == 1 && /^================================================================================/ {
    pending_episode_buffer = pending_episode_buffer $0 "\n\n"
    in_episode = 0
    next
}

END {
    if (pending_print == 1) {
        print "================================================================================"
        print "EPISODE " pending_episode_num
        print "================================================================================"
        printf "%s", pending_episode_buffer
        
        if (qvalue_buffers[pending_episode_num] != "") {
            print "Q-VALUE ANALYSIS:"
            printf "%s", qvalue_buffers[pending_episode_num]
            print ""
        }
        
        if (action_dist_buffers[pending_episode_num] != "") {
            print "ACTION DISTRIBUTION:"
            printf "%s", action_dist_buffers[pending_episode_num]
            print ""
        }
        
        # Print exploitation decisions for last episode
        if (exploit_decision_buffer != "") {
            print "EXPLOITATION DECISIONS - Agent Actual Choices:"
            printf "%s", exploit_decision_buffer
            print ""
        }
        
        # Print exploitation penalties for last episode
        if (exploit_penalty_buffer != "") {
            print "PENALTY EVENTS - Blocked Actions:"
            printf "%s", exploit_penalty_buffer
            print ""
        }
        
        # Print reward events for last episode
        if (reward_events_buffer != "") {
            print "REWARD EVENTS - Bonuses and Penalties:"
            printf "%s", reward_events_buffer
            print ""
        }
    }
}
' "$LOG_FILE"

echo ""
echo "========================================"
echo "Parsing complete!"
