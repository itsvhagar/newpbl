import cv2
import requests
import time
import json
import numpy
import time
from PIL import Image
import threading
import matplotlib.pyplot
import datetime
import os

width = 1640
height = 590

# camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1640)
# camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 590)
# camera.set(cv2.CAP_PROP_FPS, 60)
TRAIN_DATA = 'D:\\Project\\PBL\\PBL5\\test\\data\\lane'

def DocDuLieu(file):
    DuLieu = []
    Label = []
    label = ''
    for file in os.listdir(TRAIN_DATA):
        if (file == 'test'):
            file_path = os.path.join(TRAIN_DATA, file)
            list_filename_path = []
            label = file
            for filename in os.listdir(file_path):
                if (".jpg" in filename or ".png" in filename):
                    filename_path = os.path.join(file_path, filename)
                    img = numpy.array(Image.open(filename_path))
                    # img = cv2.resize(img, (width, height))
                    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    list_filename_path.append(img)
                    # Label.append(dict[(label)])
            DuLieu.extend(list_filename_path)
    return DuLieu, Label
Xtrain, Ytrain = DocDuLieu(TRAIN_DATA)
# filename_path = 'lane_model/KiemThu/1.jpg'
# img = numpy.array(Image.open(filename_path))

def Show_camera(ret, frame):
    polygons = numpy.array([[(535, 415), (1185, 415), (822, 280), (788, 280)]])
    mask = numpy.zeros_like(frame)
    cv2.fillPoly(mask, polygons, 255)
    result = cv2.bitwise_and(frame, mask)
    result =cv2.addWeighted(frame, 0.8, mask, 1, 1)
    if ret == True:
        cv2.imshow('Video', result)

# while True:
#     # start_time = time.time()
#     ret, frame = camera.read()
#     frame = cv2.resize(frame, (width, height))
#     frame = cv2.flip(frame, 1)
#     # print(ret)
#     Show_camera(ret, frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#     # matplotlib.pyplot.imshow(img)
#     # matplotlib.pyplot.show()
#     # encode image as JPEG
#     # _, img_encoded = cv2.imencode('.jpg', frame)
#     img_encoded = cv2.imencode('.jpg', frame)[1].tobytes()
#     image_bytes = cv2.imencode('.jpg', img)[1].tobytes()
#     # send image to server using POST request
#     response = requests.post('http://127.0.0.1:5000/predict_lane', data=img_encoded)
    
#     # response = requests.post('http://127.0.0.1:5000/predict_lane', data=img_encoded)

#     # response = requests.post('http://192.168.1.135:5000/predict', data=img_encoded.tostring())
#     response = json.loads(response.text)
#     if response == 1:
#         print("true")
#     elif response == 0:
#         print("flase")
#     elif response == 2: 
#         print("No lane")
#     # cv2.imshow("Client", frame)
#     # end_time = time.time()
#     # elapsed_time = end_time - start_time
#     # print("Thời gian trôi qua: ", elapsed_time, "giây")
#     # time.sleep(0.04)



def send_lane_predict():
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FPS, 60)
    while True:
        ret, frame = camera.read()
        frame = cv2.resize(frame, (width, height))
        frame = cv2.flip(frame, 1)
        Show_camera(ret, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        img_encoded = cv2.imencode('.jpg', frame)[1].tobytes()
        # image_bytes = cv2.imencode('.jpg', img)[1].tobytes()
        # response = requests.post('http://127.0.0.1:5000/predict_lane', data=img_encoded)
        requests.post('http://127.0.0.1:5000/post_predict_lane', data=img_encoded)
        # for i in Xtrain:
        #     image_bytes= cv2.flip(i, 1)
        #     image_bytes = cv2.imencode('.jpg', i)[1].tobytes()
        #     requests.post('http://127.0.0.1:5000/post_predict_lane', data=image_bytes)
    camera.release()
        # time.sleep(0.1)
        # print('xong')

def receive_lane_predict():
    # while True:
    #     print("Toan")
    while True:
        response = requests.get('http://127.0.0.1:5000/get_predict_lane')
        response = json.loads(response.text)
        # if (response == 200):
        #     print('nhan thanh cong')
        # elif (response == 404):
        #     print("Doi du lieu")
        # print(response)
        # print('nhan')
        current_time = datetime.datetime.now()
        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
        if response == 0:
            # print(current_time_str)
            print("right lane")
        elif response == 1:
            # print(current_time_str)
            print("wrong lan")
        elif response == 2: 
            # print(current_time_str)
            print("No lane")
        # elif response == 404:
        #     print()

def concentration_predict():
    camera = cv2.VideoCapture(1)
    while True:
        ret, frame = camera.read()

        # encode image as JPEG
        _, img_encoded = cv2.imencode('.jpg', frame)
        cv2.imshow('Image 2', frame)
        # cv2.imshow('Image 3', frame3)
        # Nhấn phím 'q' để thoát
        if cv2.waitKey(1) == ord('q'):
            break

        # send image to server using POST request
        # response = requests.post('http://1.55.36.6:5000/predict', data=img_encoded.tostring())
        # response = requests.post('http://172.20.10.2:5000/predict', data=img_encoded.tostring())
        # response = requests.post('http://192.168.1.135:5000/predict', data=img_encoded.tostring())
        response = requests.post('http://192.168.1.35:5000/predict', data=img_encoded.tostring())
        response = json.loads(response.text)
        # if response == 1:
        #     print("Open")
        # elif response == 0:
        #     print("Close")
        # elif response == 2: 
        #     print("Didn't detect face")
        
        # # time.sleep(0.0015)

    camera.release()

def main():
    send_lane_thread = threading.Thread(target=send_lane_predict)
    receive_lane_thread = threading.Thread(target=receive_lane_predict)
    concentration_thread = threading.Thread(target=concentration_predict)
    receive_lane_thread.start()
    send_lane_thread.start()
    # concentration_thread.start()

main()

cv2.destroyAllWindows()