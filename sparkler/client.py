from sparkler.transport import ApiRequest
from sparkler.auth.factory import *

class SparkClient:
    def __init__(self, client_key, client_secret, auth_mode="hybrid", 
            auth_endpoint_uri="https://sparkplatform.com/oauth2",
            api_endpoint_uri="https://sparkapi.com",
            auth_callback_uri=None,
            data_access_version="v1",):
        self.request = ApiRequest(api_endpoint_uri, data_access_version)
        self.auth = AuthFactory.create(auth_mode, client_key, client_secret,
                auth_endpoint_uri, api_endpoint_uri, auth_callback_uri)

    def register_session(self, access_token, refresh_token):
        pass

    ###
    # TODO: These four methods need a better proxy to self.request.
    #       Worst case scenario, this may as well just inherit ApiRequset
    ###
    def get(self,path,parameters=None):
        return self.request.get(path, parameters)

    def post(self,path,body=None):
        return self.request.post(path, body)

    def put(self,path,body=None):
        return self.request.put(path, body)

    def delete(self,path,parameters=None):
        return self.request.delete(path, parameters)

#    def __getattr__(self, attrib):
#        if attrib in ["get", "post", "put", "delete"]:
#            getattr(self.request, attrib)()
#        else:
#            getattr(self, attrib)
