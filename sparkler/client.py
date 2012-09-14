'''A Python client for Spark API: https://www.sparkplatform.com/docs
'''

from sparkler.transport import ApiRequest
from sparkler.auth.factory import AuthFactory

class SparkClient:
    '''The Spark API client.
    
    Public instance variables:
    auth    -- The authentication/authorization interface.  See the corresponding
               class or the README for more details.
    request -- The ApiRequest object.  All useful methods are wrapped by 
               the SparkClient object itself.

    The following methods are deligated to...
    self.auth:
        -- register_session
    self.request:
        -- get
        -- post
        -- put
        -- delete
    '''
    def __init__(self, client_key, client_secret, auth_mode="hybrid", 
            auth_endpoint_uri="https://sparkplatform.com/oauth2",
            api_endpoint_uri="https://sparkapi.com",
            auth_callback_uri=None,
            data_access_version="v1"):
        self.auth = AuthFactory.create(auth_mode, client_key, client_secret,
                      auth_endpoint_uri, api_endpoint_uri, auth_callback_uri)
        self.request = ApiRequest(api_endpoint_uri, self.auth, 
                         data_access_version)

    def __getattr__(self, attrib):
        if attrib in ["get", "post", "put", "delete"]:
            return getattr(self.request, attrib)
        elif attrib in ["register_session"]:
            return getattr(self.auth, attrib)
        else:
            return getattr(self, attrib)
