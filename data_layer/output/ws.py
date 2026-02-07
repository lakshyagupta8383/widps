from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .broadcaster import broadcaster   
import asyncio

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await broadcaster.connect(ws)
    try:
        while True:
            await broadcaster.broadcast({
                "type": "heartbeat",
                "msg": "ws alive"
            })
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        pass
    finally:
        await broadcaster.disconnect(ws)

