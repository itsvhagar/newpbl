import RPi.GPIO as GPIO
import cv2
import requests
import time
import json

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


while True:
    # webcam1
    ret, frame = camera.read()
    _, img_encoded = cv2.imencode('.jpg', frame)

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
    if cv2.waitKey(1) == 27:
        break
    time.sleep(0.025)




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
