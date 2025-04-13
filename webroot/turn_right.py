#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

print("TURN RIGHT")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ENB = 13       # GPIO13
IN3 = 26        # GPIO26
IN4 = 16        # GPIO16

GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

pwm = GPIO.PWM(ENB, 100)
pwm.start(10)

GPIO.output(IN3, GPIO.HIGH)
GPIO.output(IN4, GPIO.LOW)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()

