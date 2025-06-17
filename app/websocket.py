import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

from bitcoin_trader_flow.main import kickoff


router = APIRouter()

connected_clients: set[WebSocket] = set()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/get-decision")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)    
    try:
        while True:
            await websocket.send_text("Connected to Bitcoin Trading Crew WebSocket")
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)

def periodic_task():
    asyncio.run(manager.broadcast(kickoff()))
