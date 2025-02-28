import cv2
import mediapipe as mp
import numpy as np


cap = cv2.VideoCapture(0)

while True: 
    ret, frame = cap.read()
    if not ret: 
        print ("Failed to capture image")
        break
    cv2.imshow(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break