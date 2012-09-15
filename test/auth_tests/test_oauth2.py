import unittest
import time
from sparkler.exceptions import *
from sparkler.configuration import Configuration
from sparkler.auth import oauth2
from sparkler.response import Response
from sparkler.auth import client
from mock import MagicMock
from test.sparkler_test_helpers import SparklerStubber

class TestOauth2Client(unittest.TestCase):
    def setUp(self):
        self.consumer = client.Consumer("my_key", "my_secret", 
                "https://www.joshcom.net")
        self.token = oauth2.OAuth2Token.parse(TestOauth2Token.example_token())
        c = Configuration()
        self.config = c.load_dict({
            "key":"client_key",
            "secret":"client_secret",
            "auth_mode":"oauth2",
            "auth_endpoint_uri":"https://developers.sparkplatform.com/oauth2?",
            "api_endpoint_uri": "https://sparkapi.com",
            "auth_callback_uri":"https://www.joshcom.net/callback"
        })

        self.client = oauth2.OAuth2Client(self.consumer,self.config)

    def mock_token_success(self):
        self.client._perform_token_request = MagicMock(return_value=Response.parse(\
               '{"expires_in":86400,"refresh_token":"11111","access_token":"22222"}'))

    def test_init(self):
        self.assertIsInstance(self.client, oauth2.OAuth2Client)

    def test_required_configuration_options(self):
        self.config["key"] = None
        self.assertRaises(ClientConfigurationException, oauth2.OAuth2Client,
                self.consumer,self.config)


    def test_authorization_uri(self):
        # Seriously, what the heck am I doing here...
        url = self.client.authorization_uri()
        for parameter in ["redirect_uri=https%3A%2F%2Fwww.joshcom.net",
         "response_type=code",
         "client_id=my_key"]:
            url = url.replace(parameter, "")
        url = url.replace("&","")
        self.assertEqual("https://developers.sparkplatform.com/oauth2?", url)

    def test_grant_failture(self):
        self.client._perform_token_request = MagicMock(side_effect=\
                SparklerStubber.http_status_not_successful(Response.parse(\
               '{"error_description":"The access grant you supplied is invalid",\
                 "error":"invalid_grant"}')))
        self.assertRaises(AuthFailureException, self.client.grant, ("12345"))

    def test_grant_success(self):
        self.mock_token_success()
        self.assertIsInstance(self.client.grant("1234"), oauth2.OAuth2Token)
        self.assertEqual("11111", self.client.token.refresh_token)
        self.assertEqual("22222", self.client.token.access_token)

    def test_refresh_success(self):
        self.mock_token_success()
        self.assertIsInstance(self.client.refresh("1234"), oauth2.OAuth2Token)
        self.assertEqual("11111", self.client.token.refresh_token)
        self.assertEqual("22222", self.client.token.access_token)

    def test_refresh_defaults_to_registered_token(self):
        self.mock_token_success()
        self.client.register_token(self.token)
        self.assertEqual("my_token", self.client.token.access_token)
        self.assertIsInstance(self.client.refresh(), oauth2.OAuth2Token)
        self.assertEqual("22222", self.client.token.access_token)

class TestOauth2Token(unittest.TestCase):
    @staticmethod
    def example_token():
        return {
            "access_token": "my_token",
            "refresh_token": "my_refresh_token",
            "expires_in": 86400
        }

    def setUp(self):
        self.token = oauth2.OAuth2Token.parse(TestOauth2Token.example_token())

    def test_parse_results_in_token(self):
        self.assertIsInstance(self.token, oauth2.OAuth2Token)

    def test_expiration(self):
        self.assertIsInstance(self.token.expires_at, time.struct_time)
        self.assertFalse(self.token.expired())
        self.token.expires_at = time.localtime()
        self.assertTrue(self.token.expired())


if __name__ == "__main__":
    unittest.main()
