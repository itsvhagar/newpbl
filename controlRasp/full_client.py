import RPi.GPIO as GPIO
import cv2
import requests
import time
import json
from concurrent.futures import ThreadPoolExecutor

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
camera = cv2.VideoCapture(0)
# camera2 = cv2.VideoCapture(1)


buzzer_pin = 14
led_pin1 = 17
button_pin1 = 2

led_pin2 = 22
button_pin2 = 4


camera = cv2.VideoCapture(0)

isToggle = False


# button for xinhan
isToggle = False

GPIO.setup(buzzer_pin, GPIO.OUT)

GPIO.setup(led_pin1, GPIO.OUT)
GPIO.setup(button_pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(led_pin2, GPIO.OUT)
GPIO.setup(button_pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize LED to off state
GPIO.output(led_pin1, GPIO.LOW)
GPIO.output(led_pin2, GPIO.LOW)

faceCounter = 0
laneCounter = 0


def beep(duration):
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(buzzer_pin, GPIO.LOW)


def handle_face_event(img_encoded):
    response = requests.post(
        'http://192.168.1.225:5000/predict', data=img_encoded.tostring())
    response = json.loads(response.text)
    if response == 2:
        print("Face not Detected!")
    elif response == 1:
        print("Open ")
    elif response == 0:
        print("close ")


def handle_lane_event(img_encode):
    responseLane = requests.post(
        'http://192.168.1.225:5000/lane', data=img_encoded.tostring())
    responseLane = json.loads(responseLane.text)

    if responseLane == 2:
        print("Lane not Detected!")
    elif responseLane == 1:
        print("True lane")
    elif responseLane == 0:
        print("False lane ")


executor = ThreadPoolExecutor(max_workers=2)

while True:
    # webcam1
    ret, frame = camera.read()
    _, img_encoded = cv2.imencode('.jpg', frame)
    future_face = executor.submit(handle_face_event, img_encoded)
    if (isToggle == True):
        ret2, frame2 = camera.read()
        _, img_encoded2 = cv2.imencode('.jpg', frame2)
        # lane request

        # handle lane event
        future_lane = executor.submit(handle_lane_event, img_encoded2)

    if cv2.waitKey(1) == 27:
        break
    time.sleep(1)

camera.release()
cv2.destroyAllWindows()
