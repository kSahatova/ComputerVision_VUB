import os
import cv2
import numpy as np
from PIL import Image, ImageOps
from code.frankoChapello import frankotchellappa
from utils import generate_binary_mask, photometric_stereo, plot_normal_map, plot_surface3d


IMG_PATH = '../PSData/cat/Objects'
LIGHTS_PATH = '../PSData/cat/light_directions.txt'
MASKS_PATH = '../masks/'

images = []
masks = []
sources = []

# read all 20 images
for path in os.listdir(IMG_PATH):
    img = ImageOps.grayscale(Image.open(IMG_PATH + '/' + path))
    images.append(np.asarray(img))
images = np.asarray(images)  # (10 x 640 x 500)

# generate binary mask for each image
for i in range(images.shape[0]):
    mask = generate_binary_mask(images[i], threshold=10)
    masks.append(mask)
    cv2.imwrite(MASKS_PATH+f'mask{i}.png', mask*255)
masks = np.asarray(masks)

# read all light sources
with open(LIGHTS_PATH, 'r') as f:
    for line in f.readlines():
        sources.append(list(map(float, line.strip().split("  "))))

sources = np.asarray(sources[:10])
L = np.stack((sources[0], sources[1], sources[2]), axis=0)

# calculate p and q components
dx, dy, albedo_map = photometric_stereo(images, masks, L)
h, w = dx.shape
normal_map = np.ones((h, w, 3))
normal_map[:, :, 0] = dx
normal_map[:, :, 1] = dy
# plot normal map
plot_normal_map(normal_map, albedo_map, './outputs/normal_map')

# calculate depth of the object
depth = frankotchellappa(dx, dy)
depth = np.real(depth)

# plot surface
mask = cv2.imread('../masks/mask0.png', cv2.IMREAD_GRAYSCALE)
for i in range(depth.shape[0]):
    for j in range(depth.shape[1]):
        if mask[i, j] == 0:
            depth[i, j] = -60

plot_surface3d(depth)


