import numpy as np
import os
import cv2
import sys
from utils import generate_binary_mask, photometric_stereo, plot_normal_map, plot_surface
from frankoChapello import frankotchellappa
np.set_printoptions(threshold=sys.maxsize)


# read images and create masks
data_dir = './PSData/cat/Objects'
images = []
masks = []
for path in os.listdir(data_dir):
    images.append(cv2.imread(data_dir + '/' + path, cv2.IMREAD_GRAYSCALE))
images = np.asarray(images)  # (20 x 640 x 500)

for image in images:
    masks.append(generate_binary_mask(image))
masks = np.asarray(masks)

# read light sources
sources_path = './PSData/cat/light_directions.txt'
sources = []
with open(sources_path, 'r') as f:
    for line in f.readlines():
        sources.append(list(map(float, line.strip().split("  "))))

sources = np.asarray(sources)
L = np.stack((sources[0], sources[1], sources[2]), axis=0)


def main():
    p, q = photometric_stereo(images, masks, L)
    z = frankotchellappa(p, q)
    # print(z)

    width, height = p.shape
    normal = np.ones((width, height, 3))
    normal[:, :, 0] = p
    normal[:, :, 1] = q
    plot_normal_map(normal, height, width)
    plot_surface(z, normal)


if __name__ == "__main__":
    main()

