'''Classes handling the HTTP transport of data between the client
   and Spark API
'''
import urllib
import httplib2
import json
from sparkler.exceptions import *
from sparkler.response import Response
from sparkler.logger import SparkLogger

class Request(object):
    logger = SparkLogger.get()

    '''Handles HTTP requests.

    Public isntance variables:
    endpoint    -- The host to send requests to. 
    '''

    def __init__(self, configuration, endpoint=None):
        self.configuration = configuration
        if endpoint == None:
            self.endpoint = self.configuration["api_endpoint_uri"]
        else:
            self.endpoint = endpoint

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

    def post(self, path, body=None, parameters=None):
        '''Returns a response.Response object after performing a POST request
        to the endpoint.

        Arguments:
        path -- The path to append to the endpoint.

        Keyword Arguments:
        body      -- (optional) The body data to POST
        parameters -- (optional) URI parameters to supply (necessary for API Auth)
        '''
        return self._request('POST', path, body=body, parameters=parameters)

    def put(self, path, body=None):
        '''Returns a response.Response object after performing a PUT request
        to the endpoint.

        Arguments:
        path -- The path to append to the endpoint.
        
        Keyword Arguments:
        body -- (optional) The body data to PUT 
        '''
        return self._request('PUT', path, body=body)

    def delete(self, path, parameters=None):
        '''Returns a response.Response object after performing a DELETE request
        to the endpoint.

        Arguments:
        path -- The path to append to the endpoint.

        Keyword Arguments:
        parameters -- (optional) The hash of parameters to send along with
                      the request
        '''
        return self._request('DELETE', path, parameters=parameters)

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

        # PYTHON2: urllib.parse.urlencode in python 3 version
        escaped_params = urllib.urlencode(parameters)

        connector = "?"
        if uri.find("?") > -1:
            connector = "&"

        return uri + connector + escaped_params

    def _request(self, method, path, headers=None, parameters=None, body=None):
        '''Performs an HTTP request.  Should be called through a wrapper method
        (self.get, etc.) rather than directly.
        '''
        uri = self.build_request_uri(path, parameters=parameters)

        if body != None:
            body = json.dumps(body)

        Request.logger.debug("%s: %s" % (method, uri))
        response, content = self._http_request(uri, method, headers, body)
        parsed_response = Response.parse(content.decode('utf-8'))

        status = int(response['status'])
        Request.logger.debug("HTTP Status %d" % status)

        if status >= 200 and status <= 299:
            return parsed_response 
        else:
            raise HttpStatusNotSuccessfulException(parsed_response)

    def _http_request(self, uri, method, headers=None, body=None):
        '''A dumb wrapper for http.request, largely for stubbing
        when testing.
        '''
        http = httplib2.Http()
        return http.request(uri, method, headers=headers, body=body)

class ApiRequest(Request):
    '''Handles HTTP requests specifically intended for the Spark API endpoint
    (e.g. https://sparkapi.com, or subdomains.)

    Public instance variables:
    endpoint    -- The host to send requests to. 
    auth_client -- (optional) The AuthClient instance that will attatch the 
                   necessary authorization headers to each request.
    data_access_version -- (optional) The api version, defaults to "v1"
    '''

    def __init__(self, configuration, auth_client=None):
        super(ApiRequest, self).__init__(configuration)
        self.data_access_version = configuration["api_version"]
        self.auth_client = auth_client

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
        headers = self._configuration_headers()
        if self.auth_client != None:
            body = self._wrap_in_magic_d(body)
            headers, parameters = self.auth_client.authorize_request(headers,parameters,path=path,body=body)

        if body != None:
            headers["Content-Type"] = "application/json"

        try:
            response = super(ApiRequest, self)._request(method, path, headers=headers,
                parameters=parameters, body=body)
        except HttpStatusNotSuccessfulException as e:
            raise self._raise_http_status_exception(e)

        return response

    def _wrap_in_magic_d(self, body=None):
        if body != None and "D" not in body:
            return {"D": body}
        else:
            return body

    def _configuration_headers(self):
        h_name = self.configuration.get("api_user_agent")
        if h_name == None:
            ex_str = "api_user_agent is a required configuration value"
            raise ClientConfigurationException(ex_str)

        return {
                "X-SparkApi-User-Agent" : h_name
        }


    def _raise_http_status_exception(self, e):
        try: # TODO: Support Response#get
            code = e.response["Code"]
        except:
            raise e

        if code == 1020:
            raise AuthExpiredException(e.response)
        else:
            raise e

