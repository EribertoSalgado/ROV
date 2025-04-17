#!/usr/bin/env python3
#log in .csv to store in a tabluar data format
import ms5837
import time
import json
from datetime import datetime

# Initialize sensor
sensor = ms5837.MS5837_30BA()  # Default I2C bus is 1

if not sensor.init():
    print(json.dumps({"error": "Sensor could not be initialized"}))
    exit(1)

if not sensor.read():
    print(json.dumps({"error": "Sensor read failed"}))
    exit(1)

# Optionally set fluid density if you're working in saltwater
# sensor.setFluidDensity(ms5837.DENSITY_SALTWATER)

# Read data
temperature_c = sensor.temperature(ms5837.UNITS_Centigrade)
depth_m = sensor.depth()  # Defaults to freshwater unless density is changed
pressure_mbar = sensor.pressure()  # Default is mbar
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Output JSON for PHP or other web backend
# Output JSON for PHP or other web backend
data = {
    "temperature": round(temperature_c, 2),
    "depth": round(depth_m, 3),
    "pressure": round(pressure_mbar, 1),
    "timestamp": timestamp
}


print(json.dumps(data))

# Log to file
log_entry = f"{timestamp},{temperature_c},{depth_m},{pressure_mbar}\n"
with open("/var/www/html/sensor_log.csv", "a") as log_file:
    log_file.write(log_entry)
