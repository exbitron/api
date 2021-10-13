import hashlib, hmac
import requests

try:
    from urllib import urlencode
except:
    from urllib.parse import urlencode
import time

def payload(verb, path, params):
    # url params should be sorted in alphabet
    url_params = urlencode(sorted(params.items()))
    return "{verb}|{path}|{url_params}".format(
        verb = verb.upper(),
        path = path,
        url_params = url_params
    )

# Authentificate class
class Auth:
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key

    def signed_challenge(self, challenge):
        payload = "%s%s" % (self.access_key, challenge)
        signature = hmac.new(self.secret_key.encode(), payload.encode(), hashlib.sha256).hexdigest()
        return {
            "auth": {
                "access_key": self.access_key,
                "answer": signature
            }
        }

    def signed_params(self, verb, path, params):
        params = params.copy()
        params = self._format_params(params)
        signature = self.sign(verb, path, params)
        params["signature"] = signature
        return params

    def sign(self, verb, path, params):
        return hmac.new(self.secret_key.encode(), (str(params['nonce']) + self.access_key).encode(), hashlib.sha256).hexdigest() 

    def _format_params(self, params):
        if not params.get("access_key"):
            params["access_key"] = self.access_key
        if not params.get("tonce"):
            params["nonce"] = int(time.time() * 1000)
        return params


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
            self.access_key = access_key
            self.secret_key = secret_key
            self.auth = Auth(access_key, secret_key)
        else:
            self.auth = False

    def check_auth(self):
        if not self.auth:
            raise Exception("Missing access key and/or secret key")

    def get_public(self, path, params=None):
        if params is None:
            params = {}
        url = "%s%s" % (self.endpoint, path)

        response = requests.get(url,
            params = params,
            timeout = self.timeout,
            verify = self.endpoint.startswith("https://")
        )

        return self.response_to_dict(response)

    def get(self, path, params=None):
        if params is None:
            params = {}

        self.check_auth()
        url = "%s%s" % (self.endpoint, path)
        params = self.auth.signed_params("get", path, params)
        headers =  {
            "x-auth-apikey": params['access_key'], 
            "x-auth-nonce": str(params["nonce"]), 
            "x-auth-signature": params["signature"],
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0 ExbitronAPIClient",
            "Connection": "close"
        }

        response = requests.get(url,
            headers = headers,
            timeout = self.timeout,
            verify = self.endpoint.startswith("https://")
        )

        return self.response_to_dict(response)
        
    def post(self, path, params=None):
        if params is None:
            params = {}

        self.check_auth()
        url = "%s%s" % (self.endpoint, path)
        params = self.auth.signed_params("post", path, params)
        headers =  {
            "x-auth-apikey": params['access_key'], 
            "x-auth-nonce": str(params["nonce"]), 
            "x-auth-signature": params["signature"],
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0 ExbitronAPIClient",
            "Connection": "close"
        }

        response = requests.post(url,
            headers = headers,
            data = params,
            timeout = self.timeout,
            verify = self.endpoint.startswith("https://")
        )

        return self.response_to_dict(response)

    def response_to_dict(self, response):
        try:
            return response.json()
        except ValueError:
            raise Exception("Response is in bad json format")
