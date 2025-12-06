TODO:

1. Use Scale to 250-2500: Similar density per TLS as single-agent for 30 scenarios
2. Need to make sure both AI and rule based agent dont go to P1 right after P1. They will need to pass through P2
   earliest.
3. We need to track the waiting time and emission for the 30 scenarios for rule based with and without semi-sync controls
4. Check if 2-intersection corridor based controls testing still works fine
5. Correct the lane allowance and intersection radius for the 5-TLS network topology
6. Use correct traffic load for the 5-TLS test and training simulation
7. Log that we have for the rule-based controls added below
8. Update the note for bus pririty implementation


## What We Already Have (Makes Sense for Rule-Based)

| Log Tag | Purpose | Status |
|---------|---------|--------|
| `[BUS DETECTED]` | Bus enters emit lane | ✅ Added |
| `[BUS PRIORITY ACTIVATED/DEACTIVATED]` | Priority window state | ✅ Added |
| `[BUS PRIORITY ACTION]` | HOLD/CYCLE/SKIP taken | ✅ Added |
| `[BUS PRIORITY SUMMARY]` | Periodic stats | ✅ Added |
| `[SYNC TIMER SET]` | P1 ended, timer started | ✅ Added |
| `[SYNC PRIORITY ACTIVATED/DEACTIVATED]` | Sync window state | ✅ Added |
| `[SYNC PRIORITY ACTION]` | Action taken | ✅ Added |
| `[SYNC TIMER SUMMARY]` | Periodic stats | ✅ Added |
| `[PHASE CHANGE]` | With reason (gap_out, max_green, bus_priority, sync_priority) | ✅ Added |
| `[SKIP TO P1]` | Skip action taken | ✅ Added |
| `[GAP-OUT]` | Gap-out termination | ✅ Added |
| `[CONTROLLER SUMMARY]` | Transitions, skip-to-P1 count | ✅ Added |
| `[STEP N]` | Progress with wait times | ✅ Added |




In the P1 leading and P1 main, pedestrian has Protected Green and it switcheds to Red without any Yellow phase. Both protected and permissive Green for cars and Bicycle gets Yellow phase. P1 leadnign starts only with Bicycle and pedestrian and cars are served in the P1 main.

In the P2 leading and P2 main, pedestrians are always permissive Green and switched to Red without Yellow phase. Both the cars and Bicycle will have Protected Green and will sitched to Red with Yellow phase.

P3 and P4 has exactly same phase structures but for the minor roadways. So, for cars and Bicycle, we will always provide Yellow phase from both the protected and permissive Green but pedestrians will be directly switched to Red from both Protected and permissive Green.

| Phase          | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10  | 11  | 12  | 13  | 14  | 15  | 16  | 17  | 18  | 19  | 20  | 21  | 22  | 23  | 24  | 25  | 26  | 27  | 28  | 29  | 30  | 31  | 32  | 33  | 34  | 35  | 36  | 37  | 38  | 39  | 40  | 41  | 42  | 43  | 44  | 45  | 46  | 47  | 48  | 49  | 50  | 51  | 52  | Complete String                                        |
| -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------------------------------------------------ |
| **P1 Leading** | r   | r   | r   | r   | r   | r   | G   | g   | g   | G   | G   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | G   | g   | g   | G   | G   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | `rrrrrrGggGGrrrrrrrrrrrrrrrrrrrrrGggGGrrrrrrrrrrrrrrr` |
| **P1 Main**    | r   | r   | r   | r   | r   | r   | G   | g   | g   | G   | G   | r   | r   | g   | g   | G   | G   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | G   | g   | g   | G   | G   | r   | r   | g   | g   | G   | G   | r   | r   | r   | r   | r   | r   | r   | r   | r   | `rrrrrrGggGGrrggGGrrrrrrrrrrrrrrrGggGGrrggGGrrrrrrrrr` |
| **P1 Yellow**  | r   | r   | r   | r   | r   | r   | r   | y   | y   | y   | y   | r   | r   | y   | y   | y   | y   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | y   | y   | y   | y   | r   | r   | y   | y   | y   | y   | r   | r   | r   | r   | r   | r   | r   | r   | r   | `rrrrrrryyyyrryyyyrrrrrrrrrrrrrrrryyyyrryyyyrrrrrrrrr` |
| **P1 All-Red** | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | `rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr` |
| **P2 Leading** | r   | r   | r   | r   | r   | r   | g   | r   | r   | r   | r   | G   | G   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | g   | r   | r   | r   | r   | G   | G   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | `rrrrrrgrrrrGGrrrrrrrrrrrrrrrrrrrgrrrrGGrrrrrrrrrrrrr` |
| **P2 Main**    | r   | r   | r   | r   | r   | r   | g   | r   | r   | r   | r   | G   | G   | r   | r   | r   | r   | G   | G   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | g   | r   | r   | r   | r   | G   | G   | r   | r   | r   | r   | G   | G   | r   | r   | r   | r   | r   | r   | r   | `rrrrrrgrrrrGGrrrrGGrrrrrrrrrrrrrgrrrrGGrrrrGGrrrrrrr` |
| **P2 Yellow**  | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | y   | y   | r   | r   | r   | r   | y   | y   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | y   | y   | r   | r   | r   | r   | y   | y   | r   | r   | r   | r   | r   | r   | r   | `rrrrrrrrrrryyrrrryyrrrrrrrrrrrrrrrrrryyrrrryyrrrrrrr` |
| **P2 All-Red** | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | `rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr` |
| **P3 Leading** | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | G   | g   | g   | G   | G   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | G   | g   | g   | G   | G   | r   | r   | `rrrrrrrrrrrrrrrrrrrGggGGrrrrrrrrrrrrrrrrrrrrrGggGGrr` |
| **P3 Main**    | g   | g   | G   | G   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | G   | g   | g   | G   | G   | r   | r   | g   | g   | G   | G   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | G   | g   | g   | G   | G   | r   | r   | `ggGGrrrrrrrrrrrrrrrGggGGrrggGGrrrrrrrrrrrrrrrGggGGrr` |
| **P3 Yellow**  | y   | y   | y   | y   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | y   | y   | y   | y   | r   | r   | y   | y   | y   | y   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | y   | y   | y   | y   | r   | r   | `yyyyrrrrrrrrrrrrrrrryyyyrryyyyrrrrrrrrrrrrrrrryyyyrr` |
| **P3 All-Red** | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | `rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr` |
| **P4 Leading** | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | g   | r   | r   | r   | r   | G   | G   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | g   | r   | r   | r   | r   | G   | G   | `rrrrrrrrrrrrrrrrrrrgrrrrGGrrrrrrrrrrrrrrrrrrrgrrrrGG` |
| **P4 Main**    | r   | r   | r   | r   | G   | G   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | g   | r   | r   | r   | r   | G   | G   | r   | r   | r   | r   | G   | G   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | g   | r   | r   | r   | r   | G   | G   | `rrrrGGrrrrrrrrrrrrrgrrrrGGrrrrGGrrrrrrrrrrrrrgrrrrGG` |
| **P4 Yellow**  | r   | r   | r   | r   | y   | y   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | y   | y   | r   | r   | r   | r   | y   | y   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | y   | y   | `rrrryyrrrrrrrrrrrrrrrrrryyrrrryyrrrrrrrrrrrrrrrrrryy` |
| **P4 All-Red** | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | r   | `rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr` |

**Legend:**

- `G` = Protected green
- `g` = Permissive green
- `y` = Yellow
- `r` = Red




---
---

