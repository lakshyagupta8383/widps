"""
WIDPS Runtime Orchestrator

This file wires the entire data pipeline:

Ingest → State → Snapshot → Detectors → Correlation → Scoring → Output

No logic lives here.
No decisions are made here.
This is the execution backbone.
"""

import time

from data_layer.state.store import StateStore
from data_layer.events.engine import EventEngine

from data_layer.output.broadcaster import broadcaster

class WIDPSRuntime:
    def __init__(self):
        # Core components
        self.state = StateStore()
        self.event_engine = EventEngine()

    async def process_ingest_record(self, record: dict):
        """
        Called for every ingested JSON record.
        """

        # Update state
        self.state.update(record)
        print(
            "[runtime] state sizes:",
            len(self.state.aps),
            len(self.state.clients),
            flush=True
        )
        # Expire old entries
        self.state.expire()

        # Take immutable snapshot
        snapshot = self.state.snapshot()

        # ALERTS (conditional)
        scored_alerts = self.event_engine.process(snapshot)
        for scored_alert in scored_alerts:
            await self.emit(scored_alert)

    async def emit(self, scored_alert: dict):
        message = {
            "type": "alert",
            "payload": {
                "alert_type": scored_alert["type"],
                "severity": scored_alert["severity"],
                "confidence": scored_alert["confidence"],
                "data": scored_alert["payload"],
                "timestamp": int(time.time())
            }
        }
        await broadcaster.broadcast(message)
