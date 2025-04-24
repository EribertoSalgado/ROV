#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# Pin configuration
LED_PIN = 5  # Change this if using a different pin

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)

# Turn on the LED
GPIO.output(LED_PIN, GPIO.HIGH)
print("LED is ON")

# Keep it on until interrupted
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    GPIO.output(LED_PIN, GPIO.LOW)  # Optional: turn off before exiting
    GPIO.cleanup()
