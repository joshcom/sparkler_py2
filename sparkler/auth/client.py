import time
from sparkler.transport import Request, ApiRequest
from sparkler.exceptions import *
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

    def authorize_request(self, headers, parameters, path=None, body=None):
        '''To be implemented by the client.
        Attaches authorization headers to headers.

        Arguments:
        headers -- A dictionary for request headers, which
                   will be modified.
        parameters -- The hash of parameters to send along with
                      the request
        path -- (optional) The resource path being access (e.g. /v1/contacts)
        body -- (optional) The POST/PUT body

        Returns:
            Two return values: headers, parameters
        '''
        raise NotImplementedError()

    def register_session(self, access_token, refresh_token=None, 
            expires_at=None):
        '''To be implemented by the client.
        Registers an existing session with the auth client.

        Arguments:
        access_token -- The authorization token
        refresh_token -- (optional) The authorization refresh token, if
                         supported
        expires_at -- (optional) The time when the token expires.
        '''
        raise NotImplementedError()

    def register_token(self, token):
        '''Registers an existing authorization.

        Arguments:
        token -- A Token object as a record of the existing authorization
        and refresh tokens.
        '''
        self.token = token
        return self.token

class Consumer(object):
    '''Represents a client key, or a record of credentials for API access.

    Public instance variables:
    key -- The API client key
    secret --  The API client secret
    callback_uri -- (optional) The URI to the callback for the application, to which
                    the end user will be redirected to once they have granted
                    the application access to their data.
    '''
    def __init__(self, key, secret, callback_uri=None):
        self.key = key
        self.secret = secret
        self.callback_uri = callback_uri 

class Token:
    '''A record of an authorization. Token.parse should be implemented by child classes

    Public instance variables:
    access_token -- The access token, to be used in the Authorization header
                    when requesting data.
    refresh_token -- The refresh token, to be used when refreshing an
                     expired access token.
    expires_at -- The time object, at when the token will expire.
    '''

    @staticmethod
    def parse(json_dict):
        pass

    def __init__(self, access_token, refresh_token=None, expires_at=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at
        self.token = None

    def expired(self):
        '''Returns True if the token is expired, or false if not.
        '''
        if self.expires_at == None:
            return False
        else:
            return time.localtime() >= self.expires_at
