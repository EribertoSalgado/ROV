#!/usr/bin/env python3
# flask might be able to be removed.
# Livestream the CSI camera on a network for several local devices to stream. It is slow, but it
# may be best to use a local IP address to minimize delay. 
# http://10.0.0.116/CamDash.php The file is located in /var/www/html
# http://10.0.0.116:5000/video_feed

from flask import Flask, Response
from picamera2 import Picamera2
import cv2

app = Flask(__name__)

# Initialize the camera
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
camera.start()

# Further zoom-out by defining a larger ROI
# The coordinates are (x, y, width, height)
# Adjusting width and height to zoom out more
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
