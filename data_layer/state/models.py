# defining AP and client state skeleton by creating structured objects instead of dict
from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class APState:
    bssid: str  # unique identifier of an AP
    ssid: Optional[str]
    channel: Optional[int]
    signal: Optional[int]
    privacy: Optional[str]
    last_seen: float

    # NEW: temporal identity
    first_seen: float
    seen_count: int = 1

    # NEW: semantic state
    stability: str = "TRANSIENT"   # STABLE | TRANSIENT
    is_known: bool = False         # trusted AP or not

    signal_history: List[int] = field(default_factory=list)


@dataclass
class ClientState:
    station: str  # unique identifier of a client
    bssid: Optional[str]
    signal: Optional[int]
    frames: int
    last_seen: float

    # NEW: temporal identity
    first_seen: float
