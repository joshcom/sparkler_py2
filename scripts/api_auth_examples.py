import sparkler
from sparkler.client import SparkClient

# Defaults are noted as the string values, unless those values are in all caps --
# those values should be replaced with the values assigned to your API key.
client =  SparkClient({
                "key"              :"YOUR_CLIENT_KEY",  
                "secret"           :"YOUR_CLIENT_SECRET", 
                "api_user_agent"   :"YOUR_CUSTOM_API_CLIENT_NAME",
                "auth_mode"        :"spark_auth", 
                "auth_endpoint_uri":"https://sparkapi.com/v1/session",
                "api_endpoint_uri" :"https://sparkapi.com"})

client.auth.init_session()
listings = client.get("listings")  # Refreshing will occurr automatically.
