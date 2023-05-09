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
    def eye_aspect_ratio(self, eye):
        A = distance.euclidean(eye[1], eye[5])
        B = distance.euclidean(eye[2], eye[4])
        C = distance.euclidean(eye[0], eye[3])
        ear = (A + B) / (2.0 * C)
        return ear
    def detect(self, file):
        npimg = np.frombuffer(file, np.uint8)
        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        # cv2.imwrite('image.jpg', frame)

        thresh = 0.25
        frame_check = 20
        detect = dlib.get_frontal_face_detector()
        predict = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")  # Dat file is the crux of the code
        (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
        (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
        flag = 0
        while True:
            frame = imutils.resize(frame, width=450)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            subjects = detect(gray, 0)
            if len(subjects) == 0:
                return 2
            for subject in subjects:
                shape = predict(gray, subject)
                shape = face_utils.shape_to_np(shape)  # converting to NumPy Array
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                leftEAR = self.eye_aspect_ratio(leftEye)
                rightEAR = self.eye_aspect_ratio(rightEye)
                ear = (leftEAR + rightEAR) / 2.0
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                if ear < thresh:
                    flag += 1
                    print(flag)
                    if flag >= frame_check:
                        cv2.putText(frame, "****************ALERT!****************", (10, 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        cv2.putText(frame, "****************ALERT!****************", (10, 325),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    return False
                else:
                    flag = 0
                    return True

