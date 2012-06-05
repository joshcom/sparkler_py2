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
    '''
    def __init__(self, client_key, client_secret, auth_mode="hybrid", 
            auth_endpoint_uri="https://sparkplatform.com/oauth2",
            api_endpoint_uri="https://sparkapi.com",
            auth_callback_uri=None,
            data_access_version="v1"):
        self.request = ApiRequest(api_endpoint_uri, data_access_version)
        self.auth = AuthFactory.create(auth_mode, client_key, client_secret,
                auth_endpoint_uri, api_endpoint_uri, auth_callback_uri)

    def register_session(self, access_token, refresh_token):
        '''Registers and existing session with the client.
        
        Arguments:
        access_token -- The token allowing access to the API
        refresh_token -- The token allowing a session to be refreshed.
        '''
        pass

    ###
    # These four methods need a better proxy to self.request.
    # Worst case scenario, this may as well just inherit ApiRequset
    ###
    def get(self, path, parameters=None):
        '''A wrapper for self.request.get'''
        return self.request.get(path, parameters)

    def post(self, path, body=None):
        '''A wrapper for self.request.post'''
        return self.request.post(path, body)

    def put(self, path, body=None):
        '''A wrapper for self.request.put'''
        return self.request.put(path, body)

    def delete(self, path, parameters=None):
        '''A wrapper for self.request.delete'''
        return self.request.delete(path, parameters)

#    def __getattr__(self, attrib):
#        if attrib in ["get", "post", "put", "delete"]:
#            getattr(self.request, attrib)()
#        else:
#            getattr(self, attrib)
