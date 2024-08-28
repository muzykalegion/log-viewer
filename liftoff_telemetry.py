import struct
import socket
import matplotlib.pyplot as plt
import numpy as np

# ---------------   LIFTOFF DRONE TELEMETRY ----------------
#
# see https://steamcommunity.com/sharedfiles/filedetails/?id=3160488434
#
# {
#   "StreamFormat": [
#     "Timestamp", 1 float
#     "Position", 3 floats
#     "Attitude", 4 floats
#     "Gyro", 3 floats
#     "Input", 4 floats
#     "Battery", 2 floats
#     "MotorRPM" 1 byte + (1 float * number of motors)
#   ]
# }  float - a single precision floating point number, 4 bytes long.
#    int - an integral number, 4 bytes long.
#    byte - a single byte.

SFORMAT = 'fffffffffffffff'
BYTES = len(SFORMAT) * 4

UDP_IP = "127.0.0.1"
UDP_PORT = 9001
sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

initX = initY = initZ = None
while True:
    data, addr = sock.recvfrom(BYTES)  # buffer size in bytes
    values = struct.unpack(SFORMAT, data)
    print(values)
    t, pX, pY, pZ, aX, aY, aZ, aW, gX, gY, gZ, i1, i2, i3, i4 = values
    if None in (initX, initY, initZ):
        initX = pX
        initY = pY
        initZ = pZ
    # print(f'Position {pX - initX} {pY - initY} {pZ - initZ}')
    # print(f'Gyro {gX} {gY} {gZ}')
    # print(f'{i1} {i2} {i3} {i4}')





