#listens for and api request at route /ingest      
from fastapi import FastAPI, Request
from ingest.validator import validate

app = FastAPI()

@app.post("/ingest")
async def ingest(record: dict):
    if not validate(record):  #validates the json
        return {"status": "rejected"}

    #next step: forward to state manager
    print("INGESTED:", record)

    return {"status": "ok"}
