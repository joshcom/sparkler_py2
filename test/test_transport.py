import unittest
import json
from sparkler import transport
from sparkler import response
from mock import MagicMock
from sparkler.exceptions import *
from test.sparkler_test_helpers import SparklerStubber

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

    def test_invalid_json(self):
        self.request._http_request = MagicMock(return_value=SparklerStubber.http_response(200, 
            "<html><head><title>Hi</title></head></html>"))
        self.assertRaises(ValueError, self.request.get, ("listings"))

    def test_api_error(self):
        self.request._http_request = MagicMock(return_value=SparklerStubber.http_response(400, 
            "{\"Success\": false, \"Message\": \"Session token has expired\", \"Code\": 1020}"))
        self.assertRaises(HttpStatusNotSuccessfulException, self.request.get, ("listings"))

class TestApiRequest(unittest.TestCase):
    def setUp(self):
        self.request = transport.Request("https://sparkapi.com/")


