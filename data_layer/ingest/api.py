from fastapi import APIRouter, HTTPException
from .validator import validate
from ..runtime import WIDPSRuntime

# listens for and api request at route /ingest
def router(runtime: WIDPSRuntime):
    router = APIRouter()

    @router.post("/ingest")
    async def ingest(record: dict):
        if not validate(record):  # validates the json
            return {"status": "rejected"}

        # next step: forward to state manager
        try:
            #normalizing data, makking it consistent with the state
            if record["type"] == "ap":
                 record["bssid"] = record.pop("mac")
            elif record["type"] == "station":
                 record["type"] = "client"
                 record["station"] = record.pop("mac")
                 record["bssid"] = record.get("assoc_bssid")
            await runtime.process_ingest_record(record)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        return {"status": "ok"}

    return router
