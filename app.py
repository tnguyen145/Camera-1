import cv2
import mediapipe


cap = cv2.VideoCapture(0)

while True: 
    ret, frame = cap.read()
    if not ret: 
        print ("Failed to capture image")
        break
    