import cv2
import numpy as np

capture = cv2.VideoCapture(0)
capture.set(3, 640)
capture.set(4, 480)

while True:
    _, screen = capture.read()

    colorHSV = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)

    # H[0,179], S[0,255], V[0,255]
    lowerBlue = np.array([90, 50, 10])
    upperBlue = np.array([130, 255, 255])
    maskBlueFilter = cv2.inRange(colorHSV, lowerBlue, upperBlue)

    lowerRed = np.array([0, 50, 50])
    upperRed = np.array([10, 255, 255])
    maskRedFilterZero = cv2.inRange(colorHSV, lowerRed, upperRed)

    lowerRed = np.array([170, 50, 50])
    upperRed = np.array([180, 255, 255])
    maskRedFilterOne = cv2.inRange(colorHSV, lowerRed, upperRed)
    maskRedFilter = maskRedFilterZero + maskRedFilterOne

    grayscale = screen.copy()
    grayscale = cv2.cvtColor(grayscale, cv2.COLOR_BGR2GRAY)

    resolutionBlue = cv2.bitwise_and(screen, screen, mask=maskBlueFilter)
    resolutionRed = cv2.bitwise_and(screen, screen, mask=maskRedFilter)

    cv2.imshow('Original Frame', screen)
    cv2.imshow('Original to Grayscale', grayscale)
    cv2.imshow('Original to Blue Filter', resolutionBlue)
    cv2.imshow('Original to Red Filter', resolutionRed)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()