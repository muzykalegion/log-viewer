import csv
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Sample telemetry data
times = np.zeros((0, 1))
data = np.zeros((0, 3))

# Visualize Position Data
fig = plt.figure()

with open('./LOGS/board/07.08.24') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        t, x, y, z = row
        if t.startswith(('s', 't', 'x', 'e')):
            t = t[1:]
            dtime = datetime.strptime(t, '%H:%M:%S.%f')
            ta = np.array([[dtime]])
            times = np.vstack((times, ta))
        xyz = np.array([[x, y, z]])
        data = np.vstack((data, xyz))

# Visualize Gyroscope Data
ax2 = fig.add_subplot(132)
time = np.arange(len(data))
ax2.plot(time, data[:, 0], label='Acc X')
ax2.plot(time, data[:, 1], label='Acc Y')
ax2.plot(time, data[:, 2], label='Acc Z')
ax2.set_title('Gyroscope')
ax2.set_xlabel('Time')
ax2.set_ylabel('Gyro Value')
ax2.legend()

plt.tight_layout()
plt.show()
