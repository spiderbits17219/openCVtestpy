
import cv2
import numpy as np


COLOR_LIST = []
COLOR_LIST.append({'CV':cv2.COLOR_BGR2HSV,      'Name':"HSV",      'C': ("H", "S", "V")})
COLOR_LIST.append({'CV':cv2.COLOR_BGR2HSV_FULL, 'Name':"HSV_FULL", 'C': ("H", "S", "V")})
COLOR_LIST.append({'CV':cv2.COLOR_BGR2HLS,      'Name':"HLS",      'C': ("H", "L", "S")})

# Y: brightness (luma), Cr: red,  Cb: b
COLOR_LIST.append({'CV':cv2.COLOR_BGR2YCrCb,    'Name':"YCrCb",    'C': ("Y", "Cr", "Cb")})
# L: lightness   a,b: chromaticity
COLOR_LIST.append({'CV':cv2.COLOR_BGR2Lab,      'Name':"Lab",      'C': ("L", "a", "b")})
# L: lightness   u,v: chromaticity  
COLOR_LIST.append({'CV':cv2.COLOR_BGR2Luv,      'Name':"Luv",      'C': ("L", "u", "v")})
COLOR_LIST.append({'CV':cv2.COLOR_BGR2RGB,      'Name':"RGB",      'C': ("R", "G", "B")})



def findCamera():
    
    index =  0
    arr = []
    while index < 5:
        
        cap = cv2.VideoCapture(index)
        #cap.set(cv2.CAP_PROP_FOURCC, 'MJPG')
        #cap.set(cv2.CAP_PROP_FPS, 10.0)
        #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 512)
        #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)
        if not cap.read()[0]:
            break
        else:
            print(index)
            arr.append(index)
        cap.release()
        index += 1

    print(len(arr))
    return arr

def findSquare(img,output):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # create a binary thresholded image on hue between red and yellow
    lower = (0,240,160)
    upper = (30,255,255)
    thresh = cv2.inRange(hsv, lower, upper)

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
        cv2.drawContours(img,[box],0,(0,0,0),2)


def drawPolygon(img, bbox):
    print("drawPolygon not implemented")

def  findQRCodes(img, output):
    # Convert to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #print( str(np.amin(gray)) + ' ' + str(np.amax(gray)) )

    # Threshold image
    ret,thresh = cv2.threshold(gray,127,255,1)

    #print( str(np.amin(thresh)) + ' ' + str(np.amax(thresh)) )

    qrDecoder = cv2.QRCodeDetector()
    data,bbox,rectifiedImage = qrDecoder.detectAndDecode(img)

    rimg = rectifiedImage

    if len(data)>0:
        print("Decoded Data : {}".format(data))
        #display(inputImage, bbox)
        n = len(bbox)
        for b in bbox:
            for n in range(len(b)):
                if n == len(b)-1:
                    pt1 = b[n]
                    pt2 = b[0]
                else:
                    pt1 = b[n]
                    pt2 = b[n+1]
                # convert the arrays to integer and tuple..
                pt1 = tuple(np.round(pt1).astype(int).reshape(1, -1)[0])
                pt2 = tuple(np.round(pt2).astype(int).reshape(1, -1)[0])
                cv2.line(output, pt1, pt2, (255, 0, 0), 3)

        rimg = cv2.resize(rimg, (256, 256), interpolation=cv2.INTER_AREA)
        cv2.imshow("QR Code", rimg)



def formatMinMaxString(img):
    return "({:03}, {:03})".format(np.amin(img), np.amax(img))
    
def makeLabeledDisplayImage(img, text):
    
    if len(img.shape) == 2:
        img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)

    font_color = (10, 200, 200)
    font_thickness = 3
    font_scale = 3
    font_face = cv2.FONT_HERSHEY_PLAIN 
    font_pos = (40, 40)

    cv2.putText(img,text, font_pos, font_face, font_scale, font_color, font_thickness)

    return img