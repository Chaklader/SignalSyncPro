from constants.developed.multi_agent.drl_tls_constants import (
    TLS_IDS,
    PRIORITY_ACTION_HOLD,
    PRIORITY_ACTION_CYCLE,
    PRIORITY_ACTION_SKIP,
)
from controls.rule_based.developed.five_intersections.common import (
    BaseTLSController,
    MIN_GREEN,
    MAX_GREEN,
    MAIN_GREEN_PHASES,
)
from controls.rule_based.developed.five_intersections.bus_priority import (
    BusPriorityManager,
)


class IsolatedTLSController(BaseTLSController):
    def __init__(self):
        super().__init__()
        self.bus_priority_manager = BusPriorityManager()
        self.init_tls()

    def step(self):
        current_time = self._get_current_time()

        self.bus_priority_manager.update(current_time)
        self.update_phases()

        for tls_id in TLS_IDS:
            self.gap_out_detector.update(
                tls_id, self.current_phase[tls_id], current_time
            )

        for tls_id in TLS_IDS:
            phase = self.current_phase[tls_id]

            if phase in MAIN_GREEN_PHASES:
                self._handle_green_phase(tls_id, phase, current_time)
            else:
                self.handle_transition_phase(tls_id, phase)

    def _get_current_time(self):
        import traci

        return traci.simulation.getTime()

    def _handle_green_phase(self, tls_id, phase, current_time):
        self.phase_duration[tls_id] += 1
        duration = self.phase_duration[tls_id]
        min_green = MIN_GREEN.get(phase, 5)
        max_green = MAX_GREEN.get(phase, 30)

        if duration < min_green:
            return

        if duration >= max_green:
            self.terminate_phase(tls_id, phase)
            return

        bus_action = self.bus_priority_manager.get_priority_action(
            tls_id, phase, duration
        )
        if bus_action:
            if bus_action == PRIORITY_ACTION_HOLD:
                return
            elif bus_action == PRIORITY_ACTION_CYCLE:
                self.terminate_phase(tls_id, phase)
                return
            elif bus_action == PRIORITY_ACTION_SKIP:
                self._skip_to_p1(tls_id, phase)
                return

        if self.gap_out_detector.check_gap_out(tls_id, phase, current_time):
            self.terminate_phase(tls_id, phase)

    def _skip_to_p1(self, tls_id, phase):
        self.skip_to_p1_phase(tls_id, phase)
        self.bus_priority_manager.clear_priority(tls_id)

    def get_stats(self):
        stats = super().get_stats()
        for tls_id in TLS_IDS:
            stats[tls_id]["bus_priority"] = (
                self.bus_priority_manager.is_priority_active(tls_id)
            )
        return stats
