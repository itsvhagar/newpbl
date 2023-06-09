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

<<<<<<< HEAD

camera = cv2.VideoCapture(0)

isToggle = False


=======
>>>>>>> e3a9db36f8343275e03e37509c15913cc1c0db8f
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
<<<<<<< HEAD
    future_face = executor.submit(handle_face_event, img_encoded)
    if (isToggle == True):
        ret2, frame2 = camera.read()
        _, img_encoded2 = cv2.imencode('.jpg', frame2)
        # lane request

        # handle lane event
        future_lane = executor.submit(handle_lane_event, img_encoded2)

=======

    # webcam 2
    # ret2, frame2 = camera.read()
    # _, img_encoded2 = cv2.imencode('.jpg', frame2)

    # face request
    response = requests.post(
        'http://10.10.1.47:5000/predict', data=img_encoded.tostring())
    response = json.loads(response.text)


    input_state1 = GPIO.input(button_pin1)
    input_state2 = GPIO.input(button_pin2)
    if not input_state1 and not input_state2:
        # Both buttons have been pressed.
        print("Error: Both Buttons Pressed")
    elif not input_state1:
        # Button 1 has been pressed
        isToggle = not isToggle
        led_state = GPIO.input(led_pin1)  # Get current LED state
        # Toggle LED state
        if led_state == GPIO.HIGH:
            GPIO.output(led_pin1, GPIO.LOW)
        else:
            GPIO.output(led_pin1, GPIO.HIGH)
            # Wait for button release
        while not GPIO.input(button_pin1):
            time.sleep(0.000001)
    elif not input_state2:
        isToggle = not isToggle
        # Button 2 has been pressed
        led_state = GPIO.input(led_pin2)  # Get current LED state
        # Toggle LED state
        if led_state == GPIO.HIGH:
            GPIO.output(led_pin2, GPIO.LOW)
        else:
            GPIO.output(led_pin2, GPIO.HIGH)
            # Wait for button release
        while not GPIO.input(button_pin2):
            time.sleep(0.000001)

    # face handle event
    elif response == 2:
        print("Face not Detected!")
        faceCounter = 0
    elif response == 1:
        faceCounter = 0
        print("Open ", faceCounter)
    elif response == 0:
        faceCounter += 1
        if faceCounter == 4:
            # beep(0.1)
            # reset faceCounter
            faceCounter = 0
        print("close ", faceCounter)
>>>>>>> e3a9db36f8343275e03e37509c15913cc1c0db8f
    if cv2.waitKey(1) == 27:
        break
    time.sleep(1)




    # if ko bat xi nhan then handle lane event
    if(not isToggle):
        # lane request

        # responseLane = requests.post(
        # 'http://192.168.0.8:5000/lane', data=img_encoded.tostring())
        # responseLane = json.loads(responseLane.text)


        # for testing
        responseLane = 1

        # checking server msg
        if responseLane == 2:
            print("Lane not Detected!")
            laneCounter = 0
        elif response == 1:
            laneCounter = 0
            print("True lane", laneCounter)
        elif response == 0:
            laneCounter += 1
            if laneCounter == 2:
                beep(0.1)
                # reset counter
                laneCounter = 0
            print("False lane ", laneCounter)
        if cv2.waitKey(1) == 27:
            break
    time.sleep(0.025)

camera.release()
cv2.destroyAllWindows()
