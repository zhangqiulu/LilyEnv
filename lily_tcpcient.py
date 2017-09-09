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
                received = self._receive_all(buffer_size)
                length, data = LilyProtocol.unpack_response(response=received)
                return True, length, data
            except Exception,e:
                logging.error("[Lily Error][LilyTcpClient][receive]{0}".format(e))
                return False, 0, 0

    def shutdown(self):
        if self.socket:
            self.socket.close()

    def _receive_all(self,buffer_size):

        packet = self.socket.recv(buffer_size)
        length, = struct.unpack('i', packet[0:4])
        length += 4

        while len(packet) < length:
            data = self.socket.recv(length - len(packet))
            if not data: break
            packet += data
        return packet