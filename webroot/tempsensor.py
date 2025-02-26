#!/usr/bin/env python3
import ms5837
import time
import json

sensor = ms5837.MS5837_30BA()  # Default I2C bus is 1 (Raspberry Pi 3)

if not sensor.init():
    print(json.dumps({"error": "Sensor could not be initialized"}))
    exit(1)

if not sensor.read():
    print(json.dumps({"error": "Sensor read failed"}))
    exit(1)

# Get readings
temperature = sensor.temperature(ms5837.UNITS_Centigrade)
depth = sensor.depth()  # Default is freshwater

# Return JSON output
data = {
    "temperature": temperature,
    "depth": depth
}

print(json.dumps(data))  # Output JSON
