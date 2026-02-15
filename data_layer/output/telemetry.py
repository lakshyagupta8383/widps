import time
import asyncio
from collections import defaultdict

from .broadcaster import broadcaster


class TelemetryPublisher:
    def __init__(self, runtime, interval: int = 1):
        self.runtime = runtime
        self.interval = interval
        self.start_time = time.time()

    async def run(self):
        print("[telemetry] TelemetryPublisher.run() started")
        while True:
            snapshot = self.runtime.state.snapshot()  # snapshot of current state

            # ---- channel congestion ----
            channel_counts = defaultdict(int)  # hashmap for channels
            ap_signal = {}

            # ---- ssid & stability ----
            ssid_counts = defaultdict(int)
            stable_aps = 0
            transient_aps = 0

            for ap in snapshot["aps"].values():
                ch = ap.get("channel")
                sig = ap.get("signal")
                ssid = ap.get("ssid")

                # channel stats
                if ch is not None:
                    channel_counts[str(ch)] += 1

                if sig is not None:
                    ap_signal[ap["bssid"]] = sig  # signal of a particular ap

                # ssid stats
                if ssid:
                    ssid_counts[ssid] += 1

                # stability stats
                if ap.get("stability") == "STABLE":
                    stable_aps += 1
                else:
                    transient_aps += 1

            # ---- top ssids (top 5) ----
            top_ssids = sorted(
                ssid_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]

            message = {
                "type": "telemetry",
                "payload": {
                    "summary": {
                        "ap_count": len(snapshot["aps"]),
                        "client_count": len(snapshot["clients"]),
                        "stable_aps": stable_aps,
                        "transient_aps": transient_aps,
                        "uptime_sec": int(time.time() - self.start_time),
                    },

                    "heatmap": {
                        "channels": dict(channel_counts),
                        "ap_signal": ap_signal
                    },

                    # NEW (safe additive field)
                    "top_ssids": [
                        {"ssid": ssid, "ap_count": count}
                        for ssid, count in top_ssids
                    ],

                    # ---- FULL SNAPSHOT DATA (for tables) ----
                    "aps": list(snapshot["aps"].values()),
                    "clients": list(snapshot["clients"].values()),

                    "timestamp": int(time.time())
                }
            }

            # TEMP DEBUG
            print(
                "[telemetry]",
                "aps:", len(snapshot["aps"]),
                "clients:", len(snapshot["clients"]),
                "stable:", stable_aps,
                "transient:", transient_aps,
                "top_ssids:", top_ssids
            )
            print("TYPE OF APS:", type(snapshot["aps"]))

            await broadcaster.broadcast(message)
            await asyncio.sleep(self.interval)
