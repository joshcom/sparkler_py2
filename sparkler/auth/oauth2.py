import time
import urllib.parse
from sparkler.transport import Request, ApiRequest
from sparkler.errors import *

class Client:
    def __init__(self, consumer, authorization_endpoint, api_endpoint):
        self.consumer = consumer
        self.authorization_endpoint = authorization_endpoint
        self.api_endpoint = api_endpoint
        self.token = None

    def authorization_uri(self):
        parameters = self._authorization_parameters()
        parameters["response_type"] = "code"
        return Request(self.authorization_endpoint).build_request_uri("", 
                parameters)

    def grant(self, code):
        parameters = self._grant_parameters()
        parameters["grant_type"] = "authorization_code"
        parameters["code"] = code
        return self._token_request(parameters)

    def refresh(self, refresh_token=None):
        parameters = self._grant_parameters()
        parameters["grant_type"] = "refresh_token"

        if refresh_token == None:
            refresh_token = self.token.refresh_token

        parameters["refresh_token"] = refresh_token
        return self._token_request(parameters)

    def register_token(self, token):
        self.token = token
        return self.token

    def generate_base_with_path(self, base, path):
        base_uri = base.strip("/ ")
        endpoint = "{0}{1}".format(base_uri, "/" + path.strip("/ "))
        return endpoint

    def _token_request(self, parameters):
        response = self._perform_token_request(parameters)

        if "error" in response:
            raise AuthFailureException(response["error"], response["error_description"])

        return self.register_token(Token.parse(response))

    def _perform_token_request(self, parameters):
        request = ApiRequest(self.api_endpoint)
        return request.post("oauth2/grant", parameters)

    def _authorization_parameters(self):
        return {
            "client_id": self.consumer.key,
            "redirect_uri": self.consumer.redirect_uri
        }

    def _grant_parameters(self):
        parameters = self._authorization_parameters()
        parameters["client_secret"] = self.consumer.secret
        return parameters


class Consumer:
    def __init__(self, key, secret, redirect_uri):
        self.key = key
        self.secret = secret
        self.redirect_uri = redirect_uri

class Token:
    @staticmethod
    def parse(json_dict):
        expires_at = time.localtime(time.time() + json_dict['expires_in'])
        return Token(json_dict['access_token'], json_dict['refresh_token'],
                expires_at)


    def __init__(self, access_token, refresh_token, expires_at=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at

    def expired(self):
        return time.localtime() >= self.expires_at
