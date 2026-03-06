from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import json
import asyncio
import random

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                disconnected.append(connection)
        for conn in disconnected:
            self.disconnect(conn)

manager = ConnectionManager()

async def mock_price_stream():
    price = 2300.00
    while True:
        await asyncio.sleep(1)
        price += random.choice([-0.5, -0.25, 0.25, 0.5, 0.75])
        price = max(2200.0, min(price, 2400.0))  # bound the mock price
        await manager.broadcast(json.dumps({
            "type": "price_update",
            "symbol": "XAUUSD",
            "price": round(price, 2),
        }))

@asynccontextmanager
async def lifespan(application: FastAPI):
    # Startup
    task = asyncio.create_task(mock_price_stream())
    yield
    # Shutdown
    task.cancel()

app = FastAPI(title="XAUUSD Platform - API Gateway", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "service": "api_gateway"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "connections": len(manager.active_connections)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection open, waiting for any client message
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
