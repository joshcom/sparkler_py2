[![Build Status](https://travis-ci.org/joshcom/sparkler_py2.png?branch=master)](https://travis-ci.org/joshcom/sparkler_py2)

Sparkler
========
A Python 2 client for Spark API: http://sparkplatform.com/docs/overview/api

Installation
========
TODO

Usage Examples
========
#### OpenID/OAuth 2 Hybrid
    import sparkler
    from sparkler.client import SparkClient

    # Defaults are noted as the string values, unless those values are in all caps --
    # those values should be replaced with the values assigned to your API key.
    client =  SparkClient({
        "key"       :"YOUR_CLIENT_KEY",  
        "secret"    :"YOUR_CLIENT_SECRET", 
        "auth_callback_uri":"YOUR_CALLBACK_URI", 
        "api_user_agent"   :"YOUR_CUSTOM_API_CLIENT_NAME",
        "auth_mode"        :"hybrid"
    })

    # Do the following only if you already have an access and refresh token
    client.register_session("YOUR_ACCESS_TOKEN", "YOUR_REFRESH_TOKEN")

    try:
        listings = client.get("listings")
    except sparkler.exceptions.ApplicationUnauthorizedException:
        print("Go here and get your code: %s"  % client.auth.authorization_uri())
        print("Send that code to client.auth.grant('CODE')")
    except sparkler.exceptions.AuthExpiredException:
        client.auth.refresh() # If the refresh is successful, attempt your request again.

#### OAuth 2 (OpenID/OAuth 2 Hybrid flow is recommended)
    import sparkler
    from sparkler.client import SparkClient

    # Defaults are noted as the string values, unless those values are in all caps --
    # those values should be replaced with the values assigned to your API key.
    client =  SparkClient({
        "key"       :"YOUR_CLIENT_KEY",  
        "secret"    :"YOUR_CLIENT_SECRET", 
        "auth_callback_uri":"YOUR_CALLBACK_URI", 
        "api_user_agent"   :"YOUR_CUSTOM_API_CLIENT_NAME",
        "auth_mode"        :"oauth2"  # Default is "hybrid"
    })

    # Do the following only if you already have an access and refresh token
    client.register_session("YOUR_ACCESS_TOKEN", "YOUR_REFRESH_TOKEN")

    try:
        listings = client.get("listings")
    except sparkler.exceptions.ApplicationUnauthorizedException:
        print("Go here and get your code: %s"  % client.auth.authorization_uri())
        print("Send that code to client.auth.grant('CODE')")
    except sparkler.exceptions.AuthExpiredException:
        client.auth.refresh() # If the refresh is successful, attempt your request again.

### SparkApi Auth
Not supported.  We encourage you to ask for an OAuth 2 key as a replacement for a SparkApi Auth key, if that's
what you were provided.

### Additional Options
While these are applied with defaults, you can further configure the client with the parameter examples below:

    client =  SparkClient({
        # ... required parameters omitted ...
        "auth_endpoint_uri":"https://sparkplatform.com/openid",
        "api_endpoint_uri" :"https://sparkapi.com",
        "data_access_version": "v1"
    })


Logging
=======
The SparkApi client creates a global logger with the name 'spark_client'.  This can be accessed directly by the SparkClient.logger attribute.  For example, to change the client's logging to DEBUG:

    import logging
    SparkClient.logger.setLevel(logging.DEBUG)

The logger level is set to INFO by default.


Exceptions
========
Custom sparkler exceptions are available in exceptions.py.  They are fairly well documented 
in that file, but to reiterate:

### ClientConfigurationException
Raised when a required client configuration setting is not supplied.

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
* Auto-refresh oauth2
* Clean up imports
* Top-down reconfiguration on the fly
