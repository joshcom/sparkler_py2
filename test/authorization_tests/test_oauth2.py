import unittest
import time
from sparkler.authorization import oauth2

class TestOauth2Client(unittest.TestCase):
    def setUp(self):
        self.consumer = oauth2.Consumer("my_key", "my_secret", 
                "https://www.joshcom.net")
        self.token = oauth2.Token.parse(TestOauth2Token.example_token())
        self.client = oauth2.Client(self.consumer,
                "https://developers.sparkplatform.com/oauth2",
                "https://developers.sparkapi.com")

    def test_init(self):
        self.assertIsInstance(self.client, oauth2.Client)

    def test_generate_default_token_endpoint(self):
        self.assertEqual("https://developers.sparkapi.com/token",
                self.client.token_endpoint)

    def test_authorization_uri(self):
        # Seriously, what the heck am I doing here...
        url = self.client.authorization_uri()
        for parameter in ["redirect_uri=https%3A%2F%2Fwww.joshcom.net",
         "response_type=code",
         "client_id=my_key"]:
            url = url.replace(parameter, "")
        url = url.replace("&","")
        self.assertEqual("https://developers.sparkplatform.com/oauth2?",
                url)

    def test_authorization_uri_with_custom_code(self):
        url = self.client.authorization_uri("custom")
        self.assertTrue(url.find("response_type=custom") > 0)


class TestOauth2Consumer(unittest.TestCase):
    def setUp(self):
        self.consumer = oauth2.Consumer("my_key", "my_secret", 
                "https://www.joshcom.net")

    def test_init(self):
        self.assertEqual("my_key", self.consumer.key)

class TestOauth2Token(unittest.TestCase):
    @staticmethod
    def example_token():
        return {
            "access_token": "my_token",
            "refresh_token": "my_refresh_token",
            "expires_in": 86400
        }

    def setUp(self):
        self.token = oauth2.Token.parse(TestOauth2Token.example_token())

    def test_parse_results_in_token(self):
        self.assertIsInstance(self.token, oauth2.Token)

    def test_expiration(self):
        self.assertIsInstance(self.token.expires_at, time.struct_time)
        self.assertFalse(self.token.expired())
        self.token.expires_at = time.localtime()
        self.assertTrue(self.token.expired())


if __name__ == "__main__":
    unittest.main()
