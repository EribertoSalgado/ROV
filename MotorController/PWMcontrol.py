#!/usr/bin/env python3
# Iniital test to verify motor can be powered by Rpi
import RPi.GPIO as GPIO
import time

# Define GPIO pins
ENA = 18  # PWM for Motor A
IN1 = 23
IN2 = 24
ENB = 19  # PWM for Motor B
IN3 = 27
IN4 = 22

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup([ENA, ENB], GPIO.OUT)
GPIO.setup([IN1, IN2, IN3, IN4], GPIO.OUT)

# Setup PWM
pwm_a = GPIO.PWM(ENA, 1000)  # 1kHz frequency
pwm_b = GPIO.PWM(ENB, 1000)
pwm_a.start(0)  # Start with 0% duty cycle (stopped)
pwm_b.start(0)

# Function to control motor direction and speed
def motor_control(motor, speed, direction):
    if motor == "A":
        if direction == "forward":
            GPIO.output(IN1, GPIO.HIGH)
            GPIO.output(IN2, GPIO.LOW)
        else:
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.HIGH)
        pwm_a.ChangeDutyCycle(speed)  # Adjust speed
    elif motor == "B":
        if direction == "forward":
            GPIO.output(IN3, GPIO.HIGH)
            GPIO.output(IN4, GPIO.LOW)
        else:
            GPIO.output(IN3, GPIO.LOW)
            GPIO.output(IN4, GPIO.HIGH)
        pwm_b.ChangeDutyCycle(speed)

try:
    while True:
        # Example: Motor A forward at 50% speed
        motor_control("A", 50, "forward")
        motor_control("B", 50, "forward")
        time.sleep(3)

        # Motor A backward at 75% speed
        motor_control("A", 75, "backward")
        motor_control("B", 75, "backward")
        time.sleep(3)

        # Stop motors
        motor_control("A", 0, "forward")
        motor_control("B", 0, "forward")
        time.sleep(2)

except KeyboardInterrupt:
    print("Stopping motors...")
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()
