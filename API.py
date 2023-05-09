import time

from flask import Flask,jsonify,request
import flask
from app import Drowsiness_Detection

app = Flask(__name__)
model = Drowsiness_Detection()

@app.route('/predict', methods = ["POST"])
def predict():
    file = request.data
    prediction = model.detect(file)
    if prediction == True:
        return jsonify(1)
    elif not prediction:
        return jsonify(0)
    else:
        return jsonify(2)
    time.sleep(0.125)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
