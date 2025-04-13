#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

print("TURN LEFT")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ENA = 18
IN1 = 23
IN2 = 24

GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

pwm = GPIO.PWM(ENA, 100)
pwm.start(10)

GPIO.output(IN1, GPIO.HIGH)
GPIO.output(IN2, GPIO.LOW)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    pwm.stop()
    GPIO.cleanup()
