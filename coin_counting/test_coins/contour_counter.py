import cv2
import cvzone
import numpy as np


def empty(a):
    pass

# create two sliders to adjust canny filter
# thresholds on the fly

captureCamera = cv2.VideoCapture(1)
cv2.namedWindow("Settings")
cv2.resizeWindow("Settings", 640, 240)
cv2.createTrackbar("Threshold1", "Settings", 65, 255, empty)
cv2.createTrackbar("Threshold2", "Settings", 150, 255, empty)
cv2.createTrackbar("CV Min Area", "Settings", 65, 255, empty)

# prepare the image for detection
def preProcessing(img):

    # add some blur to reduce noise
    img_prep = cv2.GaussianBlur(img, (5, 5), 3)
    # use canny filter to enhance contours
    # make thresholds changeable by sliders
    threshold1 = cv2.getTrackbarPos("Threshold1", "Settings")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Settings")
    img_prep = cv2.Canny(img_prep, threshold1, threshold2)
    # make features more prominent by dilations
    kernel = np.ones((2, 2), np.uint8)
    img_prep = cv2.dilate(img_prep, kernel, iterations=1)
    # morph detected features to close gaps in geometries
    img_prep = cv2.morphologyEx(img_prep, cv2.MORPH_CLOSE, kernel)

    return img_prep

while True:
    success, img = captureCamera.read()
    img_prep = preProcessing(img)
    cv2.imshow("Contour Test", img)

    # min area slider to filter noise
    cvMinArea = cv2.getTrackbarPos("CV Min Area", "Settings")
    # findContours returns the processed image and found contours
    imgContours, conFound = cvzone.findContours(img, img_prep, cvMinArea)
    # show original vs pre-processed image
    # show all streams in 2 columns at half size
    output = cvzone.stackImages([img, img_prep, imgContours], 2, 0.3)

    # conFound will contain all contours found
    # we can limit it to circles for our coins
    if conFound:
        for contour in conFound:
            # get the arc length of the contour
            perimeter = cv2.arcLength(contour["cnt"], True)
            # calculate approx polygon count / corner points
            polycount = cv2.approxPolyDP(contour["cnt"], 0.02 * perimeter, True)
            # print no of corner points in contour
            # print(len(polycount))

            if len(polycount) >= 8:
                print(contour['area'])

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Keep running until you press `q`
        break