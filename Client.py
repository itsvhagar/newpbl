import datetime

import cv2
import requests
import time
import json

camera = cv2.VideoCapture(0)

while True:
    current_time = datetime.datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    print(current_time_str)
    ret, frame = camera.read()

    # encode image as JPEG
    _, img_encoded = cv2.imencode('.jpg', frame)

    # response = requests.post('http://192.168.1.35:5000/predict', data=img_encoded.tostring())
    response = requests.post('http://192.168.1.29:5000/face_predict', data=img_encoded.tobytes())
    response = json.loads(response.text)
    if response == 1:
        print("Open")
    elif response == 0:
        print("Close")
    elif response == 2:
        print("Didn't detect face")
    # cv2.imshow("Client", frame)
    time.sleep(0.0015)

camera.release()
cv2.destroyAllWindows()