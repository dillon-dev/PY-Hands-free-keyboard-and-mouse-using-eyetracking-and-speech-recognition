import dlib

import numpy as np

import cv2

import time

import os

detector = dlib.get_frontal_face_detector()

predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

cap = cv2.VideoCapture(0)
cap.set(3, 480)
while cap.isOpened():
    flag, im_rd = cap.read()
    k = cv2.waitKey(1)
    img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)
    faces = detector(img_gray, 0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    if len(faces) != 0:
        for i in range(len(faces)):
            landmarks = np.matrix([[p.x, p.y] for p in predictor(im_rd, faces[i]).parts()])
            for idx, point in enumerate(landmarks):
                pos = (point[0, 0], point[0, 1])
                cv2.circle(im_rd, pos, 1, color=(255, 0, 0))
                cv2.putText(im_rd, str(idx + 1), pos, font, 0.2, (187, 255, 255), 1, cv2.LINE_AA)
    else:
        cv2.putText(im_rd, "No face detected", (20, 50), font, 1, (0, 0, 0), 1, cv2.LINE_AA)

    if k == ord('q'):
        break

    cv2.namedWindow("camera", 1)
    cv2.imshow("camera", im_rd)
cap.release()
cv2.destroyAllWindows()