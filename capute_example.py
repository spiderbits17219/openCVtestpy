
# Simple python script to capture images from a webcam
#       QR Codes
#       Simple color thresholding

import os
import cv2
import numpy as np

import image_processing as ip
def nothing(x):
    pass



cv2.namedWindow('image')
        
        # create trackbars for color change
cv2.createTrackbar('lowH','image',0,179,nothing)
cv2.createTrackbar('highH','image',179,179,nothing)
    
cv2.createTrackbar('lowS','image',0,255,nothing)
cv2.createTrackbar('highS','image',255,255,nothing)
    
cv2.createTrackbar('lowV','image',0,255,nothing)
cv2.createTrackbar('highV','image',255,255,nothing)
    
    
        # get current positions of the trackbars


DO_QR_CODE_DETECTOR = False
DO_COLOR_DETECTOR = True
DO_ENABLE_SAVE_FRAMES = True
DO_FIND_SQUARE = True


CAM_NUM = 0

def nothing(x):
    pass

def on_mouse_click (event, x, y, flags, frame):
    if event == cv2.EVENT_LBUTTONUP:
        colors.append(frame[y,x].tolist())

# Instructions
if DO_ENABLE_SAVE_FRAMES:
    print('Press spacebar to save frame to disk')
    img_counter  = 0
    
if DO_FIND_SQUARE:
    print('SQUARE!!!')

if DO_QR_CODE_DETECTOR:
    print('Show the camera a QR code')


if DO_COLOR_DETECTOR:
    print('Press number keys to change color space')
    
    COLOR_INDEX = 1
    COLOR_MODE = ip.COLOR_LIST[COLOR_INDEX]
    colors = []
    MIN_CLICKS = 10

    print('{} mouse clicks on upper left image will create '.format(MIN_CLICKS))

if CAM_NUM < 0:
    CAM_NUM = ip.findCamera()

    if len(CAM_NUM) <  1:
        print("Error: Unable to find capture device")
        exit()

    # Assume first device
    CAM_NUM = CAM_NUM[0]

cam = cv2.VideoCapture(CAM_NUM)

if not cam.read()[0]:
    print('Capture Failed')
else:
    print('Capture Not failed')


while True:
    ilowH = cv2.getTrackbarPos('lowH', 'image')
    ihighH = cv2.getTrackbarPos('highH', 'image')
    ilowS = cv2.getTrackbarPos('lowS', 'image')
    ihighS = cv2.getTrackbarPos('highS', 'image')
    ilowV = cv2.getTrackbarPos('lowV', 'image')
    ihighV = cv2.getTrackbarPos('highV', 'image')
    ret, raw = cam.read()
    output = raw
    if not ret:
        print("failed to grab frame")
        break

    if DO_QR_CODE_DETECTOR:
        ip.findQRCodes(raw, output)

        cv2.imshow("test", output)

    if DO_FIND_SQUARE:
        #findSquare(raw, output)

        # Create a window

            
            # convert color to hsv because it is easy to track colors in this color model
        hsv = cv2.cvtColor(raw, cv2.COLOR_BGR2HSV)
        lower_hsv = np.array([ilowH, ilowS, ilowV])
        higher_hsv = np.array([ihighH, ihighS, ihighV])
            # Apply the cv2.inrange method to create a mask
        thresh = cv2.inRange(hsv, lower_hsv, higher_hsv)
        print(lower_hsv)
        print(higher_hsv)

       # hsv = cv2.cvtColor(raw, cv2.COLOR_BGR2HSV)

        # create a binary thresholded image on hue between red and yellow
       #lower = (90,20,10)
       # upper = (255,115,100)
       # thresh = cv2.inRange(hsv, lower, upper)

        # apply morphology
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))
        clean = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15,15))
        clean = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        # get external contours
        contours = cv2.findContours(clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]

        for c in contours:
            # get rotated rectangle from contour
            rot_rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rot_rect)
            box = np.int0(box)
            # draw rotated rectangle on copy of img
            cv2.drawContours(output,[box],0,(0,0,0),2)

            cv2.imshow("test", output)

    if DO_COLOR_DETECTOR:

        # Convert image to selected color space
        new = cv2.cvtColor(raw, COLOR_MODE["CV"])

        if len(colors) > MIN_CLICKS:

            m = np.mean(np.array(colors),0)
            s = np.std(np.array(colors),0)

            n = 3
            low = (m - n*s)
            high = (m + n*s)

            # Threshold image
            bw = cv2.inRange(new, low, high)

            # 
            kernel = np.ones((9,9),np.uint8)
            bw00 = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel)
            bw01 = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)
            bw11 = cv2.morphologyEx(bw, cv2.MORPH_ERODE, kernel)
            bw10 = cv2.morphologyEx(bw, cv2.MORPH_DILATE, kernel)

            disp_bw =  cv2.vconcat([cv2.hconcat([bw00, bw01]),  cv2.hconcat([bw10, bw11])])
            

            aspect_ratio = disp_bw.shape[0]/disp_bw.shape[1]
            max_width = 800
            new_size = (max_width, int(max_width*aspect_ratio))

            disp_img_new = cv2.resize(disp_img, new_size, interpolation=cv2.INTER_NEAREST)
            cv2.imshow('bw',disp_img_new)

        #else:
            #if cv2.getWindowProperty("bw", 0) >= 0:
            #    cv2.destroyWindow("bw")


        
        # Make a panel of the images to show color channels
        disp_img_rgb =  cv2.hconcat([ip.makeLabeledDisplayImage(raw.copy(), "BGR"),   
                                     ip.makeLabeledDisplayImage(raw[:,:,0], "Blue "  + ip.formatMinMaxString(raw[:,:,0])),
                                     ip.makeLabeledDisplayImage(raw[:,:,1], "Green " + ip.formatMinMaxString(raw[:,:,1])),
                                     ip.makeLabeledDisplayImage(raw[:,:,2], "Red "   + ip.formatMinMaxString(raw[:,:,2]))])
                                                            
        
        

        disp_img_new =  cv2.hconcat([ip.makeLabeledDisplayImage(new.copy(), COLOR_MODE["Name"]),   
                                     ip.makeLabeledDisplayImage(new[:,:,0], COLOR_MODE["C"][0] + " " + ip.formatMinMaxString(new[:,:,0])),
                                     ip.makeLabeledDisplayImage(new[:,:,1], COLOR_MODE["C"][1] + " " + ip.formatMinMaxString(new[:,:,1])),
                                     ip.makeLabeledDisplayImage(new[:,:,2], COLOR_MODE["C"][2] + " " + ip.formatMinMaxString(new[:,:,2]))])

        
        disp_img = cv2.vconcat([disp_img_rgb, disp_img_new])

        aspect_ratio = disp_img.shape[0]/disp_img.shape[1]
        max_width = 1200
        new_size = (max_width, int(max_width*aspect_ratio))

        disp_img_new = cv2.resize(disp_img, new_size, interpolation=cv2.INTER_NEAREST)
        cv2.imshow('Color Panels', disp_img_new)

        cv2.setMouseCallback('Color Panels', on_mouse_click, disp_img_new)


    # Keyboard callbacks
    k = cv2.waitKey(1)
    
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

    elif k%256 == 32 and DO_ENABLE_SAVE_FRAMES:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, raw)
        print("{} written!".format(img_name))
        img_counter += 1
    
    elif DO_COLOR_DETECTOR:
        idx = k-48
        if idx > 0  and idx <= len(ip.COLOR_LIST):
            colors.clear()
            COLOR_INDEX = idx - 1
            COLOR_MODE = ip.COLOR_LIST[COLOR_INDEX]
     






cv2.waitKey(0)
cv2.destroyAllWindows()

print(colors)




cam.release()

