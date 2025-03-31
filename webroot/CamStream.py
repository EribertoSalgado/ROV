#!/usr/bin/env python3
# Flask uses HTTP protocol to livestream and set routes that we can then embed and use in our PHP page.
# http://10.0.0.116/CamDash.php the file is located in /var/www/html
# http://10.0.0.116:5000/video_feed
from flask import Flask, Response, send_file, jsonify
from picamera2 import Picamera2
import cv2
import datetime
import os
import threading

app = Flask(__name__)

# Initialize the camera only once
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
camera.start()
roi = (0, 0, 1920, 1080)
camera.set_controls({"ScalerCrop": roi})

lock = threading.Lock()  # Prevent race conditions during snapshot

def generate_frames():
    while True:
        with lock:
            frame = camera.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/snapshot')
def snapshot():
    with lock:
        frame = camera.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        img_bytes = buffer.tobytes()

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    save_dir = "/var/www/html/Gallery"
    os.makedirs(save_dir, exist_ok=True)
    image_path = f"{save_dir}/snapshot_{timestamp}.jpg"

    with open(image_path, "wb") as f:
        f.write(img_bytes)

    print(f"[✓] Snapshot saved to {image_path}")
    return jsonify({"status": "success", "path": image_path})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
