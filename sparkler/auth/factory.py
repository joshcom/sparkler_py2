from sparkler.auth.client import *
from sparkler.auth.oauth2 import OAuth2Client

class AuthFactory:
    auth_modes = {
            "oauth2": OAuth2Client
    }
    @staticmethod
    def create(auth_mode, client_key, client_secret, auth_endpoint_uri, 
            api_endpoint_uri, auth_callback_uri=None):
        consumer = Consumer(client_key, client_secret, auth_callback_uri)
        return AuthFactory.auth_modes[auth_mode](consumer=consumer,
            auth_endpoint_uri=auth_endpoint_uri, 
            api_endpoint_uri=api_endpoint_uri)
