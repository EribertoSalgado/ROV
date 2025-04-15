#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

print("DIVING")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor 3 (PWM0)
ENA3 = 12      # GPIO12 - PWM0
IN1 = 17       # GPIO17
IN2 = 27       # GPIO27

# Motor 4 (PWM1)
ENA4 = 19      # GPIO19 - PWM1
IN3 = 22       # GPIO22
IN4 = 25       # GPIO25

all_pins = [ENA3, IN1, IN2, ENA4, IN3, IN4]
for pin in all_pins:
    GPIO.setup(pin, GPIO.OUT)

pwm3 = GPIO.PWM(ENA3, 100)
pwm4 = GPIO.PWM(ENA4, 100)

pwm3.start(10)
pwm4.start(10)

# Set direction to down (both motors forward)
GPIO.output(IN1, GPIO.HIGH)
GPIO.output(IN2, GPIO.LOW)

GPIO.output(IN3, GPIO.HIGH)
GPIO.output(IN4, GPIO.LOW)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    pwm3.stop()
    pwm4.stop()
    GPIO.cleanup()
