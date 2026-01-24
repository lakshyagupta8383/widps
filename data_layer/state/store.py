import time  # for expiry logic
import threading

from .models import APState, ClientState

# time is seconds
AP_EXPIRY = 30
CLIENT_EXPIRY = 20


class StateStore:  # one instance = one live memory store
    def __init__(self):  # self being the current object
        self.aps = {}
        self.clients = {}
        self.lock = threading.Lock()  # to make sure mutual exclusion

    def update(self, record: dict):  # the only public method, acts as an entry point
        # checks wheather the record is an ap or client
        print("[STATE UPDATE] incoming record:", record)
        rtype = record["type"]
        ts = time.time()

        # with the lock on self being enabled (so that there is mutual exclusion),
        # the function acc to the record type is called
        with self.lock:
            if rtype == "ap":
                record["bssid"] = record.get("bssid") or record.get("mac")
                self._update_ap(record, ts)
            elif rtype == "client":
                record["station"] = record.get("station") or record.get("mac")
                record["bssid"] = record.get("bssid") or record.get("assoc_bssid")
                self._update_client(record, ts)

    def _update_ap(self, r, ts):
        bssid = r["bssid"]  # extracts the bssid (unique parameter) from the record
        ap = self.aps.get(bssid)  # checks if the ap already exists in the state

        if not ap:  # for new ap
            ap = APState(
                bssid=bssid,
                ssid=r.get("ssid"),
                channel=r.get("channel"),
                signal=r.get("signal"),
                privacy=r.get("privacy"),
                last_seen=ts
            )
            self.aps[bssid] = ap
        else:  # if ap already exists, update its fields
            ap.ssid = r.get("ssid", ap.ssid)
            ap.channel = r.get("channel", ap.channel)
            ap.signal = r.get("signal", ap.signal)
            ap.privacy = r.get("privacy", ap.privacy)
            ap.last_seen = ts

        # makes sure None is not appended in signal_history
        if ap.signal is not None:
            ap.signal_history.append(ap.signal)  # appends the signal value
            ap.signal_history = ap.signal_history[-20:]  # keeps last 20 values

    def _update_client(self, r, ts):
        station = r["station"]  # extracts the station (unique parameter)
        client = self.clients.get(station)  # checks if client already exists

        if not client:  # for new client
            client = ClientState(
                station=station,
                bssid=r.get("bssid"),
                signal=r.get("signal"),
                frames=r.get("frames", 0),
                last_seen=ts
            )
            self.clients[station] = client
        else:  # if client already exists, update fields
            client.bssid = r.get("bssid", client.bssid)
            client.signal = r.get("signal", client.signal)
            client.frames += r.get("frames", 0)
            client.last_seen = ts

    def expire(self):  # return expired aps and clients
        now = time.time()  # current time

        # initializing empty lists for expired aps and clients
        expired_aps = []
        expired_clients = []

        with self.lock:  # making sure the thread is locked
            # checking and deleting expired aps
            for bssid, ap in list(self.aps.items()):
                if now - ap.last_seen > AP_EXPIRY:
                    expired_aps.append(ap)
                    del self.aps[bssid]

            # checking and deleting expired clients
            for station, client in list(self.clients.items()):
                if now - client.last_seen > CLIENT_EXPIRY:
                    expired_clients.append(client)
                    del self.clients[station]

        return expired_aps, expired_clients

    def snapshot(self):
        # returns a read-only JSON-safe snapshot of current state
        with self.lock:
            return {
                "aps": {
                    bssid: {
                        "bssid": ap.bssid,
                        "ssid": ap.ssid,
                        "channel": ap.channel,
                        "signal": ap.signal,
                        "privacy": ap.privacy,
                        "last_seen": ap.last_seen,
                        "signal_history": list(ap.signal_history),
                    }
                    for bssid, ap in self.aps.items()
                },
                "clients": {
                    station: {
                        "station": client.station,
                        "bssid": client.bssid,
                        "signal": client.signal,
                        "frames": client.frames,
                        "last_seen": client.last_seen,
                    }
                    for station, client in self.clients.items()
                }
            }


state_store = StateStore()
