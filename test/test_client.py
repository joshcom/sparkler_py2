import unittest
from mock import MagicMock
from sparkler.client import *
from sparkler.response import Response
from sparkler.auth.client import *
from sparkler.auth import oauth2

class TestSparkClient(unittest.TestCase):
    def setUp(self):
        self.client = SparkClient({
            "key":"client_key", 
            "secret":"client_secret", 
            "auth_mode":"oauth2",
            "auth_callback_uri":"https://www.joshcom.net/callback"
        })

    def test_defaults(self):
        self.assertEqual("https://sparkplatform.com/openid", self.client.auth.auth_endpoint_uri())
        self.assertEqual("v1", self.client.request.data_access_version)

    def test_auth_type(self):
        self.assertIsInstance(self.client.auth, oauth2.OAuth2Client)

    def test_proxy_methods(self):
        self.client.request.get = MagicMock(return_value=Response({"Success": True}))
        self.assertTrue(self.client.get("listings")["Success"])
