from time import time
from events.types import Event, EventType

SIGNAL_THRESHOLD = -60  # strong signal = nearby AP


def detect_evil_twins(prev, curr):
    events = []

    ssid_map = {}

    # Group APs by SSID
    for ap in curr.aps.values():
        if ap.ssid:
            ssid_map.setdefault(ap.ssid, []).append(ap)

    # Look for multiple APs using the same SSID
    for ssid, aps in ssid_map.items():
        if len(aps) <= 1:
            continue

        for ap in aps:
            if ap.signal is not None and ap.signal >= SIGNAL_THRESHOLD:
                events.append(
                    Event(
                        type=EventType.EVIL_TWIN_SUSPECT,
                        timestamp=time(),
                        payload={
                            "ssid": ssid,
                            "bssid": ap.bssid,
                            "signal": ap.signal,
                            "channel": ap.channel,
                        },
                    )
                )

    return events
