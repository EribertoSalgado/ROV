#!/usr/bin/env python3
import RPi.GPIO as GPIO

print("STOP — All Motors")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# All PWM and direction pins used across both controllers
all_pins = [
    # Motor 1 (PWM0)
    18, 23, 24,  # ENA, IN1, IN2
    # Motor 2 (PWM1)
    13, 26, 16,  # ENB, IN3, IN4
    # Motor 3 (PWM0)
    12, 17, 27,  # ENA, IN1, IN2
    # Motor 4 (PWM1)
    19, 22, 25   # ENB, IN3, IN4
]

# Clean shutdown
for pin in all_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

GPIO.cleanup()
