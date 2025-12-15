
REQUIRED_FIELDS = {
    "ap": ["bssid", "timestamp"], #bssid use used to detect the uniqueness of a device and timestamp is used to build events.
    "client": ["station", "timestamp"] # similiarly station mac use used to detect the uniqueness of a device and timestamp is used to build events.
}

def validate(record):
    #returns True if record is valid enough to process.
    rtype = record.get("type")
    if rtype not in REQUIRED_FIELDS:
        return False

    for field in REQUIRED_FIELDS[rtype]:
        if field not in record:
            return False

    return True
