from enum import Enum
from events.types import Event, EventType


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class AlertScorer:
    """
    Alert Scoring Layer

    This layer assigns:
    - severity (LOW / MEDIUM / HIGH)
    - confidence (0–100)

    It does NOT detect or correlate.
    It only grades already-confirmed alerts.
    """

    def score(self, alert_event: Event) -> dict:
        """
        Entry point.

        Takes a correlated alert Event and returns
        a UI-ready alert dictionary.
        """

        if alert_event.type == EventType.EVIL_TWIN_CONFIRMED:
            return self._score_evil_twin(alert_event)

        if alert_event.type == EventType.MASS_DEAUTH_SUSPECT:
            return self._score_mass_deauth(alert_event)

        if alert_event.type == EventType.AP_FLAPPING:
            return self._score_ap_flapping(alert_event)

        # Fallback for unknown alerts
        return {
            "type": alert_event.type.value,
            "severity": Severity.LOW.value,
            "confidence": 30,
            "timestamp": alert_event.timestamp,
            "payload": alert_event.payload,
        }

    # --------------------------------------------------
    # Individual scoring rules
    # --------------------------------------------------

    def _score_evil_twin(self, event: Event) -> dict:
        """
        Scoring logic for EVIL_TWIN_CONFIRMED.

        Evidence used:
        - number of clients that roamed to the AP
        """
        roam_count = event.payload.get("roam_count", 0)

        if roam_count >= 6:
            severity = Severity.HIGH
            confidence = 90
        elif roam_count >= 4:
            severity = Severity.HIGH
            confidence = 80
        elif roam_count >= 3:
            severity = Severity.MEDIUM
            confidence = 65
        else:
            severity = Severity.LOW
            confidence = 50

        return {
            "type": event.type.value,
            "severity": severity.value,
            "confidence": confidence,
            "timestamp": event.timestamp,
            "payload": event.payload,
        }

    def _score_mass_deauth(self, event: Event) -> dict:
        """
        Scoring logic for MASS_DEAUTH_SUSPECT.

        Evidence used:
        - number of clients that disappeared together
        """
        count = event.payload.get("count", 0)

        if count >= 10:
            severity = Severity.HIGH
            confidence = 90
        elif count >= 5:
            severity = Severity.MEDIUM
            confidence = 70
        else:
            severity = Severity.LOW
            confidence = 50

        return {
            "type": event.type.value,
            "severity": severity.value,
            "confidence": confidence,
            "timestamp": event.timestamp,
            "payload": event.payload,
        }

    def _score_ap_flapping(self, event: Event) -> dict:
        """
        Scoring logic for AP_FLAPPING.

        Evidence used:
        - length of NEW_AP / AP_GONE sequence
        """
        sequence = event.payload.get("sequence", [])
        seq_len = len(sequence)

        if seq_len >= 6:
            severity = Severity.MEDIUM
            confidence = 85
        elif seq_len >= 4:
            severity = Severity.MEDIUM
            confidence = 70
        else:
            severity = Severity.LOW
            confidence = 55

        return {
            "type": event.type.value,
            "severity": severity.value,
            "confidence": confidence,
            "timestamp": event.timestamp,
            "payload": event.payload,
        }
