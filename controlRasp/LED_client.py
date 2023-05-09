import RPi.GPIO as GPIO
import cv2
import requests
import time
import json

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
camera = cv2.VideoCapture(0)
led_pin = 12
button_pin = 2

GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize LED to off state
GPIO.output(led_pin, GPIO.LOW)

while True:
    # Wait for button press
    input_state = GPIO.input(button_pin)
    if not input_state:
        # Button has been pressed
        led_state = GPIO.input(led_pin)  # Get current LED state
        # Toggle LED state
        if led_state == GPIO.HIGH:
            GPIO.output(led_pin, GPIO.LOW)
        else:
            GPIO.output(led_pin, GPIO.HIGH)
        # Wait for button release
        while not GPIO.input(button_pin):
            time.sleep(0.01)

    else:
        print("Close")
    if cv2.waitKey(1) == 27:
        break
    time.sleep(0.025)
    
camera.release()
cv2.destroyAllWindows()