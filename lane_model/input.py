import numpy
import os
import cv2
import time
import pandas
import matplotlib.pyplot
from PIL import Image
from tensorflow import keras
import tensorflow
from tensorflow import keras
from tensorflow.keras import layers
# from tensorflow.keras import layers
from tensorflow.keras import models
from sklearn.model_selection import train_test_split
from scipy.stats import linregress

import base64
from io import BytesIO


#non_noise
from sklearn.cluster import DBSCAN

width = 1640
height = 590


def base64_to_numpy(base64_string):
    # Loại bỏ tiền tố 'data:image/png;base64,' hoặc 'data:image/jpeg;base64,' khỏi chuỗi base64
    base64_string = base64_string.split(',')[-1]

    # Giải mã base64 và chuyển đổi thành mảng bytes
    image_bytes = base64.b64decode(base64_string)

    # Đọc ảnh từ mảng bytes
    image = Image.open(BytesIO(image_bytes))

    # Chuyển đổi ảnh thành mảng numpy
    image_array = numpy.array(image)
    return image_array

# Xtrain =[]
# Ytrain = []
# TRAIN_DATA = 'data/lane'
# dict = {'dashe_ white_line': [1, 0, 0, 0, 0], 'solid_white_line': [0, 1, 0, 0, 0], 'lane': [0, 0, 1, 0, 0], '3': [0, 0, 0, 1, 0], '4': [0, 0, 0, 0, 1],}

# def DocDuLieu(file):
#     DuLieu = []
#     Label = []
#     label = ''
#     for file in os.listdir(TRAIN_DATA):
#         if (file == 'input'):
#             file_path = os.path.join(TRAIN_DATA, file)
#             list_filename_path = []
#             label = file
#             for filename in os.listdir(file_path):
#                 if (".jpg" in filename or ".png" in filename):
#                     filename_path = os.path.join(file_path, filename)
#                     img = numpy.array(Image.open(filename_path))
#                     img = cv2.resize(img, (width, height))
#                     list_filename_path.append(img)
#                     # Label.append(dict[(label)])
#             DuLieu.extend(list_filename_path)
#     return DuLieu, Label


# Xtrain, Ytrain = DocDuLieu(TRAIN_DATA)
def image_canny(lane_image):
    image_gray = cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY)
    # image_gray_blur = cv2.GaussianBlur(image_gray, (7, 7), 2)
    image_gray_blur = cv2.GaussianBlur(src=image_gray, ksize=(5, 5), sigmaX=0, sigmaY=0)
    # image_gray_blur = cv2.medianBlur(src=image_gray, ksize=3)
    image_gray_blur_canny = cv2.Canny(image_gray_blur, 50, 150)
    return image_gray_blur_canny

def regon_of_interest(image):
    polygons = numpy.array([[(535, 415), (1185, 415), (822, 280), (788, 280)]])
    mask = numpy.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    mask_canny = cv2.bitwise_and(image, mask)
    return mask_canny

def display_lines(image, lines):
    line_image = numpy.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 255, 255), 2)
    return line_image

def make_coordinates(image, line_parameters, location):
    slope, intercept = line_parameters
    if location == 'right':
        y1 = 415
    else:
        y1 = 465
    y2 = 300
    x1 = int((y1 - intercept) / slope)
    x2 = int((y2 - intercept) / slope)
    return numpy.array([x1, y1, x2, y2])

#Hàm loại bỏ những điểm nhiễu
def non_noise(lines):
    data = []
    for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            data.append((x1, y1))
            data.append((x2, y2))
    data = numpy.array(data)
    eps = 60.0  # Độ lớn của cửa sổ
    min_samples = 2  # Số điểm tối thiểu trong mỗi cụm
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels = dbscan.fit_predict(data)

# Lấy các điểm không phải điểm nhiễu
    core_samples_mask = numpy.zeros_like(dbscan.labels_, dtype=bool)
    core_samples_mask[dbscan.core_sample_indices_] = True
    non_noise_points = data[core_samples_mask]
    non_noise_points = non_noise_points.reshape((-1, 4))
    return non_noise_points

def average_slope_intercept(image, lines):
    lines = non_noise(lines)
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = numpy.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_average = numpy.average(left_fit, axis=0)
    right_fit_average = numpy.average(right_fit, axis=0)
    try:
        try: 
            left_line = make_coordinates(image, left_fit_average, 'left')
        except Exception as e:
            right_line = make_coordinates(image, right_fit_average, 'right')
            print("Exception: ", e)
        right_line = make_coordinates(image, right_fit_average, 'right')
        return numpy.array([left_line, right_line])
    except Exception as e:
        print('Exception: ', Exception)
        raise e
    

def crop_output(image):
    image = image[240:400, 450:1250]
    image = cv2.resize(image, (160, 60))
    return image

# Xtrain, Yrain = DocDuLieu(TRAIN_DATA)

def lane_detection_image(image):
    # image = Xtrain[0]
    # image = cv2.imread('data/img/00000.jpg')
    # image = cv2.resize(image, (width, height))
    lane_image = numpy.copy(image)
    # crop_lane_image = lane_image[250:590, 200:1640]
    canny = image_canny(lane_image)
    regon = regon_of_interest(canny)
    lines = cv2.HoughLinesP(image=regon, rho=1, theta=numpy.pi/180, threshold=40, lines=numpy.array([]), minLineLength=5, maxLineGap=5)

    try:
        averaged_lines = average_slope_intercept(image, lines)
        lines = averaged_lines
    except Exception as e:
        print('Exception averaged_lines: ', Exception)
        raise e

    line_image = display_lines(lane_image, lines)
    combo_image = cv2.bitwise_and(image, line_image)
    combo_image =cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
    image_output = crop_output(line_image)
    cv2.imwrite(filename='lane_model/test/testline{}.jpg'.format(0), img=image_output)
    # matplotlib.pyplot.imshow(combo_image)
    # matplotlib.pyplot.show()
    
    return image_output

    # matplotlib.pyplot.imshow(regon)
    # matplotlib.pyplot.show()
    # cv2.imwrite(filename='finish/line{}.jpg'.format(count + 1), img=line_image)

# image = Xtrain[0]
# matplotlib.pyplot.imshow(image)
# matplotlib.pyplot.show()

# lane_detection_image(Xtrain[0])

# count = 0
# for i in Xtrain:
#     # matplotlib.pyplot.imshow(i)
#     # matplotlib.pyplot.show()
#     print(count)
#     lane_detection_image(i)
#     count = count + 1

def lane_input(image):
    # count = 0
    image = cv2.resize(image, (width, height))
    try:
        image = lane_detection_image(image)
    except Exception as e:
        raise e
    return image
    # count = count + 1
    # try:
    #     cv2.imwrite(filename='lane_model/test/testline{}.jpg'.format(count + 1), img=image)
    #     print('da luu anh')
    # except Exception:
    #     print('Exception luu anh')