from fastapi import WebSocket
from typing import Set
import asyncio

class WebSocketBroadcaster:
    def __init__(self):
        self.clients: Set[WebSocket] = set()  # clients are all active WebSocket connections
        self.lock = asyncio.Lock()  # prevents race conditions

    async def connect(self, ws: WebSocket):  # called when frontend connects
        await ws.accept()  # WebSocket handshake
        async with self.lock:  # thread-safe client addition
            self.clients.add(ws)

    async def disconnect(self, ws: WebSocket):  # called when client disconnects
        async with self.lock:  # thread-safe client removal
            self.clients.discard(ws)

    async def broadcast(self, message: dict):  # sends json messages to clients
        # take a snapshot of current clients so we don't hold the lock during I/O
        async with self.lock:
            clients = list(self.clients)

        dead = set()  # initializes set to track broken connections

        for ws in clients:
            try:
                await ws.send_json(message)  # sends json to frontend
            except Exception:
                dead.add(ws)  # marks dead sockets

        # discard dead sockets
        if dead:
            async with self.lock:
                for ws in dead:
                    self.clients.discard(ws)

# singleton broadcaster instance
broadcaster = WebSocketBroadcaster()
