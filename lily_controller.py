from lily_tcpcient import LilyTcpClient
from lily_protocol import LilyProtocol


class LilyController(object):

    def __init__(self, tcp_client, **kwargs):
        self.tcp_client = tcp_client

    def create_game(self):
        return 0

    def get_observation(self, receive_size=1024):
        if self.tcp_client:
            if self.tcp_client.send(request='obs'):
                return self.tcp_client.receive(receive_size)
                print("bbb")
        return False, 0, 0, 0

    def step(self):
        return 2