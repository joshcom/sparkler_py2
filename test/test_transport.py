import unittest
import json
from sparkler import transport
from sparkler import response
from mock import MagicMock

class TestRequest(unittest.TestCase):
    def setUp(self):
        self.request = transport.Request("https://sparkapi.com/")

    def test_build_request_uri(self):
      uri = self.request.build_request_uri("/v1/listings")
      self.assertEqual("https://sparkapi.com/v1/listings", uri)

      uri = self.request.build_request_uri("")
      self.assertEqual("https://sparkapi.com", uri)

      uri = self.request.build_request_uri("/v1/listings", 
          {"_filter":"City Eq Fargo"})
      self.assertEqual("https://sparkapi.com/v1/listings?_filter=City+Eq+Fargo", uri)
    
    def test_attach_parameters_to_uri(self):
        uri = self.request.attach_parameters_to_uri("https://sparkapi.com/", {"id":"1234",
            "uri":"http://www.google.com"})

        # Seriously, there has to be a less silly way to test this.
        self.assertTrue(uri.find("https://sparkapi.com/?")==0)
        self.assertTrue(uri.find("id=1234")>0)
        self.assertTrue(uri.find("uri=http%3A%2F%2Fwww.google.com")>0)

        uri = self.request.attach_parameters_to_uri("https://sparkapi.com?okay=true", {"id":"1234",
            "uri":"http://www.google.com"})
        self.assertTrue(uri.find("https://sparkapi.com?okay=true") == 0)
        self.assertEqual(uri.count("?"), 1)

    def test_get_as_request_wrapper(self):
        self.request._request = MagicMock(return_value=response.Response.parse("{\"Success\":true}"))
        self.assertTrue(self.request.get("listings")["Success"])

class TestApiRequest(unittest.TestCase):
    def setUp(self):
        self.request = transport.Request("https://sparkapi.com/")


