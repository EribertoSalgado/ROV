#!/usr/bin/env python3 
# Enter F for Forward, R for Reverse, Q to Quit: F
# Motor running FORWARD at 100% speed
import RPi.GPIO as GPIO
import time

# Define GPIO pins for Motor A
ENA = 18  # PWM for Motor A
IN1 = 23
IN2 = 24

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup([IN1, IN2], GPIO.OUT)

# Setup PWM for Motor A
pwm_a = GPIO.PWM(ENA, 1000)  # 1kHz frequency
pwm_a.start(0)  # Start with 0% duty cycle (stopped)

# Function to control Motor A direction and speed
def motor_control(direction, speed=100):
    if direction == "forward":
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
    else:  # "backward"
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
    
    pwm_a.ChangeDutyCycle(speed)  # Adjust speed

try:
    while True:
        command = input("Enter F for Forward, R for Reverse, Q to Quit: ").strip().upper()
        
        if command == "F":
            motor_control("forward")  # Default speed = 100
            print("Motor running FORWARD at 100% speed")
        elif command == "R":
            motor_control("backward")  # Default speed = 100
            print("Motor running REVERSE at 100% speed")
        elif command == "Q":
            print("Stopping motor and exiting...")
            motor_control("forward", 0)  # Stop the motor before quitting
            break
        else:
            print("Invalid input. Type F, R, or Q.")

except KeyboardInterrupt:
    print("\nExiting program...")

finally:
    pwm_a.stop()
    GPIO.cleanup()
