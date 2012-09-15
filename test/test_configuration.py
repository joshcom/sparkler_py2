import unittest
from sparkler.configuration import Configuration

class TestConfiguration(unittest.TestCase):
    def test_initial_set_to_defaults(self):
        config = Configuration()
        self.assertEqual("hybrid", config.config["auth_mode"])

    def test_load_dict(self):
        config = Configuration()
        c = config.load_dict({"auth_mode":"spark_auth"})
        self.assertEqual("spark_auth", c["auth_mode"])

    def test_defaults(self):
        config = Configuration({"auth_mode":"openid"})
        self.assertEqual("https://sparkplatform.com/oauth2", config.config["auth_endpoint_uri"])

        config = Configuration({"auth_mode":"spark_auth"})
        self.assertEqual("https://sparkapi.com/v1/session", config.config["auth_endpoint_uri"])
