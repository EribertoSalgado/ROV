#!/usr/bin/env python3
import pygame
import RPi.GPIO as GPIO
import time

# GPIO Pin Setup
ENA = 18   # PWM Pin
IN1 = 23   # Motor Direction 1
IN2 = 24   # Motor Direction 2

# GPIO Initialization
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

# Setup PWM for speed control
pwm = GPIO.PWM(ENA, 1000)  # 1 kHz PWM frequency
pwm.start(0)  # Start with 0% duty cycle (motor off)

# Initialize Pygame and PS4 Controller
pygame.init()
pygame.joystick.init()

try:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Connected to: {joystick.get_name()}")
except pygame.error:
    print("No PS4 controller detected. Please connect and restart.")
    exit()

def control_motor(y_axis):
    """Controls motor speed and direction based on joystick input."""
    speed = int(abs(y_axis) * 100)  # Convert joystick value to 0-100 PWM
    if y_axis > 0:  # Forward
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
    elif y_axis < 0:  # Reverse
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
    else:  # Stop
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
    
    pwm.ChangeDutyCycle(speed)  # Adjust speed

print("Use the left joystick (Y-axis) to control the motor.")

try:
    while True:
        pygame.event.pump()  # Process events
        y_axis = -joystick.get_axis(1)  # Get left stick Y-axis (inverted)
        control_motor(y_axis)  # Send input to motor
        time.sleep(0.1)  # Prevent excessive CPU usage

except KeyboardInterrupt:
    print("\nExiting...")
    pwm.stop()
    GPIO.cleanup()
