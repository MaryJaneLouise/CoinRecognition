import imutils
import cv2
import os
import numpy as np
from picamera2 import Picamera2

piCam = Picamera2()
piCam.preview_configuration.main.size=(640,480)
piCam.preview_configuration.main.format="RGB888"
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

while True:
    screen = piCam.capture_array()
    screenImage = screen.copy()
    image = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    image = cv2.bilateralFilter(image, 11, 17, 17)

    _, threshold = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY)
    threshold = cv2.bitwise_not(threshold)
    threshold = cv2.medianBlur(threshold, 7)

    imageEdge = cv2.Canny(threshold, 3, 180)
    imageContour = cv2.findContours(imageEdge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    imageContourLength = 0

    for each in range(len(imageContour)):
        if cv2.contourArea(imageContour[each]) > 1000:
            screenImage = cv2.drawContours(screenImage, imageContour, each, (255, 0, 0), 3)
            imageContourLength += 1
    imageTextSample = "Total number of coins: "
    imageText = screenImage.copy()
    imageText = cv2.putText(screenImage, imageTextSample + str(imageContourLength),
                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0))

    cv2.imshow('Coin Detection', imutils.resize(imageText, width=800))

    keypress = cv2.waitKey(5) & 0xFF
    if keypress == 27:
        break

cv2.destroyAllWindows()