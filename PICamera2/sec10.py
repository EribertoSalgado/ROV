#!/usr/bin/env python3

import time
import subprocess
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder

# Initialize the camera
picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)

# Set up the H.264 encoder
encoder = H264Encoder(10000000)

# File names
raw_file = 'test.h264'
mp4_file = 'test.mp4'

# Start recording
print("Recording video...")
picam2.start_recording(encoder, raw_file)
time.sleep(10)  # Record for 10 seconds
picam2.stop_recording()
print(f"Recording stopped. Saved as {raw_file}.")

# Convert to MP4 using ffmpeg
print("Converting to MP4 format...")
subprocess.run([
    "ffmpeg", "-i", raw_file, "-c:v", "copy", mp4_file
], check=True)

print(f"Video converted and saved as {mp4_file}.")
