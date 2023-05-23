import requests
import ssl
import queue
import urllib3
import websocket

BASE_URL = "localhost:5000/v1/api"


class WebsocketClient(websocket.WebSocket):
    def __init__(self, websocket_url: str):
        self.websocket_url = websocket_url
        self.subscriptions = []

    def connect(self, session_id: str, ssl_options: dict = None):
        self.ws = websocket.create_connection(self.websocket_url, sslopt=ssl_options)
        self.ws.send(f'{{"session": "{session_id}"}}')
        return self

    def recv(self):
        return self.ws.recv()

    def send(self, message: str):
        return self.ws.send(message)


def request_session_id() -> str:
    request_endpoint = "/tickle"
    request_url = f"https://{BASE_URL}{request_endpoint}"
    response = requests.post(request_url, verify=False)
    if not response.ok:
        raise RuntimeError("Failed to request session ID")
    session_id = response.json()["session"]
    return session_id


def get_websocket_client(session_id: str) -> WebsocketClient:
    websocket_endpoint = "/ws"
    websocket_url = f"wss://{BASE_URL}{websocket_endpoint}"
    websocket = WebsocketClient(websocket_url).connect(
        session_id, {"cert_reqs": ssl.CERT_NONE}
    )
    return websocket


def main():
    session_id = request_session_id()
    websocket = get_websocket_client(session_id)
    messages = [
        "sor",  # Subscribe to order updates
        'smd+12087792+{"fields": ["84", "86"]}',  # Get bid and ask prices for EUR.USD FX pair
    ]
    message_queue = queue.Queue()
    for message in messages:
        message_queue.put(message)
    try:
        while True:
            if not message_queue.empty():
                message = message_queue.get()
                websocket.send(message)
            websocket_message = websocket.recv()
            # Implement message handling here, for example add unsubscribe logic
            print(websocket_message)
    except KeyboardInterrupt:
        raise SystemExit


if __name__ == "__main__":
    urllib3.disable_warnings()
    main()
