import time
import asyncio
from collections import defaultdict

from output.broadcaster import broadcaster


class TelemetryPublisher:
    """
    Periodically emits dashboard-ready telemetry over WebSocket.
    """

    def __init__(self, runtime, interval: int = 1):
        self.runtime = runtime
        self.interval = interval
        self.start_time = time.time()

    async def run(self):
        while True:
            snapshot = self.runtime.state.snapshot()

            # ---- channel congestion ----
            channel_counts = defaultdict(int)
            ap_signal = {}

            for ap in snapshot["aps"].values():
                ch = ap.get("channel")
                sig = ap.get("signal")

                if ch is not None:
                    channel_counts[str(ch)] += 1

                if sig is not None:
                    ap_signal[ap["bssid"]] = sig

            message = {
                "type": "telemetry",
                "payload": {
                    "summary": {
                        "ap_count": len(snapshot["aps"]),
                        "client_count": len(snapshot["clients"]),
                        "uptime_sec": int(time.time() - self.start_time),
                    },

                    "heatmap": {
                        "channels": dict(channel_counts),
                        "ap_signal": ap_signal
                    },

                    "timestamp": int(time.time())
                }
            }

            await broadcaster.broadcast(message)
            await asyncio.sleep(self.interval)
