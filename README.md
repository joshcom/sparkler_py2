Sparkler
========

Usage Examples
========

    from sparkler.client import SparkClient

    # Defaults are noted as the string values, unless those values are in all caps --
    # those values should be replaced with the values assigned to your API key.
    client =  SparkClient(client_key="YOUR_CLIENT_KEY",  
                client_secret="YOUR_CLIENT_SECRET", 
                auth_callback_uri="YOUR_CALLBACK_URI", 
                auth_mode="hybrid*", # hybrid not yet supported, so should be 'oauth2'
                auth_endpoint_uri="https://sparkplatform.com/oauth2",
                api_endpoint_uri="http://sparkapi.com")

    # Do the following only if you already have an access and refresh token
    client.register_session(access_token="YOUR_ACCESS_TOKEN", 
        refresh_token="YOUR_REFRESH_TOKEN")

    try:
        listings = client.get("listings")
    except ApplicationUnauthorizedException:
        print("Go here and get your code!: %s"  % client.auth.authorization_uri())
        print("Send that code to client.auth.grant('CODE')")
    except AuthExpiredException:
        client.auth.refresh() # If the refresh is successful, attempt your request again.
