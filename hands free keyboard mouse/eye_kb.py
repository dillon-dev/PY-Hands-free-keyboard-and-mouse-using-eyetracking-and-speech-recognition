import cv2
import numpy as np
import keyboard
import pyautogui
import time

''''# dlib's face detector and shape predictor
dlib_predict = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
dlib_detect = dlib.get_frontal_face_detector()
font = cv2.FONT_HERSHEY_PLAIN

counter = 0

mouth_has_opened = False
def face_():
    # initialize video     0 for default webcam
    global mouth_has_opened
    cap = cv2.VideoCapture(0)
    mouth_open = False

    oue = True
    while oue:
        _, frame = cap.read()

        # GREYSCALE THE IMAGE
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # store information about face position in array faces.
        # traverse array with for loop to update detector every frame
        faces = dlib_detect(grey)
        for face in faces:

            # ---------------- find eyes and apply blink ---------------- #
            # for getting specific parts of face
            landmarks = dlib_predict(grey, face)
            # ---------------- mouth open ---------------- #

            mouth_top = (landmarks.part(61).x, landmarks.part(61).y)
            mouth_bottom = (landmarks.part(67).x, landmarks.part(67).y)
            mouth_left = (landmarks.part(60).x, landmarks.part(60).y)
            mouth_right = (landmarks.part(64).x, landmarks.part(64).y)

            mouth_open_line_ver = cv2.line(frame, mouth_top, mouth_bottom, (0, 0, 255), 1)
            mouth_open_line_hor = cv2.line(frame, mouth_left, mouth_right, (0, 0, 255), 1)

            mouth_height = hypot((mouth_top[0] - mouth_bottom[0]), (mouth_top[1] - mouth_bottom[1]))
            mouth_width = hypot((mouth_left[0] - mouth_right[0]), (mouth_left[1] - mouth_right[1]))
            mouth_size = mouth_height / mouth_width
            # print(mouth_size)
            if mouth_size > 0.38:
                cv2.putText(frame, 'MOUTH OPEN', (50, 450), font, 2, (255, 0, 0), 3)
                mouth_open = True
            else:
                mouth_open = False
                # print(mouth_open)

            if mouth_has_opened:
                if mouth_open:
                    cv2.destroyWindow('keyboard')
                    mouth_has_opened = False
                    mouth_open = False
                    time.sleep(2)

            if mouth_open:
                #cv2.destroyAllWindows()
                main()
                time.sleep(2)
                mouth_has_opened = True
                mouth_open = False

                #t2.start()
                #t2.join()
                #break

        cv2.imshow("Facial Detection", frame)  # open webcam
        key = cv2.waitKey(1)
    cap.release()


def print_it():
    global counter
    threading.Timer(1.0, print_it).start()
    counter += 1
    print(counter)

    if counter == 3:
        t2 = Process(target=main)
        t2.start()'''

font = cv2.FONT_HERSHEY_PLAIN


def testing():
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
    WIN_highlighted = False
    Z_highlighted = False
    X_highlighted = False
    C_highlighted = False
    V_highlighted = False
    B_highlighted = False
    N_highlighted = False
    M_highlighted = False
    COMMA_highlighted = False
    PERIOD_highlighted = False

    EXCL_highlighted = False
    QUO_highlighted = False
    POUND_highlighted = False
    DOLLAR_highlighted = False
    PERCENT_highlighted = False
    UPPER_highlighted = False
    AMP_highlighted = False
    ASTX_highlighted = False
    OPNBRA_highlighted = False
    CLOBRA_highlighted = False
    AT_highlighted = False

    MINUS_highlighted = False
    UNDERSCORE_highlighted = False
    PLUS_highlighted = False
    EQUALS_highlighted = False
    CURLYBRACEOPEN_highlighted = False
    CURLYBRACECLOSE_highlighted = False
    SQRBRACKOPEN_highlighted = False
    SQEBRACKCLOSE_highlighted = False
    COLON_highlighted = False
    SEMICOLON_highlighted = False
    SINGQUO_highlighted = False

    DASH_highlighted = False
    HASH_highlighted = False
    LESSTHAN_highlighted = False
    GREATERTHAN_highlighted = False
    QUESTIONMARK_highlighted = False
    LINE_highlighted = False
    FORWARDSLASH_highlighted = False
    BACKSLASH_highlighted = False
    CTRL_highlighted = False
    ALT_highlighted = False
    SPACE_highlighted = False

    DELETE_highlighted = False

    SHIFT_PRESSED = False
    CAPS_ON = False

    # 2d array for keyboard
    rows, cols = 2, 2
    arr = [[0 for x in range(rows)] for y in range(cols)]
    global x, y
    x, y = 5, 2

    while True:
        window = np.zeros((400, 880, 3), np.uint8)

        # --------------------------------------------- GUI --------------------------------------------- #
        # ---------------------- FIRST ROW ---------------------- #
        # ---------- ESC ---------- #
        if ESC_highlighted:
            window = cv2.circle(window, (40, 40), 40, (255, 255, 0), -1)
            cv2.putText(window, 'Esc', (10, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        else:
            window = cv2.circle(window, (40, 40), 35, (255, 0, 0), -1)
            cv2.putText(window, 'Esc', (10, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- ESC ---------- #

        # ---------- 1 ---------- #
        if ONE_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (120, 40), 40, (255, 255, 0), -1)
            cv2.putText(window, '1', (110, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not ONE_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (120, 40), 35, (255, 0, 0), -1)
            cv2.putText(window, '1', (110, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if ONE_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (120, 40), 40, (255, 255, 0), -1)
            cv2.putText(window, '!', (110, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not ONE_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (120, 40), 35, (255, 0, 0), -1)
            cv2.putText(window, '!', (110, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- 1 ---------- #

        # ---------- 2 ---------- #
        if TWO_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (200, 40), 40, (255, 255, 0), -1)
            cv2.putText(window, '2', (190, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not TWO_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (200, 40), 35, (255, 0, 0), -1)
            cv2.putText(window, '2', (190, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if TWO_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (200, 40), 40, (255, 255, 0), -1)
            cv2.putText(window, '"', (190, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not TWO_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (200, 40), 35, (255, 0, 0), -1)
            cv2.putText(window, '"', (190, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- 2 ---------- #

        # ---------- 3 ---------- #
        if THREE_highlighted:
            window = cv2.circle(window, (280, 40), 40, (255, 255, 0), -1)
            cv2.putText(window, '3', (270, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        else:
            window = cv2.circle(window, (280, 40), 35, (255, 0, 0), -1)
            cv2.putText(window, '3', (270, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- 3 ---------- #

        # ---------- 4 ---------- #
        if FOUR_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (360, 40), 40, (255, 255, 0), -1)
            cv2.putText(window, '4', (350, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not FOUR_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (360, 40), 35, (255, 0, 0), -1)
            cv2.putText(window, '4', (350, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if FOUR_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (360, 40), 40, (255, 255, 0), -1)
            cv2.putText(window, '$', (350, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not FOUR_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (360, 40), 35, (255, 0, 0), -1)
            cv2.putText(window, '$', (350, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- 4 ---------- #

        # ---------- 5 ---------- #
        if FIVE_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (440, 40), 40, (255, 255, 0), -1)
            cv2.putText(window, '5', (430, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not FIVE_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (440, 40), 35, (255, 0, 0), -1)
            cv2.putText(window, '5', (430, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if FIVE_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (440, 40), 40, (255, 255, 0), -1)
            cv2.putText(window, '%', (430, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not FIVE_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (440, 40), 35, (255, 0, 0), -1)
            cv2.putText(window, '%', (430, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- 5 ---------- #

        # ---------- 6 ---------- #
        if SIX_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (520, 40), 40, (255, 255, 0), -1)
            cv2.putText(window, '6', (510, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not SIX_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (520, 40), 35, (255, 0, 0), -1)
            cv2.putText(window, '6', (510, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if SIX_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (520, 40), 40, (255, 255, 0), -1)
            cv2.putText(window, '^', (510, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not SIX_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (520, 40), 35, (255, 0, 0), -1)
            cv2.putText(window, '^', (510, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- 6 ---------- #

        # ---------- 7 ---------- #
        if SEVEN_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (600, 40), 40, (255, 255, 0), -1)
            cv2.putText(window, '7', (590, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not SEVEN_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (600, 40), 35, (255, 0, 0), -1)
            cv2.putText(window, '7', (590, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if SEVEN_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (600, 40), 40, (255, 255, 0), -1)
            cv2.putText(window, '&', (590, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not SEVEN_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (600, 40), 35, (255, 0, 0), -1)
            cv2.putText(window, '&', (590, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- 7 ---------- #

        # ---------- 8 ---------- #
        if EIGHT_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (680, 40), 40, (255, 255, 0), -1)
            cv2.putText(window, '8', (670, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not EIGHT_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (680, 40), 35, (255, 0, 0), -1)
            cv2.putText(window, '8', (670, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if EIGHT_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (680, 40), 40, (255, 255, 0), -1)
            cv2.putText(window, '*', (670, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not EIGHT_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (680, 40), 35, (255, 0, 0), -1)
            cv2.putText(window, '*', (670, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- 8 ---------- #

        # ---------- 9 ---------- #
        if NINE_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (760, 40), 40, (255, 255, 0), -1)
            cv2.putText(window, '9', (750, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not NINE_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (760, 40), 35, (255, 0, 0), -1)
            cv2.putText(window, '9', (750, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if NINE_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (760, 40), 40, (255, 255, 0), -1)
            cv2.putText(window, '(', (750, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not NINE_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (760, 40), 35, (255, 0, 0), -1)
            cv2.putText(window, '(', (750, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- 9 ---------- #

        # ---------- 0 ---------- #
        if ZERO_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (840, 40), 40, (255, 255, 0), -1)
            cv2.putText(window, '0', (830, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not ZERO_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (840, 40), 35, (255, 0, 0), -1)
            cv2.putText(window, '0', (830, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if ZERO_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (840, 40), 40, (255, 255, 0), -1)
            cv2.putText(window, ')', (830, 50), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

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

        else:
            window = cv2.circle(window, (40, 120), 35, (255, 0, 0), -1)
            cv2.putText(window, 'Tab', (10, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- TAB ---------- #

        # ---------- Q ---------- #
        if Q_highlighted and CAPS_ON:
            window = cv2.circle(window, (120, 120), 40, (255, 255, 0), -1)
            cv2.putText(window, 'Q', (110, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not Q_highlighted and CAPS_ON:
            window = cv2.circle(window, (120, 120), 35, (255, 0, 0), -1)
            cv2.putText(window, 'Q', (110, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if Q_highlighted and not CAPS_ON:
            window = cv2.circle(window, (120, 120), 40, (255, 255, 0), -1)
            cv2.putText(window, 'q', (110, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not Q_highlighted and not CAPS_ON:
            window = cv2.circle(window, (120, 120), 35, (255, 0, 0), -1)
            cv2.putText(window, 'q', (110, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- Q ---------- #

        # ---------- W ---------- #
        if W_highlighted and CAPS_ON:
            window = cv2.circle(window, (200, 120), 40, (255, 255, 0), -1)
            cv2.putText(window, 'W', (190, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not W_highlighted and CAPS_ON:
            window = cv2.circle(window, (200, 120), 35, (255, 0, 0), -1)
            cv2.putText(window, 'W', (190, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if W_highlighted and not CAPS_ON:
            window = cv2.circle(window, (200, 120), 40, (255, 255, 0), -1)
            cv2.putText(window, 'w', (190, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not W_highlighted and not CAPS_ON:
            window = cv2.circle(window, (200, 120), 35, (255, 0, 0), -1)
            cv2.putText(window, 'w', (190, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- W ---------- #

        # ---------- E ---------- #
        if E_highlighted and CAPS_ON:
            window = cv2.circle(window, (280, 120), 40, (255, 255, 0), -1)
            cv2.putText(window, 'E', (270, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not E_highlighted and CAPS_ON:
            window = cv2.circle(window, (280, 120), 35, (255, 0, 0), -1)
            cv2.putText(window, 'E', (270, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if E_highlighted and not CAPS_ON:
            window = cv2.circle(window, (280, 120), 40, (255, 255, 0), -1)
            cv2.putText(window, 'e', (270, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not E_highlighted and not CAPS_ON:
            window = cv2.circle(window, (280, 120), 35, (255, 0, 0), -1)
            cv2.putText(window, 'e', (270, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- E ---------- #

        # ---------- R ---------- #
        if R_highlighted and CAPS_ON:
            window = cv2.circle(window, (360, 120), 40, (255, 255, 0), -1)
            cv2.putText(window, 'R', (350, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not R_highlighted and CAPS_ON:
            window = cv2.circle(window, (360, 120), 35, (255, 0, 0), -1)
            cv2.putText(window, 'R', (350, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if R_highlighted and not CAPS_ON:
            window = cv2.circle(window, (360, 120), 40, (255, 255, 0), -1)
            cv2.putText(window, 'r', (350, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not R_highlighted and not CAPS_ON:
            window = cv2.circle(window, (360, 120), 35, (255, 0, 0), -1)
            cv2.putText(window, 'r', (350, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- R ---------- #

        # ---------- T ---------- #
        if T_highlighted and CAPS_ON:
            window = cv2.circle(window, (440, 120), 40, (255, 255, 0), -1)
            cv2.putText(window, 'T', (430, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not T_highlighted and CAPS_ON:
            window = cv2.circle(window, (440, 120), 35, (255, 0, 0), -1)
            cv2.putText(window, 'T', (430, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if T_highlighted and not CAPS_ON:
            window = cv2.circle(window, (440, 120), 40, (255, 255, 0), -1)
            cv2.putText(window, 't', (430, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not T_highlighted and not CAPS_ON:
            window = cv2.circle(window, (440, 120), 35, (255, 0, 0), -1)
            cv2.putText(window, 't', (430, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- T ---------- #

        # ---------- Y ---------- #
        if Y_highlighted and CAPS_ON:
            window = cv2.circle(window, (520, 120), 40, (255, 255, 0), -1)
            cv2.putText(window, 'Y', (510, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not Y_highlighted and CAPS_ON:
            window = cv2.circle(window, (520, 120), 35, (255, 0, 0), -1)
            cv2.putText(window, 'Y', (510, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if Y_highlighted and not CAPS_ON:
            window = cv2.circle(window, (520, 120), 40, (255, 255, 0), -1)
            cv2.putText(window, 'y', (510, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not Y_highlighted and not CAPS_ON:
            window = cv2.circle(window, (520, 120), 35, (255, 0, 0), -1)
            cv2.putText(window, 'y', (510, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- Y ---------- #

        # ---------- U ---------- #
        if U_highlighted and CAPS_ON:
            window = cv2.circle(window, (600, 120), 40, (255, 255, 0), -1)
            cv2.putText(window, 'U', (590, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not U_highlighted and CAPS_ON:
            window = cv2.circle(window, (600, 120), 35, (255, 0, 0), -1)
            cv2.putText(window, 'U', (590, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if U_highlighted and not CAPS_ON:
            window = cv2.circle(window, (600, 120), 40, (255, 255, 0), -1)
            cv2.putText(window, 'u', (590, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not U_highlighted and not CAPS_ON:
            window = cv2.circle(window, (600, 120), 35, (255, 0, 0), -1)
            cv2.putText(window, 'u', (590, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- U ---------- #

        # ---------- i ---------- #
        if I_highlighted and CAPS_ON:
            window = cv2.circle(window, (680, 120), 40, (255, 255, 0), -1)
            cv2.putText(window, 'I', (670, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not I_highlighted and CAPS_ON:
            window = cv2.circle(window, (680, 120), 35, (255, 0, 0), -1)
            cv2.putText(window, 'I', (670, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if I_highlighted and not CAPS_ON:
            window = cv2.circle(window, (680, 120), 40, (255, 255, 0), -1)
            cv2.putText(window, 'i', (670, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not I_highlighted and not CAPS_ON:
            window = cv2.circle(window, (680, 120), 35, (255, 0, 0), -1)
            cv2.putText(window, 'i', (670, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- I ---------- #

        # ---------- O ---------- #
        if O_highlighted and CAPS_ON:
            window = cv2.circle(window, (760, 120), 40, (255, 255, 0), -1)
            cv2.putText(window, 'O', (750, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not O_highlighted and CAPS_ON:
            window = cv2.circle(window, (760, 120), 35, (255, 0, 0), -1)
            cv2.putText(window, 'O', (750, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if O_highlighted and not CAPS_ON:
            window = cv2.circle(window, (760, 120), 40, (255, 255, 0), -1)
            cv2.putText(window, 'o', (750, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not O_highlighted and not CAPS_ON:
            window = cv2.circle(window, (760, 120), 35, (255, 0, 0), -1)
            cv2.putText(window, 'o', (750, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- O ---------- #

        # ---------- P ---------- #
        if P_highlighted and CAPS_ON:
            window = cv2.circle(window, (840, 120), 40, (255, 255, 0), -1)
            cv2.putText(window, 'P', (830, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not P_highlighted and CAPS_ON:
            window = cv2.circle(window, (840, 120), 35, (255, 0, 0), -1)
            cv2.putText(window, 'P', (830, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if P_highlighted and not CAPS_ON:
            window = cv2.circle(window, (840, 120), 40, (255, 255, 0), -1)
            cv2.putText(window, 'p', (830, 130), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

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

        else:
            window = cv2.circle(window, (40, 200), 35, (255, 0, 0), -1)
            cv2.putText(window, 'Cap', (10, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- TAB ---------- #

        # ---------- A ---------- #
        if A_highlighted and CAPS_ON:
            window = cv2.circle(window, (120, 200), 40, (255, 255, 0), -1)
            cv2.putText(window, 'A', (110, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not A_highlighted and CAPS_ON:
            window = cv2.circle(window, (120, 200), 35, (255, 0, 0), -1)
            cv2.putText(window, 'A', (110, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if A_highlighted and not CAPS_ON:
            window = cv2.circle(window, (120, 200), 40, (255, 255, 0), -1)
            cv2.putText(window, 'a', (110, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not A_highlighted and not CAPS_ON:
            window = cv2.circle(window, (120, 200), 35, (255, 0, 0), -1)
            cv2.putText(window, 'a', (110, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- A ---------- #

        # ---------- S ---------- #
        if S_highlighted and CAPS_ON:
            window = cv2.circle(window, (200, 200), 40, (255, 255, 0), -1)
            cv2.putText(window, 'S', (190, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not S_highlighted and CAPS_ON:
            window = cv2.circle(window, (200, 200), 35, (255, 0, 0), -1)
            cv2.putText(window, 'S', (190, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if S_highlighted and not CAPS_ON:
            window = cv2.circle(window, (200, 200), 40, (255, 255, 0), -1)
            cv2.putText(window, 's', (190, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not S_highlighted and not CAPS_ON:
            window = cv2.circle(window, (200, 200), 35, (255, 0, 0), -1)
            cv2.putText(window, 's', (190, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- S ---------- #

        # ---------- D ---------- #
        if D_highlighted and CAPS_ON:
            window = cv2.circle(window, (280, 200), 40, (255, 255, 0), -1)
            cv2.putText(window, 'D', (270, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not D_highlighted and CAPS_ON:
            window = cv2.circle(window, (280, 200), 35, (255, 0, 0), -1)
            cv2.putText(window, 'D', (270, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if D_highlighted and not CAPS_ON:
            window = cv2.circle(window, (280, 200), 40, (255, 255, 0), -1)
            cv2.putText(window, 'd', (270, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not D_highlighted and not CAPS_ON:
            window = cv2.circle(window, (280, 200), 35, (255, 0, 0), -1)
            cv2.putText(window, 'd', (270, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- D ---------- #

        # ---------- F ---------- #
        if F_highlighted and CAPS_ON:
            window = cv2.circle(window, (360, 200), 40, (255, 255, 0), -1)
            cv2.putText(window, 'F', (350, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not F_highlighted and CAPS_ON:
            window = cv2.circle(window, (360, 200), 35, (255, 0, 0), -1)
            cv2.putText(window, 'F', (350, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if F_highlighted and not CAPS_ON:
            window = cv2.circle(window, (360, 200), 40, (255, 255, 0), -1)
            cv2.putText(window, 'f', (350, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not F_highlighted and not CAPS_ON:
            window = cv2.circle(window, (360, 200), 35, (255, 0, 0), -1)
            cv2.putText(window, 'f', (350, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- F ---------- #

        # ---------- G ---------- #
        if G_highlighted and CAPS_ON:
            window = cv2.circle(window, (440, 200), 40, (255, 255, 0), -1)
            cv2.putText(window, 'G', (430, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not G_highlighted and CAPS_ON:
            window = cv2.circle(window, (440, 200), 35, (255, 0, 0), -1)
            cv2.putText(window, 'G', (430, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if G_highlighted and not CAPS_ON:
            window = cv2.circle(window, (440, 200), 40, (255, 255, 0), -1)
            cv2.putText(window, 'g', (430, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not G_highlighted and not CAPS_ON:
            window = cv2.circle(window, (440, 200), 35, (255, 0, 0), -1)
            cv2.putText(window, 'g', (430, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- G ---------- #

        # ---------- H ---------- #
        if H_highlighted and CAPS_ON:
            window = cv2.circle(window, (520, 200), 40, (255, 255, 0), -1)
            cv2.putText(window, 'H', (510, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not H_highlighted and CAPS_ON:
            window = cv2.circle(window, (520, 200), 35, (255, 0, 0), -1)
            cv2.putText(window, 'H', (510, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if H_highlighted and not CAPS_ON:
            window = cv2.circle(window, (520, 200), 40, (255, 255, 0), -1)
            cv2.putText(window, 'h', (510, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not H_highlighted and not CAPS_ON:
            window = cv2.circle(window, (520, 200), 35, (255, 0, 0), -1)
            cv2.putText(window, 'h', (510, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- H ---------- #

        # ---------- J ---------- #
        if J_highlighted and CAPS_ON:
            window = cv2.circle(window, (600, 200), 40, (255, 255, 0), -1)
            cv2.putText(window, 'J', (590, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not J_highlighted and CAPS_ON:
            window = cv2.circle(window, (600, 200), 35, (255, 0, 0), -1)
            cv2.putText(window, 'J', (590, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if J_highlighted and not CAPS_ON:
            window = cv2.circle(window, (600, 200), 40, (255, 255, 0), -1)
            cv2.putText(window, 'j', (590, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not J_highlighted and not CAPS_ON:
            window = cv2.circle(window, (600, 200), 35, (255, 0, 0), -1)
            cv2.putText(window, 'j', (590, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- J ---------- #

        # ---------- K ---------- #
        if K_highlighted and CAPS_ON:
            window = cv2.circle(window, (680, 200), 40, (255, 255, 0), -1)
            cv2.putText(window, 'K', (670, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not K_highlighted and CAPS_ON:
            window = cv2.circle(window, (680, 200), 35, (255, 0, 0), -1)
            cv2.putText(window, 'K', (670, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if K_highlighted and not CAPS_ON:
            window = cv2.circle(window, (680, 200), 40, (255, 255, 0), -1)
            cv2.putText(window, 'k', (670, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not K_highlighted and not CAPS_ON:
            window = cv2.circle(window, (680, 200), 35, (255, 0, 0), -1)
            cv2.putText(window, 'k', (670, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- K ---------- #

        # ---------- L ---------- #
        if L_highlighted and CAPS_ON:
            window = cv2.circle(window, (760, 200), 40, (255, 255, 0), -1)
            cv2.putText(window, 'L', (750, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not L_highlighted and CAPS_ON:
            window = cv2.circle(window, (760, 200), 35, (255, 0, 0), -1)
            cv2.putText(window, 'L', (750, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if L_highlighted and not CAPS_ON:
            window = cv2.circle(window, (760, 200), 40, (255, 255, 0), -1)
            cv2.putText(window, 'l', (750, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not L_highlighted and not CAPS_ON:
            window = cv2.circle(window, (760, 200), 35, (255, 0, 0), -1)
            cv2.putText(window, 'l', (750, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- L ---------- #

        # ---------- ENT ---------- #
        if RET_highlighted:
            window = cv2.circle(window, (840, 200), 40, (255, 255, 0), -1)
            cv2.putText(window, 'Ret', (810, 210), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

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

        else:
            window = cv2.circle(window, (40, 280), 35, (255, 0, 0), -1)
            cv2.putText(window, 'SFT', (10, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- SHIFT ---------- #

        # ---------- Z ---------- #
        if Z_highlighted and CAPS_ON:
            window = cv2.circle(window, (120, 280), 40, (255, 255, 0), -1)
            cv2.putText(window, 'Z', (110, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not Z_highlighted and CAPS_ON:
            window = cv2.circle(window, (120, 280), 35, (255, 0, 0), -1)
            cv2.putText(window, 'Z', (110, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if Z_highlighted and not CAPS_ON:
            window = cv2.circle(window, (120, 280), 40, (255, 255, 0), -1)
            cv2.putText(window, 'z', (110, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not Z_highlighted and not CAPS_ON:
            window = cv2.circle(window, (120, 280), 35, (255, 0, 0), -1)
            cv2.putText(window, 'z', (110, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- Z ---------- #

        # ---------- X ---------- #
        if X_highlighted and CAPS_ON:
            window = cv2.circle(window, (200, 280), 40, (255, 255, 0), -1)
            cv2.putText(window, 'X', (190, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not X_highlighted and CAPS_ON:
            window = cv2.circle(window, (200, 280), 35, (255, 0, 0), -1)
            cv2.putText(window, 'X', (190, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if X_highlighted and not CAPS_ON:
            window = cv2.circle(window, (200, 280), 40, (255, 255, 0), -1)
            cv2.putText(window, 'x', (190, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not X_highlighted and not CAPS_ON:
            window = cv2.circle(window, (200, 280), 35, (255, 0, 0), -1)
            cv2.putText(window, 'x', (190, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- X ---------- #

        # ---------- C ---------- #
        if C_highlighted and CAPS_ON:
            window = cv2.circle(window, (280, 280), 40, (255, 255, 0), -1)
            cv2.putText(window, 'C', (270, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not C_highlighted and CAPS_ON:
            window = cv2.circle(window, (280, 280), 35, (255, 0, 0), -1)
            cv2.putText(window, 'C', (270, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if C_highlighted and not CAPS_ON:
            window = cv2.circle(window, (280, 280), 40, (255, 255, 0), -1)
            cv2.putText(window, 'c', (270, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not C_highlighted and not CAPS_ON:
            window = cv2.circle(window, (280, 280), 35, (255, 0, 0), -1)
            cv2.putText(window, 'c', (270, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- C ---------- #

        # ---------- V ---------- #
        if V_highlighted and CAPS_ON:
            window = cv2.circle(window, (360, 280), 40, (255, 255, 0), -1)
            cv2.putText(window, 'V', (350, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not V_highlighted and CAPS_ON:
            window = cv2.circle(window, (360, 280), 35, (255, 0, 0), -1)
            cv2.putText(window, 'V', (350, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if V_highlighted and not CAPS_ON:
            window = cv2.circle(window, (360, 280), 40, (255, 255, 0), -1)
            cv2.putText(window, 'v', (350, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not V_highlighted and not CAPS_ON:
            window = cv2.circle(window, (360, 280), 35, (255, 0, 0), -1)
            cv2.putText(window, 'v', (350, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- V ---------- #

        # ---------- B ---------- #
        if B_highlighted and CAPS_ON:
            window = cv2.circle(window, (440, 280), 40, (255, 255, 0), -1)
            cv2.putText(window, 'B', (430, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not B_highlighted and CAPS_ON:
            window = cv2.circle(window, (440, 280), 35, (255, 0, 0), -1)
            cv2.putText(window, 'B', (430, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if B_highlighted and not CAPS_ON:
            window = cv2.circle(window, (440, 280), 40, (255, 255, 0), -1)
            cv2.putText(window, 'b', (430, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not B_highlighted and not CAPS_ON:
            window = cv2.circle(window, (440, 280), 35, (255, 0, 0), -1)
            cv2.putText(window, 'b', (430, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- B ---------- #

        # ---------- N ---------- #
        if N_highlighted and CAPS_ON:
            window = cv2.circle(window, (520, 280), 40, (255, 255, 0), -1)
            cv2.putText(window, 'N', (510, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not N_highlighted and CAPS_ON:
            window = cv2.circle(window, (520, 280), 35, (255, 0, 0), -1)
            cv2.putText(window, 'N', (510, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if N_highlighted and not CAPS_ON:
            window = cv2.circle(window, (520, 280), 40, (255, 255, 0), -1)
            cv2.putText(window, 'n', (510, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not N_highlighted and not CAPS_ON:
            window = cv2.circle(window, (520, 280), 35, (255, 0, 0), -1)
            cv2.putText(window, 'n', (510, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- N ---------- #

        # ---------- M ---------- #
        if M_highlighted and CAPS_ON:
            window = cv2.circle(window, (600, 280), 40, (255, 255, 0), -1)
            cv2.putText(window, 'M', (590, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not M_highlighted and CAPS_ON:
            window = cv2.circle(window, (600, 280), 35, (255, 0, 0), -1)
            cv2.putText(window, 'M', (590, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if M_highlighted and not CAPS_ON:
            window = cv2.circle(window, (600, 280), 40, (255, 255, 0), -1)
            cv2.putText(window, 'm', (590, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if not M_highlighted and not CAPS_ON:
            window = cv2.circle(window, (600, 280), 35, (255, 0, 0), -1)
            cv2.putText(window, 'm', (590, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- M ---------- #

        # ---------- COMMA ---------- #
        if COMMA_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (680, 280), 40, (255, 255, 0), -1)
            cv2.putText(window, ',', (670, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not COMMA_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (680, 280), 35, (255, 0, 0), -1)
            cv2.putText(window, ',', (670, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if COMMA_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (680, 280), 40, (255, 255, 0), -1)
            cv2.putText(window, '<', (670, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not COMMA_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (680, 280), 35, (255, 0, 0), -1)
            cv2.putText(window, '<', (670, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- COMMA ---------- #

        # ---------- PERIOD ---------- #
        if PERIOD_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (760, 280), 40, (255, 255, 0), -1)
            cv2.putText(window, '.', (750, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not PERIOD_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (760, 280), 35, (255, 0, 0), -1)
            cv2.putText(window, '.', (750, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if PERIOD_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (760, 280), 40, (255, 255, 0), -1)
            cv2.putText(window, '>', (750, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not PERIOD_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (760, 280), 35, (255, 0, 0), -1)
            cv2.putText(window, '>', (750, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- PERIOD ---------- #

        # ---------- SEMICOLON ---------- #
        if SEMICOLON_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (840, 280), 40, (255, 255, 0), -1)
            cv2.putText(window, ';', (830, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not SEMICOLON_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (840, 280), 35, (255, 0, 0), -1)
            cv2.putText(window, ';', (830, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if SEMICOLON_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (840, 280), 40, (255, 255, 0), -1)
            cv2.putText(window, ':', (830, 290), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

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

        else:
            window = cv2.circle(window, (40, 360), 35, (255, 0, 0), -1)
            cv2.putText(window, 'CTR', (10, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- CTRL ---------- #

        # ---------- F SLASH ---------- #
        if FORWARDSLASH_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (120, 360), 40, (255, 255, 0), -1)
            cv2.putText(window, 'FS', (110, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not FORWARDSLASH_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (120, 360), 35, (255, 0, 0), -1)
            cv2.putText(window, 'FS', (110, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if FORWARDSLASH_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (120, 360), 40, (255, 255, 0), -1)
            cv2.putText(window, '|', (110, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not FORWARDSLASH_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (120, 360), 35, (255, 0, 0), -1)
            cv2.putText(window, '|', (110, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- F SLASH ---------- #

        # ---------- B SLASH ---------- #
        if BACKSLASH_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (200, 360), 40, (255, 255, 0), -1)
            cv2.putText(window, 'BS', (190, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not BACKSLASH_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (200, 360), 35, (255, 0, 0), -1)
            cv2.putText(window, 'BS', (190, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if BACKSLASH_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (200, 360), 40, (255, 255, 0), -1)
            cv2.putText(window, '?', (190, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not BACKSLASH_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (200, 360), 35, (255, 0, 0), -1)
            cv2.putText(window, '?', (190, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- B SLASH ---------- #

        # ---------- - ---------- #
        if MINUS_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (280, 360), 40, (255, 255, 0), -1)
            cv2.putText(window, '-', (270, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not MINUS_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (280, 360), 35, (255, 0, 0), -1)
            cv2.putText(window, '-', (270, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if MINUS_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (280, 360), 40, (255, 255, 0), -1)
            cv2.putText(window, '_', (270, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not MINUS_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (280, 360), 35, (255, 0, 0), -1)
            cv2.putText(window, '_', (270, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- - ---------- #

        # ---------- EQUALS ---------- #
        if EQUALS_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (360, 360), 40, (255, 255, 0), -1)
            cv2.putText(window, '=', (350, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not EQUALS_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (360, 360), 35, (255, 0, 0), -1)
            cv2.putText(window, '=', (350, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if EQUALS_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (360, 360), 40, (255, 255, 0), -1)
            cv2.putText(window, '+', (350, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not EQUALS_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (360, 360), 35, (255, 0, 0), -1)
            cv2.putText(window, '+', (350, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- EQUALS ---------- #

        # ---------- SPACE ---------- #
        if SPACE_highlighted:
            window = cv2.circle(window, (440, 360), 40, (255, 255, 0), -1)
            cv2.putText(window, 'SP', (430, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        else:
            window = cv2.circle(window, (440, 360), 35, (255, 0, 0), -1)
            cv2.putText(window, 'SP', (430, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- SPACE ---------- #

        # ---------- left bracket ---------- #
        if SQRBRACKOPEN_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (520, 360), 40, (255, 255, 0), -1)
            cv2.putText(window, '[', (510, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not SQRBRACKOPEN_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (520, 360), 35, (255, 0, 0), -1)
            cv2.putText(window, '[', (510, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if SQRBRACKOPEN_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (520, 360), 40, (255, 255, 0), -1)
            cv2.putText(window, '{', (510, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not SQRBRACKOPEN_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (520, 360), 35, (255, 0, 0), -1)
            cv2.putText(window, '{', (510, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- [ ---------- #

        # ---------- ] ---------- #
        if SQEBRACKCLOSE_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (600, 360), 40, (255, 255, 0), -1)
            cv2.putText(window, ']', (590, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not SQEBRACKCLOSE_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (600, 360), 35, (255, 0, 0), -1)
            cv2.putText(window, ']', (590, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if SQEBRACKCLOSE_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (600, 360), 40, (255, 255, 0), -1)
            cv2.putText(window, '}', (590, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not SQEBRACKCLOSE_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (600, 360), 35, (255, 0, 0), -1)
            cv2.putText(window, '}', (590, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- ] ---------- #

        # ---------- ' ---------- #
        if SINGQUO_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (680, 360), 40, (255, 255, 0), -1)
            cv2.putText(window, "'", (670, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not SINGQUO_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (680, 360), 35, (255, 0, 0), -1)
            cv2.putText(window, "'", (670, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if SINGQUO_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (680, 360), 40, (255, 255, 0), -1)
            cv2.putText(window, "@", (670, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not SINGQUO_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (680, 360), 35, (255, 0, 0), -1)
            cv2.putText(window, "@", (670, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- ' ---------- #

        # ---------- # ---------- #
        if HASH_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (760, 360), 40, (255, 255, 0), -1)
            cv2.putText(window, '#', (750, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not HASH_highlighted and not SHIFT_PRESSED:
            window = cv2.circle(window, (760, 360), 35, (255, 0, 0), -1)
            cv2.putText(window, '#', (750, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        if HASH_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (760, 360), 40, (255, 255, 0), -1)
            cv2.putText(window, '~', (750, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        elif not HASH_highlighted and SHIFT_PRESSED:
            window = cv2.circle(window, (760, 360), 35, (255, 0, 0), -1)
            cv2.putText(window, '~', (750, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- PERIOD ---------- #

        # ---------- BACKSPACE ---------- #
        if DELETE_highlighted:
            window = cv2.circle(window, (840, 360), 40, (255, 255, 0), -1)
            cv2.putText(window, 'Del', (830, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)

        else:
            window = cv2.circle(window, (840, 360), 35, (255, 0, 0), -1)
            cv2.putText(window, 'Del', (830, 370), font, 2, (255, 0, 255), 3, cv2.LINE_AA)
        # ---------- SEMICOLON ---------- #
        # ---------------------- FIFTH ROW ---------------------- #
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

        if y == 5:
            y = 0

        if y == -1:
            y = 4
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
        # --------------------------------------------- HIGHLIGHTS --------------------------------------------- #

        # --------------------------------------------- FUNCTIONALITY --------------------------------------------- #
        if keyboard.is_pressed('b') and not SHIFT_PRESSED:  # TODO: change to blink when implementing
            SHIFT_PRESSED = True
            time.sleep(0.5)
        if keyboard.is_pressed('b') and SHIFT_PRESSED:
            SHIFT_PRESSED = False
            time.sleep(0.5)

        if keyboard.is_pressed('o') and not CAPS_ON:  # TODO: change to blink when implementing
            CAPS_ON = True
            time.sleep(0.5)
        if keyboard.is_pressed('o') and CAPS_ON:
            CAPS_ON = False
            time.sleep(0.5)

        if SHIFT_highlighted:
            if keyboard.is_pressed('p') and not SHIFT_PRESSED:  # TODO: change to blink when implementing
                SHIFT_PRESSED = True
                time.sleep(0.5)
            if keyboard.is_pressed('p') and SHIFT_PRESSED:
                SHIFT_PRESSED = False
                time.sleep(0.5)

        if CAPS_highlighted:
            if keyboard.is_pressed('o') and not CAPS_ON:  # TODO: change to blink when implementing
                CAPS_ON = True
                time.sleep(0.5)
            if keyboard.is_pressed('o') and CAPS_ON:
                CAPS_ON = False
                time.sleep(0.5)
        # --------------------------------------------- FUNCTIONALITY --------------------------------------------- #

        '''if keyboard.is_pressed('b'):  # if key 'q' is pressed
            if B_highlighted:
                pyautogui.typewrite('b', interval=0.1)'''

        cv2.imshow("keyboard", window)
        cv2.waitKey(1)


if __name__ == '__main__':
    testing()
