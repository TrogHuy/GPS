# gps_simulator.py
import requests
import time
import random
import json
import math

# Configuration
SERVER_URL = "http://localhost:5000/api/gps"
SIMULATE_ISSUES = True
UPDATE_INTERVAL = 1  # seconds

# Starting location (somewhere in city center)
latitude = 37.7749
longitude = -122.4194

# Movement parameters
current_speed = 0  # km/h
target_speed = random.uniform(20, 50)  # km/h
current_heading = random.uniform(0, 360)  # degrees, 0 = North, 90 = East
speed_change_rate = 0.5  # km/h per update
turn_rate = 2  # max degrees per update
straight_segment_counter = 0
max_straight_segment = random.randint(10, 30)  # updates before changing direction

def calculate_new_position(lat, lon, heading, speed, interval):
    """Calculate new position based on heading, speed and time interval"""
    # Convert speed from km/h to meters per second
    speed_ms = speed * 1000 / 3600
    
    # Calculate distance traveled during the interval (in meters)
    distance = speed_ms * interval
    
    # Convert heading from degrees to radians
    heading_rad = math.radians(heading)
    
    # Earth's radius in meters
    earth_radius = 6371000
    
    # Convert current lat/lon to radians
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    
    # Calculate new latitude
    new_lat_rad = math.asin(
        math.sin(lat_rad) * math.cos(distance/earth_radius) +
        math.cos(lat_rad) * math.sin(distance/earth_radius) * math.cos(heading_rad)
    )
    
    # Calculate new longitude
    new_lon_rad = lon_rad + math.atan2(
        math.sin(heading_rad) * math.sin(distance/earth_radius) * math.cos(lat_rad),
        math.cos(distance/earth_radius) - math.sin(lat_rad) * math.sin(new_lat_rad)
    )
    
    # Convert back to degrees
    new_lat = math.degrees(new_lat_rad)
    new_lon = math.degrees(new_lon_rad)
    
    return new_lat, new_lon

def update_movement_parameters():
    """Update speed and heading to simulate realistic vehicle movement"""
    global current_speed, target_speed, current_heading, straight_segment_counter, max_straight_segment
    
    # Update speed - gradually approach target speed
    if abs(current_speed - target_speed) < speed_change_rate:
        current_speed = target_speed
        # Occasionally set a new target speed
        if random.random() < 0.1:  # 10% chance each update
            target_speed = random.uniform(20, 50)  # km/h
    elif current_speed < target_speed:
        current_speed += speed_change_rate
    else:
        current_speed -= speed_change_rate
    
    # Handle direction changes
    straight_segment_counter += 1
    
    # Time to make a turn?
    if straight_segment_counter >= max_straight_segment:
        # Decide if we're making a significant turn or just a slight adjustment
        if random.random() < 0.3:  # 30% chance of significant turn
            # Simulate turning at an intersection (more dramatic turn)
            turn_angle = random.choice([90, -90, 45, -45])  # Common turn angles
            current_heading = (current_heading + turn_angle) % 360
        else:
            # Small correction or gentle curve
            turn_angle = random.uniform(-turn_rate * 3, turn_rate * 3)
            current_heading = (current_heading + turn_angle) % 360
        
        # Reset counter and set a new straight segment length
        straight_segment_counter = 0
        max_straight_segment = random.randint(10, 30)
    else:
        # Slight adjustments while "on a straight road"
        if random.random() < 0.2:  # 20% chance of minor adjustment
            turn_angle = random.uniform(-turn_rate/2, turn_rate/2)
            current_heading = (current_heading + turn_angle) % 360

def simulate_movement():
    """Simulate realistic GPS movement for a vehicle"""
    global latitude, longitude, current_speed, current_heading
    
    # Update speed and direction
    update_movement_parameters()
    
    # Calculate new position
    latitude, longitude = calculate_new_position(
        latitude, longitude, current_heading, current_speed, UPDATE_INTERVAL
    )
    
    # Add a tiny bit of GPS noise
    latitude += random.uniform(-0.00001, 0.00001)
    longitude += random.uniform(-0.00001, 0.00001)
    
    return {
        "latitude": latitude,
        "longitude": longitude,
        "speed": current_speed,
        "heading": current_heading,
        "device_id": "SIM001"
    }

def main():
    print(f"Starting GPS simulation at ({latitude}, {longitude})")
    print(f"Initial heading: {current_heading}° at {current_speed} km/h")
    
    while True:
        # Generate GPS data
        gps_data = simulate_movement()
        
        try:
            # Send to server
            url = f"{SERVER_URL}?simulate_issues={'true' if SIMULATE_ISSUES else 'false'}"
            response = requests.post(url, json=gps_data)
            
            if response.status_code == 200:
                print(f"Data sent: Lat={gps_data['latitude']:.6f}, Lon={gps_data['longitude']:.6f}, " 
                      f"Speed={gps_data['speed']:.1f}km/h, Heading={gps_data['heading']:.1f}°")
            else:
                print(f"Error sending data: {response.status_code}")
                
        except Exception as e:
            print(f"Connection error: {e}")
            
        # Wait for next update
        time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    main()