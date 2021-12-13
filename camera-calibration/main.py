import numpy as np
import cv2 as cv
from utils import read_points, direct_linear_transformation, projection_matrix, get_camera_params
from utils import draw_axes


class Image:
    def __init__(self, image_path, corresp_points):
        self.path = image_path
        self.corresp_points = corresp_points


left_img_path = 'camera_calibration/camera-calibration/inputs/left.jpg'
right_img_path = 'camera_calibration/camera-calibration/inputs/right.jpg'

xy_left = read_points('camera_calibration/camera-calibration/xy_left.txt')
xy_right = read_points('camera_calibration/camera-calibration/xy_right.txt')
obj_points = read_points('camera_calibration/camera-calibration/inputs/calibration_points3.txt')


images = [Image(left_img_path, xy_left), Image(right_img_path, xy_right)]
for image in images:
    image.B = direct_linear_transformation(obj_points, image.corresp_points)
    image.M = projection_matrix(image.B)
    image.C, image.R, image.T = get_camera_params(image.M)
    
    image.img = cv.imread(image.path)
    

images[0].img_with_axes = draw_axes(images[0].img, images[0].M, 200, (0, 0, 0))
images[1].img_with_axes = draw_axes(images[1].img, images[1].M, 200, (0, 0, 0))

cv.imwrite('camera_calibration/left_with_axs.jpg', images[0].img_with_axes)
cv.imwrite('camera_calibration/right_with_axs.jpg', images[1].img_with_axes)

while 1:

    cv.imshow('left image', images[0].img_with_axes)
    cv.imshow('right image', images[1].img_with_axes)

    keyCode = cv.waitKey() & 0xFF
    if keyCode == ord('q'):
        break