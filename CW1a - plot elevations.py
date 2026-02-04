import numpy as np
from matplotlib import pyplot as plt

x = [4, 8, 12, 16, 20, 216/11, 160/11, 72/11, 40/11]
xf = [0, 24, 96/11]
y = [1.43, 2.459, 3.105, 3.356, 3.112, 2.198, 0.387, -0.429, 0.608]
yf = [0, 24/11, -32/11]
z = [0, 0, 0, 0, 0, 12/11, 48/11, 48/11, 12/11]
zf = [0, 0, 108/11]

coord_f = np.column_stack((xf, yf, zf))
coord_free = np.column_stack((x, y, z))
coord_total = np.vstack((coord_f, coord_free))

print(coord_f)
print(coord_free)
print(coord_total)

#z=np.zeros((12, 1))



#coord_total = np.column_stack((x, y, z))


C =    [[0,0,0,0,0,0,0,0,-1],
        [-1,0,0,0,0,0,0,0,0],
        [-1,0,0,0,0,0,0,0,1],
        [0,0,0,0,0,0,0,-1,1],
        [-1,1,0,0,0,0,0,0,0],
        [0,-1,0,0,0,0,0,1,0],
        [0,0,0,0,0,0,0,-1,0],
        [0,-1,1,0,0,0,0,0,0],
        [0,0,-1,0,0,0,0,0,0],
        [0,0,0,0,0,0,-1,0,0],
        [0,0,-1,1,0,0,0,0,0],
        [0,0,0,-1,0,0,1,0,0],
        [0,0,0,0,0,-1,1,0,0],
        [0,0,0,-1,1,0,0,0,0],
        [0,0,0,0,-1,1,0,0,0],
        [0,0,0,0,0,-1,0,0,0],
        [0,0,0,0,-1,0,0,0,0]]

Cf =   [[1,0,0],
        [1,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,1],
        [0,0,0],
        [0,0,1],
        [0,0,1],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,0,0],
        [0,1,0],
        [0,1,0]]

# Combine fixed and computed coordinates
# coord_total = np.vstack((coord_f, coord))
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

print(coord_total)

# Plotting
fig_xz = plt.figure()
ax_xz = fig_xz.add_subplot(111)
ax_xz.scatter(coord_total[:, 0], coord_total[:, 2])
ax_xz.set_title("X-Z Form Diagram")
fig_xz.gca().set_aspect('equal', adjustable='box')
ax_xz.grid(True)

for conn in Conn:
    pts = coord_total[conn, :]
    ax_xz.plot(pts[:, 0], pts[:, 2])


fig_xy = plt.figure()
ax_xy = fig_xy.add_subplot(111)
ax_xy.scatter(coord_total[:, 0], coord_total[:, 1])
ax_xy.set_title("X-Y Form Diagram")
fig_xy.gca().set_aspect('equal', adjustable='box')
ax_xy.grid(True)

for conn in Conn:
    pts = coord_total[conn, :]
    ax_xy.plot(pts[:, 0], pts[:, 1])



fig_yz = plt.figure()
ax_yz = fig_yz.add_subplot(111)
ax_yz.scatter(coord_total[:, 1], coord_total[:, 2])
ax_yz.set_title("Y-Z Form Diagram")
fig_yz.gca().set_aspect('equal', adjustable='box')
ax_yz.grid(True)

# Plot Mast
ax_yz.plot([-32/11, 4.274], [108/11, -4], linewidth=4, alpha=0.6, color='gray')

for conn in Conn:
    pts = coord_total[conn, :]
    ax_yz.plot(pts[:, 1], pts[:, 2])





# 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(coord_total[:, 0], coord_total[:, 1], coord_total[:, 2])
ax.set_title("3D Form Diagram")
fig.gca().set_aspect('equal', adjustable='box')
ax.grid(True)

for conn in Conn:
    pts = coord_total[conn, :]
    ax.plot(pts[:, 0], pts[:, 1], pts[:, 2])

# Plot mast with constant x
ax.plot([96/11, 96/11], [-32/11, 4.274], [108/11, -4])
plt.show()