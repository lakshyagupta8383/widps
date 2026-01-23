import time
from collections import deque
from .rules import detect_mass_deauth, detect_evil_twin_confirmed, detect_ap_flapping
from ..types import EventType

WINDOW_SECONDS = 30  #sliding window size (to take care of events captured in last 30s)

class CorrelationEngine:
    def __init__(self):
        self.window = deque() #initializing the double ended queue to store incoming events and remove the old ones

    def process(self, event):
        now = time.time()
        self.window.append(event)

        #remove old events outside the time window(30 secs)
        while self.window and (now - self.window[0].timestamp) > WINDOW_SECONDS:
            self.window.popleft()

        alerts = []
        alerts.extend(detect_evil_twin_confirmed(self.window)) #checks for evil_twins
        alerts.extend(detect_mass_deauth(self.window)) #checks for mass deauths
        alerts.extend(detect_ap_flapping(self.window))#checks for ap flappping(AP_GONE->NEW_AP->AP_GONE)

        return alerts
