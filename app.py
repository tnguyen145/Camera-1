import cv2
import mediapipe as mp
import numpy as np
import message


mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def detect_fall(landmarks, image_width, image_height):
    """Detects a fallen person using bounding box width-to-height ratio."""
    
    nose = landmarks[mp_pose.PoseLandmark.NOSE]
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]

    nose_y = int(nose.y * image_height)
    shoulder_y = int((left_shoulder.y + right_shoulder.y) / 2 * image_height)
    hip_y = int((left_hip.y + right_hip.y) / 2 * image_height)

    bbox_top = min(nose_y, shoulder_y)
    bbox_bottom = max(hip_y, shoulder_y)
    bbox_height = bbox_bottom - bbox_top
    bbox_width = int(abs(right_shoulder.x - left_shoulder.x) * image_width)

    aspect_ratio = bbox_width / bbox_height if bbox_height > 0 else 0

    return aspect_ratio > 1.8  

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb_frame)

    image_height, image_width, _ = frame.shape

    if results.pose_landmarks:
        fall_detected = detect_fall(results.pose_landmarks.landmark, image_width, image_height)
        mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        if fall_detected:
            cv2.putText(frame, "FALL DETECTED!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            message.send_mqtt_alert()  # Call MQTT function
            message.send_sms_alert()  # Call Twilio function

    cv2.imshow("Fall Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()