from typing import Optional
from .types import Event, EventType
from time import time

class EventEngine:
    def __init__(self):
        self._prev_snapshot = None #initializing prev_snapshot

    def process(self, snapshot): #compare current snapshot with previous snapshot and emit events
        events = []

        if self._prev_snapshot is None: #checks if the snapshot is new (used in case if startup)
            self._prev_snapshot = snapshot
            return events

        events.extend(self._detect_new_aps(snapshot)) #detects new ap by unique bssid
        events.extend(self._detect_gone_aps(snapshot)) #detects ap which disappeared
        events.extend(self._detect_evil_twins(snapshot)) #to detect fake aps (same name, diff hardware)
        events.extend(self._detect_clients(snapshot)) #detects new clients 

        self._prev_snapshot = snapshot #marks current snapshots as previous snapshots to compare it with next snapshot
        return events
