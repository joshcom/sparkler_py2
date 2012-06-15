from sparkler.exceptions import *
class SparklerStubber(object):
    @staticmethod
    def http_response(response_code, response_body=""):
        return response_code, bytearray(response_body,'utf8')
    @staticmethod
    def http_status_not_successful(response=None):
        return HttpStatusNotSuccessfulException(response)

