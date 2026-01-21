from fastapi import FastAPI

from ingest.api import router as ingest_router
from output.ws import router as ws_router

app = FastAPI(title="WIDPS Data Layer")

app.include_router(ingest_router)
app.include_router(ws_router)
