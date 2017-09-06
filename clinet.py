import socket
import sys
import array
import six
import struct
import json
import numpy as np
import scipy.misc


HOST, PORT = "127.0.0.1", 8885
data = "hello lily ".join(sys.argv[1:]) + "end"

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    received = sock.recv(1024)
    print "received :",len(received), '---',received[5:]

    while True:
        input = raw_input('Enter your input:')

        request = {'request': input,'param1':1,'param2':2.4,'param3':'hello lily'}
        request = json.dumps(request)

        data_pack = struct.pack('I{0}s'.format(len(request)), len(request), request)

        sock.sendall(data_pack)

        # Receive data from the server and shut down
        received = sock.recv(1024*10000)
        stype,  = struct.unpack('?',received[0])
        length,  = struct.unpack('i',received[1:5])
        data = struct.unpack('{0}B'.format(length),received[5:])

        data = np.asarray(data).reshape([384*2,512*2,3])
        data = np.flip(data,0)

        scipy.misc.imsave('frame.bmp', data)

        print "received :", len(received), stype, length, len(data), type(data)
        print "data: ", data[:10]

finally:
    sock.close()

print "Sent:     {}".format(data)
print "Received: {}".format(received)
