#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

print("SURFACE")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ENA = 12
IN1 = 17
IN2 = 27

ENB = 19
IN3 = 22
IN4 = 25

pins = [ENA, IN1, IN2, ENB, IN3, IN4]
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)

pwmA = GPIO.PWM(ENA, 100)
pwmB = GPIO.PWM(ENB, 100)
pwmA.start(10)
pwmB.start(10)

GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.HIGH)
GPIO.output(IN3, GPIO.LOW)
GPIO.output(IN4, GPIO.HIGH)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    pwmA.stop()
    pwmB.stop()
    GPIO.cleanup()
