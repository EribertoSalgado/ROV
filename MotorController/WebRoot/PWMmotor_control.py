#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# Disable warnings
GPIO.setwarnings(False)

# Define GPIO pins
ENA = 18  # PWM for Motor A
IN1 = 23
IN2 = 24

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup([IN1, IN2], GPIO.OUT)

# Setup PWM
pwm_a = GPIO.PWM(ENA, 1000)  # 1kHz frequency
pwm_a.start(100)  # Default speed set to 100%

def motor_control(direction, speed=100):
    if direction == "forward":
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
    elif direction == "backward":
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
    elif direction == "stop":
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
    
    pwm_a.ChangeDutyCycle(speed)

# Run as a daemon
print("Motor control running... Waiting for commands.")

while True:
    try:
        with open("/var/www/html/motor_command.txt", "r") as file:
            command = file.read().strip().lower()

        if command == "f":
            motor_control("forward")
        elif command == "r":
            motor_control("backward")
        elif command == "q":
            motor_control("stop", 0)

        time.sleep(0.1)  # Small delay to prevent high CPU usage

    except KeyboardInterrupt:
        print("Stopping motors...")
        pwm_a.stop()
        GPIO.cleanup()
        break
    except:
        pass  # Ignore file read errors
