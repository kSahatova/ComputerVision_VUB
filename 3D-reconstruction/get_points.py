import cv2 as cv

#left_img = cv.imread('C:\\Users\\User\\OneDrive - ITMO UNIVERSITY\\VUB\\CV\\camera_calibration\\inputs\\left.jpg')
#right_img = cv.imread('C:\\Users\\User\\OneDrive - ITMO UNIVERSITY\\VUB\\CV\\camera_calibration\\inputs\\right.jpg')

#xy_left = open('xy_left.txt', 'a')
#xy_right = open('xy_right.txt', 'a')

def get_points(image_path, filename, window):
    image = cv.imread(image_path)
    file = open(filename, 'a')

    def pickup_points(event, x, y, flags, param):
        output = param
        if event == cv.EVENT_LBUTTONDOWN:
            print(x, y)
            output.write(f'{x}  {y} \n')

    cv.namedWindow(window)
    cv.setMouseCallback(window, pickup_points, param=file)

    while True:
        cv.imshow(window, image)
        keyCode = cv.waitKey() & 0xFF
        if keyCode == ord('q'):
            file.close()
            break


if __name__ == '__main__': 
    '''
    lpath = 'C:\\Users\\User\\OneDrive - ITMO UNIVERSITY\\VUB\\CV\\camera_calibration\\3D-reconstruction\\inputs\\left.jpg'
    rpath = 'C:\\Users\\User\\OneDrive - ITMO UNIVERSITY\\VUB\\CV\\camera_calibration\\3D-reconstruction\\inputs\\right.jpg'
    get_points(lpath, 'inputs/xy_left.txt', 'left')
    get_points(rpath, 'inputs/xy_right.txt', 'right')
    '''
    clpath = 'C:\\Users\\User\\OneDrive - ITMO UNIVERSITY\\VUB\\CV\\camera_calibration\\3D-reconstruction\\inputs\\correspondence_left.jpg'
    crpath = 'C:\\Users\\User\\OneDrive - ITMO UNIVERSITY\\VUB\\CV\\camera_calibration\\3D-reconstruction\\inputs\\correspondence_right.jpg'
    #get_points(clpath, 'inputs/corresp_left.txt', 'cor left')
    get_points(crpath, 'inputs/corresp_right.txt', 'cor right')



