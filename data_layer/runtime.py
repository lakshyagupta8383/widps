"""
WIDPS Runtime Orchestrator

This file wires the entire data pipeline:

Ingest → State → Snapshot → Detectors → Correlation → Scoring → Output

No logic lives here.
No decisions are made here.
This is the execution backbone.
"""

from ingest.api import ingest_event
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

        # 1️⃣ Update state
        self.state.update_from_ingest(record)

        # 2️⃣ Expire old entries
        self.state.expire()

        # 3️⃣ Take immutable snapshot
        snapshot = self.state.snapshot()

        # 4️⃣ Run detectors (atomic events)
        events = self.event_engine.process(snapshot)

        # 5️⃣ Correlate events (behavior patterns)
        for event in events:
            alerts = self.correlation_engine.process(event)

            # 6️⃣ Score correlated alerts
            for alert in alerts:
                scored_alert = self.alert_scorer.score(alert)

                # 7️⃣ Output (temporary)
                self.emit(scored_alert)

    def emit(self, scored_alert: dict):
        """
        Temporary sink.
        Later replaced by:
        - WebSocket
        - DB
        - Alert manager
        """
        print("\n🚨 ALERT")
        print(f"Type      : {scored_alert['type']}")
        print(f"Severity  : {scored_alert['severity']}")
        print(f"Confidence: {scored_alert['confidence']}%")
        print(f"Payload   : {scored_alert['payload']}")
        print("-" * 40)


# --------------------------------------------------
# Example runner (for testing)
# --------------------------------------------------

if __name__ == "__main__":
    runtime = WIDPSRuntime()

    print("WIDPS runtime started. Waiting for ingest events...\n")

    # Example: simulate ingest loop
    for record in ingest_event():
        runtime.process_ingest_record(record)
