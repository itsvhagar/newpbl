import cv2
import requests
import time
import json

camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()

    # encode image as JPEG
    _, img_encoded = cv2.imencode('.jpg', frame)

    # send image to server using POST request
    # response = requests.post('http://1.55.36.6:5000/predict', data=img_encoded.tostring())
    response = requests.post('http://172.20.10.2:5000/predict', data=img_encoded.tostring())
    # response = requests.post('http://192.168.1.135:5000/predict', data=img_encoded.tostring())
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
