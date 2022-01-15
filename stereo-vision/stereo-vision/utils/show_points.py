import numpy as np
from utils import read_points
from camera_calibration import Image
import cv2

lpath =  'inputs/left.jpg'
rpath =  'inputs/right.jpg'
limg = cv2.imread(lpath)
rimg = cv2.imread(rpath)

lpoints = read_points('outputs/all_points_left.txt')
print(lpoints)
rpoints = read_points('outputs/all_points_right.txt')
obj_points = read_points('inputs/calibration_points3.txt')

# Return two image objects with calculated camera parameters and corresponding points

for point in rpoints:
    rimg = cv2.circle(rimg, (point[:]), radius=0, color=(0, 255, 0), thickness=5)
#cv2.imwrite('r.jpg', img)

for point in lpoints:
    limg = cv2.circle(limg, (point[:]), radius=0, color=(0, 255, 0), thickness=5)
#cv2.imwrite('l.jpg', img)

while(1):
    cv2.imshow('right image', rimg)
    cv2.imshow('left image', limg)

    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break


