#defining AP and client state skeleton by creating structered objects instead of dict
from dataclasses import dataclass, field 
from typing import Optional, List

@dataclass
class APState:
    bssid: str #unique identifier of an AP
    ssid: Optional[str]
    channel: Optional[int]
    signal: Optional[int]
    privacy: Optional[str]
    last_seen: float
    signal_history: List[int] = field(default_factory=list)

@dataclass
class ClientState:
    station: str #unique identifier of an client
    bssid: Optional[str]
    signal: Optional[int]
    frames: int
    last_seen: float
