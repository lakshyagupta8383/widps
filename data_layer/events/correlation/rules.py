import time
from events.types import Event, EventType


def detect_evil_twin_confirmed(events):
    """
    NEW_AP followed by multiple CLIENT_ROAMING to same BSSID.
    """
    alerts = []

    new_aps = {} #remember newly appeared routers
    roam_counts = {} #counts how many devices moved to each router

    for e in events: 
        if e.type == EventType.NEW_AP:
            new_aps[e.payload["bssid"]] = e #keeps track of recently appeared routers/aps

        if e.type == EventType.CLIENT_ROAMING:
            to_bssid = e.payload.get("to_bssid")
            roam_counts[to_bssid] = roam_counts.get(to_bssid, 0) + 1 #count the routers/aps where no of clients are moving 
    #if 3 or more clients move to new aps, then the EVIL_TWIN_CONFIRMED event is triggered 
    for bssid, ap_event in new_aps.items():
        if roam_counts.get(bssid, 0) >= 3:
            alerts.append(
                Event(
                    type=EventType.EVIL_TWIN_CONFIRMED,
                    timestamp=time.time(),
                    payload={
                        "bssid": bssid,
                        "ssid": ap_event.payload.get("ssid"),
                        "roam_count": roam_counts[bssid],
                    },
                )
            )

    return alerts


def detect_mass_deauth(events):
    """
    Many CLIENT_GONE events in short time.
    """
    gone_clients = [
        e for e in events if e.type == EventType.CLIENT_GONE
    ]

    if len(gone_clients) >= 5:
        return [
            Event(
                type=EventType.MASS_DEAUTH_SUSPECT,
                timestamp=time.time(),
                payload={
                    "count": len(gone_clients)
                },
            )
        ]

    return []


def detect_ap_flapping(events):
    """
    AP repeatedly appearing and disappearing.
    """
    history = {}

    for e in events:
        if e.type in (EventType.NEW_AP, EventType.AP_GONE):
            bssid = e.payload.get("bssid")
            history.setdefault(bssid, []).append(e.type)

    alerts = []
    for bssid, seq in history.items():
        if seq.count(EventType.NEW_AP) >= 2 and seq.count(EventType.AP_GONE) >= 2:
            alerts.append(
                Event(
                    type=EventType.AP_FLAPPING,
                    timestamp=time.time(),
                    payload={
                        "bssid": bssid,
                        "sequence": [t.value for t in seq],
                    },
                )
            )

    return alerts
