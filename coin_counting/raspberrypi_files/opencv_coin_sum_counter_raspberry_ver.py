import cv2
import cvzone
import numpy as np
import pyttsx3
from cvzone.ColorModule import ColorFinder
from picamera2 import Picamera2
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
buttonPin = 2
buttonPin2 = 3
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(buttonPin2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

piCam = Picamera2()
piCam.preview_configuration.main.size=(640,480)
piCam.preview_configuration.main.format="RGB888"
piCam.preview_configuration.align()
piCam.configure("preview")
piCam.start()

totalMoney = 0
totalOnePeso = 0
totalFivePeso = 0
totalTenPeso = 0
totalTwentyPeso = 0

textSpeech = pyttsx3.init()

myColorFinder = ColorFinder(False)
# Custom Orange Color
hsvVals = {'hmin': 0, 'smin': 0, 'vmin': 145, 'hmax': 63, 'smax': 91, 'vmax': 255}

def empty(a):
    pass


cv2.namedWindow("Settings")
cv2.resizeWindow("Settings", 640, 240)
cv2.createTrackbar("Threshold1", "Settings", 15, 255, empty)
cv2.createTrackbar("Threshold2", "Settings", 230, 255, empty)


def preProcessing(img):
    imgPre = cv2.GaussianBlur(img, (5, 5), 3)
    thresh1 = cv2.getTrackbarPos("Threshold1", "Settings")
    thresh2 = cv2.getTrackbarPos("Threshold2", "Settings")
    imgPre = cv2.Canny(imgPre, thresh1, thresh2)
    kernel = np.ones((3, 3), np.uint8)
    imgPre = cv2.dilate(imgPre, kernel, iterations=1)
    imgPre = cv2.morphologyEx(imgPre, cv2.MORPH_CLOSE, kernel)

    return imgPre

def speakAmount():
    global totalMoney
    textSpeech.say(f"{totalMoney} pesos")
    textSpeech.runAndWait()

def speakTotalCoins():
    global totalOnePeso
    global totalFivePeso
    global totalTenPeso
    global totalTenPeso
    textSpeech.say(f"You have a total of {totalOnePeso} 1 peso coins,"
                   f"{totalFivePeso} 5 peso coins, "
                   f"{totalTenPeso} 10 peso coins, and "
                   f"{totalTwentyPeso} 20 peso coins.")
    textSpeech.runAndWait()


def buttonPressed(channel):
    speakAmount()

def buttonPressed2(channel):
    speakTotalCoins()

GPIO.add_event_detect(buttonPin, GPIO.RISING, callback=buttonPressed, bouncetime=300)
GPIO.add_event_detect(buttonPin2, GPIO.RISING, callback=buttonPressed2, bouncetime=300)


try:
    while True:
        img = piCam.capture_array()
        imgPre = preProcessing(img)
        imgContours, conFound = cvzone.findContours(img, imgPre, minArea=20)

        totalMoney = 0
        totalOnePeso = 0
        totalFivePeso = 0
        totalTenPeso = 0
        totalTwentyPeso = 0

        imgCount = np.zeros((480, 640, 3), np.uint8)

        if conFound:
            for count, contour in enumerate(conFound):
                peri = cv2.arcLength(contour['cnt'], True)
                approx = cv2.approxPolyDP(contour['cnt'], 0.02 * peri, True)

                if len(approx) > 5:
                    area = contour['area']
                    x, y, w, h = contour['bbox']
                    imgCrop = img[y:y + h, x:x + w]
                    # cv2.imshow(str(count),imgCrop)
                    imgColor, mask = myColorFinder.update(imgCrop, hsvVals)
                    whitePixelCount = cv2.countNonZero(mask)
                    # print(whitePixelCount)
                    # print(area)

                    # counting the sum of the coins
                    if area < 10200:
                        totalMoney += 1
                        totalOnePeso += 1
                    elif 10500 < area < 12300:
                        totalMoney += 5
                        totalFivePeso += 1
                    elif 12700 < area < 12900:
                        totalMoney += 10
                        totalTenPeso += 1

        cvzone.putTextRect(imgCount, f'P {totalMoney}', (100, 200), scale=10, offset=30, thickness=7)

        imgStacked = cvzone.stackImages([img, imgPre, imgContours, imgCount], 2, 1)
        cvzone.putTextRect(imgStacked, f'P {totalMoney}', (50, 50))

        cv2.imshow("Coin Counter", imgStacked)
        # cv2.imshow("imgColor", imgColor)
        cv2.waitKey(1)
finally:
    GPIO.cleanup()


