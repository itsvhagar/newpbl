# import numpy
# import os
# import cv2
# import time
# import matplotlib.pyplot
# from PIL import Image
# from tensorflow import keras
# import tensorflow
# from tensorflow.keras import layers
# # from tensorflow.keras import layers
# from tensorflow.keras import models

# # width = 500
# # height = 180
# width = 160
# height = 60
# # TRAIN_DATA = 'dataset/TrainData/driver_37_30frame/05181432_0203.MP4'
# # TRAIN_DATA_LABEL = 'dataset\TrainData\CULane\laneseg_label_w16_test\laneseg_label_w16_test\driver_37_30frame/05181432_0203.MP4'
# TRAIN_DATA = 'data/lane/train'

# Xtrain =[]
# Ytrain = []
# dict = {'true': [1, 0], 'false': [0, 1]}

# #demo
# def DocDuLieu(file):
#     DuLieu = []
#     Label = []
#     label = ''
#     for filename in os.listdir(file):
#         filename_path = os.path.join(file, filename)
#         list_filename_sub_path = []
#         label = filename
#         for filename_sub in os.listdir(filename_path):
#             if (".jpg" in filename_sub or ".png" in filename_sub):
#                 filename_sub_path = os.path.join(filename_path, filename_sub)
#                 img = numpy.array(Image.open(filename_sub_path))
#                 img = cv2.resize(img, (width, height))
#                 img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#                 # matplotlib.pyplot.imshow(img)
#                 # matplotlib.pyplot.show()
#                 list_filename_sub_path.append(img)
#                 Label.append(dict[(label)])
#         DuLieu.extend(list_filename_sub_path)
#     return DuLieu, Label

# Xtrain, Ytrain = DocDuLieu(TRAIN_DATA)

# print(len(Xtrain))
# print(Ytrain)

# # #test
# # def DocDuLieu(file, x):
# #     DuLieu = []
# #     # for file in os.listdir(TRAIN_DATA):
# #     #     if (".MP4" in file):
# #     #         file_path = os.path.join(TRAIN_DATA, file)
# #     list_filename_path = []
# #     for filename in os.listdir(file):
# #         if (".jpg" in filename or ".png" in filename):
# #             filename_path = os.path.join(file, filename)
# #             img = numpy.array(Image.open(filename_path))
# #             img = cv2.resize(img, (width, height))
# #             print(img)
# #             list_filename_path.append(img)
# #     DuLieu.extend(list_filename_path)
# #     return DuLieu

# # Xtrain = DocDuLieu(TRAIN_DATA, "Doc")
# # Ytrain = DocDuLieu(TRAIN_DATA_LABEL, "Dap")


# model_training_frist = models.Sequential([
#     layers.Conv2D(32, (3, 3), input_shape=(height, width, 1), activation = 'relu'),
#     layers.MaxPool2D((2, 2)),
#     layers.Dropout(0.15),
    
#     layers.Conv2D(64, (3, 3), activation = 'relu'),
#     layers.MaxPool2D((2, 2)),
#     layers.Dropout(0.2),

#     layers.Conv2D(128, (3, 3), activation = 'relu'),
#     layers.MaxPool2D((2, 2)),
#     layers.Dropout(0.2),

#     # layers.Flatten(input_shape=(32, 32, 3)),
#     layers.Flatten(),
#     # layers.Dense(10000, activation = 'relu'),
#     # layers.Dense(8000, activation = 'relu'),
#     # layers.Dense(5000, activation = 'relu'),
#     layers.Dense(3000, activation = 'relu'),
#     layers.Dense(1000, activation = 'relu'),
#     layers.Dense(2, activation = 'softmax'),
# ])

# model_training_frist.summary()
# model_training_frist.compile(optimizer='SGD',
#                              loss='mse',
#                              metrics=['accuracy'])



# early_callback = tensorflow.keras.callbacks.EarlyStopping(monitor="loss", min_delta= 0 , patience=10, verbose=1, mode="auto")

# model_training_frist.fit(numpy.array(Xtrain), numpy.array(Ytrain), epochs=100, batch_size=150,
#                          callbacks = [early_callback],
#                          verbose=True)



# print("Train xong")

# model_training_frist.save('model_demo_1_10epochs.h5')

# # model_training_frist.save("model_test.h5")

# # model_training_frist.summary()
# # # model_training_frist.compile(optimizer='SGD', 
# # #                              loss='categirical_crossentropy', 
# # #                              metrics=['accuracy'])

# # model_training_frist.compile(optimizer='SGD', 
# #                              loss='mse', 
# #                              metrics=['accuracy'])
# # # print(Xtrain[0][1])
# # # x = numpy.array([x[0] for _, x in enumerate(Xtrain)])
# # # y = numpy.array([y[0] for _, y in enumerate(Xtrain)])

# # # print(numpy.array([x[1] for _, x in enumerate(Xtrain)]))
# # # print(x)]
# # # print (len(Xtrain[0][1]))
# # # print(Ytrain)

# # model_training_frist.fit(numpy.array(Xtrain), numpy.array(Ytrain), epochs=10, batch_size=2)

# # # model_training_frist.fit(numpy.array([x[0] for _, x in enumerate(Xtrain)]), numpy.array([y[1] for _, y in enumerate(Xtrain)]), epochs=10, batch_size=2)
# # # model_training_frist.fit(x, y, epochs=10)


# # print("Train xong")

# # # model_training_frist.save('model_demo_1_10epochs.h5')

# # # models = models.load_model('model_demo_1_10epochs.h5')