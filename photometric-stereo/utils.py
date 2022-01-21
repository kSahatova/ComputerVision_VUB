import cv2
import numpy as np
from tqdm import tqdm
from plotly.offline import plot
import plotly.graph_objects as go


def generate_binary_mask(image, threshold=10):
    return np.where(image > threshold, 1, 0)


def photometric_stereo(I, binary_mask, L):
    m, h, w = I.shape
    albedo_map = np.zeros((h, w))
    surf_normals = np.zeros((h, w, 3))

    for i in tqdm(range(h)):
        for j in range(w):
            Ii = I[:, i, j]
            mask = binary_mask[:, i, j]
            filtered_mask_ind = np.where(mask > 0)[0]
            if len(filtered_mask_ind) >= 3:
                unique_pixels, unique_ind = np.unique(Ii[filtered_mask_ind], return_index=True)
                Li = L[:, unique_ind]  # 3 x K
                unique_pixels = unique_pixels.reshape(-1, 1)  # I - 1 x K -> K x 1
                LiT = Li.T  # K x 3
                res = (np.linalg.inv(Li.dot(LiT))).dot(Li)
                res = res.dot(unique_pixels)
                albedo = np.linalg.norm(res)
                albedo_map[i, j] = albedo
                surf_normals[i, j, :] = res[:, 0] / albedo

    a, b, c = surf_normals[:, :, 0], surf_normals[:, :, 1], surf_normals[:, :, 2]
    p = np.where(c > 0, -a/c, 0)
    q = np.where(c > 0, -b/c, 0)
    return p, q, albedo_map


def plot_normal_map(normal=None, albedo_map=None, winname=None):
    N = (normal.astype('float32') + 1.0) / 2.0  # rescale
    N *= 255
    cv2.imwrite(winname+'.png', cv2.cvtColor(N, cv2.COLOR_RGB2BGR))  # cv2.cvtColor(N, cv2.COLOR_RGB2BGR)
    cv2.imwrite('outputs/albedo.png', albedo_map.astype('float32'))


def plot_surface3d(z):
    '''z = np.where(z > 20, 10, z)
    z = np.where(z < -50, -20, z)'''
    fig = go.Figure(data=[go.Surface(z=z)])
    fig.update_layout(autosize=False,
                      width=500, height=500,
                      margin=dict(l=65, r=50, b=65, t=90))
    camera = dict(
        up=dict(x=0, y=0, z=1),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=1.25, y=1.25, z=3)
    )
    fig.update_layout(scene_camera=camera)
    fig.write_image("outputs/3D-surface.png")
    plot(fig)