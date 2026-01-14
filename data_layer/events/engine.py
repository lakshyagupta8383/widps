from events.detectors.ap_detectors import detect_new_aps, detect_gone_aps
from events.detectors.client_detectors import detect_clients
from events.detectors.evil_twin import detect_evil_twins

from events.correlation.engine import CorrelationEngine
from events.scoring.scorer import AlertScorer


class EventEngine:
    def __init__(self):
        self._prev_snapshot = None
        self._correlation = CorrelationEngine()  
        self._scorer = AlertScorer()               

    def process(self, snapshot):
        events = []

        # first snapshot → nothing to compare
        if self._prev_snapshot is None:
            self._prev_snapshot = snapshot
            return []

        # 1. DETECTION (atomic)
        events.extend(detect_new_aps(self._prev_snapshot, snapshot))
        events.extend(detect_gone_aps(self._prev_snapshot, snapshot))
        events.extend(detect_clients(self._prev_snapshot, snapshot))
        events.extend(detect_evil_twins(self._prev_snapshot, snapshot))

        alerts = []

        # 2. CORRELATION (patterns)
        for event in events:
            alerts.extend(self._correlation.process(event))

        # 3. SCORING (severity)
        scored_alerts = []
        for alert in alerts:
            scored_alerts.append(self._scorer.score(alert))

        self._prev_snapshot = snapshot
        return scored_alerts
