"""
ACEest Fitness & Gym - Flask Web Application
Base Version - Core Fitness Tracking Functionality
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# In-memory storage (in production, use a database)
workouts = {
    "Warm-up": [],
    "Workout": [],
    "Cool-down": []
}

@app.route('/')
def index():
    """Home page - Display workout logging interface"""
    return render_template('index.html', workouts=workouts)

@app.route('/api/workouts', methods=['GET'])
def get_workouts():
    """API endpoint to get all workouts"""
    return jsonify(workouts)

@app.route('/api/workouts', methods=['POST'])
def add_workout():
    """API endpoint to add a new workout"""
    data = request.get_json()
    
    category = data.get('category', 'Workout')
    exercise = data.get('exercise', '').strip()
    duration = data.get('duration', 0)
    
    if not exercise or not duration:
        return jsonify({'error': 'Exercise and duration are required'}), 400
    
    try:
        duration = int(duration)
        if duration <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({'error': 'Duration must be a positive integer'}), 400
    
    entry = {
        'exercise': exercise,
        'duration': duration,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    if category in workouts:
        workouts[category].append(entry)
        return jsonify({'message': 'Workout added successfully', 'workout': entry}), 201
    else:
        return jsonify({'error': 'Invalid category'}), 400

@app.route('/api/workouts/summary', methods=['GET'])
def get_summary():
    """API endpoint to get workout summary"""
    total_time = sum(
        sum(entry['duration'] for entry in sessions)
        for sessions in workouts.values()
    )
    
    category_totals = {
        category: sum(entry['duration'] for entry in sessions)
        for category, sessions in workouts.items()
    }
    
    return jsonify({
        'total_time': total_time,
        'category_totals': category_totals,
        'workouts': workouts
    })

@app.route('/summary')
def summary():
    """Summary page - Display workout statistics"""
    total_time = sum(
        sum(entry['duration'] for entry in sessions)
        for sessions in workouts.values()
    )
    return render_template('summary.html', workouts=workouts, total_time=total_time)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'version': '1.0'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

