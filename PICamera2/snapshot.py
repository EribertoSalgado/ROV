#!/usr/bin/env python3
import sys
import select
import time
from picamera2 import Picamera2, Preview
cam = Picamera2()
cam.start()
cam.capture_file("helloworld4.jpg")
print("Image Captured")
cam.stop()
salgadoe@ra
