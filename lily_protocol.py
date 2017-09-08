import struct
import json


class LilyProtocol(object):

    @staticmethod
    def empty_request():
        return {'request': '','param1':0,'param2':0.0,'param3':''}

    @staticmethod
    def get_param(**kwargs):

        request = LilyProtocol.empty_request()
        if 'request' in kwargs:
            request['request'] = kwargs['request']
        if 'param1' in kwargs:
            request['param1'] = kwargs['param1']
        if 'param2' in kwargs:
            request['param2'] = kwargs['param2']
        if 'param3' in kwargs:
            request['param3'] = kwargs['param3']

        return request

    @staticmethod
    def pack_request(**kwargs):
        assert 'request' in kwargs
        request = LilyProtocol.get_param(**kwargs)
        request = json.dumps(request)
        request_pack = struct.pack('I{0}s'.format(len(request)), len(request), request)
        return request_pack

    @staticmethod
    def unpack_response(**kwargs):
        assert 'response' in kwargs
        response = kwargs['response']

        rtype, = struct.unpack('i', response[0:4])
        length, = struct.unpack('i', response[4:8])

        if rtype == 1:
            data = struct.unpack('{0}B'.format(length),response[8:8+length])
        else:
            data = response[8:8+length]

        return rtype, length, data




