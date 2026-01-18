from fastapi import WebSocket
from typing import Set
import asyncio

class WebSocketBroadcaster:
    def __init__(self):
        self.clients: Set[WebSocket] = set() #clients are all active webSockets connections
        self.lock = asyncio.Lock() #prevents race conditions 

    async def connect(self, ws: WebSocket): #called when frontend connects 
        await ws.accept() #webSocket handshake 
        async with self.lock: #thread-safe client addition 
            self.clients.add(ws)

    async def disconnect(self, ws: WebSocket): #called when client disconnects.
        async with self.lock:#thread-safe client removal
            self.clients.discard(ws)

    async def broadcast(self, message: dict): #sends json messages to clients 
        async with self.lock:
            dead = set() #initializes set to track broken connections
            for ws in self.clients:
                try:
                    await ws.send_json(message) #sends json to frontend
                except Exception:
                    dead.add(ws) #marks dead sockets

            for ws in dead: # discard dead sockets
                self.clients.discard(ws) 

broadcaster = WebSocketBroadcaster()
