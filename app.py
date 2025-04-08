# app.py - Main Flask application
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import time
import random
from datetime import datetime
import json

app = Flask(__name__)
socketio = SocketIO(app)

# Mock database (in-memory storage)
gps_data_log = []

@app.route('/')
def index():
    return render_template('index_test.html')

@app.route('/api/gps', methods=['POST'])
def receive_gps():
    # Get GPS data from request
    data = request.json
    
    # Add timestamp
    data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Simulate network issues if enabled
    if request.args.get('simulate_issues', 'false') == 'true':
        # Random delay (0-3 seconds)
        delay = random.uniform(0, 3)
        time.sleep(delay)
        
        # Random packet loss (20% chance)
        if random.random() < 0.2:
            return jsonify({"status": "packet_lost"}), 408
    
    # Store in our mock database
    gps_data_log.append(data)
    
    # Keep only last 100 entries
    if len(gps_data_log) > 100:
        gps_data_log.pop(0)
    
    # Emit to all connected clients
    socketio.emit('new_gps_data', data)
    
    return jsonify({"status": "success", "stored_entries": len(gps_data_log)})

@app.route('/api/history')
def get_history():
    return jsonify(gps_data_log)

if __name__ == '__main__':
    socketio.run(app, debug=True)