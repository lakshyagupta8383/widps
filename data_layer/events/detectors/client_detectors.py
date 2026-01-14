from time import time
from events.types import Event, EventType


def detect_clients(prev, curr):
    events = []

    for mac, client in curr["clients"].items():
        if mac not in prev["clients"]:  # checking new devices
            events.append(
                Event(
                    type=EventType.NEW_CLIENT,
                    timestamp=time(),
                    payload={
                        "station": mac,
                        "bssid": client["bssid"],
                        "signal": client["signal"],
                    },
                )
            )
        else:
            old = prev["clients"][mac]
            if old["bssid"] != client["bssid"]:  # checking if client switched ap
                events.append(
                    Event(
                        type=EventType.CLIENT_ROAMING,
                        timestamp=time(),
                        payload={
                            "station": mac,
                            "from_bssid": old["bssid"],
                            "to_bssid": client["bssid"],
                        },
                    )
                )

    for mac, client in prev["clients"].items():
        if mac not in curr["clients"]:  # if client disappeared
            events.append(
                Event(
                    type=EventType.CLIENT_GONE,
                    timestamp=time(),
                    payload={
                        "station": mac,
                    },
                )
            )

    return events
