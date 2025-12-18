import time #for expiry logic
import threading 
from state.models import APState, ClientState
#time is seconds
AP_EXPIRY = 10
CLIENT_EXPIRY = 10

class StateStore: #one instance=one live memory store
    def __init__(self): # self being the current object
        self.aps = {}
        self.clients = {}
        self.lock = threading.Lock() #to make sure mutual exclusion

    def update(self, record: dict): #the only public method, acts as an entry point
        #checks wheather the record is an ap or client
        rtype = record["type"] 
        ts = record["timestamp"]

        #with the lock on slef being enabled(so that there is mutual exclusion), the function acc to the record type is called
        with self.lock:
            if rtype == "ap":
                self._update_ap(record, ts)
            elif rtype == "client":
                self._update_client(record, ts)

    def _update_ap(self, r, ts):
        bssid = r["bssid"] #extracts the bssid(unique parameter) from the record 
        ap = self.aps.get(bssid) #checks if the ap already exists in the state

        if not ap: #for new ap
            ap = APState(
                bssid=bssid,
                ssid=r.get("ssid"),
                channel=r.get("channel"),
                signal=r.get("signal"),
                privacy=r.get("privacy"),
                last_seen=ts
            )
            self.aps[bssid] = ap
        else: #if ap already exists, the state updates its ssid, channel, signal, privacy, last_seen
            ap.ssid = r.get("ssid", ap.ssid)
            ap.channel = r.get("channel", ap.channel)
            ap.signal = r.get("signal", ap.signal)
            ap.privacy = r.get("privacy", ap.privacy)
            ap.last_seen = ts

        if ap.signal is not None: #makes sure none is not appened in signal_history
            ap.signal_history.append(ap.signal) #appends the signal value
            ap.signal_history = ap.signal_history[-20:] #keeps track of last 20 signal values

    def _update_client(self, r, ts):
        station = r["station"] #extracts the station(unique parameter) from the record 
        client = self.clients.get(station) #checks if the client already exists in the state

        if not client: #for new client
            client = ClientState(
                station=station,
                bssid=r.get("bssid"),
                signal=r.get("signal"),
                frames=r.get("frames", 0),
                last_seen=ts
            )
            self.clients[station] = client
        else: #if client already exists, the state updates its bssid, no of frames, signal, privacy, last_seen
            client.bssid = r.get("bssid", client.bssid)
            client.signal = r.get("signal", client.signal)
            client.frames += r.get("frames", 0)
            client.last_seen = ts

    def expire(self): # return expires aps and client
        now = time.time() #current time
        #initializing empty list for expired aps and client
        expired_aps = [] 
        expired_clients = []

        with self.lock: #making sure the the thread is locked 
            #checking and deleting the expired aps
            for bssid, ap in list(self.aps.items()):
                if now - ap.last_seen > AP_EXPIRY:
                    expired_aps.append(ap)
                    del self.aps[bssid]

            #checking and deleting the expired client
            for station, client in list(self.clients.items()):
                if now - client.last_seen > CLIENT_EXPIRY:
                    expired_clients.append(client)
                    del self.clients[station]

        return expired_aps, expired_clients


state_store = StateStore()
