from lily_process import LilyProcess

env = LilyProcess(host='127.0.0.1',port=8885,args=['lily.exe'])
obs = env.controller.get_observation(receive_size=1000000)
print (obs)
