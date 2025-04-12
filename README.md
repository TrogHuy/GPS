# GPS Tracking System

A real-time GPS tracking simulation system that demonstrates location tracking with simulated GPS data. This repository includes a complete solution for generating realistic GPS data, transmitting it over a network, and visualizing it on an interactive dashboard.


## Overview

This system consists of three main components:

1. **GPS Simulator** - A Python application that generates realistic GPS movement data
2. **Backend Server** - A Flask application that receives, processes, and broadcasts GPS data
3. **Web Dashboard** - An interactive web interface for real-time GPS visualization and analysis

The system simulates real-world conditions including signal loss, GPS accuracy variations, and network latency to provide a realistic testing environment for location-based applications.

## Features

- **Real-time GPS Simulation**
  - Random walk algorithm with configurable parameters
  - Realistic GPS jitter and accuracy variations
  - Simulated signal loss scenarios
  - Speed and heading calculations

- **Data Transmission**
  - REST API for GPS data submission
  - WebSocket real-time updates via Socket.IO
  - Configurable network latency and packet loss simulation

- **Interactive Dashboard**
  - Real-time map tracking with path history
  - Live analytics charts (speed, heading, accuracy)
  - Comprehensive data logging
  - Responsive UI with tabbed data visualization

## Getting Started

### Prerequisites

- Python 3.7+
- Flask
- Flask-SocketIO
- Requests (Python library)
- Modern web browser

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/TrogHuy/GPS.git
   cd gps-tracking-system
   ```

2. Install required Python packages:
   ```bash
   pip install flask flask-socketio requests
   ```

3. Run the Flask server:
   ```bash
   python app.py
   ```

4. In a separate terminal, start the GPS simulator:
   ```bash
   python gps_simulator.py
   ```

5. Open your browser and navigate to http://localhost:5000

## Usage

### GPS Simulator

The GPS simulator provides a simple GUI to generate and send GPS data:

- **Start** - Begin GPS data generation and transmission
- **Stop** - Pause data transmission
- **Clear** - Clear the log output

The simulator creates realistic GPS movement patterns with:
- Random direction changes
- Variable speed
- Configurable accuracy
- Occasional signal loss
- Position jitter for realism

### Web Dashboard

The dashboard provides several features:

- **Live Map View** - Shows current position and path history
- **Current Status Panel** - Displays real-time metrics
- **Analytics Charts** - Visual representation of GPS data over time
- **Data Log** - Comprehensive history of all GPS readings

#### Dashboard Controls

- **Simulate Network Issues** - Turn on/off network latency and packet loss
- **Clear Path** - Remove the current path history from the map
- **Auto-Center Map** - Turn on/off automatic map centering on new positions

## Technical Details

### Architecture

```
┌─────────────────┐     HTTP/JSON     ┌─────────────────┐    WebSocket    ┌─────────────────┐
│  GPS Simulator  │ ----------------> │  Flask Server   │ ---------------> │  Web Dashboard  │
└─────────────────┘                   └─────────────────┘                  └─────────────────┘
                                             │
                                             │ Store
                                             ▼
                                      ┌─────────────────┐
                                      │   In-Memory     │
                                      │   Data Store    │
                                      └─────────────────┘
```

### API Endpoints

- `GET /` - Serves the dashboard HTML
- `POST /api/gps` - Receives GPS data from simulators
  - Query param: `simulate_issues=true|false`
- `GET /api/history` - Returns recent GPS data history

### Data Format

GPS data is transmitted as JSON with the following structure:

```json
{
  "device_id": "mock_tracker_01",
  "timestamp": "2023-08-01T12:34:56.789Z",
  "latitude": 37.123456,
  "longitude": -122.654321,
  "speed": 1.23,
  "heading": 45.6,
  "accuracy": 8.7
}
```

## Customization

### GPS Simulator Parameters

Edit `gps_simulator.py` to modify:
- `STEP_SIZE` - Controls movement speed
- `SIGNAL_LOSS_CHANCE` - Probability of simulated signal loss
- `MAX_JITTER` - Maximum position jitter for realism
- `UPDATE_INTERVAL` - Frequency of GPS updates

### Server Configuration

Edit `app.py` to change:
- Listening port
- Maximum history size
- Simulated network delay parameters

## Acknowledgments

- [Leaflet.js](https://leafletjs.com/) for map visualization
- [Chart.js](https://www.chartjs.org/) for data charts
- [Socket.IO](https://socket.io/) for real-time communication
