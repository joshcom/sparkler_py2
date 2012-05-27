import json

class Response:
    @staticmethod
    def parse(json_string):
        json_hash = json.loads(json_string)

        # Account for the big-D
        if 'D' in json_hash:
            json_hash = json_hash['D']

        return Response(json_hash)

    def __init__(self, json_hash):
        for key in json_hash:
            self[key] = json_hash[key]

    def __getitem__(self, key):
        return getattr(self,key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __delitem__(self, key):
        return delattr(self, key)

    def __iter__(self):
        return self.__dict__.__iter__()
