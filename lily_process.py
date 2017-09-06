import sys
import subprocess
import time
from lily_tcpcient import LilyTcpClient
from lily_controller import LilyController
from lily_config import *


class LilyProcess(object):

    def __init__(self,**kwargs):
        self._proc = None
        self._tcp_client = None
        self._controller = None
        self._start(**kwargs)

    def _start(self,**kwargs):
        try:
            #if self.launch(**kwargs):
            if self.connect(**kwargs):
                self.set_controller()
        except Exception,e:
            logging.error("[Lily Error][LilyProcess][__init__]".join(e))
            self.shutdown()

    @property
    def controller(self):
        return self._controller

    def launch(self, **kwargs):
        assert 'args' in kwargs
        try:
            self._proc = subprocess.Popen(kwargs['args'])
            return True
        except OSError:
            self.close()
            sys.exit("Failed to load process")

        return False

    def connect(self,**kwargs):
        self._tcp_client = LilyTcpClient(**kwargs)
        self._tcp_client.connect()
        return True

    def set_controller(self):
        self._controller = LilyController(self._tcp_client)
        return True

    def close(self):
        self._shutdown_proc()
        self._proc = None

    def shutdown(self):
        self._shutdown_socket()
        self._shutdown_proc()

    def _shutdown_socket(self):
        if self._tcp_client:
            self._tcp_client.shutdown()

    def _shutdown_proc(self):
        if self._proc:
            freq = 10
            timeout = 5
            for _ in range(1 + freq * timeout):
                ret = self._proc.poll()
                if ret is not None:
                    return ret
                time.sleep(1.0 / freq)
            for attemp in range(timeout):
                self._proc.terminate()
                for _ in range(1 + freq * timeout):
                    ret = self._proc.poll()
                    if ret is not None:
                        return ret
                    time.sleep(1.0 / freq)
            self._proc.kill()

