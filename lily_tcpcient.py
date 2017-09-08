import socket
from lily_config import *
import struct
import json
from lily_protocol import LilyProtocol


class LilyTcpClient(object):

    def __init__(self, **kwargs):
        assert 'host' in kwargs
        assert 'port' in kwargs
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(10)
        self.host = kwargs['host']
        self.port = kwargs['port']

    def connect(self):
        if self.socket:
            try:
                ret = self.socket.connect_ex((self.host, self.port))
            except Exception, err:
                logging.error("[Lily Error][LilyTcpClient][connect]{0}".format(err))

    def send(self, **kwargs):
        if self.socket:
            try:
                data_pack = LilyProtocol.pack_request(**kwargs)
                self.socket.sendall(data_pack)
                return True
            except Exception,e:
                logging.error("[Lily Error][LilyTcpClient][send]{0}".format(e))
                return False

    def receive(self, buffer_size):
        if self.socket:
            try:
                received = self.socket.recv(buffer_size)
                rtype, length, data = LilyProtocol.unpack_response(response=received)

                return True, rtype, length, data
            except Exception,e:
                logging.error("[Lily Error][LilyTcpClient][receive]{0}".format(e))
                return False, 0, 0, 0

    def shutdown(self):
        if self.socket:
            self.socket.close()
