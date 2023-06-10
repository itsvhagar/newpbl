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

import input
import predict

width = 160
height = 60

# width = 800
# height = 300

dict = {'right': [1, 0], 'wrong': [0, 1]}
name_result = ['right', 'worng']
# Xtrain = Xtrain/255

new_model = tensorflow.keras.models.load_model('model_demo_1_10epochs.h5')
# Check its architecture
new_model.summary()

TRAIN_DATA = 'data/lane/acc'

def DocDuLieu(file):
    DuLieu = []
    Label = []
    label = ''
    for file in os.listdir(TRAIN_DATA):
        file_path = os.path.join(TRAIN_DATA, file)
        list_filename_path = []
        label = file
        print(file)
        for filename in os.listdir(file_path):
            if (".jpg" in filename or ".png" in filename):
                filename_path = os.path.join(file_path, filename)
                img = numpy.array(Image.open(filename_path))
                list_filename_path.append(img)
                Label.append(label)
        DuLieu.extend(list_filename_path)
    return DuLieu, Label

Xtrain, Ytrain = DocDuLieu(TRAIN_DATA)

X_acc = []
Y_acc = []

for i in range (0, len(Xtrain)):
    try:
        file = input.lane_input(Xtrain[i])
        X_acc.append(file)
        Y_acc.append(Ytrain[1])
    except Exception:
        print()

print(len(Xtrain))
print(len(Ytrain))
print(len(X_acc))
print(len(Y_acc))

width = 160
height = 60
Y_acc_pre = []
for i in X_acc:
    i = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
    result = name_result[numpy.argmax(new_model.predict(i.reshape(-1, height, width, 1)))]
    Y_acc_pre.append(result)

print(Y_acc)
print(Y_acc_pre)

from sklearn.metrics import accuracy_score
print(accuracy_score(Y_acc,Y_acc_pre))