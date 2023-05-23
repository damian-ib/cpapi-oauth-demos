import json
import websocket

class WebsocketClient(websocket.WebSocket):
    def __init__(self, websocket_url: str):
        self.websocket_url = websocket_url

    def connect(self):
        self.ws = websocket.create_connection(self.websocket_url, header={
            "User-Agent": "python:requests",
        })
        return self

    def recv(self):
        response_data = self.ws.recv_frame().data
        decoded_response_data = response_data.decode("utf-8")
        return json.loads(decoded_response_data)

    def send(self, message: str):
        return self.ws.send(message)


def get_websocket_client() -> WebsocketClient:
    websocket_url = f"wss://api.ibkr.com/v1/api/ws"
    websocket = WebsocketClient(websocket_url)
    websocket.connect()
    return websocket