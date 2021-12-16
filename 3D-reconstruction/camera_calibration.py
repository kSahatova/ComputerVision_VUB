import os
import numpy as np
import cv2 as cv
from utils import read_points, direct_linear_transformation
from utils import projection_matrix, get_camera_params
from utils import draw_axes


class Image:
    def __init__(self, image_path, corresp_points, obj_points):
        self.path = image_path
        self.corresp_points = corresp_points
        self.obj_points = obj_points
        self.B = direct_linear_transformation(self.obj_points, self.corresp_points)
        self.M = projection_matrix(self.B)
        self.K, self.R, self.T = get_camera_params(self.M)
        self.A =   np.vstack((np.hstack((self.R, self.T)), [0, 0, 0, 1])) 
        self.M_calc = np.dot(self.K, self.A) 
        self.img = cv.imread(self.path)


if __name__ == '__main__':
    #Read corresponding points from both images  
    lpath =  'inputs/left.jpg'
    rpath =  'inputs/right.jpg'

    lpoints = read_points('inputs/xy_left.txt')
    rpoints = read_points('inputs/xy_right.txt')
    obj_points = read_points('inputs/calibration_points3.txt')

    limage = Image(lpath, lpoints, obj_points)
    rimage = Image(rpath, rpoints, obj_points)

    limage.img_with_axes = draw_axes(limage.img, limage.M_calc, 200, (0, 0, 0))
    rimage.img_with_axes = draw_axes(rimage.img, rimage.M_calc, 200, (0, 0, 0))

    cv.imwrite('outputs/left_with_axs.jpg', limage.img_with_axes)
    cv.imwrite('outputs/right_with_axs.jpg', rimage.img_with_axes)

    print(np.allclose(limage.M, limage.M_calc))
    print(np.allclose(rimage.M, rimage.M_calc))



