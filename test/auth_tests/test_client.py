import unittest
from sparkler.auth.client import *

class TestAuthClient(unittest.TestCase):
    pass

class TestOauth2Consumer(unittest.TestCase):
    def setUp(self):
        self.consumer = Consumer("my_key", "my_secret", 
            "https://www.joshcom.net")

    def test_init(self):
        self.assertEqual("my_key", self.consumer.key)
