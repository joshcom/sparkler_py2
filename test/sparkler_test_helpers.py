class SparklerStubber(object):
    @staticmethod
    def http_response(response_code, response_body=""):
        return response_code, bytearray(response_body,'utf8')
