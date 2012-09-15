from sparkler.auth.client import *
from sparkler.exceptions import *
from sparkler.auth.oauth2 import OAuth2Client, HybridClient
from sparkler.auth.spark_auth import SparkAuthClient

class AuthFactory:
    '''An AuthClient factory that returns an instance for the appropriate
    auth mechanism as defined in auth_mode'''
    auth_modes = {
            "oauth2": OAuth2Client,
            "hybrid": HybridClient,
            "spark_auth": SparkAuthClient
    }

    @staticmethod
    def create(configuration):
        '''
        Arguments:
        configuration -- A SafeConfigParser object defining:
            * auth_mode -- The authentication/authorization mode, which determines
                           which instance the factory will instantiate.
            * key       -- The API client key
            * secret    -- The API client secret
            * auth_endpoint_uri -- The URI fo the auth endpoint to redirect 
                                   end users to.
            * api_endpoint_uri  -- The URI for the data access API
            * auth_callback_uri -- The optional callback URI
        '''
        try:
            auth_mode = configuration["auth_mode"]
            consumer = Consumer(configuration["key"], configuration["secret"], 
                    configuration.get("auth_callback_uri"))
            return AuthFactory.auth_modes[auth_mode](consumer, configuration)
        except KeyError as e:
            if e == 'key' or e == 'secret':
                ex_str = "%s is a required configuration attribute" % (e)
            else:
                ex_str = "Unknown auth_mode configuration value"

            raise ClientConfigurationException(ex_str)
