import cv2 as cv
import numpy as np


def read_points(filename):
    points = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.strip().split()
            if len(line) == 0:
                pass
            else:
                line = list(map(int, line))
                points.append(line)
    points = np.asarray(points)

    return points


def direct_linear_transformation(obj_points, img_points):
    X, Y, Z = obj_points[:, 0], obj_points[:, 1], obj_points[:, 2]
    
    u, v = img_points[:, 0], img_points[:, 1]

    i = 0
    n = len(img_points)
    B = np.zeros((2*n, 12))
    for j in range(0, n):
        #print(X[j], Y[j], Z[j])
        B[i, :] = [X[j], Y[j], Z[j], 1, 0, 0, 0, 0, -u[j]*X[j], -u[j]*Y[j], -u[j]*Z[j], -u[j]]
        B[i+1, :] = [0, 0, 0, 0, X[j], Y[j], Z[j], 1, -v[j]*X[j], -v[j]*Y[j], -v[j]*Z[j], -v[j]]
        i += 2
    #print(B)
    return B


def projection_matrix(B):
    u, s, vh = np.linalg.svd(B, full_matrices=False)
    #print('s\n', s)
    #print('vh\n', vh)
    #v = vh.T
    M = vh[-1, :]
    M = np.reshape(M, (3, 4)) 
    return M


def get_camera_params(M):
    m1 = M[0, :3]
    m2 = M[1, :3]
    m3 = M[2, :3]
    
    r3 = m3
    cx = np.dot(m1, m3)
    cy = np.dot(m2, m3)
    fx = np.linalg.norm(np.cross(m1, m3))
    fy = np.linalg.norm(np.cross(m2, m3))

    r1 = 1 / fx * (m1 - cx * m3)
    r2 = 1 / fy * (m2 - cy * m3)

    tx = 1 / fx * (M[0, 3] - cx * M[2, 3])
    ty = 1 / fy * (M[1, 3] - cx * M[2, 3])
    tz = M[2, 3]

    # extrinsic parameters of the camera
    R = np.array([[*r1], [*r2], [*r3]])
    T = np.array([[tx], [ty], [tz]])

    # intrinsic parameters of the camera
    C = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
    P = np.hstack((np.eye(3), np.zeros((3, 1))))
    K = np.dot(C, P)

    return [K, R, T]


def draw_axes(img, M, axis_len, origin3D):
    origin3D_h = np.array([*origin3D, 1])
    xaxis3D_h = np.array([axis_len, 0, 0, 1])
    yaxis3D_h = np.array([0, axis_len, 0, 1])
    zaxis3D_h = np.array([0, 0, axis_len, 1])

    origin2D_h = M.dot(origin3D_h.T)
    xaxis2D_h = M.dot(xaxis3D_h.T)
    yaxis2D_h = M.dot(yaxis3D_h.T)
    zaxis2D_h = M.dot(zaxis3D_h.T)

    origin2D = tuple(map( int, origin2D_h[:2]/origin2D_h[2]))
    xaxis2D = tuple(map( int, xaxis2D_h[:2]/xaxis2D_h[2]))
    yaxis2D = tuple(map( int, yaxis2D_h[:2]/yaxis2D_h[2]))
    zaxis2D = tuple(map( int, zaxis2D_h[:2]/zaxis2D_h[2]))

    print('origin of the image', origin2D)
    print('point for X axis', xaxis2D)
    print('point for Y axis',yaxis2D)
    print('point for Z axis',zaxis2D)

    img = cv.line(img, origin2D, xaxis2D, color=(255, 0, 0), thickness=3)
    img = cv.line(img, origin2D, yaxis2D, color=(0, 255, 0), thickness=3)
    img = cv.line(img, origin2D, zaxis2D, color=(0, 0, 255), thickness=3)

    return img


