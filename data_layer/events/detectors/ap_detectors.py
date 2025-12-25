from time import time
from events.types import Event, EventType

#compares current snapshot with previous on,by running a loop on the curr snapshot and appends an event when new bssid is discovered
def detect_new_aps(prev, curr):
    events = []
    for bssid, ap in curr.aps.items(): #running the loop
        if bssid not in prev.aps: #checking if the bssid is new or not
            events.append( # appends new aps
                Event(
                    type=EventType.NEW_AP,
                    timestamp=time(),
                    payload={
                        "bssid": ap.bssid,
                        "ssid": ap.ssid,
                        "channel": ap.channel,
                        "signal": ap.signal,
                    },
                )
            )

    return events #returns all the new aps

#compares current snapshot with previous on,by running a loop on the prev snapshot and appends an event when any bssid dissappears
def detect_gone_aps(prev, curr):
    events = []

    for bssid, ap in prev.aps.items(): #running the loop
        if bssid not in curr.aps:  #checking if the bssid is there in the curr snapshot 
            events.append(# appends disappeared aps
                Event(
                    type=EventType.AP_GONE,
                    timestamp=time(),
                    payload={
                        "bssid": ap.bssid,
                        "ssid": ap.ssid,
                    },
                )
            )

    return events #returns disappeared aps
