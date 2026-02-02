##### FROM MOODLE PAGE

import numpy as np
import matplotlib.pyplot as plt

compute_x = input("Do you want to compute the x coordinates? (y/n): ").strip().lower() == 'y'
compute_y = input("Do you want to compute the y coordinates? (y/n): ").strip().lower() == 'y'
compute_z = input("Do you want to compute the z coordinates? (y/n): ").strip().lower() == 'y'

C_file = 'C.csv'

try:
    C = np.loadtxt('C.csv', delimiter=',')
except OSError:
    raise FileNotFoundError(f"There is no default value for this, please upload '{C_file}'")
print(C)

Cf_file = 'Cf.csv'

try:
    Cf = np.loadtxt('Cf.csv', delimiter=',')
except OSError:
    raise FileNotFoundError(f"There is no default value for this, please upload '{Cf_file}'")
print(Cf)


Q_file = 'Q.csv'

try:
    Q = np.diag(np.loadtxt(Q_file, delimiter=','))
except OSError:
    # If file doesn't exist, set a default value
    print(f"File '{Q_file}' not found. Using the -1 for the force density of all bars.")
    Q = -np.eye(C.shape[0])

print(Q)


def load_coordinate(filename):
  try:
      return np.loadtxt(filename, delimiter=',')
  except OSError:
      print(f"File '{filename}' not found. Using 0 for this coordinate for all nodes.")
      return np.zeros(Cf.shape[1])

xf, yf, zf = np.zeros(Cf.shape[1]), np.zeros(Cf.shape[1]), np.zeros(Cf.shape[1])
if compute_x:
    xf = load_coordinate('xf.csv')
if compute_y:
    yf = load_coordinate('yf.csv')
if compute_z:
    zf = load_coordinate('zf.csv')

coord_f = np.column_stack((xf, yf, zf))
print(coord_f)


def load_force(filename):
  try:
      return np.loadtxt(filename, delimiter=',')
  except OSError:
      print(f"File '{filename}' not found. Using 0 for this force for all nodes.")
      return np.zeros(C.shape[1])

fx, fy, fz = np.zeros(C.shape[1]), np.zeros(C.shape[1]), np.zeros(C.shape[1])
if compute_x:
    fx = load_force('fx.csv')
if compute_y:
    fy = load_force('fy.csv')  
if compute_z:
    fz = load_force('fz.csv')

print(np.column_stack((fx, fy, fz)))

#known nodes
if C.shape[1] == len(fx) == len(fy) == len(fz):
  print("There are "+ str(C.shape[1])+" known nodes")
else:
  print(C.shape[1], len(xf), len(yf), len(zf))

#unknown nodes
if Cf.shape[1] == len(xf) == len(yf) == len(zf):
  print("There are "+ str(Cf.shape[1])+" unknown nodes")
else:
  print(Cf.shape[1], len(fx), len(fy), len(fz))

#bars
if C.shape[0] == Cf.shape[0] == Q.shape[0] == Q.shape[1]:
  print("There are "+ str(C.shape[0])+" bars")
else:
  print(C.shape[0], Cf.shape[0], Q.shape[0], Q.shape[1])


# Compute equilibrium
D = C.T @ Q @ C
Df = C.T @ Q @ Cf

x, y, z = np.zeros(C.shape[1]), np.zeros(C.shape[1]), np.zeros(C.shape[1])
if compute_x:
    x = np.linalg.solve(D, fx - Df @ xf)
if compute_y:
    y = np.linalg.solve(D, fy - Df @ yf)
if compute_z:
    z = np.linalg.solve(D, fz - Df @ zf)

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