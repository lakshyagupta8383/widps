from fastapi import FastAPI
import asyncio
from contextlib import asynccontextmanager

from .ingest.api import router as ingest_router
from data_layer.output.ws import router as ws_router
from .runtime import WIDPSRuntime
from data_layer.output.telemetry import TelemetryPublisher

# Core runtime (single instance)
runtime = WIDPSRuntime()

# Telemetry publisher
telemetry = TelemetryPublisher(runtime, interval=1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[lifespan] starting telemetry")
    task = asyncio.create_task(telemetry.run())
    yield
    print("[lifespan] shutting down telemetry")
    task.cancel()

app = FastAPI(
    title="WIDPS Data Layer",
    lifespan=lifespan
)

# Routers
app.include_router(ingest_router(runtime))
app.include_router(ws_router)
