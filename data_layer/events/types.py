#defining an event 
from enum import Enum
from dataclasses import dataclass
from typing import Any
import time

class EventType(str, Enum): #enum will behave like a string aswell 
    NEW_AP = "new_ap"
    AP_GONE = "ap_gone"
    EVIL_TWIN_SUSPECT = "evil_twin_suspect"
    NEW_CLIENT = "new_client"
    CLIENT_ROAMING = "client_roaming"
    CLIENT_GONE = "client_gone"

@dataclass(frozen=True)
class Event:
    type: EventType
    timestamp: float
    payload: dict[str, Any] #for storing mac, from and to
