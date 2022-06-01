import cvzone
from cv2 import VideoCapture
from cvzone.ColorModule import ColorFinder
import cv2
import serial



cap = cv2.VideoCapture('/dev/video0')

cap.set(3,1280)
cap.set(4,720)

success, img = cap.read()
print(img.shape)
h,w,_ = img.shape

ArduinoSerial=serial.Serial('/dev/ttyACM0',9600,timeout=0.1)

myColorFinder = ColorFinder(False)
hsvVals = {'hmin': 47, 'smin': 58, 'vmin': 166, 'hmax': 71, 'smax': 217, 'vmax': 255}

while True:
    success, img = cap.read()
    # print(img.shape)
    imgColor, mask = myColorFinder.update(img, hsvVals)
    imgContour, contours = cvzone.findContours(img, mask)

    txxt = []
    if contours:
        data = contours[0]['center'][0], \
               contours[0]['center'][1], \
               int(contours[0]['area'])
        print(data)

        (x, y, a) = data
        print(x)

        xx = x
        if xx > 590:
            xx += 300
        elif xx < 590:
            xx -= 300

        string = 'X{0:d}'.format(int(xx))
        print(string)
        ArduinoSerial.write(string.encode('utf-8'))
        # plot the center of the face

        txt = (x,y)

        text = cv2.putText(img, '({0:d},{1:d})'.format(x,y), txt, cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3, lineType=cv2.LINE_AA)
        text2 = cv2.putText(imgContour, '({0:d},{1:d})'.format(x,y), txt, cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

    # imgStack = cvzone.stackImages([img,imgColor],2,0.5)
    line = cv2.line(img, (0,h//2), (w,h//2),(0,255,0),2)
    line2 = cv2.line(img, (w//2,0), (w//2,h),(0,255,0),2)

    imgStack = cvzone.stackImages([img,imgColor, mask, imgContour],2,0.5)
    imS = cv2.resize(imgStack, (1800, 900))
    # imS = cv2.resize(imgStack, (1000, 500))
    cv2.imshow('imgColor', imS)
    cv2.waitKey(1)

