from flask import request
from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2
import base64
import numpy as np
import requests



class Drowsiness_Detection():
    def __init__(self):
        self.thresh = 0.25
        self.predict = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")  # Dat file is the crux of the code
        self.lStart, self.lEnd = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
        self.rStart, self.rEnd = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
    def eye_aspect_ratio(self, eye):
        A = distance.euclidean(eye[1], eye[5])
        B = distance.euclidean(eye[2], eye[4])
        C = distance.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear

    def detect(self, file):
        npimg = np.frombuffer(file, np.uint8)
        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        cv2.imwrite('image.jpg', frame)
        detect = dlib.get_frontal_face_detector()
        while True:
            frame = imutils.resize(frame, width=450)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            subjects = detect(gray, 0)
            if len(subjects) == 0:
                return 2
            for subject in subjects:
                shape = self.predict(gray, subject)
                shape = face_utils.shape_to_np(shape)  # converting to NumPy Array
                leftEye = shape[self.lStart:self.lEnd]
                rightEye = shape[self.rStart:self.rEnd]
                leftEAR = self.eye_aspect_ratio(leftEye)
                rightEAR = self.eye_aspect_ratio(rightEye)
                ear = (leftEAR + rightEAR) / 2.0
                if ear < self.thresh:
                    return False
                else:
                    return True

