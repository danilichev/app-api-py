from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from src.api.command import router as command_router
from src.api.file import router as file_router
from src.api.instruction import router as instruction_router
from src.api.ping import router as ping_router
from src.api.post import router as post_router
from src.api.ws.websocket_route import websocket_endpoint
from .config import config

print(config.db_url)

app = FastAPI()

app.include_router(command_router)
app.include_router(file_router)
app.include_router(instruction_router)
app.include_router(ping_router)
app.include_router(post_router)


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h2>WebSocket</h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8080/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


app.websocket("/ws")(websocket_endpoint)
