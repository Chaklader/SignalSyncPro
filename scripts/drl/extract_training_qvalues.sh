#!/bin/bash
# extract_qvalues.sh - Extract Q-value summary statistics from training.log

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

echo "Extracting Q-value statistics from: $LOG_FILE"
echo "================================================================================"
echo ""
echo "Episode | Avg Continue | Avg Skip2P1 | Avg Next | Avg Ped | Gap (Ped-Cont) | Best Action Distribution"
echo "--------|--------------|-------------|----------|---------|----------------|---------------------------"

awk '
/^\[Q-VALUE CHECK\] Episode [0-9]+ - Pedestrian Q-value Analysis/ {
    # Extract episode number
    for (i=1; i<=NF; i++) {
        if ($i == "Episode") {
            episode = $(i+1)
            break
        }
    }
}

/Avg Continue Q-value:/ {
    continue_q = $4
}

/Avg Skip2P1 Q-value:/ {
    skip2p1_q = $4
}

/Avg Next Q-value:/ {
    next_q = $4
}

/Avg Ped Q-value:/ {
    ped_q = $4
}

/Gap \(Ped - Continue\):/ {
    gap = $5
}

/Best Action Distribution:/ {
    in_distribution = 1
    continue_pct = ""
    skip2p1_pct = ""
    next_pct = ""
    ped_pct = ""
}

in_distribution == 1 && /Continue    :/ {
    # Extract percentage from format: ( 24.9%)
    # Field 5 is the percentage with %)
    pct = $5
    gsub(/[()%]/, "", pct)
    continue_pct = pct
}

in_distribution == 1 && /Skip2P1     :/ {
    # Handle both formats: ( 75.1%) and (100.0%)
    # Also handle line wrapping where % might be on next line
    if (NF >= 5) {
        pct = $5
    } else {
        pct = $4
    }
    gsub(/[()%]/, "", pct)
    # Remove any trailing characters
    gsub(/[^0-9.]/, "", pct)
    skip2p1_pct = pct
}

in_distribution == 1 && /Next        :/ {
    pct = $5
    gsub(/[()%]/, "", pct)
    next_pct = pct
}

in_distribution == 1 && /Pedestrian  :/ {
    pct = $5
    gsub(/[()%]/, "", pct)
    ped_pct = pct
    
    # Print the complete row
    printf "%7s | %12s | %11s | %8s | %7s | %14s | C:%s%% S:%s%% N:%s%% P:%s%%\n", 
           episode, continue_q, skip2p1_q, next_q, ped_q, gap,
           continue_pct, skip2p1_pct, next_pct, ped_pct
    
    # Reset for next episode
    in_distribution = 0
    episode = ""
    continue_q = ""
    skip2p1_q = ""
    next_q = ""
    ped_q = ""
    gap = ""
}
' "$LOG_FILE"

echo ""
echo "================================================================================"
echo "Legend:"
echo "  C = Continue, S = Skip2P1, N = Next, P = Pedestrian"
echo "  Gap = Ped Q-value - Continue Q-value (target: < 0.5 for competitive)"
echo "================================================================================"
