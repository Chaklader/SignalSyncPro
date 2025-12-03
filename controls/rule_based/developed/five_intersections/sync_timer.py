from constants.developed.multi_agent.drl_tls_constants import (
    TLS_IDS,
    p1_main_green,
    PRIORITY_ACTION_HOLD,
    PRIORITY_ACTION_CYCLE,
    PRIORITY_ACTION_SKIP,
    WARNING_TIME,
    HOLD_THRESHOLD,
)


TRAVEL_TIMES = {
    ("3", "6"): 64,
    ("6", "3"): 64,
    ("6", "17"): 64,
    ("17", "6"): 64,
    ("17", "18"): 64,
    ("18", "17"): 64,
    ("18", "19"): 64,
    ("19", "18"): 64,
}

ADJACENT_TLS = {
    "3": ["6"],
    "6": ["3", "17"],
    "17": ["6", "18"],
    "18": ["17", "19"],
    "19": ["18"],
}


class SyncTimerManager:
    def __init__(self):
        self.sync_timers = {tls_id: {} for tls_id in TLS_IDS}
        self.sync_priority_active = {tls_id: False for tls_id in TLS_IDS}

    def on_p1_end(self, source_tls_id, current_time):
        adjacent = ADJACENT_TLS.get(source_tls_id, [])

        for target_tls_id in adjacent:
            travel_time = TRAVEL_TIMES.get((source_tls_id, target_tls_id), 64)
            sync_offset = travel_time - WARNING_TIME
            arrival_time = current_time + travel_time

            self.sync_timers[target_tls_id][source_tls_id] = {
                "set_time": current_time,
                "arrival_time": arrival_time,
                "sync_offset": sync_offset,
            }

    def update(self, current_time):
        for tls_id in TLS_IDS:
            self._update_priority_status(tls_id, current_time)
            self._cleanup_expired_timers(tls_id, current_time)

    def _update_priority_status(self, tls_id, current_time):
        timers = self.sync_timers.get(tls_id, {})

        self.sync_priority_active[tls_id] = False

        for _, timer_info in timers.items():
            arrival_time = timer_info["arrival_time"]
            time_to_arrival = arrival_time - current_time

            if 0 < time_to_arrival <= WARNING_TIME:
                self.sync_priority_active[tls_id] = True
                break

    def _cleanup_expired_timers(self, tls_id, current_time):
        timers = self.sync_timers.get(tls_id, {})
        expired = []

        for source_tls_id, timer_info in timers.items():
            if current_time > timer_info["arrival_time"]:
                expired.append(source_tls_id)

        for source_tls_id in expired:
            del timers[source_tls_id]

    def is_priority_active(self, tls_id):
        return self.sync_priority_active.get(tls_id, False)

    def get_priority_action(self, tls_id, current_phase, green_duration):
        if not self.is_priority_active(tls_id):
            return None

        if current_phase == p1_main_green:
            if green_duration < HOLD_THRESHOLD:
                return PRIORITY_ACTION_HOLD
            else:
                return PRIORITY_ACTION_CYCLE
        else:
            return PRIORITY_ACTION_SKIP

    def clear_timers(self, tls_id):
        self.sync_timers[tls_id] = {}
        self.sync_priority_active[tls_id] = False
