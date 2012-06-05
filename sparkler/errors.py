'''Exceptions raised by the Sparkler client.
'''

class ApplicationUnauthorizedException(Exception):
    '''Raised when a request is made to the API when no authorization has been 
    granted to the client.
    '''
    pass
class AuthExpiredException(Exception):
    '''Raised when an authorization token has expired.  Signals the need
    to refresh the session, if the particular auth method supports it.
    '''
    pass
class AuthFailureException(Exception):
    '''Signals a general failure with an authorization attempt.
    '''
    pass
