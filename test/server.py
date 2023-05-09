from flask import Flask, request, jsonify
import cv2
import os
import numpy as np
import base64
import time

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def video_feed():
    file = request.data
    npimg = np.frombuffer(file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    # testing = base64.b64encode(img)
    # print(testing)
    time.sleep(0.125)
    
    # Save the decoded image file to current directory
    cv2.imwrite('image.jpg', img)
    
    return jsonify(1)

if __name__ == '__main__':
    app.run(host='0.0.0.0')