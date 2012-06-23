import unittest
import json
from sparkler import response

class TestResponse(unittest.TestCase):

    @staticmethod
    def big_d_json():
        response_dict = {
                "D": {
                    "Success": True,
                    "Results": [
                        {"Id":"20100000000000000000000000"}
                    ]
                }
        }
        return json.dumps(response_dict)

    def setUp(self):
        self.response = response.Response.parse(TestResponse.big_d_json())

    def test_strip_big_D(self):
        self.assertTrue(self.response.Success)
        self.assertEqual("20100000000000000000000000", self.response.Results[0]["Id"])

    def test_parse_any_json_string(self):
        r = response.Response.parse('{"Success":true}')
        self.assertTrue(r.Success)

    def test_works_like_a_dict(self):
        self.assertTrue(self.response['Success'])
        self.assertEqual("20100000000000000000000000", self.response['Results'][0]["Id"])

        # Check iterable
        for key in self.response:
            if key == 'Success':
                self.assertTrue(self.response[key])

        # Verify assignment
        self.response['Success'] = False
        self.assertFalse(self.response['Success'])
        
