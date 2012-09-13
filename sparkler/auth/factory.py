from sparkler.auth.client import *
from sparkler.auth.oauth2 import OAuth2Client
from sparkler.auth.spark_auth import SparkAuthClient

class AuthFactory:
    '''An AuthClient factory that returns an instance for the appropriate
    auth mechanism as defined in auth_mode'''
    auth_modes = {
            "oauth2": OAuth2Client,
            "spark_auth": SparkAuthClient
    }

    @staticmethod
    def create(auth_mode, client_key, client_secret, auth_endpoint_uri, 
            api_endpoint_uri, auth_callback_uri=None):
        '''
        Arguments:
        auth_mode -- The authentication/authorization mode, which determines
                     which instance the factory will instantiate.
        client_key -- The API client key
        client_secret -- The API client secret
        auth_endpoint_uri -- The URI fo the auth endpoint to redirect 
                             end users to.
        api_endpoint_uri -- The URI for the data access API

        Keyword Arguments:
        auth_callback_uri -- The optional callback URI
        '''
        consumer = Consumer(client_key, client_secret, auth_callback_uri)
        return AuthFactory.auth_modes[auth_mode](consumer=consumer,
            auth_endpoint_uri=auth_endpoint_uri, 
            api_endpoint_uri=api_endpoint_uri)
