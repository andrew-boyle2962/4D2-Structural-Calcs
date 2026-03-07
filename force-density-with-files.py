##### FROM MOODLE PAGE

import os
import numpy as np
import matplotlib.pyplot as plt

compute_x = True#input("Do you want to compute the x coordinates? (y/n): ").strip().lower() == 'y'
compute_y = True#input("Do you want to compute the y coordinates? (y/n): ").strip().lower() == 'y'
compute_z = True#input("Do you want to compute the z coordinates? (y/n): ").strip().lower() == 'y'

def choose_folder():
    folders = sorted([d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.')])
    if not folders:
        return '.'
    for i, f in enumerate(folders): print(f"{i}: {f}")
    s = input(f"Choose folder index (Enter=0): ").strip()
    return folders[int(s)] if s else folders[0]

folder = choose_folder()

C_file  = os.path.join(folder, 'C.csv')
Cf_file = os.path.join(folder, 'Cf.csv')
Q_file  = os.path.join(folder, 'Q.csv')
xf_file = os.path.join(folder, 'xf.csv')
yf_file = os.path.join(folder, 'yf.csv')
zf_file = os.path.join(folder, 'zf.csv')
fx_file = os.path.join(folder, 'fx.csv')
fy_file = os.path.join(folder, 'fy.csv')
fz_file = os.path.join(folder, 'fz.csv')

try:
    C = np.genfromtxt(C_file, delimiter=',', filling_values=0)
except OSError:
    raise FileNotFoundError(f"There is no default value for this, please upload '{C_file}'")
print('C shape, ',C.shape)

try:
    Cf = np.genfromtxt(Cf_file, delimiter=',', filling_values=0)
except OSError:
    raise FileNotFoundError(f"There is no default value for this, please upload '{Cf_file}'")
print('Cf shape, ',Cf.shape)

try:
    Q = np.diag(np.genfromtxt(Q_file, delimiter=',', filling_values=0))
except OSError:
    # If file doesn't exist, set a default value
    print(f"File '{Q_file}' not found. Using the -1 for the force density of all bars.")
    Q = -np.eye(C.shape[0])
print('Q shape, ',Q.shape)

def load_coordinate(filename):
  try:
      return np.genfromtxt(filename, delimiter=',', filling_values=0)
  except OSError:
      print(f"File '{filename}' not found. Using 0 for this coordinate for all nodes.")
      return np.zeros(Cf.shape[1])

xf, yf, zf = np.zeros(Cf.shape[1]), np.zeros(Cf.shape[1]), np.zeros(Cf.shape[1])
if compute_x:
    xf = load_coordinate(xf_file)
if compute_y:
    yf = load_coordinate(yf_file)
if compute_z:
    zf = load_coordinate(zf_file)

coord_f = np.column_stack((xf, yf, zf))
print('Coord_f ', coord_f)

def load_force(filename):
  try:
      return np.genfromtxt(filename, delimiter=',', filling_values=0)
  except OSError:
      print(f"File '{filename}' not found. Using 0 for this force for all nodes.")
      return np.zeros(C.shape[1])

fx, fy, fz = np.zeros(C.shape[1]), np.zeros(C.shape[1]), np.zeros(C.shape[1])
if compute_x:
    fx = load_force(fx_file)
if compute_y:
    fy = load_force(fy_file)  
if compute_z:
    fz = load_force(fz_file)

#print('fixed forces ', np.column_stack((fx, fy, fz)))

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

Q_C = Q @ C
Q_Cf = Q@Cf
print('Q_C shape, ',Q_C.shape)
print('Q_Cf shape, ',Q_Cf.shape)

# Compute equilibrium
D = C.T @ Q @ C
Df = C.T @ Q @ Cf

print(D.shape)
print(Df.shape)
print((Df @ xf).shape)
print(fx.shape)

x, y, z = np.zeros(C.shape[1]), np.zeros(C.shape[1]), np.zeros(C.shape[1])
if compute_x:
    x = np.linalg.solve(D, fx - Df @ xf)
if compute_y:
    y = np.linalg.solve(D, fy - Df @ yf)
if compute_z:
    z = np.linalg.solve(D, fz - Df @ zf)

coord = np.column_stack((x, y, z))

print(coord)

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


######### PLOTTING ##########

# 3D
if np.any(coord_total[:, 0]) and np.any(coord_total[:, 1]) and np.any(coord_total[:, 2]):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(coord_total[:, 0], coord_total[:, 1], coord_total[:, 2])
    ax.set_title("Force Density")
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box')

    lengths = []
    for conn in Conn:
        pts = coord_total[conn, :]
        ax.plot(pts[:, 0], pts[:, 1], pts[:, 2])

# X-Z
if np.any(coord_total[:, 0]) and np.any(coord_total[:, 2]):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(coord_total[:, 0], coord_total[:, 2])
    ax.set_title("Force Density")
    ax.set_xlabel('x')
    ax.set_ylabel('z')
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box')


    lengths = []
    for conn in Conn:
        pts = coord_total[conn, :]
        ax.plot(pts[:, 0], pts[:, 2])

        dx = pts[:,0][0] - pts[:,0][1]
        dz = pts[:,2][0] - pts[:,2][1]
        lengths.append(np.sqrt(dx**2 + dz**2))

    print('X-Z LENGTHS')
    for i in lengths:
        print(i)

# X-Y
if np.any(coord_total[:, 0]) and np.any(coord_total[:, 1]):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(coord_total[:, 0], coord_total[:, 1])
    ax.set_title("Force Density")
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box')

    lengths = []
    for conn in Conn:
        pts = coord_total[conn, :]
        ax.plot(pts[:, 1], pts[:, 2])

        dx = pts[:,0][0] - pts[:,0][1]
        dy = pts[:,1][0] - pts[:,1][1]
        lengths.append(np.sqrt(dx**2 + dy**2))

    print('X-Y LENGTHS')
    for i in lengths:
        print(i)

# Y-Z
if np.any(coord_total[:, 1]) and np.any(coord_total[:, 2]):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(coord_total[:, 1], coord_total[:, 2])
    ax.set_title("Force Density")
    ax.set_xlabel('y')
    ax.set_ylabel('z')
    ax.grid(True)
    ax.set_aspect('equal', adjustable='box')

    lengths = []
    for conn in Conn:
        pts = coord_total[conn, :]
        ax.plot(pts[:, 1], pts[:, 2])
    
        dy = pts[:,1][0] - pts[:,1][1]
        dz = pts[:,2][0] - pts[:,2][1]
        lengths.append(np.sqrt(dx**2 + dz**2))

    print('Y-Z LENGTHS')
    for i in lengths:
        print(i)

plt.show()