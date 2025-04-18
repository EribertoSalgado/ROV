#!/usr/bin/env python3
import requests

try:
    response = requests.get("http://localhost:5000/snapshot")
    if response.ok:
        print("Snapshot triggered!")
    else:
        print("Snapshot failed:", response.status_code)
except Exception as e:
    print("Snapshot error:", e)
