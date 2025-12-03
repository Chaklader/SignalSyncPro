from constants.developed.multi_agent.drl_tls_constants import (
    TLS_IDS,
    HEADWAY_TIME_FOR_SIGNAL_CONTROL,
    get_priority_action,
)

"""

                    c              e              g              i              k
                    │              │              │              │              │
                    9             13             26             30             34
                    │              │              │              │              │
                   10             14             27             31             35
                    │              │              │              │              │
   a────1────2────[3]────4────5──[6]────7───20─[17]───21───22─[18]───23───24─[19]───25────8────b
                    │              │              │              │              │
                   11             15             28             32             36
                    │              │              │              │              │
                   12             16             29             33             37
                    │              │              │              │              │
                    d              f              h              j              l


   x=-1100        x=0          x=1000         x=2000         x=3000         x=4000        x=5100
   (Entry)      TLS-1          TLS-2          TLS-3          TLS-4          TLS-5         (Exit)

"""

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
            sync_offset = travel_time - HEADWAY_TIME_FOR_SIGNAL_CONTROL
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

            if 0 < time_to_arrival <= HEADWAY_TIME_FOR_SIGNAL_CONTROL:
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

    def get_sync_priority_action(self, tls_id, current_phase, green_duration):
        if not self.is_priority_active(tls_id):
            return None
        return get_priority_action(current_phase, green_duration)

    def clear_timers(self, tls_id):
        self.sync_timers[tls_id] = {}
        self.sync_priority_active[tls_id] = False
