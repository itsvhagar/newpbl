import numpy
import os
import cv2
import time
import matplotlib.pyplot
from PIL import Image
from tensorflow import keras
import tensorflow
from tensorflow.keras import layers
# from tensorflow.keras import layers
from tensorflow.keras import models

width = 160
height = 60

# width = 800
# height = 300

dict = {'right': [1, 0], 'wrong': [0, 1]}
name_result = ['right', 'wrong']

new_model = tensorflow.keras.models.load_model('model_demo_1_10epochs.h5')
new_model.summary()

def result(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    result = name_result[numpy.argmax(new_model.predict(image.reshape(-1, height, width, 1)))]
    return result