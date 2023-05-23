import requests
import cpapi_websocket
from time import time
from typing import Any
from oauth_utils import read_private_key, generate_rsa_sha_256_signature, generate_base_string, generate_authorization_header_string, generate_oauth_nonce, generate_dh_challenge, generate_dh_random_bytes, calculate_live_session_token, calculate_live_session_token_prepend, generate_hmac_sha_256_signature, validate_live_session_token

class OAuthSession:
    def __init__(self, session_config: dict[str, str], live_session_token: str = None, live_session_token_expiration: int = None):
        self.encryption_key = read_private_key(session_config["encryption_key_fp"])
        self.signature_key = read_private_key(session_config["signature_key_fp"])
        self.consumer_key = session_config["consumer_key"]
        self.access_token = session_config["access_token"]
        self.access_token_secret = session_config["access_token_secret"]
        self.dh_prime = session_config["dh_prime"]
        self.realm = session_config["realm"]
        self.live_session_token = live_session_token
        self.live_session_token_expiration = int(live_session_token_expiration) if live_session_token_expiration is not None else None

    def __generate_request_headers(self, signature_method: str = "HMAC-SHA256") -> dict[str, str]:
        request_headers = {
            "oauth_consumer_key": self.consumer_key,
            "oauth_nonce": generate_oauth_nonce(),
            "oauth_signature_method": signature_method,
            "oauth_timestamp": str(int(time())),
            "oauth_token": self.access_token
        }
        return request_headers

    def __is_valid_live_session_token(self):
        """
        Check if the live session token is valid.  
        """
        if self.live_session_token_expiration is None:
            return False
        return time() < self.live_session_token_expiration

    def request_live_session_token(self):
        """  
        Get the live session token from the API. This token is used to sign subsequent requests to the API.
        """
        if self.live_session_token is not None and self.__is_valid_live_session_token():
            print(f"Using existing live session token: {self.live_session_token} expires: {self.live_session_token_expiration}", end="\n\n")
            return None
        request_method = "POST"
        request_url = "https://api.ibkr.com/v1/api/oauth/live_session_token"
        request_headers = self.__generate_request_headers("RSA-SHA256")
        dh_random = generate_dh_random_bytes()
        request_headers["diffie_hellman_challenge"] = generate_dh_challenge(self.dh_prime, dh_random)
        base_string = generate_base_string(request_method, request_url, request_headers)
        prepend = calculate_live_session_token_prepend(self.access_token_secret, self.encryption_key)
        base_string = generate_base_string(request_method, request_url, request_headers, prepend=prepend)
        signature = generate_rsa_sha_256_signature(base_string, self.signature_key)
        request_headers["oauth_signature"] = signature
        response = requests.post(
            request_url, 
            headers={
                "Authorization": generate_authorization_header_string(request_headers, self.realm)
            },
        )
        if not response.ok:
            raise Exception(f"Error getting live session token: {response.text}; {response.status_code}; {response.raw}")
        response_data = response.json()
        dh_response = response_data["diffie_hellman_response"]
        lst_signature = response_data["live_session_token_signature"]
        lst_expiration = response_data["live_session_token_expiration"]
        lst = calculate_live_session_token(self.dh_prime, dh_random, dh_response, prepend)
        is_valid_lst = validate_live_session_token(lst, lst_signature, self.consumer_key)
        if not is_valid_lst:
            raise Exception("Invalid LST calculation.")
        self.live_session_token = lst
        self.live_session_token_expiration = lst_expiration
        print(f"Generated new live session token: {self.live_session_token} expires: {self.live_session_token_expiration}", end="\n\n")

    # Non-brokerage endpoints - These endpoints do not require that the user has a brokerage session, just the live session token.

    def get_user_details(self):
        """  
        Get user details from the API. This endpoint does not require a brokerage session.
        """
        request_method = "GET"
        request_url = "https://api.ibkr.com/v1/api/one/user"
        request_headers = self.__generate_request_headers()
        base_string = generate_base_string(request_method, request_url, request_headers)
        signature = generate_hmac_sha_256_signature(base_string, self.live_session_token)
        request_headers["oauth_signature"] = signature
        response = requests.get(
            request_url,
            headers={
                "authorization": generate_authorization_header_string(request_headers, self.realm)
            }
        )
        return response.json()
    
    def tickle(self):
        """  
        Tickle the session to maintain it.
        """
        request_method = "POST"
        request_url = "https://api.ibkr.com/v1/api/tickle"
        request_headers = self.__generate_request_headers()
        base_string = generate_base_string(request_method, request_url, request_headers)
        signature = generate_hmac_sha_256_signature(base_string, self.live_session_token)
        request_headers["oauth_signature"] = signature
        response = requests.get(
            request_url,
            headers={
                "authorization": generate_authorization_header_string(request_headers, self.realm)
            }
        )
        return response.json()

    def get_websocket(self, session_id: str) -> cpapi_websocket.WebsocketClient:
        request_method = "POST"
        request_url = "wss://api.ibkr.com/v1/api/ws"
        request_headers = self.__generate_request_headers()
        base_string = generate_base_string(request_method, request_url, request_headers)
        signature = generate_hmac_sha_256_signature(base_string, self.live_session_token)
        request_headers["oauth_signature"] = signature
        oauth_websocket = cpapi_websocket.WebsocketClient(request_url).connect(
            session_id=session_id,
            # ssl_options=None,
            headers=request_headers
        )
        return oauth_websocket


    def get_secdef_by_conid(self, conid_list: list[int]):
        """  
        Get security definitions by conid. This endpoint does not require a brokerage session.
        """
        request_method = "GET"
        request_url = "https://api.ibkr.com/v1/api/trsrv/secdef"
        request_headers = self.__generate_request_headers()
        request_params = {
            "conids": ",".join([str(conid) for conid in conid_list])
        }
        base_string = generate_base_string(request_method, request_url, request_headers, request_params)
        signature = generate_hmac_sha_256_signature(base_string, self.live_session_token)
        request_headers["oauth_signature"] = signature
        response = requests.get(
            request_url,
            headers={
                "authorization": generate_authorization_header_string(request_headers, self.realm)
            },
            params=request_params
        )
        return response.json()

    def get_stocks_by_symbol(self, symbol_list: list[str]):
        """  
        Get stocks by symbol. This endpoint does not require a brokerage session.
        """
        request_method = "GET"
        request_url = "https://api.ibkr.com/v1/api/trsrv/stocks"
        request_headers = self.__generate_request_headers()
        request_params = {
            "symbols": ",".join(symbol_list)
        }
        base_string = generate_base_string(request_method, request_url, request_headers, request_params)
        signature = generate_hmac_sha_256_signature(base_string, self.live_session_token)
        request_headers["oauth_signature"] = signature
        response = requests.get(
            request_url,
            headers={
                "authorization": generate_authorization_header_string(request_headers, self.realm)
            },
            params=request_params
        )
        return response.json()

    def get_list_of_md_subscriptions(self):
        """  
        Get a list of all market data subscriptions. This endpoint does not require a brokerage session.
        """
        request_method = "GET"
        request_url = "https://api.ibkr.com/v1/api/ibcust/marketdata/subscriptions"
        request_headers = self.__generate_request_headers()
        base_string = generate_base_string(request_method, request_url, request_headers)
        signature = generate_hmac_sha_256_signature(base_string, self.live_session_token)
        request_headers["oauth_signature"] = signature
        response = requests.get(
            request_url,
            headers={
                "authorization": generate_authorization_header_string(request_headers, self.realm)
            }
        )
        return response.json()

    # IServer endpoints - In order to access these endpoints, you need to initialize a brokerage session.

    def init_brokerage_session(self, compete: bool = True, publish: bool = True):
        """  
        A brokerage session is required to access protected resources using the API. Protected resources include market
        data requests, position information, account performance. This endpoint needs to be called after requesting
        the live session token.
        """
        if self.live_session_token is None:
            raise Exception("No LST found. You need to request an LST first, before attempting to open a brokerage session.")
        request_method = "POST"
        request_url = f"https://api.ibkr.com/v1/api/iserver/auth/ssodh/init/"
        request_headers = self.__generate_request_headers()
        request_data = {
            "publish": publish,
            "compete": compete 
        }
        base_string = generate_base_string(request_method, request_url, request_headers, request_data)
        signature = generate_hmac_sha_256_signature(base_string, self.live_session_token)
        request_headers["oauth_signature"] = signature
        response = requests.post(
            request_url,
            headers={
                "authorization": generate_authorization_header_string(request_headers, self.realm),
            },
            params=request_data
        )
        return response

    def get_auth_status(self) -> dict[str, Any]:
        """  
        Get the authentication status for the current session.
        """
        request_method = "GET"
        request_url = "https://api.ibkr.com/v1/api/iserver/auth/status"
        request_headers = self.__generate_request_headers()
        base_string = generate_base_string(request_method, request_url, request_headers)
        signature = generate_hmac_sha_256_signature(base_string, self.live_session_token)
        request_headers["oauth_signature"] = signature
        response = requests.get(
            request_url,
            headers={
                "authorization": generate_authorization_header_string(request_headers, self.realm)
            }
        )
        return response.json()

    def get_list_of_brokerage_accounts(self) -> dict[str, Any]:
        """ 
        Returns a list of brokerage accounts associated that the user has access to. 
        """
        request_method = "GET"
        request_url = "https://api.ibkr.com/v1/api/iserver/accounts"
        request_headers = self.__generate_request_headers()
        base_string = generate_base_string(request_method, request_url, request_headers)
        signature = generate_hmac_sha_256_signature(base_string, self.live_session_token)
        request_headers["oauth_signature"] = signature
        response = requests.get(
            request_url,
            headers={
                "authorization": generate_authorization_header_string(request_headers, self.realm)
            }
        )
        return response.json()

    def get_md_snapshot(self, conid_list: list[int], fields: list[str]) -> dict[str, Any]:
        """  
        Returns a snapshot of market data for a list of conids. The fields parameter contains a list of fields to be returned.
        This endpoint needs to be called at least twice, with the first call initiating the subscription and the second call returning the data.
        """
        request_method = "GET"
        request_url = "https://api.ibkr.com/v1/api/iserver/marketdata/snapshot"
        request_headers = self.__generate_request_headers()
        request_params = {
            "conids": ",".join(map(str, conid_list)),
            "fields": ",".join(map(str, fields))
        }
        base_string = generate_base_string(request_method, request_url, request_headers, request_params)
        signature = generate_hmac_sha_256_signature(base_string, self.live_session_token)
        request_headers["oauth_signature"] = signature
        response = requests.get(
            request_url,
            headers={
                "authorization": generate_authorization_header_string(request_headers, self.realm)
            },
            params=request_params
        )
        return response.json()

    def get_historical_md_data(self, conid: int, period: str = "1w", bar: str = "1d"):
        """  
        Get historical OHLVC data for a given conid. 
        """
        request_method = "GET"
        request_url = "https://api.ibkr.com/v1/api/iserver/marketdata/history"
        request_headers = self.__generate_request_headers()
        request_params = {
            "conid": conid,
            "period": period,
            "bar": bar
        }
        base_string = generate_base_string(request_method, request_url, request_headers, request_params)
        signature = generate_hmac_sha_256_signature(base_string, self.live_session_token)
        request_headers["oauth_signature"] = signature
        response = requests.get(
            request_url,
            headers={
                "authorization": generate_authorization_header_string(request_headers, self.realm)
            },
            params=request_params
        )
        return response.json()

    def get_account_summary(self, account_id: str) -> dict[str, Any]:
        request_method = "GET"
        request_url = f"https://api.ibkr.com/v1/api/portfolio/{account_id}/summary"
        request_headers = self.__generate_request_headers()
        base_string = generate_base_string(request_method, request_url, request_headers)
        signature = generate_hmac_sha_256_signature(base_string, self.live_session_token)
        request_headers["oauth_signature"] = signature
        response = requests.get(
            request_url,
            headers={
                "authorization": generate_authorization_header_string(request_headers, self.realm)
            }
        )
        return response.json()