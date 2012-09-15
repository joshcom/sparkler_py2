'''A Python client for Spark API: https://www.sparkplatform.com/docs
'''

from sparkler.transport import ApiRequest
from sparkler.auth.factory import AuthFactory
from sparkler.configuration import Configuration

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
    def __init__(self, options_dict={}):
        # TODO: Reconfigre on the fly
        c = Configuration(options_dict)
        self.auth = AuthFactory.create(c.config)
        self.request = ApiRequest(c.config, self.auth)

    def __getattr__(self, attrib):
        if attrib in ["get", "post", "put", "delete"]:
            return getattr(self.request, attrib)
        elif attrib in ["register_session"]:
            return getattr(self.auth, attrib)
        else:
            return getattr(self, attrib)
