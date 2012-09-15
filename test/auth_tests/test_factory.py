import unittest
from sparkler.configuration import Configuration
from sparkler.auth.factory import AuthFactory
from sparkler.auth import oauth2, spark_auth
from sparkler.exceptions import *

class TestAuthFactory(unittest.TestCase):
    def setUp(self):
        c = Configuration()
        self.config = c.load_dict({
            "key":"client_key",
            "secret":"client_secret",
            "auth_mode":"oauth2",
            "auth_endpoint_uri":"https://www.joshcom.net",
            "api_endpoint_uri":"https://sparkapi.com",
            "auth_callback_uri":"https://www.joshcom.net/callback"
        })

    def test_oauth2_creation(self):
        auth = AuthFactory.create(self.config)
        self.assertIsInstance(auth, oauth2.OAuth2Client)

    def test_spark_hybrid_creation(self):
        self.config["auth_mode"] = "hybrid"
        auth = AuthFactory.create(self.config)
        self.assertIsInstance(auth, oauth2.HybridClient)

    def test_spark_auth_creation(self):
        self.config["auth_mode"] = "spark_auth"
        auth = AuthFactory.create(self.config)
        self.assertIsInstance(auth, spark_auth.SparkAuthClient)

    def test_unknown_client(self):
        self.config["auth_mode"] = "josh_auth"
        self.assertRaises(ClientConfigurationException,
                AuthFactory.create, (self.config))

    def test_missing_client(self):
        self.config["auth_mode"] = None
        self.assertRaises(ClientConfigurationException,
                AuthFactory.create, (self.config))
