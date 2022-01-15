from utils import read_points
import cv2

path =  'inputs/right.jpg'
img = cv2.imread(path)

mouseX, mouseY = -1, -1
file = open('outputs/all_points_right.txt', 'w')


def draw_circle(event,x,y,flags,param):
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img,(x,y), 1, (255,0,0), 3)
        mouseX,mouseY = x,y
        file.write(f'{mouseX}   {mouseY}\n')


cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)

while(1):
    cv2.imshow('image', img)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        file.close()
        break
    elif k == ord('a'):
        print (mouseX,mouseY)

