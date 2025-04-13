#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

print("FORWARD")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor 1 (PWM0)
ENA1 = 18       # GPIO18
IN1 = 23        # GPIO23
IN2 = 24        # GPIO24

# Motor 2 (PWM1)
ENA2 = 13       # GPIO13
IN3 = 26        # GPIO26
IN4 = 16        # GPIO16

all_pins = [ENA1, IN1, IN2, ENA2, IN3, IN4]
for pin in all_pins:
    GPIO.setup(pin, GPIO.OUT)

pwm1 = GPIO.PWM(ENA1, 100)
pwm2 = GPIO.PWM(ENA2, 100)

pwm1.start(10)
pwm2.start(10)

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
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
