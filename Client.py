import json
import time

import cv2
import base64
import numpy as np
import requests

cap=cv2.VideoCapture(0)
url = 'http://192.168.1.48:5000/predict'
while cap.isOpened():
    ret, frame = cap.read()
    encoded_img = base64.b64encode(frame)
    # data = {
    #     'base64_img' : str(encoded_img[2:-1])
    # }
    # res = requests.post(url = url, json= data)
    # res = json.loads(res.text)
    # if res == 1:
    #     print("Open")
    # else:
    #     print("Closed")
    file = open("encoded.txt", "a")
    file.write(str(encoded_img))
    file.close()
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    time.sleep(1000)
cv2.destroyAllWindows()
cap.release()
