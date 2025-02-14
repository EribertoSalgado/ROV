#!/usr/bin/env python3 
# Enter F for Forward, R for Reverse, S to Stop, Q to Quit: R
# Enter duty cycle (0-100): 50
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
def motor_control(speed, direction):
    if direction == "forward":
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
    else:  # "backward"
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
    
    pwm_a.ChangeDutyCycle(speed)  # Adjust speed

try:
    while True:
        command = input("Enter F for Forward, R for Reverse, S to Stop, Q to Quit: ").strip().upper()
        
        if command == "F":
            speed = int(input("Enter speed (0-100): "))
            motor_control(speed, "forward")
        elif command == "R":
            speed = int(input("Enter speed (0-100): "))
            motor_control(speed, "backward")
        elif command == "S":
            motor_control(0, "forward")  # Stop the motor
            print("Motor stopped")
        elif command == "Q":
            print("Exiting...")
            break
        else:
            print("Invalid input. Type F, R, S, or Q.")

except KeyboardInterrupt:
    print("\nExiting program...")

finally:
    pwm_a.stop()
    GPIO.cleanup()
