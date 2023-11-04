

import cv2
import numpy as np

colors = []

def on_mouse_click (event, x, y, flags, frame):
    if event == cv2.EVENT_LBUTTONUP:
        colors.append(frame[y,x].tolist())

#import apriltag   # pip install apriltag

#filename = "C:/Users/leicham1/Documents/APL/SpiderBits/SpiderByte/easy/qr1.PNG"
#filename = 'C:/Users/leicham1/Documents/APL/SpiderBits/SpiderByte/images/opencv_qr3.png'
filename = 'C:/Users/leicham1/Documents/APL/SpiderBits/SpiderByte/code/opencv-example/opencv_frame_35.png'


# Read image

img = cv2.imread(filename)


hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

cv2.imshow('hsv',hsv)

while True:
    cv2.setMouseCallback('hsv', on_mouse_click, hsv)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


m = np.mean(np.array(colors),0)
s = np.std(np.array(colors),0)


low = (m - 10*s)
high = (m + 10*s)

bw = cv2.inRange(hsv, low, high)

cv2.imshow('bw',bw)

cv2.waitKey(0)
cv2.destroyAllWindows()

print(colors)




# Convert to gray scale
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Find contours
#thresh = 100
#contours,h = cv2.findContours(thresh,1,2)

#print( str(len(contours)))
#approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)

#for cnt in contours:
#    cv2.drawContours(img,[cnt],0,(255,255,0),-1)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()