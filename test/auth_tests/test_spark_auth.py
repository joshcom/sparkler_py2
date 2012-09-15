import unittest
import time
from sparkler.auth import spark_auth
from sparkler.response import Response
from sparkler.configuration import Configuration
from sparkler.auth import client
from mock import MagicMock
from test.sparkler_test_helpers import SparklerStubber
from sparkler.exceptions import *

class TestSparkAuthClient(unittest.TestCase):
    def setUp(self):
        self.consumer = client.Consumer("my_key", "my_secret")
        self.token = spark_auth.SparkAuthToken.parse(TestSparkAuthToken.example_token())

        c = Configuration()
        self.config = c.load_dict({
            "key":"client_key",
            "secret":"client_secret",
            "auth_mode":"spark_auth",
            "auth_endpoint_uri":"https://developers.sparkapi.com/v1/session",
            "api_endpoint_uri": "https://sparkapi.com"
        })
        self.client = spark_auth.SparkAuthClient(self.consumer,self.config)
        self.client.register_session(self.token.access_token)

    def mock_token_success(self):
        self.client._perform_token_request = MagicMock(return_value=Response.parse(\
               '''{
                 "D" : {
                         Success: true,
                             Results: [{
                                 AuthToken: "my_new_token",
                                 Expires: "2010-10-30T15:49:01-05:00"
                             }]
                       }
                 }'''))

    def test_init(self):
        self.assertIsInstance(self.client, spark_auth.SparkAuthClient)

    def test_required_configuration_options(self):
        self.config["key"] = None
        self.assertRaises(ClientConfigurationException, spark_auth.SparkAuthClient,
                self.consumer,self.config)

    def test_generate_signature(self):
        self.assertEqual("c731cf2455fbc7a4ef937b2301108d7a",
                self.client._generate_signature("/v1/session", None, None))

        contacts_parameters = {
                "name" : "John Contact",
                "email": "contact@fbsdata.com",
                "phone": "555-5555",
                "group": "IDX Lead"
        }
        self.assertEqual("655dcba2ccb1ceccf51484b89513cccc", 
                self.client._generate_signature("/v1/contacts", contacts_parameters, None))

    def test_hash_signature_string(self):
        self.assertEqual("c731cf2455fbc7a4ef937b2301108d7a",
                self.client._hash_signature_string("my_secretApiKeymy_key"))
        self.assertEqual("655dcba2ccb1ceccf51484b89513cccc", 
                self.client._hash_signature_string("my_secretApiKeymy_keyServicePath/v1/contactsAuthTokenmy_tokenemailcontact@fbsdata.comgroupIDX LeadnameJohn Contactphone555-5555"))

    def test_generate_signature_string(self):
        # Test expected authentication signature string
        authentication_string = self.client._generate_signature_string("/v1/session", None, None)
        expected_string = "my_secretApiKeymy_key"
        self.assertEqual(authentication_string, expected_string)

        # Test signature for authenticated GET request
        contacts_parameters = {
                "name" : "John Contact",
                "email": "contact@fbsdata.com",
                "phone": "555-5555",
                "group": "IDX Lead"
        }
        authentication_string = self.client._generate_signature_string("/v1/contacts", contacts_parameters, None)
        expected_string = "my_secretApiKeymy_keyServicePath/v1/contactsAuthTokenmy_tokenemailcontact@fbsdata.comgroupIDX LeadnameJohn Contactphone555-5555"
        self.assertEqual(authentication_string, expected_string)

        # Test authentication signature for authenticated POST request (TODO)

    def test_is_authentication_path(self):
        good_paths = ["/v1/session", "/v2/session", "/v20/session"] 
        bad_paths = ["/session","/v1/contacts"]

        for path in good_paths:
            self.assertTrue(self.client._is_authentication_path(path))

        for path in bad_paths:
            self.assertFalse(self.client._is_authentication_path(path))
        


class TestSparkAuthToken(unittest.TestCase):
    @staticmethod
    def example_token():
        return {
            "AuthToken": "my_token",
            "Expires": "2010-10-30T15:49:01-05:00"
        }

    def setUp(self):
        self.token = spark_auth.SparkAuthToken.parse(TestSparkAuthToken.example_token())

    def test_parse_results_in_token(self):
        self.assertIsInstance(self.token, spark_auth.SparkAuthToken)
        self.assertEqual(self.token.access_token, "my_token")

    def test_expiration(self):
        self.assertIsNone(self.token.expires_at)


if __name__ == "__main__":
    unittest.main()
