from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from .broadcaster import broadcaster   

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await broadcaster.connect(ws)      
    try:
        await ws.wait_closed()
    finally:
        await broadcaster.disconnect(ws)
