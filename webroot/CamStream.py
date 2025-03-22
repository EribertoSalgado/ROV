#!/usr/bin/env python3
from flask import Flask, Response, send_file
from picamera2 import Picamera2
import cv2
import io

app = Flask(__name__)

# Initialize the camera
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
camera.start()

# Further zoom-out by defining a larger ROI
roi = (0, 0, 1920, 1080)  # Increase the width and height to zoom out further
camera.set_controls({"ScalerCrop": roi})

def generate_frames():
    while True:
        frame = camera.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/snapshot')
def snapshot():
    # Capture a snapshot
    frame = camera.capture_array()
    
    # Encode as JPEG
    ret, buffer = cv2.imencode('.jpg', frame)
    img_bytes = buffer.tobytes()

    # Define the file path
    image_path = "/var/www/html/Gallery/snapshot.jpg"  # Change to your desired directory

    # Save the image to the Raspberry Pi
    with open(image_path, "wb") as f:
        f.write(img_bytes)

    # Return the saved image
    return send_file(image_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
