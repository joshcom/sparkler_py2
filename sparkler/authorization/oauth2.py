import time
import urllib.parse

# TODO! Authorization!  Refresh/Access tokens must be managed and setable.
# TODO! Register a client
class Client:
    def __init__(self, consumer, authorization_endpoint, api_endpoint):
        self.consumer = consumer
        self.authorization_endpoint = authorization_endpoint
        self.api_endpoint = api_endpoint
        self.token_endpoint = self.generate_default_token_endpoint()

    def authorization_uri(self, response_type="code"):
        params = urllib.parse.urlencode({
            "client_id": self.consumer.key,
            "redirect_uri": self.consumer.redirect_uri,
            "response_type": response_type 
        })
        return self.authorization_endpoint + "?" + params

    def grant(self, code):
        # POST
        # Check
        # Token-time
        pass

    def refresh(self, code):
        # POST
        # Check
        # Token-time
        pass

    def request(self):
        pass

    def register_token(self, token):
        self.token = token

    def generate_default_token_endpoint(self):
        return self.generate_base_with_path(self.api_endpoint, "/token")

    def generate_base_with_path(self, base, path):
        base_uri = base.strip("/ ")
        endpoint = "{0}{1}".format(base_uri, "/" + path.strip("/ "))
        return endpoint


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


    def __init__(self, access_token, refresh_token, expires_at):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at

    def expired(self):
        return time.localtime() >= self.expires_at
