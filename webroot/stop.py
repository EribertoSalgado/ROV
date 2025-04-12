#!/usr/bin/env python3
import RPi.GPIO as GPIO

print("STOP")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ENA = 18
IN1 = 23
IN2 = 24

GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)
GPIO.output(ENA, GPIO.LOW)

GPIO.cleanup()
