import json

class Response(object):
    '''Wraps an API response and dict.

    Data can be accessed just as though it were a directionary, 
    structured as JSON from the API (with the "Big D" attribute
    stripped, if applicable).

    Thus, self["Success"] would be true if the response were successful,
    while self["Results"] would be the array of API data results.
    '''

    @staticmethod
    def parse(json_string):
        '''Returns a Response object from a parsed JSON string.
        If a "D" attribute wraps the JSON data, the Response object
        will strip this attribute and treat its subattribute as top-level.

        Arguments:
        json_string -- A string of JSON data to be processed.
        '''
        json_hash = json.loads(json_string)

        # Account for the big-D
        if 'D' in json_hash:
            json_hash = json_hash['D']

        return Response(json_hash)

    def __init__(self, json_hash):
        for key in json_hash:
            self[key] = json_hash[key]

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        return setattr(self, key, value)

    def __delitem__(self, key):
        return delattr(self, key)

    def __iter__(self):
        return self.__dict__.__iter__()
