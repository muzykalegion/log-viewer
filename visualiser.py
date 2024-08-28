import csv

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


# Sample telemetry data
# Replace these with your actual data

def quaternion_to_euler_angle_vectorized1(w, x, y, z):
    ysqr = y * y

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + ysqr)
    X = np.degrees(np.arctan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)
    t2 = np.where(t2 > +1.0, +1.0, t2)
    # t2 = +1.0 if t2 > +1.0 else t2

    t2 = np.where(t2 < -1.0, -1.0, t2)
    # t2 = -1.0 if t2 < -1.0 else t2
    Y = np.degrees(np.arcsin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (ysqr + z * z)
    Z = np.degrees(np.arctan2(t3, t4))

    return X, Y, Z


positions = np.zeros((0, 3))
attitudes = np.zeros((0, 3))
gyroscopes = np.zeros((0, 3))

with open('./LOGS/liftoff/1.log') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        t, pX, pY, pZ, aX, aY, aZ, aW, gX, gY, gZ, i1, i2, i3, i4 = row
        position = np.array([[float(pX), float(pY), float(pZ)]])
        positions = np.vstack((positions, position))
        aX, aY, aZ = quaternion_to_euler_angle_vectorized1(float(aW), float(aX), float(aY), float(aZ))
        attitude = np.array([[aX, aY, aZ]])
        attitudes = np.vstack((attitudes, attitude))
        gyro = np.array([[float(gX), float(gY), float(gZ)]])
        gyroscopes = np.vstack((gyroscopes, gyro))
# Visualize Position Data
fig = plt.figure()
ax = fig.add_subplot(131, projection='3d')
ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], marker=',')
ax.set_title('Position')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Visualize Gyroscope Data
ax2 = fig.add_subplot(132,projection='3d')
time = np.arange(len(gyroscopes))
ax2.plot(gyroscopes[:, 0],gyroscopes[:, 1],gyroscopes[:, 2], marker='x')
# ax2.plot(time, gyroscopes[:, 1], label='Gyro Y')
# ax2.plot(time, gyroscopes[:, 2], label='Gyro Z')
ax2.set_title('Gyroscope')
ax2.set_xlabel('Time')
ax2.set_ylabel('Gyro Value')
ax2.legend()

# Visualize Attitude Data as quaternions
ax3 = fig.add_subplot(133, projection='3d')
ax3.plot(attitudes[:, 0], attitudes[:, 1], attitudes[:, 2], marker='.')
# ax3.plot(time, attitudes[:, 1], label='Attitude Y')
# ax3.plot(time, attitudes[:, 2], label='Attitude Z')
ax3.set_title('Attitude')
ax3.set_xlabel('Time')
ax3.set_ylabel('Quaternion Value')
ax3.legend()

plt.tight_layout()
plt.show()
