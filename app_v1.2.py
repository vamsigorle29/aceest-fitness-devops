"""
ACEest Fitness & Gym - Flask Web Application
Version 1.2 - Added Workout Plans and Diet Guide Tabs
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

workouts = {
    "Warm-up": [],
    "Workout": [],
    "Cool-down": []
}

# Workout plan data
WORKOUT_PLANS = {
    "Warm-up (5-10 min)": [
        "5 min light cardio (Jog/Cycle)",
        "Jumping Jacks (30 reps)",
        "Arm Circles (15 Fwd/Bwd)",
        "Leg Swings",
        "Dynamic Stretching"
    ],
    "Workout (45-60 min)": [
        "Push-ups (3 sets of 10-15)",
        "Squats (3 sets of 15-20)",
        "Plank (3 sets of 60 seconds)",
        "Lunges (3 sets of 10/leg)",
        "Burpees",
        "Crunches"
    ],
    "Cool-down (5 min)": [
        "Slow Walking",
        "Static Stretching",
        "Deep Breathing",
        "Yoga Poses"
    ]
}

# Diet plan data
DIET_PLANS = {
    "Weight Loss": [
        "Oatmeal with Fruits",
        "Grilled Chicken Salad",
        "Vegetable Soup",
        "Brown Rice & Stir-fry Veggies"
    ],
    "Muscle Gain": [
        "Egg Omelet",
        "Chicken Breast",
        "Quinoa & Beans",
        "Protein Shake",
        "Greek Yogurt with Nuts"
    ],
    "Endurance": [
        "Banana & Peanut Butter",
        "Whole Grain Pasta",
        "Sweet Potatoes",
        "Salmon & Avocado",
        "Trail Mix"
    ]
}

@app.route('/')
def index():
    """Home page with multiple tabs"""
    return render_template('index_v1.2.html', workouts=workouts, 
                         workout_plans=WORKOUT_PLANS, diet_plans=DIET_PLANS)

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
    
    if category not in workouts:
        return jsonify({'error': 'Invalid category'}), 400
    
    entry = {
        'exercise': exercise,
        'duration': duration,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    workouts[category].append(entry)
    return jsonify({'message': 'Workout added successfully', 'workout': entry}), 201

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

@app.route('/api/workout-plans', methods=['GET'])
def get_workout_plans():
    """API endpoint to get workout plans"""
    return jsonify(WORKOUT_PLANS)

@app.route('/api/diet-plans', methods=['GET'])
def get_diet_plans():
    """API endpoint to get diet plans"""
    return jsonify(DIET_PLANS)

@app.route('/summary')
def summary():
    """Summary page"""
    total_time = sum(
        sum(entry['duration'] for entry in sessions)
        for sessions in workouts.values()
    )
    return render_template('summary_v1.2.html', workouts=workouts, total_time=total_time)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'version': '1.2'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

