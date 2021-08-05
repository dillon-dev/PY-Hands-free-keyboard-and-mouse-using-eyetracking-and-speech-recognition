import cv2
import numpy as np
import dlib
from math import hypot
import tkinter as tk
import mouse
import time
import keyboard
import testKB
from threading import Timer
from multiprocessing import Process
from threading import Thread
import pyautogui


def blink(eye_landmarks, dlib_face_landmarks):
    # each eye's coordinates for blink
    eye_left = (dlib_face_landmarks.part(eye_landmarks[0]).x, dlib_face_landmarks.part(eye_landmarks[0]).y)
    eye_right = (dlib_face_landmarks.part(eye_landmarks[3]).x, dlib_face_landmarks.part(eye_landmarks[3]).y)
    eye_top = (dlib_face_landmarks.part(eye_landmarks[1]).x, dlib_face_landmarks.part(eye_landmarks[2]).y)
    eye_bottom = (dlib_face_landmarks.part(eye_landmarks[5]).x, dlib_face_landmarks.part(eye_landmarks[4]).y)

    # display
    # eye_width_line = cv2.line(frame, eye_left, eye_right, (0, 0, 255), 1)
    # eye_height_line = cv2.line(frame, eye_top, eye_bottom, (0, 0, 255), 1)

    # blink detection requires changes in vertical line
    # divide hor line against ver line for blink detection
    # (using only ver line distance can have issues relating to
    # physical distance from camera, the division method is more reliable)
    eye_height = hypot((eye_top[0] - eye_bottom[0]), (eye_top[1] - eye_bottom[1]))
    eye_width = hypot((eye_left[0] - eye_right[0]), (eye_left[1] - eye_right[1]))

    try:
        blink_ratio = eye_width / eye_height
    except ZeroDivisionError:
        blink_ratio = None

    # print(blink_ratio)
    return blink_ratio


def moveMouseRight():
    pyautogui.move(10, 0)
    # print("right mouse move")


def moveMouseLeft():
    pyautogui.move(-10, 0)
    # print("left mouse move")


def moveMouseDown():
    pyautogui.move(0, 10)
    # print("down mouse move")


def moveMouseUp():
    pyautogui.move(0, -10)
    # print("up mouse move")


def mouseLeftClick():
    pyautogui.click()


def mouseRightClick():
    pyautogui.click(button='right')