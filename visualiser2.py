from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
import numpy as np

# Sample telemetry data (attitudes as quaternions: [w, x, y, z])
attitudes = np.array([
    [1, 0, 0, 0],
    [0.707, 0, 0.707, 0],
    [0.5, 0.5, 0.5, 0.5],
    [0, 1, 0, 0],
    [-0.5, 0.5, 0.5, -0.5]
])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


def plot_orientation(ax, attitude, length=1.0):
    r = R.from_quat([attitude[1], attitude[2], attitude[3], attitude[0]])  # Order: [x, y, z, w]
    origin = np.array([0, 0, 0])
    x_axis = r.apply([length, 0, 0])
    y_axis = r.apply([0, length, 0])
    z_axis = r.apply([0, 0, length])

    ax.quiver(*origin, *x_axis, color='r', length=length, arrow_length_ratio=0.1)
    ax.quiver(*origin, *y_axis, color='g', length=length, arrow_length_ratio=0.1)
    ax.quiver(*origin, *z_axis, color='b', length=length, arrow_length_ratio=0.1)


for attitude in attitudes:
    plot_orientation(ax, attitude)

ax.set_xlim([-1, 1])
ax.set_ylim([-1, 1])
ax.set_zlim([-1, 1])
ax.set_title('Drone Orientation')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()