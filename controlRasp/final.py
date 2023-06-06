import cv2
import RPi.GPIO as GPIO
import requests
import time
import json
import numpy
import time
from PIL import Image
import threading
import matplotlib.pyplot
import datetime


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

width = 1640
height = 590

buzzer_pin = 14
led_pin1 = 17
button_pin1 = 2

led_pin2 = 22
button_pin2 = 4

faceCounter=0
laneCounter = 0
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


def Show_camera(ret, frame):
    polygons = numpy.array([[(535, 415), (1185, 415), (822, 280), (788, 280)]])
    mask = numpy.zeros_like(frame)
    cv2.fillPoly(mask, polygons, 255)
    result = cv2.bitwise_and(frame, mask)
    result =cv2.addWeighted(frame, 0.8, mask, 1, 1)
    if ret == True:
        cv2.imshow('Video', result)

def beep(duration):
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(buzzer_pin, GPIO.LOW)



def send_lane_predict():
    camera = cv2.VideoCapture(2)
    camera.set(cv2.CAP_PROP_FPS, 60)
    global isToggle
    while True:
        if not isToggle:    
            ret, frame = camera.read()
            frame = cv2.resize(frame, (width, height))
            frame = cv2.flip(frame, 1)
            # Show_camera(ret, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            img_encoded = cv2.imencode('.jpg', frame)[1].tobytes()
            # response = requests.post('http://127.0.0.1:5000/predict_lane', data=img_encoded)
            requests.post('http://192.168.1.123:5000/post_predict_lane', data=img_encoded)
            time.sleep(0.1)
    camera.release()
            # print('xong')


def receive_lane_predict():
    # while True:
    #     print("Toan")
    global isToggle
    global laneCounter
    while True:
        # call api
        response = requests.get('http://192.168.1.123:5000/get_predict_lane')
        response = json.loads(response.text)

        # handle toggle event
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


        if not isToggle:
            # checking server msg
            if response == 2:
                print("Lane not Detected!")
                laneCounter = 0
            elif response == 1:
                laneCounter = 0
                print("Right lane", laneCounter)
            elif response == 0:
                laneCounter += 1
                if laneCounter == 3:
                    beep(0.1)
                    # reset counter
                    laneCounter = 0
                print("Wrong lane ", laneCounter)

def concentration_predict():
    global faceCounter
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()

        # encode image as JPEG
        _, img_encoded = cv2.imencode('.jpg', frame)
        # cv2.imshow('Image 2', frame)
        # cv2.imshow('Image 3', frame3)
        # Nhấn phím 'q' để thoát
        if cv2.waitKey(1) == ord('q'):
            break

        # send image to server using POST request
        # response = requests.post('http://1.55.36.6:5000/predict', data=img_encoded.tostring())
        # response = requests.post('http://172.20.10.2:5000/predict', data=img_encoded.tostring())
        # response = requests.post('http://192.168.1.135:5000/predict', data=img_encoded.tostring())
        response = requests.post('http://192.168.1.40:5000/face-predict', data=img_encoded.tostring())
        response = json.loads(response.text)
        if response == 2:
            print("Face not Detected!")
            faceCounter = 0
        elif response == 1:
            faceCounter = 0
            print("Concentrated ", faceCounter)
        elif response == 0:
            faceCounter += 1
            if faceCounter == 4:
                beep(0.1)
                # reset faceCounter
                faceCounter = 0
            print("Distracted ", faceCounter)
        if cv2.waitKey(1) == 27:
            break
        time.sleep(0.025)
    camera.release()

def main():
    send_lane_thread = threading.Thread(target=send_lane_predict)
    receive_lane_thread = threading.Thread(target=receive_lane_predict)
    concentration_thread = threading.Thread(target=concentration_predict)
    receive_lane_thread.start()
    send_lane_thread.start()
    concentration_thread.start()

main()

cv2.destroyAllWindows()