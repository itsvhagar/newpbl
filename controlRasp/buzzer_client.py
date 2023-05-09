import cv2
import requests
import time
import RPi.GPIO as GPIO
import json


GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setwarnings(False)
camera = cv2.VideoCapture(0)


buzzer_pin = 17
counter = 0


def beep(duration):
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(buzzer_pin, GPIO.LOW)

while True:
    ret, frame = camera.read()

    # encode image as JPEG
    _, img_encoded = cv2.imencode('.jpg', frame)

    # send image to server using POST request
    # response = requests.post('http://1.55.36.6:5000/predict', data=img_encoded.tostring())
    response = requests.post(
        'http://192.168.1.139:5000/predict', data=img_encoded.tostring())
    response = json.loads(response.text)
    if response == 1:
       counter += 1
       if counter == 4:
           beep(0.1)
           # reset counter
           counter = 0
    else:
        print("Close")
        counter =0 
    if cv2.waitKey(1) == 27:  # ESC key pressed
        break
    time.sleep(0.025)

camera.release()
cv2.destroyAllWindows()
