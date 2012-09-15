import unittest
from sparkler.auth.client import *
from sparkler.configuration import Configuration

class TestAuthClient(unittest.TestCase):
    pass

class TestOauth2Consumer(unittest.TestCase):
    def setUp(self):
        c = Configuration()
        self.config = c.load_dict({
            "auth_endpoint_uri":"https://www.joshcom.net"
        })
        self.consumer = Consumer("my_key", "my_secret", 
            self.config)

    def test_init(self):
        self.assertEqual("my_key", self.consumer.key)
