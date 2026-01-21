"""
WIDPS Runtime Orchestrator

This file wires the entire data pipeline:

Ingest → State → Snapshot → Detectors → Correlation → Scoring → Output

No logic lives here.
No decisions are made here.
This is the execution backbone.
"""

import time

from state.store import StateStore
from events.engine import EventEngine

from .output.telemetry import TelemetryPublisher

from .output.broadcaster import broadcaster



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

        # Expire old entries
        self.state.expire()

        # Take immutable snapshot
        snapshot = self.state.snapshot()

        # TELEMETRY (always emitted)
        telemetry_msg = build_telemetry_message(snapshot)
        await broadcaster.broadcast(telemetry_msg)

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
