'''The OAuth 2 authorization client and supporting classes.  
Intended for instantiation through AuthFactory, rather than directly.
'''
import time
import urllib # PYTHON2: Was urllib.parse in python 3 version
from sparkler.transport import Request, ApiRequest
from sparkler.auth.client import AuthClient
from sparkler.exceptions import *

class OAuth2Client(AuthClient):
    '''The OAuth 2 authorization client
    
    Public instance variables:
    consumer -- The Consumer instance represented the client key
    auth_endpoint_uri -- The URI of the auth endpoint to access or
                         redirect the user to.
    api_endpoint_uri  -- The URI of the API which we are requesting
                         authorizatino for.
    token -- An instance of the Token class, which contains the access
             and refresh tokens for an API authorization.'''
    def __init__(self, consumer, auth_endpoint_uri, api_endpoint_uri):
        super(OAuth2Client, self).__init__(consumer, auth_endpoint_uri, api_endpoint_uri)
        self.token = None

    def authorize_request(self, headers):
        '''Attaches authorization headers to headers, e.g.:
        Authorization: OAuth ACCESS_TOKEN

        Arguments
        headers -- A dictionary for request headers, which
                   will be modified.
        '''
        if self.token == None or self.token.access_token == None:
            raise ApplicationUnauthorizedException()

        headers["Authorization"] = ("OAuth %s" % self.token.access_token)

    def register_session(self, access_token, refresh_token=None, 
            expires_at=None):
        '''
        Registers an existing session with the auth client.

        Arguments:
        access_token -- The authorization token
        refresh_token -- The refresh token
        expires_at -- (optional) The time when the token expires.
        '''
        self.register_token(Token(access_token, refresh_token, expires_at))


    def authorization_uri(self):
        '''Returns a string of the full URI, with paramters, the
        end user should be redirected to in order to authorize
        the client to access their data.'''
        parameters = self._authorization_parameters()
        parameters["response_type"] = "code"
        return Request(self.auth_endpoint_uri).build_request_uri("", 
                parameters)

    def grant(self, code):
        '''Performs a grant request, and if successful, stores the authrization
        token as self.token.

        Arguments:
        code -- The code returned when the users was redirected back
        to the callback_uri.
        '''
        parameters = self._grant_parameters()
        parameters["grant_type"] = "authorization_code"
        parameters["code"] = code
        return self._token_request(parameters)

    def refresh(self, refresh_token=None):
        '''Performs a refresh request, and if successful, stores the authrization
        token as self.token.

        Keyword Arguments:
        refresh_token -- (optional) the OAuth2 refresh token.  If a grant has
        already been performed or a token is already registered, this argument
        is not necessary.
        '''
        parameters = self._grant_parameters()
        parameters["grant_type"] = "refresh_token"

        if refresh_token == None:
            refresh_token = self.token.refresh_token

        parameters["refresh_token"] = refresh_token
        return self._token_request(parameters)

    def register_token(self, token):
        '''Registers an existing authorization.

        Arguments:
        token -- A Token object as a record of the existing authorization
        and refresh tokens.
        '''
        self.token = token
        return self.token

    def _token_request(self, parameters):
        try:
            response = self._perform_token_request(parameters)
        except HttpStatusNotSuccessfulException as e:
            raise AuthFailureException(e.response)

        return self.register_token(Token.parse(response))

    def _perform_token_request(self, parameters):
        request = ApiRequest(self.api_endpoint_uri)
        return request.post("oauth2/grant", parameters)

    def _authorization_parameters(self):
        return {
            "client_id": self.consumer.key,
            "redirect_uri": self.consumer.callback_uri
        }

    def _grant_parameters(self):
        parameters = self._authorization_parameters()
        parameters["client_secret"] = self.consumer.secret
        return parameters

class Token:
    '''A record of an OAuth2 authrozation.

    Public instance variables:
    access_token -- The access token, to be used in the Authorization header
                    when requesting data.
    refresh_token -- The refresh token, to be used when refreshing an
                     expired access token.
    expires_at -- The time object, at when the token will expire.
    '''

    @staticmethod
    def parse(json_dict):
        '''Parses a grant or refresh request and returns a Token object.

        Arguments:
        json_dict -- A dictionary representing the JSON response of a
                     successful API grant/refresh request.
        '''
        expires_at = time.localtime(time.time() + json_dict['expires_in'])
        return Token(json_dict['access_token'], json_dict['refresh_token'],
                expires_at)


    def __init__(self, access_token, refresh_token, expires_at=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_at = expires_at

    def expired(self):
        '''Returns True if the token is expired, or false if not.
        '''
        return time.localtime() >= self.expires_at
