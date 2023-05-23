from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as PKCS1_v1_5_Signature
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_v1_5_Cipher
from Crypto.Hash import SHA256, HMAC, SHA1
from urllib.parse import quote, quote_plus
from string import ascii_letters, digits
import random
import base64

def read_private_key(private_key_fp: str) -> RSA.RsaKey:
    with open(private_key_fp, "r") as f:
        private_key = RSA.importKey(f.read())
    return private_key

def generate_oauth_nonce() -> str:
    nonce_length = 32
    nonce_characters = ascii_letters + digits
    nonce = "".join(random.choice(nonce_characters) for _ in range(nonce_length))
    return nonce

def generate_base_string(request_method: str, request_url: str, request_headers: dict, request_body: dict = None, prepend: str = None) -> str:
    """ 
    A lexicographically sorted list of key/value pairs including the authorization header pairs, query parameters and if the request
    contains a body of type x-www-form-urlencoded, the body parameters. The list values are separated using the character '&', then the list is percent
    encoded.
    """
    method_upper = request_method.upper()
    encoded_request_url = quote_plus(request_url)
    oauth_params = {**request_headers, **request_body} if request_body is not None else request_headers
    oauth_params_string = "&".join([f"{k}={v}" for k, v in sorted(oauth_params.items())])
    encoded_oauth_params_string = quote(oauth_params_string)
    base_string = "&".join([method_upper, encoded_request_url, encoded_oauth_params_string])
    if prepend is not None:
        base_string = f"{prepend}{base_string}"
    return base_string

def generate_dh_random_bytes() -> str:
    """  
    Generates a random 256 bit number and returns it as a hex value. This is used when generating the DH challenge.
    """
    dh_random_bytes = random.getrandbits(256)
    return hex(dh_random_bytes)[2:]

def generate_dh_challenge(dh_prime: str, dh_random: str, dh_generator: int = 2) -> str:
    """  
    Generate the DH challenge using the prime, random and generator values. The result needs to be recorded as a hex value and sent to LST endpoint.
    """
    dh_challenge = pow(dh_generator, int(dh_random, 16), int(dh_prime, 16))
    return hex(dh_challenge)[2:]

def calculate_live_session_token_prepend(access_token_secret: str, private_encryption_key: RSA.RsaKey) -> str:
    """  
    Decrypts the access token secret using the private encryption key. The result is then converted to a hex value, and returned as the prepend
    used when requesting the live session token.
    """
    access_token_secret_bytes = base64.b64decode(access_token_secret)
    cipher = PKCS1_v1_5_Cipher.new(private_encryption_key)
    decrypted_access_token_secret = cipher.decrypt(access_token_secret_bytes, None)
    return decrypted_access_token_secret.hex()

def generate_rsa_sha_256_signature(base_string: str, private_signature_key: RSA.RsaKey) -> str:
    """
    Generates the signature for the base string using the private signature key. The signature is generated using the
    RSA-SHA256 algorithm and is encoded using base64. The signature is then decoded to utf-8 and the newline character
    is removed. Finally, the signature is URL encoded.

    This method is used when getting the request, access and live session tokens.
    """
    encoded_base_string = base_string.encode("utf-8")
    signer = PKCS1_v1_5_Signature.new(private_signature_key)
    hash = SHA256.new(encoded_base_string)
    signature = signer.sign(hash)
    encoded_signature = base64.encodebytes(signature)
    return quote_plus(encoded_signature.decode("utf-8").replace("\n", ""))

def generate_hmac_sha_256_signature(base_string: str, live_session_token: str) -> str:
    """  
    When accessing any other endpoint, which means any protected resource, the key used is the live session token as a byte array and the signature
    method is HMAC-SHA256.
    """
    encoded_base_string = base_string.encode("utf-8")
    hmac = HMAC.new(bytes(base64.b64decode(live_session_token)), digestmod=SHA256)
    hmac.update(encoded_base_string)
    return quote_plus(base64.b64encode(hmac.digest()).decode("utf-8"))

def get_access_token_secret_bytes(access_token_secret: str) -> list[int]:
    access_token_secret_bytes = bytearray.fromhex(access_token_secret)
    return [int(byte) for byte in access_token_secret_bytes]

def to_byte_array(x) -> list[int]:
    hex_string = hex(x)[2:]
    if len(hex_string) % 2 > 0:
        hex_string = "0" + hex_string
    byte_array = []
    if len(bin(x)[2:]) % 8 == 0:
        byte_array.append(0)
    for i in range(0, len(hex_string), 2):
        byte_array.append(int(hex_string[i:i+2], 16))
    return byte_array

def calculate_live_session_token(dh_prime: str, dh_random_value: str, dh_response: str, prepend: str) -> str:
    """  
    Calculates the live session token using the DH prime, random value, response and prepend.
    The live session token is used to sign requests for protected resources.
    """
    access_token_secret_bytes = get_access_token_secret_bytes(prepend)
    a = int(dh_random_value, 16)
    B = int(dh_response, 16)
    K = pow(B, a, int(dh_prime, 16))
    hmac = HMAC.new(bytes(to_byte_array(K)), digestmod=SHA1)
    hmac.update(bytes(access_token_secret_bytes))
    return base64.b64encode(hmac.digest()).decode("utf-8")

def validate_live_session_token(live_session_token: str, live_session_token_signature: str, consumer_key: str) -> bool:
    hmac = HMAC.new(bytes(base64.b64decode(live_session_token)), digestmod=SHA1)
    hmac.update(bytes(consumer_key, "utf-8"))
    return hmac.hexdigest() == live_session_token_signature

def generate_authorization_header_string(request_data: dict, realm: str = "limited_poa") -> str:
    """  
    Generates the authorization header string using the request data. The request data is a dictionary containing the
    key value pairs for the authorization header. The request data is sorted by key and then joined together using the
    character ',' and the string 'OAuth realm=' is prepended to the string. For most cases, the realm is set as limited_poa.
    """
    authorization_header_string = f"OAuth realm=\"{realm}\", "+", ".join([f"{key}=\"{value}\"" for key, value in sorted(request_data.items())])
    return authorization_header_string