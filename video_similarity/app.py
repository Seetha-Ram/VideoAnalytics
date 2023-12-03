# /video_similarity/app.py

from flask import Flask, render_template, request, redirect, url_for
import cv2
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Define the folder where uploaded videos will be stored

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    if 'file1' not in request.files or 'file2' not in request.files:
        return "Please upload both video files."

    file1 = request.files['file1']
    file2 = request.files['file2']

    if file1.filename == '' or file2.filename == '':
        return "Please select two video files to upload."

    video1_path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
    video2_path = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)

    file1.save(video1_path)
    file2.save(video2_path)

    video1 = cv2.VideoCapture(video1_path)
    video2 = cv2.VideoCapture(video2_path)

    if not video1.isOpened() or not video2.isOpened():
        return "Error occurred while opening video files."

    frame_width = int(video1.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"H264")
    out = cv2.VideoWriter("static/difference.mp4", fourcc, 30.0, (frame_width, frame_height))

    while True:
        success1, frame1 = video1.read()
        success2, frame2 = video2.read()

        if not success1 or not success2:
            break

        difference = cv2.absdiff(frame1, frame2)
        out.write(difference)

    video1.release()
    video2.release()
    out.release()

    return redirect(url_for('result'))

@app.route('/result')
def result():
    difference_video_path = 'static/difference.mp4'
    return render_template('result.html', difference_video_path=difference_video_path)

if __name__ == '__main__':
    app.run(debug=True)
