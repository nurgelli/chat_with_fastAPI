import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

connections = []

@app.websocket("/")
async def ws(websocket: WebSocket):
   
    await websocket.accept()
    connections.append(websocket)
    
    try:
        while True:
            message = await websocket.receive_text()
            
            for connection in connections:
                await connection.send_text(message)
                
    except WebSocketDisconnect:
        connections.remove(websocket)
        print(f"One of client disconnected")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)