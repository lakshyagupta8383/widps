REQUIRED_FIELDS = {
    "ap": ["mac", "timestamp"],
    "station": ["mac", "timestamp"]
}

def validate(record: dict) -> bool:
    rtype = record.get("type")
    if rtype not in REQUIRED_FIELDS:
        return False

    for field in REQUIRED_FIELDS[rtype]:
        if field not in record or record[field] is None:
            return False

    return True
