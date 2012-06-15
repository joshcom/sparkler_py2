Sparkler
========
A Python 3 client for Spark API: http://sparkplatform.com/docs/overview/api

Installation
========
TODO

Usage Examples
========
#### OAuth 2
    import sparkler
    from sparkler.client import SparkClient

    # Defaults are noted as the string values, unless those values are in all caps --
    # those values should be replaced with the values assigned to your API key.
    client =  SparkClient(client_key="YOUR_CLIENT_KEY",  
                client_secret="YOUR_CLIENT_SECRET", 
                auth_callback_uri="YOUR_CALLBACK_URI", 
                auth_mode="oauth2", # Default is "hybrid"
                auth_endpoint_uri="https://sparkplatform.com/oauth2",
                api_endpoint_uri="https://sparkapi.com")

    # Do the following only if you already have an access and refresh token
    client.register_session("YOUR_ACCESS_TOKEN", "YOUR_REFRESH_TOKEN")

    try:
        listings = client.get("listings")
    except sparkler.exceptions.ApplicationUnauthorizedException:
        print("Go here and get your code: %s"  % client.auth.authorization_uri())
        print("Send that code to client.auth.grant('CODE')")
    except sparkler.exceptions.AuthExpiredException:
        client.auth.refresh() # If the refresh is successful, attempt your request again.

Exceptions
========
Custom sparkler exceptions are available in exceptions.py.  They are fairly well documented 
in that file, but to reiterate:

#### HttpStatusNotSuccessfulException
Raised when a request to the API resulted in a non-2xx code, and did not fit the use
case for another exception above.  This exception instance will have the public 
attribute "response", which is an instance of sparkler.response.Response() and contains
the API error code and error message.

All other exceptions extend HttpStatusNotSuccessfulException

#### ApplicationUnauthorizedException
Raised if the application has not yet been authorized by the end user
to access to the API.

#### AuthExpiredException
Raised when the authorization token has expired, thus requiring a refresh or a new token.

#### AuthFailureException
Raised when a step in the authorization process has failed. 


TODO
========
* Acceptance tests against live API
