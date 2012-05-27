import urllib
import httplib2
from sparkler.response import Response

class Request:
    def __init__(self, data_access_endpoint):
        self.endpoint = data_access_endpoint

    def get(self,path,parameters=None):
        return self._request('GET', path, parameters=parameters)

    def put(self,path,body=None):
        pass # TODO
        # return self._request('PUT', path, body=body)

    def post(self,path,body=None):
        pass # TODO
        # return self._request('POST', path, body=body)

    def delete(self,path,parameters=None):
        pass # TODO
        # return self._request('DELETE', path, parameters=parameters)

    def build_request_uri(self, path, parameters=None):
        base_uri = self.endpoint.strip("/ ")
        uri = "{0}{1}".format(base_uri, "/" + path.strip("/ "))
        return self.attach_parameters_to_uri(uri, parameters)

    def attach_parameters_to_uri(self, uri, parameters):
        if parameters == None:
            return uri

        escaped_params = urllib.parse.urlencode(parameters)

        connector = "?"
        if uri.find("?") > -1:
            connector = "&"

        return uri + connector + escaped_params

    def _request(self, method, path, headers=None, parameters=None, body=None):
        http = httplib2.Http()
        uri = self.build_request_uri(path,parameters=parameters)
        response, content = http.request(uri, 'GET', headers=headers, 
                body=body)
        return Response.parse(content.decode('utf-8')) # The decode here feels weak.

class ApiRequest(Request):
    def __init__(self, data_access_endpoint, data_access_version="v1"):
        self.endpoint = data_access_endpoint
        self.data_access_version = data_access_version

    def build_api_path(self, path):
        if path.lower().find("/v1/") != 0 and path.lower().find("http") != 0:
            path = "/"+self.data_access_version+"/" + path.strip("/ ")
        return path

    def _request(self, method, path, parameters=None, body=None):
        path = build_api_path(path)
        headers = {"Authorization": "OAuth ACCESS_CODE_GOES_HERE_FOR_NOW"}
        return super(ApiRequest, self)._request(method, path, headers=headers,
                parameters=parameters, body=body)
