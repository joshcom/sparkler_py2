'''Base classes to be used or extended by all Auth clients.
'''

class AuthClient(object):
    '''The base client for all auth mechinisms.

    Public instance variables:
    consumer -- The Consumer instance represented the client key
    auth_endpoint_uri -- The URI of the auth endpoint to access or
                         redirect the user to.
    api_endpoint_uri  -- The URI of the API which we are requesting
                         authorizatino for.
    '''
    def __init__(self, consumer, auth_endpoint_uri, api_endpoint_uri):
        self.consumer = consumer
        self.auth_endpoint_uri = auth_endpoint_uri
        self.api_endpoint_uri = api_endpoint_uri

class Consumer(object):
    '''Represents a client key, or a record of credentials for API access.

    Public instance variables:
    key -- The API client key
    secret --  The API client secret
    callback_uri -- The URI to the callback for the application, to which
                    the end user will be redirected to once they have granted
                    the application access to their data.
    '''
    def __init__(self, key, secret, callback_uri):
        self.key = key
        self.secret = secret
        self.callback_uri = callback_uri 
