import numpy as np
import matplotlib.pyplot as plt

# Define matrices
C = np.array([
    [-1, 0, 0, 0],
    [0, -1, 0, 0],
    [0, 0, -1, 0],
    [0, 0, 0, -1],
    [-1, 1, 0, 0],
    [0, -1, 1, 0],
    [0, 0, -1, 1],
    [-1, 0, 0, 1]
])

Cf = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
])

Q = np.diag([8, 8, 8, 8, 4, 4, 4, 4])

xf = np.array([-40, 40, 40, -40])
yf = np.array([40, 40, -40, -40])
zf = np.array([0, 20, 40, 60])

coord_f = np.column_stack((xf, yf, zf))

# Compute coordinates
D = C.T @ Q @ C
Df = C.T @ Q @ Cf

x = np.linalg.solve(D, -Df @ xf)
y = np.linalg.solve(D, -Df @ yf)
z = np.linalg.solve(D, -Df @ zf)

coord = np.column_stack((x, y, z))

# Combine fixed and computed coordinates
coord_total = np.vstack((coord_f, coord))
C_total = np.hstack((Cf, C))

# Determine connectivity
Conn = []
for row in range(C_total.shape[0]):
    start, end = None, None
    for col in range(C_total.shape[1]):
        if C_total[row, col] == 1:
            start = col
        elif C_total[row, col] == -1:
            end = col
    Conn.append([start, end])
Conn = np.array(Conn)

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(coord_total[:, 0], coord_total[:, 1], coord_total[:, 2])
ax.set_title("Force Density")
ax.grid(True)

for conn in Conn:
    pts = coord_total[conn, :]
    ax.plot(pts[:, 0], pts[:, 1], pts[:, 2])

plt.show()