'''The OAuth 2 authorization client and supporting classes.  
Intended for instantiation through AuthFactory, rather than directly.
'''

import urllib # PYTHON2: Was urllib.parse in python 3 version             
from sparkler.auth.client import *

class OAuth2Client(AuthClient):
    '''The OAuth 2 authorization client
    
    Public instance variables:
    consumer -- The Consumer instance represented the client key
    configuration -- References the client's configuration object
    token -- An instance of the OAuth2Token class, which contains the access
             and refresh tokens for an API authorization.'''
    def __init__(self, consumer, configuration):
        self.configuration = configuration
        self.token = None
        super(OAuth2Client, self).__init__(consumer, configuration)

    def validate_configuration(self):
        self.validate_configuration_keys(["key","secret",
            "auth_endpoint_uri", "api_endpoint_uri", "auth_callback_uri"])


    def authorize_request(self, headers, parameters, path=None, body=None):
        '''Attaches authorization headers to headers, e.g.:
        Authorization: OAuth ACCESS_TOKEN

        Arguments
        headers -- A dictionary for request headers, which
                   will be modified.

        Returns:
            Two return values: headers, parameters
        '''
        if self.token == None or self.token.access_token == None:
            raise ApplicationUnauthorizedException()

        headers["Authorization"] = ("OAuth %s" % self.token.access_token)

        return headers, parameters

    def register_session(self, access_token, refresh_token=None, 
            expires_at=None):
        '''
        Registers an existing session with the auth client.

        Arguments:
        access_token -- The authorization token
        refresh_token -- The refresh token
        expires_at -- (optional) The time when the token expires.
        '''
        self.register_token(OAuth2Token(access_token, refresh_token, expires_at))


    def authorization_uri(self):
        '''Returns a string of the full URI, with paramters, the
        end user should be redirected to in order to authorize
        the client to access their data.'''
        parameters = self._authorization_endpoint_parameters()
        return Request(self.configuration, self.configuration["auth_endpoint_uri"]).build_request_uri("", 
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

    def _token_request(self, parameters):
        try:
            response = self._perform_token_request(parameters)
        except HttpStatusNotSuccessfulException as e:
            raise AuthFailureException(e.response)

        return self.register_token(OAuth2Token.parse(response))

    def _perform_token_request(self, parameters):
        request = ApiRequest(self.configuration)
        return request.post("oauth2/grant", parameters)

    def _authorization_endpoint_parameters(self):
        parameters = self._authorization_parameters()
        parameters["response_type"] = "code"
        return parameters

    def _authorization_parameters(self):
        return {
            "client_id": self.consumer.key,
            "redirect_uri": self.consumer.callback_uri
        }

    def _grant_parameters(self):
        parameters = self._authorization_parameters()
        parameters["client_secret"] = self.consumer.secret
        return parameters

class HybridClient(OAuth2Client):
    def __init__(self, consumer, configuration):
        super(HybridClient, self).__init__(consumer, configuration)

    def _authorization_endpoint_parameters(self):
        return {
            "openid.mode"               : "checkid_setup",
            "openid.spark.client_id"    : self.consumer.key,
            "openid.return_to"          : self.consumer.callback_uri,
            "openid.spark.combined_flow": "true"
        }

class OAuth2Token(Token):
    '''A record of an OAuth2 authorization.

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
        return OAuth2Token(json_dict['access_token'], json_dict['refresh_token'],
                expires_at)
