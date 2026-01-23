from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from .broadcaster import broadcaster

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await broadcaster.connect(ws)
    try:
        # Keep connection alive; broadcaster pushes data
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        await broadcaster.disconnect(ws)
