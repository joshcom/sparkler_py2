'''Exceptions raised by the Sparkler client.
'''

class HttpStatusNotSuccessfulException(Exception):
    '''Raised any time the HTTP response was not >=200 and <=299.
    Public attributes:
    response -- The Response object of the failed request.
    '''
    def __init__(self, response):
        self.response = response

class ApplicationUnauthorizedException(HttpStatusNotSuccessfulException):
    '''Raised when a request is made to the API when no authorization has been 
    granted to the client.
    '''
    pass
class AuthExpiredException(HttpStatusNotSuccessfulException):
    '''Raised when an authorization token has expired.  Signals the need
    to refresh the session, if the particular auth method supports it.
    '''
    pass
class AuthFailureException(HttpStatusNotSuccessfulException):
    '''Signals a general failure with an authorization attempt.
    '''
    pass
