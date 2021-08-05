# main

import cv2
import numpy as np
import dlib
from math import hypot
import time
import keyboard
import pyautogui
import threading
from eye_functions import blink, moveMouseRight, moveMouseLeft, mouseLeftClick, mouseRightClick, moveMouseDown, moveMouseUp
import speech_recognition as sr  # https://www.simplifiedpython.net/speech-recognition-python/
from gui import errorgui, commandgui, keyboardgui, mousegui, lookingdownallowedgui, lookingdownnotallowedgui
import mouse

# dlib's face detector and shape predictor
dlib_predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
dlib_detect = dlib.get_frontal_face_detector()
font = cv2.FONT_HERSHEY_PLAIN

mouth_open = False
mouth_has_opened = False
lookingRight = False
lookingLeft = False
lookingStraight = False
lookingUp = False
leftWink = False
rightWink = False
blink_true = False
keyboard_running = False
lookingDown = False
speech_running = False
eyes_running = True
lookingDownAllowed = True
count = 0


def faceDetect():
    global mouth_has_opened
    global mouth_open
    global lookingDown
    global lookingRight
    global lookingLeft
    global lookingUp
    global lookingStraight
    global leftWink
    global rightWink
    global blink_true
    global keyboard_running
    global speech_running
    global eyes_running
    global lookingDownAllowed
    global count

    # initialize video     0 for default webcam
    cap = cv2.VideoCapture(0)
    if not (cap.isOpened()):
        print("No camera detected")
    while eyes_running:
        _, camera_feed = cap.read()

        # GREYSCALE THE IMAGE
        grey_camera_feed = cv2.cvtColor(camera_feed, cv2.COLOR_BGR2GRAY)

        # store information about face position in array frames.
        # traverse array with for loop to update detector every frame
        frames = dlib_detect(grey_camera_feed)

        # for morphology
        kernel = np.ones((5, 5), np.uint8)
        for frame in frames:

            # ---------------- find eyes and apply blink ---------------- #
            # for getting specific parts of face
            landmarks = dlib_predict(grey_camera_feed, frame)

            # points of right and left eye
            right_eye_blink = blink([36, 37, 38, 39, 40, 41], landmarks)
            left_eye_blink = blink([42, 43, 44, 45, 46, 47], landmarks)

            if (right_eye_blink > 3) and (left_eye_blink > 3) or (right_eye_blink > 3) or (left_eye_blink > 3):
                lookingUpAllowed = False
                # print(right_eye_blink)
            else:
                lookingUpAllowed = True
                # print(right_eye_blink)

            # uncomment when running
            if (right_eye_blink > 6) and (left_eye_blink > 6):
                time.sleep(0.5)
                count += 1
                if count % 2 == 0:
                    lookingdownallowedgui()
                    lookingDownAllowed = True
                else:
                    lookingdownnotallowedgui()
                    lookingDownAllowed = False
                #print(count)
                #print(lookingDownAllowed)

            if not lookingDownAllowed:
                if 6.5 > left_eye_blink > 5 > right_eye_blink:
                    time.sleep(1)
                    leftWink = True
                else:
                    leftWink = False

                if 6.5 > right_eye_blink > 5 > left_eye_blink:
                    time.sleep(1)
                    rightWink = True
                else:
                    rightWink = False

            '''if (right_eye_blink > 5) and (left_eye_blink > 5) and (right_eye_blink < 8) and (left_eye_blink < 8) \
                    and (right_eye_blink + 0.3 > left_eye_blink) and (right_eye_blink - 0.3 < left_eye_blink) \
                    and (left_eye_blink + 0.3 > right_eye_blink) and (left_eye_blink - 0.3 < right_eye_blink):
                blink_true = False
                leftWink = False
                rightWink = False
                lookingDown = True
                print("down")
            else:
                lookingDown = False'''

            if rightWink:
                cv2.putText(camera_feed, "RIGHT WINK", (50, 150), font, 5, (255, 0, 0))
                print("===RIGHT WINK===")
                # time.sleep(0.5)

            if leftWink:
                cv2.putText(camera_feed, "LEFT WINK", (50, 450), font, 5, (255, 0, 0))
                print("===LEFT WINK===")
                # time.sleep(0.5)

            if blink_true:
                cv2.putText(camera_feed, "BLINK", (50, 300), font, 5, (255, 0, 0))
                # print("===BLINK===")
                # time.sleep(0.9)

            # ---------------- find eyes and apply blink ---------------- #

            # ---------------------------------------------- right eye ---------------------------------------------- #
            # ---------------- landmarks ---------------- #
            right_eye_points = [36, 37, 38, 39, 40, 41]
            right_eye_landmarks = np.array([(landmarks.part(point).x, landmarks.part(point).y)
                                            for point in right_eye_points])
            # cv2.polylines(frame, [right_eye_landmarks], True, (0, 0, 255), 1)
            # ---------------- landmarks ---------------- #

            # ---------------- mask ---------------- #
            RIGHT_height, RIGHT_width, _ = camera_feed.shape
            mask = np.zeros((RIGHT_height, RIGHT_width), np.uint8)
            cv2.polylines(mask, [right_eye_landmarks], True, 255, 2)    # play with the 255
            cv2.fillPoly(mask, [right_eye_landmarks], 255)
            right_eye = cv2.bitwise_and(grey_camera_feed, grey_camera_feed, mask=mask)
            # ---------------- mask ---------------- #

            # ---------------- window and threshold ---------------- #
            min_x = np.min(right_eye_landmarks[:, 0])   # single out points of right eye to put in its own
            max_x = np.max(right_eye_landmarks[:, 0])   # frame by isolating the x, y coordinates around the
            min_y = np.min(right_eye_landmarks[:, 1])   # eye in a new window
            max_y = np.max(right_eye_landmarks[:, 1])

            right_eye_thresholded = right_eye[min_y + 2: max_y - 2, min_x + 10: max_x - 5]
            right_threshold = cv2.adaptiveThreshold(right_eye_thresholded, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                    cv2.THRESH_BINARY_INV, 35, 1)
            try:
                right_eye_frame = cv2.resize(right_threshold, None, fx=10, fy=10)
            except Exception as e:
                pass

            dilated_right_eye = cv2.dilate(right_eye_frame, kernel, iterations=5)
            eroded_right_eye = cv2.erode(dilated_right_eye, kernel, iterations=0)
            # cv2.imshow("Right Eye", eroded_right_eye)

            dilated_right_eye_UD = cv2.dilate(right_eye_frame, kernel, iterations=2)
            eroded_right_eye_UD = cv2.erode(dilated_right_eye_UD, kernel, iterations=14)
            # cv2.imshow("Right Eye UD", eroded_right_eye_UD)
            # ---------------- window and threshold ---------------- #

            # ---------------- divide window and count whiteness ---------------- #
            # left/right
            RIGHT_height, RIGHT_width = eroded_right_eye.shape
            RIGHT_left_side_threshold = eroded_right_eye[0: RIGHT_height, 0: int(RIGHT_width / 2)]
            RIGHT_right_side_threshold = eroded_right_eye[0: RIGHT_height, int(RIGHT_width / 2): RIGHT_width]

            RIGHT_left_side_threshold = cv2.resize(RIGHT_left_side_threshold, None, fx=2, fy=2)
            # cv2.imshow("LEFT OF RIGHT THRESH", RIGHT_left_side_threshold)
            RIGHT_right_side_threshold = cv2.resize(RIGHT_right_side_threshold, None, fx=2, fy=2)
            # cv2.imshow("RIGHT OF RIGHT THRESH", RIGHT_right_side_threshold)

            # get white count
            RIGHT_left_side_white = cv2.countNonZero(RIGHT_left_side_threshold)
            RIGHT_left_side_white = round(RIGHT_left_side_white)
            RIGHT_right_side_white = cv2.countNonZero(RIGHT_right_side_threshold)
            RIGHT_right_side_white = round(RIGHT_right_side_white)

            # cv2.putText(frame, 'RIGHT LEFTNESS: ' + str(RIGHT_left_side_white), (50, 100), font, 2, (255, 0, 0), 3)
            # cv2.putText(frame, 'RIGHT RIGHTNESS: ' + str(RIGHT_right_side_white), (50, 150), font, 2, (255, 0, 0), 3)

            # ---------------------- up/down ---------------------- #
            RIGHT_height_UD, RIGHT_width_UD = eroded_right_eye_UD.shape
            RIGHT_upper_side_threshold_UD = eroded_right_eye_UD[0: int(RIGHT_height_UD / 2), 0: RIGHT_width_UD]
            RIGHT_lower_side_threshold_UD = eroded_right_eye_UD[int(RIGHT_height_UD / 2): RIGHT_height, 0: RIGHT_width]

            RIGHT_upper_side_threshold_UD = cv2.resize(RIGHT_upper_side_threshold_UD, None, fx=1, fy=1)
            # cv2.imshow("UD RIGHT", RIGHT_upper_side_threshold_UD)
            RIGHT_lower_side_threshold_UD = cv2.resize(RIGHT_lower_side_threshold_UD, None, fx=1, fy=1)
            # cv2.imshow("bottom RIGHT", RIGHT_lower_side_threshold_UD)

            # get white count
            RIGHT_upper_side_white_UD = cv2.countNonZero(RIGHT_upper_side_threshold_UD)
            RIGHT_upper_side_white_UD = round(RIGHT_upper_side_white_UD)
            RIGHT_lower_side_white_UD = cv2.countNonZero(RIGHT_lower_side_threshold_UD)
            RIGHT_lower_side_white_UD = round(RIGHT_lower_side_white_UD)
            # ---------------------- up/down ---------------------- #
            # ---------------- divide window and count whiteness ---------------- #

            # ---------------------------------------------- right eye ---------------------------------------------- #

            # ---------------------------------------------- left eye ---------------------------------------------- #
            # ---------------- landmarks ---------------- #
            left_eye_points = [42, 43, 44, 45, 46, 47]
            left_eye_landmarks = np.array([(landmarks.part(point).x, landmarks.part(point).y)
                                           for point in left_eye_points])
            # cv2.polylines(frame, [left_eye_landmarks], True, (0, 0, 255), 1)
            # ---------------- landmarks ---------------- #

            # ---------------- mask ---------------- #
            height, width, _ = camera_feed.shape
            mask = np.zeros((height, width), np.uint8)
            cv2.polylines(mask, [left_eye_landmarks], True, 255, 2)
            cv2.fillPoly(mask, [left_eye_landmarks], 255)
            left_eye = cv2.bitwise_and(grey_camera_feed, grey_camera_feed, mask=mask)
            # ---------------- mask ---------------- #

            # ---------------- window and threshold ---------------- #
            min_x = np.min(left_eye_landmarks[:, 0])
            max_x = np.max(left_eye_landmarks[:, 0])
            min_y = np.min(left_eye_landmarks[:, 1])
            max_y = np.max(left_eye_landmarks[:, 1])

            left_eye_thresholded = left_eye[min_y + 2: max_y - 2, min_x + 10: max_x - 5]
            left_threshold = cv2.adaptiveThreshold(left_eye_thresholded, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                   cv2.THRESH_BINARY_INV, 35, 1)
            try:
                left_eye_frame = cv2.resize(left_threshold, None, fx=10, fy=10)
            except Exception as e:
                pass

            dilated_left_eye_LR = cv2.dilate(left_eye_frame, kernel, iterations=5)
            eroded_left_eye_LR = cv2.erode(dilated_left_eye_LR, kernel, iterations=0)
            # cv2.imshow("Left Eye LR", eroded_left_eye_LR)

            dilated_left_eye_UD = cv2.dilate(left_eye_frame, kernel, iterations=2)
            eroded_left_eye_UD = cv2.erode(dilated_left_eye_UD, kernel, iterations=14)
            # cv2.imshow("Left Eye UD", eroded_left_eye_UD)
            # ---------------- window and threshold ---------------- #

            # ---------------- divide window and count whiteness ---------------- #
            LEFT_height, LEFT_width = eroded_left_eye_LR.shape
            LEFT_left_side_threshold = eroded_left_eye_LR[0: LEFT_height, 0: int((LEFT_width/2))]
            LEFT_right_side_threshold = eroded_left_eye_LR[0: LEFT_height, int(LEFT_width/2): LEFT_width]

            LEFT_left_side_threshold = cv2.resize(LEFT_left_side_threshold, None, fx=3, fy=3)
            # cv2.imshow("LEFT left THRESH", LEFT_left_side_threshold)
            LEFT_right_side_threshold = cv2.resize(LEFT_right_side_threshold, None, fx=3, fy=3)
            # cv2.imshow("RIGHT left THRESH", LEFT_right_side_threshold)

            # get white count
            LEFT_left_side_white = cv2.countNonZero(LEFT_left_side_threshold)
            LEFT_left_side_white = round(LEFT_left_side_white)
            LEFT_right_side_white = cv2.countNonZero(LEFT_right_side_threshold)
            LEFT_right_side_white = round(LEFT_right_side_white)

            # cv2.putText(frame, 'LEFT LEFTNESS: ' + str(LEFT_left_side_white), (50, 100), font, 2, (255, 0, 0), 3)
            # cv2.putText(frame, 'LEFT RIGHTNESS: ' + str(LEFT_right_side_white), (50, 150), font, 2, (255, 0, 0), 3)

            # ---------------------- up/down ---------------------- #
            LEFT_height_UD, LEFT_width_UD = eroded_left_eye_UD.shape
            LEFT_upper_side_threshold_UD = eroded_left_eye_UD[0: int(RIGHT_height_UD / 2), 0: RIGHT_width_UD]
            LEFT_lower_side_threshold_UD = eroded_left_eye_UD[int(RIGHT_height_UD / 2): RIGHT_height, 0: RIGHT_width]

            LEFT_upper_side_threshold_UD = cv2.resize(LEFT_upper_side_threshold_UD, None, fx=3, fy=3)
            # cv2.imshow("UD LEFT", LEFT_upper_side_threshold_UD)
            try:
                LEFT_lower_side_threshold_UD = cv2.resize(LEFT_lower_side_threshold_UD, None, fx=3, fy=3)
            except Exception as e:
                pass
            # cv2.imshow("bottom LEFT", LEFT_lower_side_threshold_UD)

            # get white count
            left_upper_side_white_UD = cv2.countNonZero(LEFT_upper_side_threshold_UD)
            left_upper_side_white_UD = round(left_upper_side_white_UD)
            left_lower_side_white_UD = cv2.countNonZero(LEFT_lower_side_threshold_UD)
            left_lower_side_white_UD = round(left_lower_side_white_UD)
            # ---------------------- up/down ---------------------- #
            # ---------------- divide window and count whiteness ---------------- #
            # ---------------------------------------------- left eye ---------------------------------------------- #

            # ---------------- looking left/right ---------------- #

            if round((RIGHT_right_side_white + LEFT_right_side_white) / 2) > \
                    round(2*((LEFT_left_side_white+RIGHT_left_side_white) / 2)):
                cv2.putText(camera_feed, 'LOOKING LEFT', (50, 250), font, 2, (255, 0, 0), 3)
                lookingRight = False
                lookingDown = False
                lookingLeft = True
                lookingStraight = False
                lookingUp = False
                # print("====left====")

            elif round((LEFT_left_side_white + RIGHT_left_side_white) / 2) > \
                    round(2*((LEFT_right_side_white + RIGHT_right_side_white) / 2)):
                cv2.putText(camera_feed, 'LOOKING RIGHT', (50, 350), font, 2, (255, 0, 0), 3)
                lookingRight = True
                lookingDown = False
                lookingLeft = False
                lookingStraight = False
                lookingUp = False
                # print("====right====")

            elif round((left_upper_side_white_UD + RIGHT_upper_side_white_UD) / 2) > \
                    round(4 * ((left_lower_side_white_UD + RIGHT_lower_side_white_UD) / 2)):
                if lookingUpAllowed:
                    cv2.putText(camera_feed, 'UP', (150, 250), font, 2, (255, 0, 0), 3)
                    lookingRight = False
                    lookingDown = False
                    lookingLeft = False
                    lookingStraight = False
                    lookingUp = True
                    # print("====up====")

            elif lookingDownAllowed and (LEFT_width > (4 * LEFT_height)) and (RIGHT_width > (4 * RIGHT_height)) and \
                    (LEFT_width < (8 * LEFT_height)) and (RIGHT_width < (8 * RIGHT_height)): #and \
                    #(LEFT_width + 1 <= RIGHT_width) and (RIGHT_width + 1 <= LEFT_width) and \
                    #(LEFT_height + 1 <= RIGHT_height) and (LEFT_height + 1 <= RIGHT_height):
                cv2.putText(camera_feed, 'DOWN', (150, 450), font, 2, (255, 0, 0), 3)
                lookingRight = False
                lookingDown = True
                lookingLeft = False
                lookingStraight = False
                lookingUp = False

                leftWink = False
                rightWink = False
                # print("====down====")

            else:
                cv2.putText(camera_feed, 'LOOKING STRAIGHT', (50, 300), font, 2, (255, 0, 0), 3)
                lookingRight = False
                lookingLeft = False
                lookingStraight = True
                lookingUp = False
                lookingDown = False

            # ---------------- looking left/right ---------------- #

            # ---------------- mouse control ---------------- #

            if not speech_running:
                if not keyboard_running:
                    if lookingRight:
                        moveMouseRight()

                    if lookingLeft:
                        moveMouseLeft()

                    if lookingDown and lookingDownAllowed:
                        moveMouseDown()

                    if lookingUp and lookingUpAllowed:
                        moveMouseUp()

                    if leftWink:
                        mouseLeftClick()

                    if rightWink:
                        mouseRightClick()

            # ---------------- mouse control ---------------- #

            # ---------------- mouth open ---------------- #

            mouth_top = (landmarks.part(61).x, landmarks.part(61).y)
            mouth_bottom = (landmarks.part(67).x, landmarks.part(67).y)
            mouth_left = (landmarks.part(60).x, landmarks.part(60).y)
            mouth_right = (landmarks.part(64).x, landmarks.part(64).y)

            mouth_open_line_ver = cv2.line(camera_feed, mouth_top, mouth_bottom, (0, 0, 255), 1)
            mouth_open_line_hor = cv2.line(camera_feed, mouth_left, mouth_right, (0, 0, 255), 1)

            mouth_height = hypot((mouth_top[0] - mouth_bottom[0]), (mouth_top[1] - mouth_bottom[1]))
            mouth_width = hypot((mouth_left[0] - mouth_right[0]), (mouth_left[1] - mouth_right[1]))
            mouth_size = mouth_height / mouth_width
            # print(mouth_size)
            if mouth_size > 0.38:
                cv2.putText(camera_feed, 'MOUTH OPEN', (50, 450), font, 2, (255, 0, 0), 3)
                mouth_open = True
            else:
                mouth_open = False

            if mouth_has_opened:
                if mouth_open:
                    cv2.destroyWindow('keyboard')
                    keyboard_running = False
                    mouth_has_opened = False
                    mouth_open = False
                    time.sleep(1)

            if mouth_open:
                keyboard_running = True
                p1 = threading.Thread(target=eye_keyboard, args=())
                p1.start()
                time.sleep(1)
                mouth_has_opened = True
                mouth_open = False

        if keyboard.is_pressed('q'):  # if key 'q' is pressed
            break

        # uncomment for binary images
        '''cv2.imshow("Right Eye", eroded_right_eye)
        cv2.imshow("Right Eye UD", eroded_right_eye_UD)'''

        '''cv2.imshow("LEFT OF RIGHT THRESH", RIGHT_left_side_threshold)
        cv2.imshow("RIGHT OF RIGHT THRESH", RIGHT_right_side_threshold)'''

        '''cv2.imshow("UP RIGHT", RIGHT_upper_side_threshold_UD)
        cv2.imshow("bottom RIGHT", RIGHT_lower_side_threshold_UD)'''

        cv2.imshow("Facial Detection", camera_feed)  # open webcam

        cv2.waitKey(1)
    cap.release()


def eye_keyboard():
    # initial
    ESC_highlighted = True
    ONE_highlighted = False
    TWO_highlighted = False
    THREE_highlighted = False
    FOUR_highlighted = False
    FIVE_highlighted = False
    SIX_highlighted = False
    SEVEN_highlighted = False
    EIGHT_highlighted = False
    NINE_highlighted = False
    ZERO_highlighted = False

    TAB_highlighted = False
    Q_highlighted = False
    W_highlighted = False
    E_highlighted = False
    R_highlighted = False
    T_highlighted = False
    Y_highlighted = False
    U_highlighted = False
    I_highlighted = False
    O_highlighted = False
    P_highlighted = False

    CAPS_highlighted = False
    A_highlighted = False
    S_highlighted = False
    D_highlighted = False
    F_highlighted = False
    G_highlighted = False
    H_highlighted = False
    J_highlighted = False
    K_highlighted = False
    L_highlighted = False
    RET_highlighted = False

    SHIFT_highlighted = False
    Z_highlighted = False
    X_highlighted = False
    C_highlighted = False
    V_highlighted = False
    B_highlighted = False
    N_highlighted = False
    M_highlighted = False
    COMMA_highlighted = False
    PERIOD_highlighted = False

    MINUS_highlighted = False
    EQUALS_highlighted = False
    SQRBRACKOPEN_highlighted = False
    SQEBRACKCLOSE_highlighted = False
    SEMICOLON_highlighted = False
    SINGQUO_highlighted = False

    HASH_highlighted = False
    FORWARDSLASH_highlighted = False
    BACKSLASH_highlighted = False
    CTRL_highlighted = False
    SPACE_highlighted = False
    DELETE_highlighted = False

    SPEECH_highlighted = False

    SHIFT_PRESSED = False
    CAPS_ON = False

    # 2d array for keyboard
    rows, cols = 2, 2
    arr = [[0 for x in range(rows)] for y in range(cols)]
    global x, y
    x, y = 0, 0

    if not speech_running:
        while keyboard_running:
            window = np.zeros((480, 880, 3), np.uint8)

            # --------------------------------------------- GUI --------------------------------------------- #
            # ---------------------- FIRST ROW ---------------------- #
            # ---------- ESC ---------- #
            if ESC_highlighted:
                window = cv2.circle(window, (40, 40), 40, (255, 255, 0), -1)
                cv2.putText(window, 'Esc', (10, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.press('escape')
                    time.sleep(0.5)

            else:
                window = cv2.circle(window, (40, 40), 35, (255, 0, 0), -1)
                cv2.putText(window, 'Esc', (10, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- ESC ---------- #

            # ---------- 1 ---------- #
            if ONE_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (120, 40), 40, (255, 255, 0), -1)
                cv2.putText(window, '1', (110, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('1', interval=0.1)
                    time.sleep(0.5)

            elif not ONE_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (120, 40), 35, (255, 0, 0), -1)
                cv2.putText(window, '1', (110, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if ONE_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (120, 40), 40, (255, 255, 0), -1)
                cv2.putText(window, '!', (110, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('!', interval=0.1)
                    time.sleep(0.5)

            elif not ONE_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (120, 40), 35, (255, 0, 0), -1)
                cv2.putText(window, '!', (110, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- 1 ---------- #

            # ---------- 2 ---------- #
            if TWO_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (200, 40), 40, (255, 255, 0), -1)
                cv2.putText(window, '2', (190, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('2', interval=0.1)
                    time.sleep(0.5)

            elif not TWO_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (200, 40), 35, (255, 0, 0), -1)
                cv2.putText(window, '2', (190, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if TWO_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (200, 40), 40, (255, 255, 0), -1)
                cv2.putText(window, '"', (190, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('"', interval=0.1)
                    time.sleep(0.5)

            elif not TWO_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (200, 40), 35, (255, 0, 0), -1)
                cv2.putText(window, '"', (190, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- 2 ---------- #

            # ---------- 3 ---------- #
            if THREE_highlighted:
                window = cv2.circle(window, (280, 40), 40, (255, 255, 0), -1)
                cv2.putText(window, '3', (270, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('3', interval=0.1)
                    time.sleep(0.5)

            else:
                window = cv2.circle(window, (280, 40), 35, (255, 0, 0), -1)
                cv2.putText(window, '3', (270, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- 3 ---------- #

            # ---------- 4 ---------- #
            if FOUR_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (360, 40), 40, (255, 255, 0), -1)
                cv2.putText(window, '4', (350, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('4', interval=0.1)
                    time.sleep(0.5)

            elif not FOUR_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (360, 40), 35, (255, 0, 0), -1)
                cv2.putText(window, '4', (350, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if FOUR_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (360, 40), 40, (255, 255, 0), -1)
                cv2.putText(window, '$', (350, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('$', interval=0.1)
                    time.sleep(0.5)

            elif not FOUR_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (360, 40), 35, (255, 0, 0), -1)
                cv2.putText(window, '$', (350, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- 4 ---------- #

            # ---------- 5 ---------- #
            if FIVE_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (440, 40), 40, (255, 255, 0), -1)
                cv2.putText(window, '5', (430, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('5', interval=0.1)
                    time.sleep(0.5)

            elif not FIVE_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (440, 40), 35, (255, 0, 0), -1)
                cv2.putText(window, '5', (430, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if FIVE_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (440, 40), 40, (255, 255, 0), -1)
                cv2.putText(window, '%', (430, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('%', interval=0.1)
                    time.sleep(0.5)

            elif not FIVE_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (440, 40), 35, (255, 0, 0), -1)
                cv2.putText(window, '%', (430, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- 5 ---------- #

            # ---------- 6 ---------- #
            if SIX_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (520, 40), 40, (255, 255, 0), -1)
                cv2.putText(window, '6', (510, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('6', interval=0.1)
                    time.sleep(0.5)

            elif not SIX_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (520, 40), 35, (255, 0, 0), -1)
                cv2.putText(window, '6', (510, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if SIX_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (520, 40), 40, (255, 255, 0), -1)
                cv2.putText(window, '^', (510, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('^', interval=0.1)
                    time.sleep(0.5)

            elif not SIX_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (520, 40), 35, (255, 0, 0), -1)
                cv2.putText(window, '^', (510, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- 6 ---------- #

            # ---------- 7 ---------- #
            if SEVEN_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (600, 40), 40, (255, 255, 0), -1)
                cv2.putText(window, '7', (590, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('7', interval=0.1)
                    time.sleep(0.5)

            elif not SEVEN_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (600, 40), 35, (255, 0, 0), -1)
                cv2.putText(window, '7', (590, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if SEVEN_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (600, 40), 40, (255, 255, 0), -1)
                cv2.putText(window, '&', (590, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('&', interval=0.1)
                    time.sleep(0.5)

            elif not SEVEN_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (600, 40), 35, (255, 0, 0), -1)
                cv2.putText(window, '&', (590, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- 7 ---------- #

            # ---------- 8 ---------- #
            if EIGHT_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (680, 40), 40, (255, 255, 0), -1)
                cv2.putText(window, '8', (670, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('8', interval=0.1)
                    time.sleep(0.5)

            elif not EIGHT_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (680, 40), 35, (255, 0, 0), -1)
                cv2.putText(window, '8', (670, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if EIGHT_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (680, 40), 40, (255, 255, 0), -1)
                cv2.putText(window, '*', (670, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('*', interval=0.1)
                    time.sleep(0.5)

            elif not EIGHT_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (680, 40), 35, (255, 0, 0), -1)
                cv2.putText(window, '*', (670, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- 8 ---------- #

            # ---------- 9 ---------- #
            if NINE_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (760, 40), 40, (255, 255, 0), -1)
                cv2.putText(window, '9', (750, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('9', interval=0.1)
                    time.sleep(0.5)

            elif not NINE_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (760, 40), 35, (255, 0, 0), -1)
                cv2.putText(window, '9', (750, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if NINE_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (760, 40), 40, (255, 255, 0), -1)
                cv2.putText(window, '(', (750, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('(', interval=0.1)
                    time.sleep(0.5)

            elif not NINE_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (760, 40), 35, (255, 0, 0), -1)
                cv2.putText(window, '(', (750, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- 9 ---------- #

            # ---------- 0 ---------- #
            if ZERO_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (840, 40), 40, (255, 255, 0), -1)
                cv2.putText(window, '0', (830, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('0', interval=0.1)
                    time.sleep(0.5)

            elif not ZERO_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (840, 40), 35, (255, 0, 0), -1)
                cv2.putText(window, '0', (830, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if ZERO_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (840, 40), 40, (255, 255, 0), -1)
                cv2.putText(window, ')', (830, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite(')', interval=0.1)
                    time.sleep(0.5)

            elif not ZERO_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (840, 40), 35, (255, 0, 0), -1)
                cv2.putText(window, ')', (830, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- 0 ---------- #
            # ---------------------- FIRST ROW ---------------------- #

            # ---------------------- SECOND ROW ---------------------- #
            # ---------- TAB ---------- #
            if TAB_highlighted:
                window = cv2.circle(window, (40, 120), 40, (255, 255, 0), -1)
                cv2.putText(window, 'Tab', (10, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.press('tab')
                    time.sleep(0.5)

            else:
                window = cv2.circle(window, (40, 120), 35, (255, 0, 0), -1)
                cv2.putText(window, 'Tab', (10, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- TAB ---------- #

            # ---------- Q ---------- #
            if Q_highlighted and CAPS_ON:
                window = cv2.circle(window, (120, 120), 40, (255, 255, 0), -1)
                cv2.putText(window, 'Q', (110, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('Q', interval=0.1)
                    time.sleep(0.5)

            elif not Q_highlighted and CAPS_ON:
                window = cv2.circle(window, (120, 120), 35, (255, 0, 0), -1)
                cv2.putText(window, 'Q', (110, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if Q_highlighted and not CAPS_ON:
                window = cv2.circle(window, (120, 120), 40, (255, 255, 0), -1)
                cv2.putText(window, 'q', (110, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('q', interval=0.1)
                    time.sleep(0.5)

            elif not Q_highlighted and not CAPS_ON:
                window = cv2.circle(window, (120, 120), 35, (255, 0, 0), -1)
                cv2.putText(window, 'q', (110, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- Q ---------- #

            # ---------- W ---------- #
            if W_highlighted and CAPS_ON:
                window = cv2.circle(window, (200, 120), 40, (255, 255, 0), -1)
                cv2.putText(window, 'W', (190, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('W', interval=0.1)
                    time.sleep(0.5)

            elif not W_highlighted and CAPS_ON:
                window = cv2.circle(window, (200, 120), 35, (255, 0, 0), -1)
                cv2.putText(window, 'W', (190, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if W_highlighted and not CAPS_ON:
                window = cv2.circle(window, (200, 120), 40, (255, 255, 0), -1)
                cv2.putText(window, 'w', (190, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('w', interval=0.1)
                    time.sleep(0.5)

            elif not W_highlighted and not CAPS_ON:
                window = cv2.circle(window, (200, 120), 35, (255, 0, 0), -1)
                cv2.putText(window, 'w', (190, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- W ---------- #

            # ---------- E ---------- #
            if E_highlighted and CAPS_ON:
                window = cv2.circle(window, (280, 120), 40, (255, 255, 0), -1)
                cv2.putText(window, 'E', (270, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('E', interval=0.1)
                    time.sleep(0.5)

            elif not E_highlighted and CAPS_ON:
                window = cv2.circle(window, (280, 120), 35, (255, 0, 0), -1)
                cv2.putText(window, 'E', (270, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if E_highlighted and not CAPS_ON:
                window = cv2.circle(window, (280, 120), 40, (255, 255, 0), -1)
                cv2.putText(window, 'e', (270, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('e', interval=0.1)
                    time.sleep(0.5)

            elif not E_highlighted and not CAPS_ON:
                window = cv2.circle(window, (280, 120), 35, (255, 0, 0), -1)
                cv2.putText(window, 'e', (270, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- E ---------- #

            # ---------- R ---------- #
            if R_highlighted and CAPS_ON:
                window = cv2.circle(window, (360, 120), 40, (255, 255, 0), -1)
                cv2.putText(window, 'R', (350, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('R', interval=0.1)
                    time.sleep(0.5)

            elif not R_highlighted and CAPS_ON:
                window = cv2.circle(window, (360, 120), 35, (255, 0, 0), -1)
                cv2.putText(window, 'R', (350, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if R_highlighted and not CAPS_ON:
                window = cv2.circle(window, (360, 120), 40, (255, 255, 0), -1)
                cv2.putText(window, 'r', (350, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('r', interval=0.1)
                    time.sleep(0.5)

            elif not R_highlighted and not CAPS_ON:
                window = cv2.circle(window, (360, 120), 35, (255, 0, 0), -1)
                cv2.putText(window, 'r', (350, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- R ---------- #

            # ---------- T ---------- #
            if T_highlighted and CAPS_ON:
                window = cv2.circle(window, (440, 120), 40, (255, 255, 0), -1)
                cv2.putText(window, 'T', (430, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('T', interval=0.1)
                    time.sleep(0.5)

            elif not T_highlighted and CAPS_ON:
                window = cv2.circle(window, (440, 120), 35, (255, 0, 0), -1)
                cv2.putText(window, 'T', (430, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if T_highlighted and not CAPS_ON:
                window = cv2.circle(window, (440, 120), 40, (255, 255, 0), -1)
                cv2.putText(window, 't', (430, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('t', interval=0.1)
                    time.sleep(0.5)

            elif not T_highlighted and not CAPS_ON:
                window = cv2.circle(window, (440, 120), 35, (255, 0, 0), -1)
                cv2.putText(window, 't', (430, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- T ---------- #

            # ---------- Y ---------- #
            if Y_highlighted and CAPS_ON:
                window = cv2.circle(window, (520, 120), 40, (255, 255, 0), -1)
                cv2.putText(window, 'Y', (510, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('Y', interval=0.1)
                    time.sleep(0.5)

            if not Y_highlighted and CAPS_ON:
                window = cv2.circle(window, (520, 120), 35, (255, 0, 0), -1)
                cv2.putText(window, 'Y', (510, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if Y_highlighted and not CAPS_ON:
                window = cv2.circle(window, (520, 120), 40, (255, 255, 0), -1)
                cv2.putText(window, 'y', (510, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('y', interval=0.1)
                    time.sleep(0.5)

            if not Y_highlighted and not CAPS_ON:
                window = cv2.circle(window, (520, 120), 35, (255, 0, 0), -1)
                cv2.putText(window, 'y', (510, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- Y ---------- #

            # ---------- U ---------- #
            if U_highlighted and CAPS_ON:
                window = cv2.circle(window, (600, 120), 40, (255, 255, 0), -1)
                cv2.putText(window, 'U', (590, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('U', interval=0.1)
                    time.sleep(0.5)

            if not U_highlighted and CAPS_ON:
                window = cv2.circle(window, (600, 120), 35, (255, 0, 0), -1)
                cv2.putText(window, 'U', (590, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if U_highlighted and not CAPS_ON:
                window = cv2.circle(window, (600, 120), 40, (255, 255, 0), -1)
                cv2.putText(window, 'u', (590, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('u', interval=0.1)
                    time.sleep(0.5)

            if not U_highlighted and not CAPS_ON:
                window = cv2.circle(window, (600, 120), 35, (255, 0, 0), -1)
                cv2.putText(window, 'u', (590, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- U ---------- #

            # ---------- i ---------- #
            if I_highlighted and CAPS_ON:
                window = cv2.circle(window, (680, 120), 40, (255, 255, 0), -1)
                cv2.putText(window, 'I', (670, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('I', interval=0.1)
                    time.sleep(0.5)

            if not I_highlighted and CAPS_ON:
                window = cv2.circle(window, (680, 120), 35, (255, 0, 0), -1)
                cv2.putText(window, 'I', (670, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if I_highlighted and not CAPS_ON:
                window = cv2.circle(window, (680, 120), 40, (255, 255, 0), -1)
                cv2.putText(window, 'i', (670, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('i', interval=0.1)
                    time.sleep(0.5)

            if not I_highlighted and not CAPS_ON:
                window = cv2.circle(window, (680, 120), 35, (255, 0, 0), -1)
                cv2.putText(window, 'i', (670, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- I ---------- #

            # ---------- O ---------- #
            if O_highlighted and CAPS_ON:
                window = cv2.circle(window, (760, 120), 40, (255, 255, 0), -1)
                cv2.putText(window, 'O', (750, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('O', interval=0.1)
                    time.sleep(0.5)

            if not O_highlighted and CAPS_ON:
                window = cv2.circle(window, (760, 120), 35, (255, 0, 0), -1)
                cv2.putText(window, 'O', (750, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if O_highlighted and not CAPS_ON:
                window = cv2.circle(window, (760, 120), 40, (255, 255, 0), -1)
                cv2.putText(window, 'o', (750, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('o', interval=0.1)
                    time.sleep(0.5)

            if not O_highlighted and not CAPS_ON:
                window = cv2.circle(window, (760, 120), 35, (255, 0, 0), -1)
                cv2.putText(window, 'o', (750, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- O ---------- #

            # ---------- P ---------- #
            if P_highlighted and CAPS_ON:
                window = cv2.circle(window, (840, 120), 40, (255, 255, 0), -1)
                cv2.putText(window, 'P', (830, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('P', interval=0.1)
                    time.sleep(0.5)

            if not P_highlighted and CAPS_ON:
                window = cv2.circle(window, (840, 120), 35, (255, 0, 0), -1)
                cv2.putText(window, 'P', (830, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if P_highlighted and not CAPS_ON:
                window = cv2.circle(window, (840, 120), 40, (255, 255, 0), -1)
                cv2.putText(window, 'p', (830, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('p', interval=0.1)
                    time.sleep(0.5)

            if not P_highlighted and not CAPS_ON:
                window = cv2.circle(window, (840, 120), 35, (255, 0, 0), -1)
                cv2.putText(window, 'p', (830, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- P ---------- #
            # ---------------------- SECOND ROW ---------------------- #

            # ---------------------- THIRD ROW ---------------------- #
            # ---------- CAPS ---------- #
            if CAPS_highlighted:
                window = cv2.circle(window, (40, 200), 40, (255, 255, 0), -1)
                cv2.putText(window, 'Cap', (10, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    CAPS_ON = True
                    time.sleep(0.5)
                if CAPS_ON:
                    if rightWink:
                        CAPS_ON = False
                        time.sleep(0.5)

            else:
                window = cv2.circle(window, (40, 200), 35, (255, 0, 0), -1)
                cv2.putText(window, 'Cap', (10, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- CAPS ---------- #

            # ---------- A ---------- #
            if A_highlighted and CAPS_ON:
                window = cv2.circle(window, (120, 200), 40, (255, 255, 0), -1)
                cv2.putText(window, 'A', (110, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('A', interval=0.1)
                    time.sleep(0.5)

            if not A_highlighted and CAPS_ON:
                window = cv2.circle(window, (120, 200), 35, (255, 0, 0), -1)
                cv2.putText(window, 'A', (110, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if A_highlighted and not CAPS_ON:
                window = cv2.circle(window, (120, 200), 40, (255, 255, 0), -1)
                cv2.putText(window, 'a', (110, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('a', interval=0.1)
                    time.sleep(0.5)

            if not A_highlighted and not CAPS_ON:
                window = cv2.circle(window, (120, 200), 35, (255, 0, 0), -1)
                cv2.putText(window, 'a', (110, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- A ---------- #

            # ---------- S ---------- #
            if S_highlighted and CAPS_ON:
                window = cv2.circle(window, (200, 200), 40, (255, 255, 0), -1)
                cv2.putText(window, 'S', (190, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('S', interval=0.1)
                    time.sleep(0.5)

            if not S_highlighted and CAPS_ON:
                window = cv2.circle(window, (200, 200), 35, (255, 0, 0), -1)
                cv2.putText(window, 'S', (190, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if S_highlighted and not CAPS_ON:
                window = cv2.circle(window, (200, 200), 40, (255, 255, 0), -1)
                cv2.putText(window, 's', (190, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('s', interval=0.1)
                    time.sleep(0.5)

            if not S_highlighted and not CAPS_ON:
                window = cv2.circle(window, (200, 200), 35, (255, 0, 0), -1)
                cv2.putText(window, 's', (190, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- S ---------- #

            # ---------- D ---------- #
            if D_highlighted and CAPS_ON:
                window = cv2.circle(window, (280, 200), 40, (255, 255, 0), -1)
                cv2.putText(window, 'D', (270, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('D', interval=0.1)
                    time.sleep(0.5)

            if not D_highlighted and CAPS_ON:
                window = cv2.circle(window, (280, 200), 35, (255, 0, 0), -1)
                cv2.putText(window, 'D', (270, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if D_highlighted and not CAPS_ON:
                window = cv2.circle(window, (280, 200), 40, (255, 255, 0), -1)
                cv2.putText(window, 'd', (270, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('d', interval=0.1)
                    time.sleep(0.5)

            if not D_highlighted and not CAPS_ON:
                window = cv2.circle(window, (280, 200), 35, (255, 0, 0), -1)
                cv2.putText(window, 'd', (270, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- D ---------- #

            # ---------- F ---------- #
            if F_highlighted and CAPS_ON:
                window = cv2.circle(window, (360, 200), 40, (255, 255, 0), -1)
                cv2.putText(window, 'F', (350, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('F', interval=0.1)
                    time.sleep(0.5)

            if not F_highlighted and CAPS_ON:
                window = cv2.circle(window, (360, 200), 35, (255, 0, 0), -1)
                cv2.putText(window, 'F', (350, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if F_highlighted and not CAPS_ON:
                window = cv2.circle(window, (360, 200), 40, (255, 255, 0), -1)
                cv2.putText(window, 'f', (350, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('f', interval=0.1)
                    time.sleep(0.5)

            if not F_highlighted and not CAPS_ON:
                window = cv2.circle(window, (360, 200), 35, (255, 0, 0), -1)
                cv2.putText(window, 'f', (350, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- F ---------- #

            # ---------- G ---------- #
            if G_highlighted and CAPS_ON:
                window = cv2.circle(window, (440, 200), 40, (255, 255, 0), -1)
                cv2.putText(window, 'G', (430, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('G', interval=0.1)
                    time.sleep(0.5)

            if not G_highlighted and CAPS_ON:
                window = cv2.circle(window, (440, 200), 35, (255, 0, 0), -1)
                cv2.putText(window, 'G', (430, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if G_highlighted and not CAPS_ON:
                window = cv2.circle(window, (440, 200), 40, (255, 255, 0), -1)
                cv2.putText(window, 'g', (430, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('g', interval=0.1)
                    time.sleep(0.5)

            if not G_highlighted and not CAPS_ON:
                window = cv2.circle(window, (440, 200), 35, (255, 0, 0), -1)
                cv2.putText(window, 'g', (430, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- G ---------- #

            # ---------- H ---------- #
            if H_highlighted and CAPS_ON:
                window = cv2.circle(window, (520, 200), 40, (255, 255, 0), -1)
                cv2.putText(window, 'H', (510, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('H', interval=0.1)
                    time.sleep(0.5)

            if not H_highlighted and CAPS_ON:
                window = cv2.circle(window, (520, 200), 35, (255, 0, 0), -1)
                cv2.putText(window, 'H', (510, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if H_highlighted and not CAPS_ON:
                window = cv2.circle(window, (520, 200), 40, (255, 255, 0), -1)
                cv2.putText(window, 'h', (510, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('h', interval=0.1)
                    time.sleep(0.5)

            if not H_highlighted and not CAPS_ON:
                window = cv2.circle(window, (520, 200), 35, (255, 0, 0), -1)
                cv2.putText(window, 'h', (510, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- H ---------- #

            # ---------- J ---------- #
            if J_highlighted and CAPS_ON:
                window = cv2.circle(window, (600, 200), 40, (255, 255, 0), -1)
                cv2.putText(window, 'J', (590, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('J', interval=0.1)
                    time.sleep(0.5)

            if not J_highlighted and CAPS_ON:
                window = cv2.circle(window, (600, 200), 35, (255, 0, 0), -1)
                cv2.putText(window, 'J', (590, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if J_highlighted and not CAPS_ON:
                window = cv2.circle(window, (600, 200), 40, (255, 255, 0), -1)
                cv2.putText(window, 'j', (590, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('j', interval=0.1)
                    time.sleep(0.5)

            if not J_highlighted and not CAPS_ON:
                window = cv2.circle(window, (600, 200), 35, (255, 0, 0), -1)
                cv2.putText(window, 'j', (590, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- J ---------- #

            # ---------- K ---------- #
            if K_highlighted and CAPS_ON:
                window = cv2.circle(window, (680, 200), 40, (255, 255, 0), -1)
                cv2.putText(window, 'K', (670, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('K', interval=0.1)
                    time.sleep(0.5)

            if not K_highlighted and CAPS_ON:
                window = cv2.circle(window, (680, 200), 35, (255, 0, 0), -1)
                cv2.putText(window, 'K', (670, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if K_highlighted and not CAPS_ON:
                window = cv2.circle(window, (680, 200), 40, (255, 255, 0), -1)
                cv2.putText(window, 'k', (670, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('k', interval=0.1)
                    time.sleep(0.5)

            if not K_highlighted and not CAPS_ON:
                window = cv2.circle(window, (680, 200), 35, (255, 0, 0), -1)
                cv2.putText(window, 'k', (670, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- K ---------- #

            # ---------- L ---------- #
            if L_highlighted and CAPS_ON:
                window = cv2.circle(window, (760, 200), 40, (255, 255, 0), -1)
                cv2.putText(window, 'L', (750, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('L', interval=0.1)
                    time.sleep(0.5)

            if not L_highlighted and CAPS_ON:
                window = cv2.circle(window, (760, 200), 35, (255, 0, 0), -1)
                cv2.putText(window, 'L', (750, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if L_highlighted and not CAPS_ON:
                window = cv2.circle(window, (760, 200), 40, (255, 255, 0), -1)
                cv2.putText(window, 'l', (750, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('l', interval=0.1)
                    time.sleep(0.5)

            if not L_highlighted and not CAPS_ON:
                window = cv2.circle(window, (760, 200), 35, (255, 0, 0), -1)
                cv2.putText(window, 'l', (750, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- L ---------- #

            # ---------- ENT ---------- #
            if RET_highlighted:
                window = cv2.circle(window, (840, 200), 40, (255, 255, 0), -1)
                cv2.putText(window, 'Ret', (810, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.press('enter')
                    time.sleep(0.5)

            else:
                window = cv2.circle(window, (840, 200), 35, (255, 0, 0), -1)
                cv2.putText(window, 'Ret', (810, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- ENT ---------- #
            # ---------------------- THIRD ROW ---------------------- #

            # ---------------------- FOURTH ROW ---------------------- #
            # ---------- SHIFT ---------- #
            if SHIFT_highlighted:
                window = cv2.circle(window, (40, 280), 40, (255, 255, 0), -1)
                cv2.putText(window, 'SFT', (10, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    SHIFT_PRESSED = True
                    time.sleep(0.5)
                if SHIFT_PRESSED:
                    if rightWink:
                        SHIFT_PRESSED = False
                        time.sleep(0.5)

            else:
                window = cv2.circle(window, (40, 280), 35, (255, 0, 0), -1)
                cv2.putText(window, 'SFT', (10, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- SHIFT ---------- #

            # ---------- Z ---------- #
            if Z_highlighted and CAPS_ON:
                window = cv2.circle(window, (120, 280), 40, (255, 255, 0), -1)
                cv2.putText(window, 'Z', (110, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('Z', interval=0.1)
                    time.sleep(0.5)

            if not Z_highlighted and CAPS_ON:
                window = cv2.circle(window, (120, 280), 35, (255, 0, 0), -1)
                cv2.putText(window, 'Z', (110, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if Z_highlighted and not CAPS_ON:
                window = cv2.circle(window, (120, 280), 40, (255, 255, 0), -1)
                cv2.putText(window, 'z', (110, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('z', interval=0.1)
                    time.sleep(0.5)

            if not Z_highlighted and not CAPS_ON:
                window = cv2.circle(window, (120, 280), 35, (255, 0, 0), -1)
                cv2.putText(window, 'z', (110, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- Z ---------- #

            # ---------- X ---------- #
            if X_highlighted and CAPS_ON:
                window = cv2.circle(window, (200, 280), 40, (255, 255, 0), -1)
                cv2.putText(window, 'X', (190, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('X', interval=0.1)
                    time.sleep(0.5)

            if not X_highlighted and CAPS_ON:
                window = cv2.circle(window, (200, 280), 35, (255, 0, 0), -1)
                cv2.putText(window, 'X', (190, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if X_highlighted and not CAPS_ON:
                window = cv2.circle(window, (200, 280), 40, (255, 255, 0), -1)
                cv2.putText(window, 'x', (190, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('x', interval=0.1)
                    time.sleep(0.5)

            if not X_highlighted and not CAPS_ON:
                window = cv2.circle(window, (200, 280), 35, (255, 0, 0), -1)
                cv2.putText(window, 'x', (190, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- X ---------- #

            # ---------- C ---------- #
            if C_highlighted and CAPS_ON:
                window = cv2.circle(window, (280, 280), 40, (255, 255, 0), -1)
                cv2.putText(window, 'C', (270, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('C', interval=0.1)
                    time.sleep(0.5)

            if not C_highlighted and CAPS_ON:
                window = cv2.circle(window, (280, 280), 35, (255, 0, 0), -1)
                cv2.putText(window, 'C', (270, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if C_highlighted and not CAPS_ON:
                window = cv2.circle(window, (280, 280), 40, (255, 255, 0), -1)
                cv2.putText(window, 'c', (270, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('c', interval=0.1)
                    time.sleep(0.5)

            if not C_highlighted and not CAPS_ON:
                window = cv2.circle(window, (280, 280), 35, (255, 0, 0), -1)
                cv2.putText(window, 'c', (270, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- C ---------- #

            # ---------- V ---------- #
            if V_highlighted and CAPS_ON:
                window = cv2.circle(window, (360, 280), 40, (255, 255, 0), -1)
                cv2.putText(window, 'V', (350, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('V', interval=0.1)
                    time.sleep(0.5)

            if not V_highlighted and CAPS_ON:
                window = cv2.circle(window, (360, 280), 35, (255, 0, 0), -1)
                cv2.putText(window, 'V', (350, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if V_highlighted and not CAPS_ON:
                window = cv2.circle(window, (360, 280), 40, (255, 255, 0), -1)
                cv2.putText(window, 'v', (350, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('v', interval=0.1)
                    time.sleep(0.5)

            if not V_highlighted and not CAPS_ON:
                window = cv2.circle(window, (360, 280), 35, (255, 0, 0), -1)
                cv2.putText(window, 'v', (350, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- V ---------- #

            # ---------- B ---------- #
            if B_highlighted and CAPS_ON:
                window = cv2.circle(window, (440, 280), 40, (255, 255, 0), -1)
                cv2.putText(window, 'B', (430, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('B', interval=0.1)
                    time.sleep(0.5)

            if not B_highlighted and CAPS_ON:
                window = cv2.circle(window, (440, 280), 35, (255, 0, 0), -1)
                cv2.putText(window, 'B', (430, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if B_highlighted and not CAPS_ON:
                window = cv2.circle(window, (440, 280), 40, (255, 255, 0), -1)
                cv2.putText(window, 'b', (430, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('b', interval=0.1)
                    time.sleep(0.5)

            if not B_highlighted and not CAPS_ON:
                window = cv2.circle(window, (440, 280), 35, (255, 0, 0), -1)
                cv2.putText(window, 'b', (430, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- B ---------- #

            # ---------- N ---------- #
            if N_highlighted and CAPS_ON:
                window = cv2.circle(window, (520, 280), 40, (255, 255, 0), -1)
                cv2.putText(window, 'N', (510, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('N', interval=0.1)
                    time.sleep(0.5)

            if not N_highlighted and CAPS_ON:
                window = cv2.circle(window, (520, 280), 35, (255, 0, 0), -1)
                cv2.putText(window, 'N', (510, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if N_highlighted and not CAPS_ON:
                window = cv2.circle(window, (520, 280), 40, (255, 255, 0), -1)
                cv2.putText(window, 'n', (510, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('n', interval=0.1)
                    time.sleep(0.5)

            if not N_highlighted and not CAPS_ON:
                window = cv2.circle(window, (520, 280), 35, (255, 0, 0), -1)
                cv2.putText(window, 'n', (510, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- N ---------- #

            # ---------- M ---------- #
            if M_highlighted and CAPS_ON:
                window = cv2.circle(window, (600, 280), 40, (255, 255, 0), -1)
                cv2.putText(window, 'M', (590, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('M', interval=0.1)
                    time.sleep(0.5)

            if not M_highlighted and CAPS_ON:
                window = cv2.circle(window, (600, 280), 35, (255, 0, 0), -1)
                cv2.putText(window, 'M', (590, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if M_highlighted and not CAPS_ON:
                window = cv2.circle(window, (600, 280), 40, (255, 255, 0), -1)
                cv2.putText(window, 'm', (590, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('m', interval=0.1)
                    time.sleep(0.5)

            if not M_highlighted and not CAPS_ON:
                window = cv2.circle(window, (600, 280), 35, (255, 0, 0), -1)
                cv2.putText(window, 'm', (590, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- M ---------- #

            # ---------- COMMA ---------- #
            if COMMA_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (680, 280), 40, (255, 255, 0), -1)
                cv2.putText(window, ',', (670, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite(',', interval=0.1)
                    time.sleep(0.5)

            elif not COMMA_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (680, 280), 35, (255, 0, 0), -1)
                cv2.putText(window, ',', (670, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if COMMA_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (680, 280), 40, (255, 255, 0), -1)
                cv2.putText(window, '<', (670, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('<', interval=0.1)
                    time.sleep(0.5)

            elif not COMMA_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (680, 280), 35, (255, 0, 0), -1)
                cv2.putText(window, '<', (670, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- COMMA ---------- #

            # ---------- PERIOD ---------- #
            if PERIOD_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (760, 280), 40, (255, 255, 0), -1)
                cv2.putText(window, '.', (750, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('.', interval=0.1)
                    time.sleep(0.5)

            elif not PERIOD_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (760, 280), 35, (255, 0, 0), -1)
                cv2.putText(window, '.', (750, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if PERIOD_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (760, 280), 40, (255, 255, 0), -1)
                cv2.putText(window, '>', (750, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('>', interval=0.1)
                    time.sleep(0.5)

            elif not PERIOD_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (760, 280), 35, (255, 0, 0), -1)
                cv2.putText(window, '>', (750, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- PERIOD ---------- #

            # ---------- SEMICOLON ---------- #
            if SEMICOLON_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (840, 280), 40, (255, 255, 0), -1)
                cv2.putText(window, ';', (830, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite(';', interval=0.1)
                    time.sleep(0.5)

            elif not SEMICOLON_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (840, 280), 35, (255, 0, 0), -1)
                cv2.putText(window, ';', (830, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if SEMICOLON_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (840, 280), 40, (255, 255, 0), -1)
                cv2.putText(window, ':', (830, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite(':', interval=0.1)
                    time.sleep(0.5)

            elif not SEMICOLON_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (840, 280), 35, (255, 0, 0), -1)
                cv2.putText(window, ':', (830, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- SEMICOLON ---------- #
            # ---------------------- FOURTH ROW ---------------------- #

            # ---------------------- FIFTH ROW ---------------------- #
            # ---------- CTRL ---------- #
            if CTRL_highlighted:
                window = cv2.circle(window, (40, 360), 40, (255, 255, 0), -1)
                cv2.putText(window, 'CTR', (10, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.press('ctrl')
                    time.sleep(0.5)

            else:
                window = cv2.circle(window, (40, 360), 35, (255, 0, 0), -1)
                cv2.putText(window, 'CTR', (10, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- CTRL ---------- #

            # ---------- F SLASH ---------- #
            if FORWARDSLASH_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (120, 360), 40, (255, 255, 0), -1)
                cv2.putText(window, 'FS', (110, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('\\', interval=0.1)
                    time.sleep(0.5)

            elif not FORWARDSLASH_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (120, 360), 35, (255, 0, 0), -1)
                cv2.putText(window, 'FS', (110, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if FORWARDSLASH_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (120, 360), 40, (255, 255, 0), -1)
                cv2.putText(window, '|', (110, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('|', interval=0.1)
                    time.sleep(0.5)

            elif not FORWARDSLASH_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (120, 360), 35, (255, 0, 0), -1)
                cv2.putText(window, '|', (110, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- F SLASH ---------- #

            # ---------- B SLASH ---------- #
            if BACKSLASH_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (200, 360), 40, (255, 255, 0), -1)
                cv2.putText(window, 'BS', (190, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('/', interval=0.1)
                    time.sleep(0.5)

            elif not BACKSLASH_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (200, 360), 35, (255, 0, 0), -1)
                cv2.putText(window, 'BS', (190, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if BACKSLASH_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (200, 360), 40, (255, 255, 0), -1)
                cv2.putText(window, '?', (190, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('?', interval=0.1)
                    time.sleep(0.5)

            elif not BACKSLASH_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (200, 360), 35, (255, 0, 0), -1)
                cv2.putText(window, '?', (190, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- B SLASH ---------- #

            # ---------- - ---------- #
            if MINUS_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (280, 360), 40, (255, 255, 0), -1)
                cv2.putText(window, '-', (270, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('-', interval=0.1)
                    time.sleep(0.5)

            elif not MINUS_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (280, 360), 35, (255, 0, 0), -1)
                cv2.putText(window, '-', (270, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if MINUS_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (280, 360), 40, (255, 255, 0), -1)
                cv2.putText(window, '_', (270, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('_', interval=0.1)
                    time.sleep(0.5)

            elif not MINUS_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (280, 360), 35, (255, 0, 0), -1)
                cv2.putText(window, '_', (270, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- - ---------- #

            # ---------- EQUALS ---------- #
            if EQUALS_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (360, 360), 40, (255, 255, 0), -1)
                cv2.putText(window, '=', (350, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('=', interval=0.1)
                    time.sleep(0.5)

            elif not EQUALS_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (360, 360), 35, (255, 0, 0), -1)
                cv2.putText(window, '=', (350, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if EQUALS_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (360, 360), 40, (255, 255, 0), -1)
                cv2.putText(window, '+', (350, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('+', interval=0.1)
                    time.sleep(0.5)

            elif not EQUALS_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (360, 360), 35, (255, 0, 0), -1)
                cv2.putText(window, '+', (350, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- EQUALS ---------- #

            # ---------- CLOSE ---------- #
            if SPACE_highlighted:
                window = cv2.circle(window, (440, 360), 40, (255, 255, 0), -1)
                cv2.putText(window, 'SP', (430, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.press('space', interval=0.1)
                    time.sleep(0.5)

            else:
                window = cv2.circle(window, (440, 360), 35, (255, 0, 0), -1)
                cv2.putText(window, 'SP', (430, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- CLOSE ---------- #

            # ---------- left bracket ---------- #
            if SQRBRACKOPEN_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (520, 360), 40, (255, 255, 0), -1)
                cv2.putText(window, '[', (510, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('[', interval=0.1)
                    time.sleep(0.5)

            elif not SQRBRACKOPEN_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (520, 360), 35, (255, 0, 0), -1)
                cv2.putText(window, '[', (510, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if SQRBRACKOPEN_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (520, 360), 40, (255, 255, 0), -1)
                cv2.putText(window, '{', (510, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('{', interval=0.1)
                    time.sleep(0.5)

            elif not SQRBRACKOPEN_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (520, 360), 35, (255, 0, 0), -1)
                cv2.putText(window, '{', (510, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- [ ---------- #

            # ---------- ] ---------- #
            if SQEBRACKCLOSE_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (600, 360), 40, (255, 255, 0), -1)
                cv2.putText(window, ']', (590, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite(']', interval=0.1)
                    time.sleep(0.5)

            elif not SQEBRACKCLOSE_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (600, 360), 35, (255, 0, 0), -1)
                cv2.putText(window, ']', (590, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if SQEBRACKCLOSE_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (600, 360), 40, (255, 255, 0), -1)
                cv2.putText(window, '}', (590, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('}', interval=0.1)
                    time.sleep(0.5)

            elif not SQEBRACKCLOSE_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (600, 360), 35, (255, 0, 0), -1)
                cv2.putText(window, '}', (590, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- ] ---------- #

            # ---------- ' ---------- #
            if SINGQUO_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (680, 360), 40, (255, 255, 0), -1)
                cv2.putText(window, "'", (670, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite("'", interval=0.1)
                    time.sleep(0.5)

            elif not SINGQUO_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (680, 360), 35, (255, 0, 0), -1)
                cv2.putText(window, "'", (670, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if SINGQUO_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (680, 360), 40, (255, 255, 0), -1)
                cv2.putText(window, "@", (670, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('@', interval=0.1)
                    time.sleep(0.5)

            elif not SINGQUO_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (680, 360), 35, (255, 0, 0), -1)
                cv2.putText(window, "@", (670, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- ' ---------- #

            # ---------- # ---------- #
            if HASH_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (760, 360), 40, (255, 255, 0), -1)
                cv2.putText(window, '#', (750, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('#', interval=0.1)
                    time.sleep(0.5)

            elif not HASH_highlighted and not SHIFT_PRESSED:
                window = cv2.circle(window, (760, 360), 35, (255, 0, 0), -1)
                cv2.putText(window, '#', (750, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

            if HASH_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (760, 360), 40, (255, 255, 0), -1)
                cv2.putText(window, '~', (750, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.typewrite('~', interval=0.1)
                    time.sleep(0.5)

            elif not HASH_highlighted and SHIFT_PRESSED:
                window = cv2.circle(window, (760, 360), 35, (255, 0, 0), -1)
                cv2.putText(window, '~', (750, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- PERIOD ---------- #

            # ---------- BACKSPACE ---------- #
            if DELETE_highlighted:
                window = cv2.circle(window, (840, 360), 40, (255, 255, 0), -1)
                cv2.putText(window, 'Del', (830, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    pyautogui.press('backspace')
                    time.sleep(0.5)

            else:
                window = cv2.circle(window, (840, 360), 35, (255, 0, 0), -1)
                cv2.putText(window, 'Del', (830, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- SEMICOLON ---------- #
            # ---------------------- FIFTH ROW ---------------------- #

            # ---------------------- SIXTH ROW ---------------------- #
            # ---------- Voice ---------- #
            if SPEECH_highlighted:
                window = cv2.rectangle(window, (20, 460), (860, 410), (255, 255, 0), -1)
                cv2.putText(window, 'Voice Control', (320, 450), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
                if leftWink:
                    cv2.destroyWindow('keyboard')
                    speech()
                    # keyboard_running = False
                    time.sleep(1)
                if keyboard.is_pressed('l'):
                    cv2.destroyWindow('keyboard')
                    speech()
                    # keyboard_running = False
                    time.sleep(1)

            else:
                window = cv2.rectangle(window, (20, 460), (860, 410), (255, 0, 0), -1)
                cv2.putText(window, 'Voice Control', (320, 450), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
            # ---------- Voice ---------- #
            # ---------------------- SIXTH ROW ---------------------- #
            # --------------------------------------------- GUI --------------------------------------------- #

            # --------------------------------------------- TRAVERSE --------------------------------------------- #
            if keyboard.is_pressed('w'):    # if key 'w' is pressed
                y = y - 1                   # up
                time.sleep(0.5)
                print([x, y])

            if keyboard.is_pressed('a'):    # if key 'a' is pressed
                x = x - 1                   # left
                time.sleep(0.5)
                print([x, y])

            if keyboard.is_pressed('s'):    # if key 's' is pressed
                y = y + 1                   # down
                time.sleep(0.5)
                print([x, y])

            if keyboard.is_pressed('d'):    # if key 'd' is pressed
                x = x + 1                   # right
                time.sleep(0.5)
                print([x, y])

            if x == 11:
                x = 0

            if x == -1:
                x = 10

            if y == 6:
                y = 0

            if y == -1:
                y = 5
            # --------------------------------------------- TRAVERSE --------------------------------------------- #

            # --------------------------------------------- HIGHLIGHTS --------------------------------------------- #
            # ---------------------- FIRST ROW ---------------------- #
            # ---------- ESC ---------- #
            if [x, y] == [0, 0]:
                ESC_highlighted = True
            else:
                ESC_highlighted = False
            # ---------- ESC ---------- #

            # ---------- 1 ---------- #
            if [x, y] == [1, 0]:
                ONE_highlighted = True
            else:
                ONE_highlighted = False
            # ---------- 1 ---------- #

            # ---------- 2 ---------- #
            if [x, y] == [2, 0]:
                TWO_highlighted = True
            else:
                TWO_highlighted = False
            # ---------- 2 ---------- #

            # ---------- 3 ---------- #
            if [x, y] == [3, 0]:
                THREE_highlighted = True
            else:
                THREE_highlighted = False
            # ---------- 3 ---------- #

            # ---------- 4 ---------- #
            if [x, y] == [4, 0]:
                FOUR_highlighted = True
            else:
                FOUR_highlighted = False
            # ---------- 4 ---------- #

            # ---------- 5 ---------- #
            if [x, y] == [5, 0]:
                FIVE_highlighted = True
            else:
                FIVE_highlighted = False
            # ---------- 5 ---------- #

            # ---------- 6 ---------- #
            if [x, y] == [6, 0]:
                SIX_highlighted = True
            else:
                SIX_highlighted = False
            # ---------- 6 ---------- #

            # ---------- 7 ---------- #
            if [x, y] == [7, 0]:
                SEVEN_highlighted = True
            else:
                SEVEN_highlighted = False
            # ---------- 7 ---------- #

            # ---------- 8 ---------- #
            if [x, y] == [8, 0]:
                EIGHT_highlighted = True
            else:
                EIGHT_highlighted = False
            # ---------- 8 ---------- #

            # ---------- 9 ---------- #
            if [x, y] == [9, 0]:
                NINE_highlighted = True
            else:
                NINE_highlighted = False
            # ---------- 5 ---------- #

            # ---------- 0 ---------- #
            if [x, y] == [10, 0]:
                ZERO_highlighted = True
            else:
                ZERO_highlighted = False
            # ---------- 0 ---------- #
            # ---------------------- FIRST ROW ---------------------- #

            # ---------------------- SECOND ROW ---------------------- #
            # ---------- TAB ---------- #
            if [x, y] == [0, 1]:
                TAB_highlighted = True
            else:
                TAB_highlighted = False
            # ---------- TAB ---------- #

            # ---------- Q ---------- #
            if [x, y] == [1, 1]:
                Q_highlighted = True
            else:
                Q_highlighted = False
            # ---------- Q ---------- #

            # ---------- W ---------- #
            if [x, y] == [2, 1]:
                W_highlighted = True
            else:
                W_highlighted = False
            # ---------- W ---------- #

            # ---------- E ---------- #
            if [x, y] == [3, 1]:
                E_highlighted = True
            else:
                E_highlighted = False
            # ---------- E ---------- #

            # ---------- R ---------- #
            if [x, y] == [4, 1]:
                R_highlighted = True
            else:
                R_highlighted = False
            # ---------- R ---------- #

            # ---------- T ---------- #
            if [x, y] == [5, 1]:
                T_highlighted = True
            else:
                T_highlighted = False
            # ---------- T ---------- #

            # ---------- Y ---------- #
            if [x, y] == [6, 1]:
                Y_highlighted = True
            else:
                Y_highlighted = False
            # ---------- Y ---------- #

            # ---------- U ---------- #
            if [x, y] == [7, 1]:
                U_highlighted = True
            else:
                U_highlighted = False
            # ---------- U ---------- #

            # ---------- i ---------- #
            if [x, y] == [8, 1]:
                I_highlighted = True
            else:
                I_highlighted = False
            # ---------- i ---------- #

            # ---------- O ---------- #
            if [x, y] == [9, 1]:
                O_highlighted = True
            else:
                O_highlighted = False
            # ---------- O ---------- #

            # ---------- P ---------- #
            if [x, y] == [10, 1]:
                P_highlighted = True
            else:
                P_highlighted = False
            # ---------- P ---------- #
            # ---------------------- SECOND ROW ---------------------- #

            # ---------------------- THIRD ROW ---------------------- #
            # ---------- CAPS ---------- #
            if [x, y] == [0, 2]:
                CAPS_highlighted = True
            else:
                CAPS_highlighted = False
            # ---------- CAPS ---------- #

            # ---------- A ---------- #
            if [x, y] == [1, 2]:
                A_highlighted = True
            else:
                A_highlighted = False
            # ---------- A ---------- #

            # ---------- S ---------- #
            if [x, y] == [2, 2]:
                S_highlighted = True
            else:
                S_highlighted = False
            # ---------- S ---------- #

            # ---------- D ---------- #
            if [x, y] == [3, 2]:
                D_highlighted = True
            else:
                D_highlighted = False
            # ---------- D ---------- #

            # ---------- F ---------- #
            if [x, y] == [4, 2]:
                F_highlighted = True
            else:
                F_highlighted = False
            # ---------- F ---------- #

            # ---------- G ---------- #
            if [x, y] == [5, 2]:
                G_highlighted = True
            else:
                G_highlighted = False
            # ---------- G ---------- #

            # ---------- H ---------- #
            if [x, y] == [6, 2]:
                H_highlighted = True
            else:
                H_highlighted = False
            # ---------- H ---------- #

            # ---------- J ---------- #
            if [x, y] == [7, 2]:
                J_highlighted = True
            else:
                J_highlighted = False
            # ---------- J ---------- #

            # ---------- K ---------- #
            if [x, y] == [8, 2]:
                K_highlighted = True
            else:
                K_highlighted = False
            # ---------- K ---------- #

            # ---------- L ---------- #
            if [x, y] == [9, 2]:
                L_highlighted = True
            else:
                L_highlighted = False
            # ---------- L ---------- #

            # ---------- RET ---------- #
            if [x, y] == [10, 2]:
                RET_highlighted = True
            else:
                RET_highlighted = False
            # ---------- RET ---------- #
            # ---------------------- THIRD ROW ---------------------- #

            # ---------------------- FOURTH ROW ---------------------- #
            # ---------- SH ---------- #
            if [x, y] == [0, 3]:
                SHIFT_highlighted = True
            else:
                SHIFT_highlighted = False
            # ---------- SH ---------- #

            # ---------- Z ---------- #
            if [x, y] == [1, 3]:
                Z_highlighted = True
            else:
                Z_highlighted = False
            # ---------- Z ---------- #

            # ---------- X ---------- #
            if [x, y] == [2, 3]:
                X_highlighted = True
            else:
                X_highlighted = False
            # ---------- X ---------- #

            # ---------- C ---------- #
            if [x, y] == [3, 3]:
                C_highlighted = True
            else:
                C_highlighted = False
            # ---------- C ---------- #

            # ---------- V ---------- #
            if [x, y] == [4, 3]:
                V_highlighted = True
            else:
                V_highlighted = False
            # ---------- V ---------- #

            # ---------- B ---------- #
            if [x, y] == [5, 3]:
                B_highlighted = True
            else:
                B_highlighted = False
            # ---------- B ---------- #

            # ---------- N ---------- #
            if [x, y] == [6, 3]:
                N_highlighted = True
            else:
                N_highlighted = False
            # ---------- N ---------- #

            # ---------- M ---------- #
            if [x, y] == [7, 3]:
                M_highlighted = True
            else:
                M_highlighted = False
            # ---------- M ---------- #

            # ---------- COMMA ---------- #
            if [x, y] == [8, 3]:
                COMMA_highlighted = True
            else:
                COMMA_highlighted = False
            # ---------- XOMMA ---------- #

            # ---------- PERIOD ---------- #
            if [x, y] == [9, 3]:
                PERIOD_highlighted = True
            else:
                PERIOD_highlighted = False
            # ---------- PERIOD ---------- #

            # ---------- SEMICOLON ---------- #
            if [x, y] == [10, 3]:
                SEMICOLON_highlighted = True
            else:
                SEMICOLON_highlighted = False
            # ---------- SEMICOLON ---------- #
            # ---------------------- FOURTH ROW ---------------------- #

            # ---------------------- FIFTH ROW ---------------------- #
            # ---------- ctrl ---------- #
            if [x, y] == [0, 4]:
                CTRL_highlighted = True
            else:
                CTRL_highlighted = False
            # ---------- SH ---------- #

            # ---------- Z ---------- #
            if [x, y] == [1, 4]:
                FORWARDSLASH_highlighted = True
            else:
                FORWARDSLASH_highlighted = False
            # ---------- Z ---------- #

            # ---------- X ---------- #
            if [x, y] == [2, 4]:
                BACKSLASH_highlighted = True
            else:
                BACKSLASH_highlighted = False
            # ---------- X ---------- #

            # ---------- C ---------- #
            if [x, y] == [3, 4]:
                MINUS_highlighted = True
            else:
                MINUS_highlighted = False
            # ---------- C ---------- #

            # ---------- V ---------- #
            if [x, y] == [4, 4]:
                EQUALS_highlighted = True
            else:
                EQUALS_highlighted = False
            # ---------- V ---------- #

            # ---------- B ---------- #
            if [x, y] == [5, 4]:
                SPACE_highlighted = True
            else:
                SPACE_highlighted = False
            # ---------- B ---------- #

            # ---------- N ---------- #
            if [x, y] == [6, 4]:
                SQRBRACKOPEN_highlighted = True
            else:
                SQRBRACKOPEN_highlighted = False
            # ---------- N ---------- #

            # ---------- M ---------- #
            if [x, y] == [7, 4]:
                SQEBRACKCLOSE_highlighted = True
            else:
                SQEBRACKCLOSE_highlighted = False
            # ---------- M ---------- #

            # ---------- COMMA ---------- #
            if [x, y] == [8, 4]:
                SINGQUO_highlighted = True
            else:
                SINGQUO_highlighted = False
            # ---------- XOMMA ---------- #

            # ---------- PERIOD ---------- #
            if [x, y] == [9, 4]:
                HASH_highlighted = True
            else:
                HASH_highlighted = False
            # ---------- PERIOD ---------- #

            # ---------- SEMICOLON ---------- #
            if [x, y] == [10, 4]:
                DELETE_highlighted = True
            else:
                DELETE_highlighted = False
            # ---------- SEMICOLON ---------- #
            # ---------------------- FIFTH ROW ---------------------- #

            # ---------- SPEECH ---------- #
            if [x, y] == [x, 5]:
                SPEECH_highlighted = True
            else:
                SPEECH_highlighted = False
            # ---------- SPEECH ---------- #
            # --------------------------------------------- HIGHLIGHTS --------------------------------------------- #

            # -------------------------------------------- FUNCTIONALITY -------------------------------------------- #
            if keyboard.is_pressed('b') and not SHIFT_PRESSED:
                SHIFT_PRESSED = True
                time.sleep(0.5)
            if keyboard.is_pressed('b') and SHIFT_PRESSED:
                SHIFT_PRESSED = False
                time.sleep(0.5)

            if keyboard.is_pressed('o') and not CAPS_ON:
                CAPS_ON = True
                time.sleep(0.5)
            if keyboard.is_pressed('o') and CAPS_ON:
                CAPS_ON = False
                time.sleep(0.5)

            if SHIFT_highlighted:
                if keyboard.is_pressed('p') and not SHIFT_PRESSED:
                    SHIFT_PRESSED = True
                    time.sleep(0.5)
                if keyboard.is_pressed('p') and SHIFT_PRESSED:
                    SHIFT_PRESSED = False
                    time.sleep(0.5)

            if lookingRight:
                time.sleep(1)
                x = x + 1
                print([x, y])

            if lookingLeft:
                time.sleep(1)
                x = x - 1
                print([x, y])

            if lookingDown and lookingDownAllowed:
                time.sleep(1)
                y = y + 1
                print([x, y])

            if lookingUp:
                time.sleep(1)
                y = y - 1
                print([x, y])

            #if rightWink:
             #   pyautogui.press('space')
              #  time.sleep(0.5)

            # -------------------------------------------- FUNCTIONALITY -------------------------------------------- #

            cv2.imshow("keyboard", window)
            cv2.waitKey(1)


def speech():
    global speech_running
    speech_running = True
    sens_right = 300
    sens_left = -300
    sens_down = 200
    sens_up = -200
    if speech_running:
        r = sr.Recognizer()  # initialize recognizer

        with sr.Microphone() as source:
            mousegui()
            isActive_OuterLoop = True  # while true, will listen for command until command == stop
            isActive_InnerLoop = True  # while true, will listen for command once, then repeat
            isActive_KeyboardLoop = False  # while true, will be in keyboard mode

            while isActive_OuterLoop:
                isActive_InnerLoop = True

                while isActive_InnerLoop:
                    print("Speak: ")
                    audio = r.listen(source)  # listen to the source

                    try:
                        command = r.recognize_google(audio)  # use recognizer to convert audio into text

                        print("You said: {}".format(command))

                        # ---------------- clicks ---------------- #

                        if command == "click":
                            pyautogui.click()
                            isActive_InnerLoop = False

                        elif command == "right-click":
                            pyautogui.click(button='right')
                            isActive_InnerLoop = False

                        elif command == "middle click":
                            pyautogui.click(button='middle')
                            isActive_InnerLoop = False

                        elif command == "double click":
                            pyautogui.doubleClick()
                            isActive_InnerLoop = False

                        # ---------------- clicks ---------------- #

                        # ---------------- drags ---------------- #

                        elif command == "drag left":
                            pyautogui.drag(sens_left, 0, 1, button='left')
                            isActive_InnerLoop = False

                        elif command == "drag right":
                            pyautogui.drag(sens_right, 0, 1, button='left')
                            isActive_InnerLoop = False

                        elif command == "drag up":
                            pyautogui.drag(0, sens_up, 1, button='left')
                            isActive_InnerLoop = False

                        elif command == "drag down":
                            pyautogui.drag(0, sens_down, 1, button='left')
                            isActive_InnerLoop = False

                        elif command == "drag top left":
                            pyautogui.drag(sens_left, sens_up, 1, button='left')
                            isActive_InnerLoop = False

                        elif command == "drag bottom left":
                            pyautogui.drag(sens_left, sens_down, 1, button='left')
                            isActive_InnerLoop = False

                        elif command == "drag top right":
                            pyautogui.drag(sens_right, sens_up, 1, button='left')
                            isActive_InnerLoop = False

                        elif command == "drag bottom right":
                            pyautogui.drag(sens_right, sens_down, 1, button='left')
                            isActive_InnerLoop = False

                        # ---------------- drags ---------------- #

                        # ---------------- scrolling ---------------- #

                        elif command == "scroll up":
                            pyautogui.scroll(500)
                            isActive_InnerLoop = False

                        elif command == "scroll down":
                            pyautogui.scroll(-500)
                            isActive_InnerLoop = False

                        # ---------------- scrolling ---------------- #

                        # ---------------- movement ---------------- #

                        elif command == "left":
                            # pyautogui.move(-300, 0)
                            mouse.move(sens_left, 0, absolute=False, duration=1)
                            #            X,  Y,  // keep false // duration time in seconds
                            isActive_InnerLoop = False

                        elif command == "right":
                            mouse.move(sens_right, 0, absolute=False, duration=1)
                            isActive_InnerLoop = False

                        elif command == "up":
                            mouse.move(0, sens_up, absolute=False, duration=1)
                            isActive_InnerLoop = False

                        elif command == "down":
                            mouse.move(0, sens_down, absolute=False, duration=1)
                            isActive_InnerLoop = False

                        elif command == "top left":
                            mouse.move(sens_left, sens_up, absolute=False, duration=1)
                            isActive_InnerLoop = False

                        elif command == "bottom left":
                            mouse.move(sens_left, sens_down, absolute=False, duration=1)
                            isActive_InnerLoop = False

                        elif command == "top right":
                            mouse.move(sens_right, sens_up, absolute=False, duration=1)
                            isActive_InnerLoop = False

                        elif command == "bottom right":
                            mouse.move(sens_right, sens_down, absolute=False, duration=1)
                            isActive_InnerLoop = False

                        # ---------------- movement ---------------- #

                        # ---------------- snap movement ---------------- #
                        elif command == "snap bottom right":
                            pyautogui.moveTo(1920, 1080)
                            isActive_InnerLoop = False

                        elif command == "snap top right":
                            pyautogui.moveTo(1920, -1080)
                            isActive_InnerLoop = False

                        elif command == "snap bottom left":
                            pyautogui.moveTo(-1920, 1080)
                            isActive_InnerLoop = False

                        elif command == "snap top left":
                            pyautogui.moveTo(-1920, -1080)
                            isActive_InnerLoop = False

                        # ---------------- snap movement ---------------- #

                        elif command == "sensitivity up":
                            sens_right = sens_right + 50
                            print("right", sens_right)
                            sens_left = sens_left - 50
                            sens_down = sens_down + 50
                            print("down", sens_down)
                            sens_up = sens_up - 50
                            if sens_right > 700:
                                sens_right = 700
                                print("sensitivty too high")
                            if sens_left < (-700):
                                sens_left = -700
                                print("sensitivity too high")
                            if sens_down > 600:
                                sens_down = 600
                                print("sensitivity too high")
                            if sens_up < (-600):
                                sens_up = -600
                                print("sensitivity too high")

                        elif command == "sensitivity down":
                            sens_right = sens_right - 50
                            print("right", sens_right)
                            sens_left = sens_left + 50
                            sens_down = sens_down - 50
                            print("down", sens_down)
                            sens_up = sens_up + 50
                            if sens_right < 50:
                                sens_right = 50
                                print("sensitivty too low")
                            if sens_left > (-50):
                                sens_left = -50
                                print("sensitivity too low")
                            if sens_down < 50:
                                sens_down = 50
                                print("sensitivity too low")
                            if sens_up > (-50):
                                sens_up = -50
                                print("sensitivity too low")

                        # ---------------- keyboard ---------------- #

                        elif command == "keyboard":
                            keyboardgui()
                            isActive_KeyboardLoop = True
                            isActive_InnerLoop = False

                            while isActive_KeyboardLoop:
                                print("[Keyboard] Waiting... ")
                                audio = r.listen(source)

                                try:
                                    KeyboardCommand = r.recognize_google(audio)
                                    print("You said: {}".format(KeyboardCommand))
                                    if KeyboardCommand != "command" and KeyboardCommand != "stop" and \
                                            KeyboardCommand != "back to Mouse":
                                        pyautogui.typewrite(KeyboardCommand, interval=0.1)

                                    # ---------------- command words ---------------- #

                                    elif KeyboardCommand == "command":
                                        commandgui()
                                        CommandLoop = True

                                        while CommandLoop:
                                            try:
                                                print("[Command] Waiting... ")
                                                audio = r.listen(source)
                                                KeyboardCommand = r.recognize_google(audio)
                                                print("You said: {}".format(KeyboardCommand))

                                                if KeyboardCommand == "enter":
                                                    pyautogui.press('enter')

                                                elif KeyboardCommand == "escape":
                                                    pyautogui.press(['esc'])

                                                elif KeyboardCommand == "shift":
                                                    pyautogui.press('shiftleft')

                                                elif KeyboardCommand == "control":
                                                    pyautogui.press('ctrl')

                                                elif KeyboardCommand == "tab":
                                                    pyautogui.press('tab')

                                                elif KeyboardCommand == "backspace":
                                                    pyautogui.press('backspace')

                                                elif KeyboardCommand == "up":
                                                    pyautogui.press('up')

                                                elif KeyboardCommand == "down":
                                                    pyautogui.press('down')

                                                elif KeyboardCommand == "left":
                                                    pyautogui.press('left')

                                                elif KeyboardCommand == "right":
                                                    pyautogui.press('right')

                                                elif KeyboardCommand == "mute":
                                                    pyautogui.press('volumemute')

                                                elif KeyboardCommand == "volume up":
                                                    pyautogui.press('volumeup')

                                                elif KeyboardCommand == "volume down":
                                                    pyautogui.press('volumedown')

                                                elif KeyboardCommand == "capitals":
                                                    pyautogui.press('capslock')

                                                elif KeyboardCommand == "windows":
                                                    pyautogui.press('winleft')

                                                elif KeyboardCommand == "alt":
                                                    pyautogui.press('alt')

                                                elif KeyboardCommand == "refresh":
                                                    pyautogui.press('browserrefresh')

                                                elif KeyboardCommand == "decimal":
                                                    pyautogui.press('decimal')

                                                elif KeyboardCommand == "space bar":
                                                    pyautogui.press('space')

                                                elif KeyboardCommand == "space":
                                                    pyautogui.press('space')

                                                elif KeyboardCommand == "keyboard":
                                                    keyboardgui()
                                                    CommandLoop = False

                                            except:
                                                errorgui()

                                    # ---------------- commands ---------------- #

                                    # ---------------- stop program ---------------- #

                                    elif KeyboardCommand == "back to Mouse":
                                        mousegui()
                                        isActive_KeyboardLoop = False
                                        # isActive_OuterLoop = False
                                        isActive_InnerTrue = False

                                # ---------------- stop program ---------------- #

                                # ---------------- error with keyboard ---------------- #

                                except:
                                    errorgui()

                        # ---------------- error with keyboard ---------------- #

                        # ---------------- keyboard ---------------- #

                        # ---------------- stop program ---------------- #

                        elif command == "stop":
                            isActive_OuterLoop = False
                            isActive_InnerLoop = False
                            speech_running = False

                        # ---------------- stop program ---------------- #

                        # ---------------- error with mouse ---------------- #
                    except:
                        errorgui()

                        # ---------------- error with mouse ---------------- #


if __name__ == '__main__':
    p = threading.Thread(target=faceDetect, args=())
    p.start()
