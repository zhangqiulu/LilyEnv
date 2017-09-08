from lily_process import LilyProcess
import time

#env = LilyProcess(host='192.168.37.1',port=8885,args=['lily.exe'])
env = LilyProcess(host='10.24.77.34',port=8885 ,args=['lily.exe'])
obs = env.controller.get_observation(receive_size=100000)

time.sleep(2)
obs = env.controller.get_observation(receive_size=100000)