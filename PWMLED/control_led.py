#!/usr/bin/env python3
from gpiozero import PWMLED
from sys import argv

led = PWMLED(14)  # GPIO14

if len(argv) > 1:
    brightness = int(argv[1]) / 100.0  # Convert to range 0.0 - 1.0
    led.value = brightness
