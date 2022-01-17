import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def generate_binary_mask(img, threshold=80):
    mask = np.where(img > threshold, 1, 0)
    return mask


def photometric_stereo(I, mask, L):
    """
    Parameters:
    I - intensities matrix (M x h x W)
    mask - matrix of the active pixels (M x h x W)
    L - direction if the light source (3 x 20)
    Returns [p, q]
    """
    # reshape I and mask
    m, h, w = I.shape
    n = h * w
    I = np.reshape(I, (n, m))
    mask = np.reshape(mask, (n, m))
    normal = np.zeros((3, n))
    for i in range(n):
        indices = np.where(mask[i] > 0)[0]
        if len(indices) < 3:
            pass
        else:
            # get unique intensities for ith pixel under more than 3 incident light sources
            Ii = I[i, indices].reshape(-1, 1)  # ith pixel for K number of light directions
            unique_pixels, unique_ind = np.unique(Ii[:, 0], return_index=True)
            # print(unique_ind)
            # print(unique_pixels)
            # get these sources illuminating the ith pixel
            Li = L[:, unique_ind]  # Li (3 x K)
            # solve by least squares fitting
            res = (np.linalg.pinv(Li.T)).dot(unique_pixels)
            albedo = np.linalg.norm(res)
            # normalize the result
            normal[:, i] = res / albedo

    normal = np.reshape(normal, (3, w, h))
    a = normal[0, :, :]
    b = normal[1, :, :]
    c = normal[2, :, :]
    p = np.where(c != 0, -a / c, 0)
    q = np.where(c != 0, -b / c, 0)

    return p, q


def plot_normal_map(normal=None, height=None, width=None):
    """
    Parameters:
    normal - array of surface normal (width x height x 3)
    height - height of the image
    width - width of the image
    """
    if normal is None:
        raise ValueError("Surface normal `normal` is None")
    N = np.reshape(normal, (height, width, 3))  # reshape to image coordinates
    N = cv2.cvtColor(N.astype('float32'), cv2.COLOR_BGR2RGB)
    N = (N + 1.0) / 2.0  # rescale
    name = 'normal map'
    cv2.imshow(name, N)
    cv2.waitKey(0)
    cv2.destroyWindow(name)


def plot_surface(depth, normals):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X, Y, _ = np.meshgrid(np.arange(0, np.shape(normals)[0]),
                          np.arange(0, np.shape(normals)[1]),
                          np.arange(1))
    X = X[..., 0]
    Y = Y[..., 0]
    H = np.real(depth)
    ax.plot_surface(X, Y, H.T)
    plt.show()



