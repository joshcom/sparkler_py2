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
    # In your callback, call grant then register your token as follows:
    # token = client.auth.grant("CODE")
    # client.register_session(token.access_token, token.refresh_token)
except sparkler.exceptions.AuthExpiredException:
    client.auth.refresh() # If the refresh is successful, attempt your request again.
