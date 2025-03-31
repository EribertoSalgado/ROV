#!/usr/bin/env python3
import pygame
import RPi.GPIO as GPIO
import time
import requests  # For triggering the snapshot via Flask

# GPIO Pin Setup
ENA = 18  # PWM0
ENA2 = 12
ENA3 = 13  # PWM1
ENA4 = 19

IN1 = 23  # Motor Direction 1
IN2 = 24
IN3 = 26
IN4 = 16
IN5 = 17
IN6 = 27
IN7 = 22
IN8 = 25

# GPIO Initialization
GPIO.setmode(GPIO.BCM)
GPIO.setup([ENA, ENA2, ENA3, ENA4, IN1, IN2, IN3, IN4, IN5, IN6, IN7, IN8], GPIO.OUT)

# Setup PWM for speed control
pwm = GPIO.PWM(ENA, 1000)
pwm2 = GPIO.PWM(ENA2, 1000)
pwm3 = GPIO.PWM(ENA3, 1000)
pwm4 = GPIO.PWM(ENA4, 1000)

pwm.start(0)
pwm2.start(0)
pwm3.start(0)
pwm4.start(0)

# Initialize Pygame and PS4 Controller
pygame.init()
pygame.joystick.init()

while True:
    try:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print(f"Connected to: {joystick.get_name()}")
        break
    except pygame.error:
        print("No PS4 controller detected. Please connect and press any key to retry.")
        input()

DEADZONE = 0.1  # Joystick drift filter

def control_motor(y_axis):
    """Controls motor speed and direction based on joystick input."""
    if abs(y_axis) < DEADZONE:
        y_axis = 0

    speed = int(abs(y_axis) * 100)

    if y_axis > 0:  # Forward
        GPIO.output([IN1, IN3], GPIO.HIGH)
        GPIO.output([IN2, IN4], GPIO.LOW)
        GPIO.output([IN5, IN7], GPIO.HIGH)
        GPIO.output([IN6, IN8], GPIO.LOW)
    elif y_axis < 0:  # Reverse
        GPIO.output([IN1, IN3], GPIO.LOW)
        GPIO.output([IN2, IN4], GPIO.HIGH)
        GPIO.output([IN5, IN7], GPIO.LOW)
        GPIO.output([IN6, IN8], GPIO.HIGH)
    else:  # Stop
        GPIO.output([IN1, IN2, IN3, IN4, IN5, IN6, IN7, IN8], GPIO.LOW)

    pwm.ChangeDutyCycle(speed)
    pwm2.ChangeDutyCycle(speed)
    pwm3.ChangeDutyCycle(speed)
    pwm4.ChangeDutyCycle(speed)

print("Left joystick controls movement. Press X to take a snapshot.")

try:
    while True:
        pygame.event.pump()
        y_axis = -joystick.get_axis(1)
        control_motor(y_axis)

        if joystick.get_button(0):  # X button
            try:
                response = requests.get("http://localhost:5000/snapshot")
                if response.ok:
                    print("[✓] Snapshot triggered")
                else:
                    print("[!] Snapshot failed:", response.status_code)
            except Exception as e:
                print("[!] Snapshot error:", e)
            time.sleep(0.3)  # Button debounce

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nExiting...")
    pwm.stop()
    pwm2.stop()
    pwm3.stop()
    pwm4.stop()
    GPIO.cleanup()
