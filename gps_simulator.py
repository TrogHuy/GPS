# gps_simulator.py
import requests
import time
import random
import json

# Configuration
SERVER_URL = "http://localhost:5000/api/gps"
SIMULATE_ISSUES = True
UPDATE_INTERVAL = 1  # seconds

# Starting location (somewhere in city center)
latitude = 37.7749
longitude = -122.4194

def simulate_movement():
    global latitude, longitude
    # Simulate small random movement
    latitude += random.uniform(-0.001, 0.001)
    longitude += random.uniform(-0.001, 0.001)
    
    return {
        "latitude": latitude,
        "longitude": longitude,
        "speed": random.uniform(0, 15),  # speed in km/h
        "device_id": "SIM001"
    }

def main():
    while True:
        # Generate GPS data
        gps_data = simulate_movement()
        
        try:
            # Send to server
            url = f"{SERVER_URL}?simulate_issues={'true' if SIMULATE_ISSUES else 'false'}"
            response = requests.post(url, json=gps_data)
            
            if response.status_code == 200:
                print(f"Data sent: {gps_data}")
            else:
                print(f"Error sending data: {response.status_code}")
                
        except Exception as e:
            print(f"Connection error: {e}")
            
        # Wait for next update
        time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    main()