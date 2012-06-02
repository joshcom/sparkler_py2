import unittest
import json
from sparkler.auth.client import *
from sparkler.auth.factory import AuthFactory
from sparkler.auth import oauth2

class TestAuthFactory(unittest.TestCase):
    def test_oauth2_creation(self):
        auth = AuthFactory.create("oauth2", "client_key", "client_secret",
                "https://sparkplatform.com/oauth2", "https://sparkapi.com",
                "https://www.joshcom.net/callback")
        self.assertIsInstance(auth, oauth2.OAuth2Client)
