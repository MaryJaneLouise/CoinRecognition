import imutils
import cv2
import numpy as np

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FPS, 5)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    _, screen = capture.read()

    colorGray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    colorGray = colorGray[0:620, 0:960]

    colorOtsu = cv2.threshold(colorGray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    adaptiveThreshold = cv2.adaptiveThreshold(colorGray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 79, 10)
    adaptiveThreshold = cv2.medianBlur(adaptiveThreshold, 25)

    cv2.imshow('Original background to Grayscale', imutils.resize(colorGray, width=800))
    cv2.imshow('Original background to Adaptive Threshold', imutils.resize(adaptiveThreshold, width=800))

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()