import json
import time
import queue
import oauth_requests
import cpapi_websocket

def non_brokerage_call_operations(session: oauth_requests.OAuthSession):
    line_terminator = "\n\n"
    print(session.get_user_details(), end=line_terminator)
    print(session.get_list_of_md_subscriptions(), end=line_terminator)
    print(session.get_secdef_by_conid([265598, 8314]), end=line_terminator)
    print(session.get_stocks_by_symbol(["AAPL", "MSFT"]), end=line_terminator)

def iserver_operations(session: oauth_requests.OAuthSession):
    session.init_brokerage_session()
    print(session.get_list_of_brokerage_accounts()) # This step is required in order to make market data snapshot requests
    time.sleep(2) # Sleep for a short while to ensure brokerage session has been initialized
    num_requests = 0
    max_num_snapshot_request = 3
    time_between_requests = 5
    while num_requests < max_num_snapshot_request:
        print(session.get_md_snapshot([265598, 8314], [84, 85, 86, 88]), end="\n\n")
        time.sleep(time_between_requests) if max_num_snapshot_request > 1 else None
        num_requests += 1
    print(session.get_historical_md_data(8314, "1m", "1d"))

def websocket_demo(session: oauth_requests.OAuthSession):
    tickle_response = session.tickle()
    session_id = tickle_response['session']
    websocket = cpapi_websocket.get_websocket_client()
    websocket.send(f'{{"session": "{session_id}"}}')
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
            print(websocket_message, end="\n\n")
    except KeyboardInterrupt:
        raise SystemExit

def main(config_data: dict, live_session_token: str = None, live_session_token_expiration: int = None):
    session = oauth_requests.OAuthSession(config_data, live_session_token, live_session_token_expiration)
    session.request_live_session_token()
    session.init_brokerage_session()
    # non_brokerage_call_operations(session)
    # iserver_operations(session)
    websocket_demo(session)
    
if __name__=="__main__":
    CONFIG = "config.json"
    live_session_token = None # Update with the obtained live session token, instead of constantly requesting a new one
    live_session_token_expiration = None
    with open(CONFIG, "r") as config_file:
        config_data = json.load(config_file)
    main(config_data, live_session_token, live_session_token_expiration)