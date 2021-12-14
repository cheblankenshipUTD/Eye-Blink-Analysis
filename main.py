#!/usr/bin/env python
# -*- coding: utf8 -*-
import os,sys
import cv2
import threading

capture = cv2.VideoCapture(0)
# This path is to access the harr-cascade files installed under python3.6 directory.
path = "./../../../../../Shared/Relocated_Items/Security/anaconda3/lib/python3.6/site-packages/cv2/data/"
cascade = cv2.CascadeClassifier(path+'haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier(path+'haarcascade_eye_tree_eyeglasses.xml')


# Face Size for checking distance
FACE_W = 0
FACE_H = 0
# Eye blink count
eye_blink_count = 0

def FaceDistance():
    print("FaceDistance function is called")
    threading.Timer(5.0, FaceDistance).start()
    print("check side h >> ", FACE_H)
    print("check side w >> ", FACE_W)
    if ((FACE_W > 500) or (FACE_H > 500)):
        print("Too Close to screen! Blue light Damage!!")
        # text_msg = "Too close to the PC screen!!"
        # cv2.putText(rgb,text_msg, (10,100), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 2, cv2.LINE_AA)



def EyeBlink():
    global FACE_H, FACE_W, eye_blink_count
    print("EyeBlink function is called")
    FaceDistance()
    while True:
        ret, rgb = capture.read()

        gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(gray, scaleFactor=1.11, minNeighbors=3, minSize=(100, 100))

        if len(faces) == 1:
            x, y, w, h = faces[0, :]
            cv2.rectangle(rgb, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # Update the face distance values every loop
            FACE_W = w
            FACE_H = h

            # Only detect eyes from upper half of the face rectangle.
            eyes_gray = gray[y : y + int(h/2), x : x + w]
            eyes = eye_cascade.detectMultiScale(
                eyes_gray, scaleFactor=1.11, minNeighbors=3, minSize=(8, 8))

            for ex, ey, ew, eh in eyes:
                cv2.rectangle(rgb, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (255, 255, 0), 1)

            if len(eyes) == 0:
                cv2.putText(rgb,"Blink detect", (10,100), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 2, cv2.LINE_AA)
                print("Eye blink detected!!", eye_blink_count)
                eye_blink_count = eye_blink_count + 0.5

        ############# Open video frame #############
        cv2.imshow('frame', rgb)
        # print("check >> ", face_w , " ", face_h)
        if cv2.waitKey(1) == 27:
            break  # esc to quit



EyeBlink()

capture.release()
cv2.destroyAllWindows()
