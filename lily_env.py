from lily_process import LilyProcess
from lily_config import *
import scipy.misc
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import random


def get_config():
    with open('config.yaml') as f:
        # use safe_load instead load
        config = yaml.safe_load(f)

        return config

def main():

    config = get_config()

    host = config['tcp']['ip']
    port = config['tcp']['port']

    env = LilyProcess(host=host, port=port, args=['lily.exe'],config=config)
    obs = env.controller.get_observation(receive_size=1000000)
    obs = np.flip(obs,axis=0)

    #imgplot = plt.imshow(obs)
    #plt.show()
    time.sleep(2)

    while True:
        action = [random.randint(0, 1)]+[random.uniform(-1,1) for i in range(4)]
        reward, state = env.controller.act(action= action)
        state = np.flip(state, axis=0)
        #plt.imshow(state)
        #plt.show()
        #time.sleep(2)

    #time.sleep(2)
    #obs = env.controller.get_observation(receive_size=100000)

if __name__ == '__main__':
    main()

