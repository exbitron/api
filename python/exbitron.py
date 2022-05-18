import hashlib, hmac
import requests
from requests.auth import AuthBase
import json

try:
    from urllib import urlencode
except:
    from urllib.parse import urlencode
from time import time

# Authentificate class
class Auth(AuthBase):
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key

    def __call__(self, req):
        nonce, signature = self.sign()
        headers =  {
            "x-auth-apikey": self.access_key,
            "x-auth-nonce": nonce,
            "x-auth-signature": signature,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0 PeatioAPIClient",
        }
        req.headers = headers
        return req

    def sign(self):
        # https://github.com/openware/peatio/blob/master/docs/api/trading_api.md#how-to-use-api-key
        nonce = str(int(time() * 1000))
        signature = hmac.new(
            self.secret_key.encode(),
            (nonce + self.access_key).encode(),
            hashlib.sha256
        ).hexdigest()
        return nonce, signature

# Connection class
class Client:
    def __init__(
        self,
        endpoint = "https://www.exbitron.com",
        access_key = None,
        secret_key = None,
        timeout = 60
    ):
        self.endpoint = endpoint
        self.timeout = timeout

        if access_key and secret_key:
            self.auth = Auth(access_key, secret_key)
        else:
            self.auth = False
        self.session = requests.Session()
        self.session.auth = self.auth

    def check_auth(self):
        if not self.auth:
            raise Exception("Missing access key and/or secret key")

    def get_public(self, path, params=None):
        if params is None:
            params = {}
        url = "%s%s" % (self.endpoint, path)
        response = self.session.get(url,
            data = json.dumps(params),
            timeout = self.timeout,
            verify = self.endpoint.startswith("https://")
        )

        return self.response_to_dict(response)

    def get(self, path, params=None):
        if params is None:
            params = {}
        self.check_auth()
        url = "%s%s" % (self.endpoint, path)
        response = self.session.get(url,
            data = json.dumps(params),
            timeout = self.timeout,
            verify = self.endpoint.startswith("https://")
        )

        return self.response_to_dict(response)

    def post(self, path, params=None):
        if params is None:
            params = {}
        self.check_auth()
        url = "%s%s" % (self.endpoint, path)
        response = self.session.post(url,
            data = json.dumps(params),
            timeout = self.timeout,
            verify = self.endpoint.startswith("https://")
        )
        return self.response_to_dict(response)

    def response_to_dict(self, response):
        try:
            return response.json()
        except ValueError:
            raise Exception("Response is in bad json format")
