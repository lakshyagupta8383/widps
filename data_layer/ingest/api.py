#listens for and api request at route /ingest      
from fastapi import FastAPI, HTTPException
from ingest.validator import validate
from runtime import WIDPSRuntime

router = APIRouter()
runtime = WIDPSRuntime()

@router.post("/ingest")
async def ingest(record: dict):
    if not validate(record):  #validates the json
        return {"status": "rejected"}

    #next step: forward to state manager
    try:
        runtime.process_ingest_record(record)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "ok"}


