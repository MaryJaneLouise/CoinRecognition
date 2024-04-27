import imutils
import cv2
import numpy as np

def contour_coin(x):
    pass
capture = cv2.VideoCapture(0)
capture.set(3,240)
capture.set(4,160)

cv2.namedWindow("Adjustable Threshold Value")
cv2.createTrackbar("Threshold Value","Adjustable Threshold Value", 80, 255,  contour_coin)

while True:
    thresholdValue = cv2.getTrackbarPos("Threshold Value", "Adjustable Threshold Value")
    _, screen = capture.read()
    image = screen.copy()
    imageGrayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, imageThreshold = cv2.threshold(imageGrayscale, thresholdValue, 255, cv2.THRESH_BINARY)

    imageThresholdValue = cv2.bitwise_not(imageThreshold)
    imageThresholdValue = cv2.medianBlur(imageThresholdValue, 5)

    contours = cv2.findContours(imageThresholdValue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    imageThresholdFrame = cv2.cvtColor(imageThresholdValue, cv2.COLOR_GRAY2RGB)

    for each in range(len(contours)):
        if cv2.contourArea(contours[each]) > 100:
            if cv2.contourArea(contours[each]) < 800:
                imageThresholdFrame = cv2.drawContours(imageThresholdFrame, contours, each, (128, 128, 0), 4)

    cv2.imshow("Adjustable Threshold Value", imageThresholdFrame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()