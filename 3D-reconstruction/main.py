import numpy as np
from helpers.utils import read_points
from helpers.camera_calibration import Image


lpath =  'inputs/left.jpg'
rpath =  'inputs/right.jpg'

lpoints = read_points('inputs/xy_left.txt')
rpoints = read_points('inputs/xy_right.txt')
obj_points = read_points('inputs/calibration_points3.txt')

# Return two image objects with calculated camera parameters and corresponding points
limage = Image(lpath, lpoints, obj_points)
rimage = Image(rpath, rpoints, obj_points)

lpoints18 = read_points('inputs/corresp_left.txt')
rpoints18 = read_points('inputs/corresp_right.txt')

# Concatenate all corresponding points on the left and on the right image
limage.corresp_points = np.vstack((limage.corresp_points, lpoints18))
rimage.corresp_points = np.vstack((rimage.corresp_points, rpoints18))

m1l = limage.M_calc[0]
m2l = limage.M_calc[1]
m3l = limage.M_calc[2]

m1r = rimage.M_calc[0]
m2r = rimage.M_calc[1]
m3r = rimage.M_calc[2]

# Calculate 3D homogeneous coordinates (1x4)
X_h = []
for i in range(len(limage.corresp_points)):
    xl = limage.corresp_points[i, 0]
    yl = limage.corresp_points[i, 1]
    xr = rimage.corresp_points[i, 0]
    yr = rimage.corresp_points[i, 1]

    P = np.zeros((4, 4))
    P[0, :] = xl*m3l - m1l
    P[1, :] = yl*m3l - m2l
    P[2, :]  = xr*m3r - m1r
    P[3, :]  = yr*m3r - m2r

    _, _, vh = np.linalg.svd(P)
    solution = vh[-1, :]
    X_h.append(solution)

X_h = np.asarray(X_h)
estimated_points = X_h[:, :3]/np.expand_dims(X_h[:, 3], axis=1)
#print(estimated_points)

# Mean squared error for 12 given points
mse = (np.square(obj_points - estimated_points[:12, :])).mean()
print(mse)

if 0 < mse < 1:
    with open('outputs/estimated_points3D.txt', 'w') as f:
        for i in range(estimated_points.shape[0]):
            line = list(map(int, estimated_points[i, :]))
            f.write(str(line).replace(',', ' ').strip('[]')+'\n')
else:
    print('MSE is bigger than 1. Solution is incorrect!')



