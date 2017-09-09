from lily_tcpcient import LilyTcpClient
from lily_protocol import LilyProtocol
import numpy as np


class LilyController(object):

    def __init__(self, tcp_client, **kwargs):
        self.tcp_client = tcp_client
        self.config = kwargs['config']

    def create_game(self):
        return 0

    def get_observation(self, receive_size=1024):
        if self.tcp_client:
            if self.tcp_client.send(request='obs'):
                res, length, data = self.tcp_client.receive(receive_size)
                if res == 1:
                    width = self.config['data']['width']
                    height = self.config['data']['height']

                    return np.reshape(np.asarray(data), (height,width,3)).astype(np.uint8)

        return None

    def act(self,action, value, receive_size=1024):
        if self.tcp_client:
            action_request = LilyProtocol.action_request(action=action,value=value);
            if self.tcp_client.send(request='action',param=action_request):
                res, rtype, length, data = self.tcp_client.receive(receive_size)




    def step(self):
        return 2