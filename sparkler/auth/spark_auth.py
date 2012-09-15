'''The OAuth 2 authorization client and supporting classes.  
Intended for instantiation through AuthFactory, rather than directly.
'''

from sparkler.auth.client import *
import re
import hashlib

class SparkAuthClient(AuthClient):
    def __init__(self, consumer, configuration):
        super(SparkAuthClient, self).__init__(consumer, configuration)
        self.token = None

    def init_session(self):
        request = ApiRequest(self.configuration)
        params = {
          "ApiKey":self.consumer.key,
          "ApiSig":self._generate_signature("/v1/session", None, None)
        }
        results = request.post("/v1/session", None, params)
        self.register_session(results["Results"][0]["AuthToken"])

    def validate_configuration(self):
        self.validate_configuration_keys(["key","secret",
            "auth_endpoint_uri", "api_endpoint_uri"])

    def authorize_request(self, headers, parameters, path, body=None):
        '''To be implemented by the client.
        Attaches authorization headers to headers.

        Arguments:
        headers -- A dictionary for request headers, which
                   will be modified.
        path -- (optional) The resource path being access (e.g. /v1/contacts)
        parameters -- (optional) The hash of parameters to send along with
                      the request
        body -- (optional) The POST/PUT body

        Returns:
            Two return values: headers, parameters
        '''
        if parameters == None:
            parameters = {}

        parameters["ApiSig"] = self._generate_signature(path, parameters, body)

        return headers, parameters

    def register_session(self, access_token, refresh_token=None, 
            expires_at=None):
        '''To be implemented by the client.
        Registers an existing session with the auth client.

        Arguments:
        access_token -- The authorization token
        '''
        self.register_token(SparkAuthToken(access_token))

    def _generate_signature(self, path, parameters, body):
        s = self._generate_signature_string(path, parameters, body)
        return self._hash_signature_string(s)

    def _hash_signature_string(self, s):
        return hashlib.md5(s.encode('utf-8')).hexdigest()

    def _generate_signature_string(self, path, parameters, body):
        signature_string = "%sApiKey%s" % (self.consumer.secret, self.consumer.key)
        if self._is_authentication_path(path):
            return signature_string

        if self.token == None:
            raise ApplicationUnauthorizedException

        signature_string += "ServicePath%s" % path
        parameters["AuthToken"] = self.token.access_token

        for key in sorted(parameters):
            signature_string += "%s%s" % (key, parameters[key])

        # TODO: Support post body

        return signature_string

    def _is_authentication_path(self, path):
        p = re.compile('^\/v\d+\/session$')
        return p.match(path) != None

class SparkAuthToken(Token):
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
        return SparkAuthToken(json_dict['AuthToken'], None,
                None)
