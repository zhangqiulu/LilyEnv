import struct
import json
from lily_config import *


class LilyProtocol(object):




    @staticmethod
    def empty_request(request='', param=''):
        return {'request': request,'param': param}

    @staticmethod
    def action_request(action=''):
        return {'action': action}

    @staticmethod
    def get_param(**kwargs):

        request = LilyProtocol.empty_request()
        if 'request' in kwargs:
            request['request'] = kwargs['request']
        if 'param' in kwargs:
            request['param'] = kwargs['param']

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

        length, = struct.unpack('i', response[0:4])

        data = response[4:4 + length]

        data = LilyProtocol._unpack_response(data)

        return length, data

    @staticmethod
    def _unpack_response(data_json):
        data = json.loads(data_json);
        type = data['type']

        unpacked = None

        try:
            unpacked = getattr(LilyProtocol, '_unpack_' + type + '_response')(data)
        except AttributeError:
            logging.error("[Lily Error][LilyProtocol][_unpack_response] No attr called {0}".format(type))

        return unpacked


    @staticmethod
    def _unpack_msg_response(response):
        response = response['data']
        data, = struct.unpack('{0}s'.format(len(response)), bytearray(response))
        return data

    @staticmethod
    def _unpack_obs_response(response):
        response = response['data']
        data = struct.unpack('{0}B'.format(len(response)), bytearray(response))
        return data

    @staticmethod
    def _unpack_act_response(response):
        reward = response['reward']
        state = response['state']
        state = struct.unpack('{0}B'.format(len(state)), bytearray(state))
        return (reward,state)