#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

print("FORWARD ON")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ENA = 18
IN1 = 23
IN2 = 24

GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

pwm = GPIO.PWM(ENA, 1000)
pwm.start(1)

GPIO.output(IN1, GPIO.HIGH)
GPIO.output(IN2, GPIO.LOW)

# Run forever — press Ctrl+C to stop manually (or run stop.py remotely)
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting forward loop")
    pwm.stop()
    GPIO.cleanup()
