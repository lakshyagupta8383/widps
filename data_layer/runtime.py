"""
WIDPS Runtime Orchestrator

This file wires the entire data pipeline:

Ingest → State → Snapshot → Detectors → Correlation → Scoring → Output

No logic lives here.
No decisions are made here.
This is the execution backbone.
"""

from state.store import StateStore

from events.engine import EventEngine
from events.correlation.engine import CorrelationEngine
from events.scoring.scorer import AlertScorer


class WIDPSRuntime:
    def __init__(self):
        # Core components
        self.state = StateStore()
        self.event_engine = EventEngine()
        self.correlation_engine = CorrelationEngine()
        self.alert_scorer = AlertScorer()

    def process_ingest_record(self, record: dict):
        """
        Called for every ingested JSON record.
        """

        #Update state
        self.state.update(record)

        #Expire old entries
        self.state.expire()

        #Take immutable snapshot
        snapshot = self.state.snapshot()

        #Run detectors->correlators->scorer (atomic events)
        scored_alerts = self.event_engine.process(snapshot)
        for scored_alert in scored_alerts:
            self.emit(scored_alert)

    def emit(self, scored_alert: dict):
        """
        Temporary sink.
        Later replaced by:
        - WebSocket
        - DB
        - Alert manager
        """
        print("\n ALERT")
        print(f"Type      : {scored_alert['type']}")
        print(f"Severity  : {scored_alert['severity']}")
        print(f"Confidence: {scored_alert['confidence']}%")
        print(f"Payload   : {scored_alert['payload']}")
        print("-" * 40)


