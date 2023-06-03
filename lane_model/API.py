import time

from flask import Flask,jsonify,request
import flask
from flask_sockets import Sockets
# from app import Drowsiness_Detection
import numpy
import input
import predict
import cv2
import queue

import threading

import matplotlib.pyplot

import base64
from PIL import Image
from io import BytesIO

import decode
import input
import predict

app = Flask(__name__)
# @app.route('/predict_lane', methods = ["POST"])
# def predict_lane():
#     file = request.data
#     file = decode.De(file)
#     print(file.shape)
#     try:
#         file = input.lane_input(file)
#     except:
#         return jsonify(2)
#     result = predict.result(file)
#     if (result == 'true'):
#         return jsonify(1)
#     else:
#         return jsonify(0)

data_queue = queue.Queue()



@app.route('/get_predict_lane', methods = ["GET"])
def get_predict_lane():
    while True:
        if not data_queue.empty():
            file = data_queue.get()
            if isinstance(file, Exception):
                return jsonify(2)
            result = predict.result(file)
            if (result == 'true'):
                return jsonify(1)
            else:             
                return jsonify(0)
        else:
           return jsonify(200)
    # return jsonify(404)
    # return jsonify(data_queue.qsize())    
    # if not data_queue.empty():
    #     print('vao')
    #     # file = data_queue.get()
    #     # if isinstance(file, Exception):
    #     #     return jsonify(2)
    #     # result = predict.result(file)
    #     # if (result == 'true'):
    #     #     return jsonify(1)
    #     # else:
    #     #     return jsonify(0)
    #     return jsonify(0)
    # else:
    #     jsonify(200)
    
    # file = data_queue.get()
    # if isinstance(file, Exception):
    #     return jsonify(2)
    # result = predict.result(file)
    # if (result == 'true'):
    #     return jsonify(1)
    # else:
    #     return jsonify(0)

    # return jsonify(200)

@app.route('/post_predict_lane', methods = ["POST"])
def post_predict_lane():
    file = request.data
    file = decode.De(file)
    # matplotlib.pyplot.imshow(file)
    # matplotlib.pyplot.show()
    try:
        file = input.lane_input(file)
        print("vao hang doi")
        data_queue.put(file)
    except Exception as e:
        print('Vao Exception: ', e)
        data_queue.put(e)
    return jsonify(200)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0')


def run_server():
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    # Khởi chạy server trong một thread riêng biệt
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
