#!/usr/bin/env python3
import RPi.GPIO as GPIO

# Pin configuration
LED_PIN = 5  # Same pin used in LEDON.py

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)

# Turn off the LED
GPIO.output(LED_PIN, GPIO.LOW)
print("LED on GPIO 5 is OFF")

# Clean up GPIO state
GPIO.cleanup()
