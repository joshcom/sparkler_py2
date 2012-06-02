class AuthClient:
    def __init__(self, consumer, auth_endpoint_uri, api_endpoint_uri):
        self.consumer = consumer
        self.auth_endpoint_uri = auth_endpoint_uri
        self.api_endpoint_uri = api_endpoint_uri

class Consumer:
    def __init__(self, key, secret, callback_uri):
        self.key = key
        self.secret = secret
        self.callback_uri = callback_uri 
