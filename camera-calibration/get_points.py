import cv2 as cv

left_img = cv.imread('C:\\Users\\User\\OneDrive - ITMO UNIVERSITY\\VUB\\CV\\camera_calibration\\inputs\\left.jpg')
right_img = cv.imread('C:\\Users\\User\\OneDrive - ITMO UNIVERSITY\\VUB\\CV\\camera_calibration\\inputs\\right.jpg')

xy_left = open('xy_left.txt', 'a')
xy_right = open('xy_right.txt', 'a')


def get_points(event, x, y, flags, param):
    output = param
    if event == cv.EVENT_LBUTTONDOWN:
        print(x, y)
        output.write(f'{x}  {y} \n')

cv.namedWindow('left image')
cv.namedWindow('right image')

cv.setMouseCallback('left image', get_points, param=xy_left)
cv.setMouseCallback('right image', get_points, param=xy_right)

while (True):
    cv.imshow('left image', left_img)
    cv.imshow('right image', right_img)
    keyCode = cv.waitKey() & 0xFF
    if keyCode == ord('q'):
        xy_left.close()
        xy_right.close()
        break