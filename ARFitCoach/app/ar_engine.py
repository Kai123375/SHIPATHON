import cv2
import mediapipe as mp
import numpy as np
from kivy.graphics.texture import Texture

class AREngine:
    def __init__(self):
        self.mp_pose = mp.solutions.pose.Pose(
            min_detection_confidence=0.8,
            min_tracking_confidence=0.8
        )
        self.cap = cv2.VideoCapture(0)
        self.current_exercise = None

    def calculate_angle(self, a, b, c):
        a, b, c = np.array(a), np.array(b), np.array(c)
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        return np.abs(radians*180.0/np.pi)

    def process_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None, {}

        frame = cv2.flip(frame, 1)
        results = self.mp_pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        feedback = {}

        if results.pose_landmarks and self.current_exercise:
            landmarks = results.pose_landmarks.landmark
            if self.current_exercise == "squat":
                # Get key points
                hip = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].x,
                       landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y]
                knee = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].x,
                         landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].y]
                ankle = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].x,
                          landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].y]

                angle = self.calculate_angle(hip, knee, ankle)
                feedback['angle'] = angle

                if angle < 140:
                    cv2.putText(frame, "TOO HIGH!", (50, 50), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    feedback['correction'] = "Lower your hips"
                elif angle > 170:
                    cv2.putText(frame, "TOO DEEP!", (50, 50), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    feedback['correction'] = "Raise slightly"
                else:
                    cv2.putText(frame, "PERFECT FORM!", (50, 50), 
                              cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    feedback['success'] = True

        return frame, feedback

    def release(self):
        self.cap.release()