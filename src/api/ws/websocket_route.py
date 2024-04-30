from fastapi import WebSocket, WebSocketDisconnect

from .connection_manager import manager


async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(f"Message text was: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
