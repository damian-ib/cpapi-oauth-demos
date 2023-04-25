from json import load
from time import sleep
from oauth_requests import OAuthSession
from oauth_utils import oauth_config_hook
import os


def non_brokerage_call_operations(session: OAuthSession):
    line_terminator = "\n\n"
    print(session.get_user_details(), end=line_terminator)
    print(session.get_list_of_md_subscriptions(), end=line_terminator)
    print(session.get_secdef_by_conid([265598, 8314]), end=line_terminator)
    print(session.get_stocks_by_symbol(["AAPL", "MSFT"]), end=line_terminator)


def iserver_operations(session: OAuthSession):
    session.init_brokerage_session()
    session.get_list_of_brokerage_accounts()  # This step is required in order to make market data snapshot requests
    sleep(2)  # Sleep for a short while to ensure brokerage session has been initialized
    num_requests = 0
    max_num_snapshot_request = 3
    time_between_requests = 5
    while num_requests < max_num_snapshot_request:
        print(session.get_md_snapshot([265598, 8314], [84, 85, 86, 88]), end="\n\n")
        sleep(time_between_requests) if max_num_snapshot_request > 1 else None
        num_requests += 1
    print(session.get_historical_md_data(8314, "1m", "1d"))


def main(
    oauth_config_fp: os.PathLike | str,
    live_session_token: str = None,
    live_session_token_expiration: int = None,
):
    with open(oauth_config_fp, "r") as config_file:
        oauth_config = load(config_file, object_hook=oauth_config_hook)
    session = OAuthSession(
        oauth_config, live_session_token, live_session_token_expiration
    )
    session.request_live_session_token()
    non_brokerage_call_operations(session)
    iserver_operations(session)


if __name__ == "__main__":
    CONFIG_FILE = "test-config.json"
    config_file_path = os.path.join(os.path.dirname(__file__), CONFIG_FILE)
    live_session_token = None
    live_session_token_expiration = None
    main(config_file_path, live_session_token, live_session_token_expiration)
