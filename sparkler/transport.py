'''Classes handling the HTTP transport of data between the client
   and Spark API
'''
import urllib
import httplib2
from sparkler.response import Response

class Request(object):
    '''Handles HTTP requests.

    Public isntance variables:
    endpoint    -- The host to send requests to. 
    '''

    def __init__(self, data_access_endpoint):
        self.endpoint = data_access_endpoint

    def get(self, path, parameters=None):
        '''Returns a response.Response object after performing a GET request
        to the endpoint.

        Arguments:
        path -- The path to append to the endpoint.

        Keyword Arguments:
        parameters -- (optional) The hash of parameters to send along with
                      the request
        '''
        return self._request('GET', path, parameters=parameters)

    def post(self, path, body=None):
        '''Returns a response.Response object after performing a POST request
        to the endpoint.

        Arguments:
        path -- The path to append to the endpoint.

        Keyword Arguments:
        body -- (optional) The body data to POST
        '''
        return self._request('POST', path, body=body)

    def put(self, path, body=None):
        '''Returns a response.Response object after performing a PUT request
        to the endpoint.

        Arguments:
        path -- The path to append to the endpoint.
        
        Keyword Arguments:
        body -- (optional) The body data to PUT 
        '''
        pass # TODO
        # return self._request('PUT', path, body=body)

    def delete(self, path, parameters=None):
        '''Returns a response.Response object after performing a DELETE request
        to the endpoint.

        Arguments:
        path -- The path to append to the endpoint.

        Keyword Arguments:
        parameters -- (optional) The hash of parameters to send along with
                      the request
        '''
        pass # TODO
        # return self._request('DELETE', path, parameters=parameters)

    def build_request_uri(self, path, parameters=None):
        '''Returns a string of the URI to send a HTTP request to.
        Arguments:
        path -- The path to append to the endpoint.

        Keyword Arguments
        parameters -- the URI parameters to append to the URI
        '''
        base_uri = self.endpoint.strip("/ ")
        path = path.strip("/ ")
        uri = "{0}{1}".format(base_uri, "/" + path).rstrip("/")
        return self.attach_parameters_to_uri(uri, parameters)

    def attach_parameters_to_uri(self, uri, parameters):
        '''Returns a string value concatinating the parameter list,
        encoded, to the given uri.

        Arguments:
        uri -- The full URI to attach the parameters to.
        parameters -- a hash of the parameters to generate a string
                      to append to the URI.
        '''
        if parameters == None:
            return uri

        escaped_params = urllib.parse.urlencode(parameters)

        connector = "?"
        if uri.find("?") > -1:
            connector = "&"

        return uri + connector + escaped_params

    def _request(self, method, path, headers=None, parameters=None, body=None):
        '''Performs an HTTP request.  Should be called through a wrapper method
        (self.get, etc.) rather than directly.
        '''
        http = httplib2.Http()
        uri = self.build_request_uri(path, parameters=parameters)

        if body != None:
            body = urllib.parse.urlencode(body)

        response, content = http.request(uri, method, headers=headers, 
                body=body)

        # Check response -- raise error?

        return Response.parse(content.decode('utf-8'))

class ApiRequest(Request):
    '''Handles HTTP requests specifically intended for the Spark API endpoint
    (e.g. https://sparkapi.com, or subdomains.)

    Public isntance variables:
    endpoint    -- The host to send requests to. 
    data_access_version -- The api version, defaults to "v1"
    '''

    def __init__(self, data_access_endpoint, data_access_version="v1"):
        super(ApiRequest, self).__init__(data_access_endpoint)
        self.endpoint = data_access_endpoint
        self.data_access_version = data_access_version

    def build_api_path(self, path):
        '''Returns a string that formats the API path with the version
           appended to it, unless that version is already present.

           Arguments:
           path -- The path to append to the versioned endpoint.
        '''
        if path.lower().find("/v1/") != 0 and path.lower().find("http") != 0:
            path = "/"+self.data_access_version+"/" + path.strip("/ ")
        return path

    # TODO: Timeouts and other options
    def _request(self, method, path, headers=None, parameters=None, body=None):
        '''Performs an HTTP request.  Should be called through a wrapper method
        (self.get, etc.) rather than directly.
        '''
        path = self.build_api_path(path)
        headers = {"Authorization": "OAuth ACCESS_CODE_GOES_HERE_FOR_NOW"}
        return super(ApiRequest, self)._request(method, path, headers=headers,
                parameters=parameters, body=body)
