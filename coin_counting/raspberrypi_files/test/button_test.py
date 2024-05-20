import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
BUTTON_PIN = 2
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def buttonPressed(channel):
    print("button pressed!")
try:
    GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=buttonPressed, bouncetime=300)
except RuntimeError as e:
    print(f"Error {e}")
    GPIO.cleanup()
    exit(1)
try:
    print("waiting for button press. press ctrl + c to exit")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("exit")
finally:
    GPIO.cleanup()
