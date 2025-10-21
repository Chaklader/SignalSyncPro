#!/bin/bash
# summarize_training_log.sh - Comprehensive training diagnostics
# Usage: ./summarize_training_log.sh [training_log_file]
# Default: Uses training.log in project root

# Set log file path
if [ $# -eq 0 ]; then
    LOG_FILE="training.log"
else
    LOG_FILE="$1"
fi

# Check if file exists
if [ ! -f "$LOG_FILE" ]; then
    echo "Error: File '$LOG_FILE' not found!"
    echo "Usage: $0 [training_log_file]"
    exit 1
fi

echo "================================================================================"
echo "TRAINING DIAGNOSTICS SUMMARY"
echo "================================================================================"
echo "Log file: $LOG_FILE"
echo "Generated: $(date)"
echo ""

# ============================================================================
# 1. MAX_GREEN BUG CHECK (Most Critical)
# ============================================================================
echo "================================================================================"
echo "1. MAX_GREEN BUG CHECK (Should see 44s for Phase 0-3, not 12s)"
echo "================================================================================"
echo ""
echo "Sample of forced changes for Phase 0-3 (Major arterial):"
grep "MAX_GREEN FORCED.*Phase [0-3]" "$LOG_FILE" | grep -v "Phase 16\|Phase 12" | head -10
echo ""
echo "If you see 'duration 12s >= MAX 12s' for Phase 0-3, the bug is NOT fixed!"
echo "Should see 'duration 44s >= MAX 44s' for Phase 0-3"
echo ""

# ============================================================================
# 2. FORCED CHANGES COUNT (Should Decrease Over Time)
# ============================================================================
echo "================================================================================"
echo "2. FORCED MAX_GREEN CHANGES"
echo "================================================================================"
echo ""
TOTAL_FORCED=$(grep "MAX_GREEN FORCED" "$LOG_FILE" | wc -l | tr -d ' ')
echo "Total forced changes: $TOTAL_FORCED"
echo ""
echo "Sample of recent forced changes:"
grep "MAX_GREEN FORCED" "$LOG_FILE" | tail -10
echo ""
echo "Target: < 2 per episode (< 200 total for 100 episodes)"
echo ""

# ============================================================================
# 3. STUCK WARNINGS (Should Decrease Over Time)
# ============================================================================
echo "================================================================================"
echo "3. STUCK WARNINGS (40s threshold)"
echo "================================================================================"
echo ""
TOTAL_STUCK=$(grep "STUCK WARNING" "$LOG_FILE" | wc -l | tr -d ' ')
echo "Total stuck warnings: $TOTAL_STUCK"
echo ""
if [ "$TOTAL_STUCK" -gt 0 ]; then
    echo "Sample of stuck warnings:"
    grep "STUCK WARNING" "$LOG_FILE" | tail -10
else
    echo "✅ No stuck warnings! Agent switching before 40s threshold."
fi
echo ""
echo "Target: Decreasing trend, ideally 0 by end of training"
echo ""

# ============================================================================
# 4. PHASE CHANGE RATE (Should Increase Over Time)
# ============================================================================
echo "================================================================================"
echo "4. PHASE CHANGE RATE PROGRESSION"
echo "================================================================================"
echo ""
echo "Recent phase change rates (last 20 episodes):"
grep "Phase change rate" "$LOG_FILE" | tail -20
echo ""
echo "Target: 20-40% by end of training"
echo ""

# ============================================================================
# 5. EPISODE SUMMARY STATISTICS
# ============================================================================
echo "================================================================================"
echo "5. EPISODE SUMMARY STATISTICS (Recent Episodes)"
echo "================================================================================"
echo ""
echo "Recent episode summaries (last 5):"
grep -A 3 "EPISODE SUMMARY" "$LOG_FILE" | tail -20
echo ""
echo "Target: Phase changes 1400-2000 per episode by end of training"
echo ""

# ============================================================================
# 6. REWARD PROGRESSION
# ============================================================================
echo "================================================================================"
echo "6. REWARD PROGRESSION"
echo "================================================================================"
echo ""
echo "Recent total rewards (last 20 episodes):"
grep "TOTAL:" "$LOG_FILE" | tail -20
echo ""
echo "Target: Trending upward (less negative), ideally > -2.0 by end"
echo ""

# ============================================================================
# 7. PEDESTRIAN PHASE ACTIVATION
# ============================================================================
echo "================================================================================"
echo "7. PEDESTRIAN PHASE ACTIVATION"
echo "================================================================================"
echo ""
TOTAL_PED=$(grep "Phase.*→ 16" "$LOG_FILE" | wc -l | tr -d ' ')
echo "Total pedestrian phase activations: $TOTAL_PED"
echo ""
if [ "$TOTAL_PED" -gt 0 ]; then
    echo "✅ Agent IS using pedestrian phases!"
else
    echo "❌ Agent NOT using pedestrian phases (Q-value likely very negative)"
fi
echo ""
echo "Target: > 100 total activations"
echo ""

# ============================================================================
# 8. TRAINING PROGRESS
# ============================================================================
echo "================================================================================"
echo "8. TRAINING PROGRESS"
echo "================================================================================"
echo ""
echo "Latest training progress:"
grep "Training:" "$LOG_FILE" | tail -5
echo ""

# ============================================================================
# 9. SAFETY VIOLATIONS
# ============================================================================
echo "================================================================================"
echo "9. SAFETY VIOLATIONS (Recent Episodes)"
echo "================================================================================"
echo ""
echo "Recent safety summaries (last 5 episodes):"
grep -A 5 "FINAL SAFETY SUMMARY" "$LOG_FILE" | tail -30
echo ""
echo "Target: Violations should stay low and not increase over time"
echo ""

# ============================================================================
# 10. QUICK HEALTH SUMMARY
# ============================================================================
echo "================================================================================"
echo "10. QUICK HEALTH SUMMARY"
echo "================================================================================"
echo ""

# Count episodes completed
EPISODES_DONE=$(grep "Episode [0-9]* Complete:" "$LOG_FILE" | wc -l | tr -d ' ')
echo "Episodes completed: $EPISODES_DONE / 100"
echo ""

# Get latest phase change rate
LATEST_RATE=$(grep "Phase change rate" "$LOG_FILE" | tail -1)
echo "Latest phase change rate: $LATEST_RATE"
echo ""

# Get latest reward
LATEST_REWARD=$(grep "TOTAL:" "$LOG_FILE" | tail -1)
echo "Latest reward: $LATEST_REWARD"
echo ""

# Calculate forced changes per episode
if [ "$EPISODES_DONE" -gt 0 ]; then
    FORCED_PER_EP=$(echo "scale=2; $TOTAL_FORCED / $EPISODES_DONE" | bc)
    echo "Forced changes per episode: $FORCED_PER_EP (target: < 2.0)"
else
    echo "Forced changes per episode: N/A (no episodes completed yet)"
fi
echo ""

# ============================================================================
# SUCCESS INDICATORS
# ============================================================================
echo "================================================================================"
echo "SUCCESS INDICATORS CHECKLIST"
echo "================================================================================"
echo ""

# Check MAX_GREEN bug
if grep -q "Phase [0-3].*duration 12s >= MAX 12s" "$LOG_FILE" 2>/dev/null; then
    echo "❌ MAX_GREEN Bug: STILL PRESENT (Phase 0-3 showing 12s instead of 44s)"
else
    echo "✅ MAX_GREEN Bug: FIXED (Phase 0-3 using correct values)"
fi

# Check phase change rate
LATEST_RATE_NUM=$(grep "Phase change rate" "$LOG_FILE" | tail -1 | grep -oE "[0-9]+\.[0-9]+")
if [ ! -z "$LATEST_RATE_NUM" ]; then
    if (( $(echo "$LATEST_RATE_NUM > 15.0" | bc -l) )); then
        echo "✅ Phase Change Rate: GOOD ($LATEST_RATE_NUM% - approaching target 20-40%)"
    elif (( $(echo "$LATEST_RATE_NUM > 10.0" | bc -l) )); then
        echo "⚠️  Phase Change Rate: IMPROVING ($LATEST_RATE_NUM% - target 20-40%)"
    else
        echo "❌ Phase Change Rate: LOW ($LATEST_RATE_NUM% - target 20-40%)"
    fi
fi

# Check forced changes
if [ "$EPISODES_DONE" -gt 0 ]; then
    if (( $(echo "$FORCED_PER_EP < 2.0" | bc -l) )); then
        echo "✅ Forced Changes: EXCELLENT ($FORCED_PER_EP per episode - target < 2.0)"
    elif (( $(echo "$FORCED_PER_EP < 5.0" | bc -l) )); then
        echo "⚠️  Forced Changes: GOOD ($FORCED_PER_EP per episode - target < 2.0)"
    else
        echo "❌ Forced Changes: TOO HIGH ($FORCED_PER_EP per episode - target < 2.0)"
    fi
fi

# Check stuck warnings
if [ "$TOTAL_STUCK" -eq 0 ]; then
    echo "✅ Stuck Warnings: PERFECT (0 warnings - agent switching proactively)"
elif [ "$TOTAL_STUCK" -lt 100 ]; then
    echo "⚠️  Stuck Warnings: LOW ($TOTAL_STUCK total - acceptable)"
else
    echo "❌ Stuck Warnings: HIGH ($TOTAL_STUCK total - agent not learning timing)"
fi

# Check pedestrian activation
if [ "$TOTAL_PED" -gt 1000 ]; then
    echo "✅ Pedestrian Phases: EXCELLENT ($TOTAL_PED activations)"
elif [ "$TOTAL_PED" -gt 100 ]; then
    echo "⚠️  Pedestrian Phases: GOOD ($TOTAL_PED activations)"
elif [ "$TOTAL_PED" -gt 0 ]; then
    echo "⚠️  Pedestrian Phases: LOW ($TOTAL_PED activations)"
else
    echo "❌ Pedestrian Phases: NONE (agent not using pedestrian action)"
fi

echo ""
echo "================================================================================"
echo "END OF DIAGNOSTICS"
echo "================================================================================"
echo ""
echo "For detailed episode-by-episode breakdown, use:"
echo "  ./scripts/drl/parse_training_log.sh $LOG_FILE"
echo ""
