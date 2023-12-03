# /multi_person_pose_estimation/app.py

from flask import Flask, render_template, request
import cv2
import numpy as np
import mediapipe as mp

app = Flask(__name__)

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

@app.route('/')
def index():
    return render_template('index.html')

def calculate_angle(a, b, c):
    radians_a = np.arctan2(a.y - b.y, a.x - b.x)
    radians_b = np.arctan2(c.y - b.y, c.x - b.x)
    angle_radians = radians_a - radians_b
    angle_degrees = np.degrees(angle_radians)
    return angle_degrees

def generate_frames(video_path):
    cap = cv2.VideoCapture(video_path)

    with mp_pose.Pose(min_detection_confidence=0.3, min_tracking_confidence=0.3) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
                left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]

                right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
                right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]

                neck = landmarks[mp_pose.PoseLandmark.NOSE]

                left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
                left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
                left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]

                right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
                right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
                right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]

                left_elbow_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
                right_elbow_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
                neck_angle = calculate_angle(left_shoulder, neck, right_shoulder)
                left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
                right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)

                font_scale = 1.5  # Increase font size
                font_color = (0, 255, 0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(image, f"Left Elbow Angle: {left_elbow_angle:.2f} degrees", (50, 50), font, font_scale, font_color, 2)
                cv2.putText(image, f"Right Elbow Angle: {right_elbow_angle:.2f} degrees", (50, 100), font, font_scale, font_color, 2)
                cv2.putText(image, f"Neck Angle: {neck_angle:.2f} degrees", (50, 150), font, font_scale, font_color, 2)
                cv2.putText(image, f"Left Knee Angle: {left_knee_angle:.2f} degrees", (50, 200), font, font_scale, font_color, 2)
                cv2.putText(image, f"Right Knee Angle: {right_knee_angle:.2f} degrees", (50, 250), font, font_scale, font_color, 2)

            ret, buffer = cv2.imencode('.jpg', image)
            if ret:
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/video_feed', methods=['POST'])
def video_feed():
    if 'video' in request.files:
        video = request.files['video']
        if video and video.filename != '':
            video_path = 'uploads/' + video.filename
            video.save(video_path)
            return generate_frames(video_path)

if __name__ == "__main__":
    app.run(debug=True)
