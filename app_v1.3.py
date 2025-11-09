"""
ACEest Fitness & Gym - Flask Web Application
Version 1.3 - Advanced features with Progress Tracking, User Info, and Calorie Calculation
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime, date
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

workouts = {
    "Warm-up": [],
    "Workout": [],
    "Cool-down": []
}

daily_workouts = {}  # key=date_iso, value={category:[entries]}

# User information storage
user_info = {}

# MET Values for calorie calculation
MET_VALUES = {
    "Warm-up": 3.0,
    "Workout": 6.0,
    "Cool-down": 2.5
}

WORKOUT_PLANS = {
    "Warm-up (5-10 min)": [
        "5 min light cardio (Jog/Cycle) to raise heart rate.",
        "Jumping Jacks (30 reps) for dynamic mobility.",
        "Arm Circles (15 Fwd/Bwd) to prepare shoulders."
    ],
    "Strength & Cardio (45-60 min)": [
        "Push-ups (3 sets of 10-15) - Upper body strength.",
        "Squats (3 sets of 15-20) - Lower body foundation.",
        "Plank (3 sets of 60 seconds) - Core stabilization.",
        "Lunges (3 sets of 10/leg) - Balance and leg development."
    ],
    "Cool-down (5 min)": [
        "Slow Walking - Bring heart rate down gradually.",
        "Static Stretching (Hold 30s each) - Focus on major muscle groups.",
        "Deep Breathing Exercises - Aid recovery and relaxation."
    ]
}

DIET_PLANS = {
    "Weight Loss Focus (Calorie Deficit)": [
        "Breakfast: Oatmeal with Berries (High Fiber).",
        "Lunch: Grilled Chicken/Tofu Salad (Lean Protein).",
        "Dinner: Vegetable Soup with Lentils (Low Calorie, High Volume)."
    ],
    "Muscle Gain Focus (High Protein)": [
        "Breakfast: 3 Egg Omelet, Spinach, Whole-wheat Toast (Protein/Carb combo).",
        "Lunch: Chicken Breast, Quinoa, and Steamed Veggies (Balanced Meal).",
        "Post-Workout: Protein Shake & Greek Yogurt (Immediate Recovery)."
    ],
    "Endurance Focus (Complex Carbs)": [
        "Pre-Workout: Banana & Peanut Butter (Quick Energy).",
        "Lunch: Whole Grain Pasta with Light Sauce (Sustainable Carbs).",
        "Dinner: Salmon & Avocado Salad (Omega-3s and Healthy Fats)."
    ]
}

def calculate_calories(weight_kg, met, duration_min):
    """Calculate calories burned using MET formula"""
    return (met * 3.5 * weight_kg / 200) * duration_min

def calculate_bmi(height_cm, weight_kg):
    """Calculate BMI"""
    return weight_kg / ((height_cm / 100) ** 2)

def calculate_bmr(weight_kg, height_cm, age, gender):
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
    if gender.upper() == 'M':
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

@app.route('/')
def index():
    """Home page with all features"""
    return render_template('index_v1.3.html', workouts=workouts,
                         workout_plans=WORKOUT_PLANS, diet_plans=DIET_PLANS,
                         user_info=user_info)

@app.route('/api/user', methods=['POST'])
def save_user_info():
    """API endpoint to save user information"""
    data = request.get_json()
    
    try:
        name = data.get('name', '').strip()
        regn_id = data.get('regn_id', '').strip()
        age = int(data.get('age', 0))
        gender = data.get('gender', '').strip().upper()
        height_cm = float(data.get('height', 0))
        weight_kg = float(data.get('weight', 0))
        
        if not all([name, regn_id, age, gender, height_cm, weight_kg]):
            return jsonify({'error': 'All fields are required'}), 400
        
        if gender not in ['M', 'F']:
            return jsonify({'error': 'Gender must be M or F'}), 400
        
        bmi = calculate_bmi(height_cm, weight_kg)
        bmr = calculate_bmr(weight_kg, height_cm, age, gender)
        
        user_info.update({
            'name': name,
            'regn_id': regn_id,
            'age': age,
            'gender': gender,
            'height': height_cm,
            'weight': weight_kg,
            'bmi': round(bmi, 1),
            'bmr': round(bmr, 0),
            'weekly_cal_goal': 2000
        })
        
        return jsonify({'message': 'User info saved successfully', 'user_info': user_info}), 201
    except (ValueError, TypeError) as e:
        return jsonify({'error': f'Invalid input: {str(e)}'}), 400

@app.route('/api/user', methods=['GET'])
def get_user_info():
    """API endpoint to get user information"""
    return jsonify(user_info if user_info else {})

@app.route('/api/workouts', methods=['GET'])
def get_workouts():
    """API endpoint to get all workouts"""
    return jsonify(workouts)

@app.route('/api/workouts', methods=['POST'])
def add_workout():
    """API endpoint to add a new workout with calorie calculation"""
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
    
    # Calculate calories
    weight = user_info.get('weight', 70)  # Default weight if not set
    met = MET_VALUES.get(category, 5.0)
    calories = calculate_calories(weight, met, duration)
    
    entry = {
        'exercise': exercise,
        'duration': duration,
        'calories': round(calories, 1),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    workouts[category].append(entry)
    
    # Store in daily workouts
    today_iso = date.today().isoformat()
    if today_iso not in daily_workouts:
        daily_workouts[today_iso] = {"Warm-up": [], "Workout": [], "Cool-down": []}
    daily_workouts[today_iso][category].append(entry)
    
    return jsonify({'message': 'Workout added successfully', 'workout': entry}), 201

@app.route('/api/workouts/summary', methods=['GET'])
def get_summary():
    """API endpoint to get detailed workout summary"""
    total_time = sum(
        sum(entry['duration'] for entry in sessions)
        for sessions in workouts.values()
    )
    
    total_calories = sum(
        sum(entry.get('calories', 0) for entry in sessions)
        for sessions in workouts.values()
    )
    
    category_totals = {
        category: {
            'time': sum(entry['duration'] for entry in sessions),
            'calories': sum(entry.get('calories', 0) for entry in sessions)
        }
        for category, sessions in workouts.items()
    }
    
    return jsonify({
        'total_time': total_time,
        'total_calories': round(total_calories, 1),
        'category_totals': category_totals,
        'workouts': workouts
    })

@app.route('/api/progress', methods=['GET'])
def get_progress():
    """API endpoint to get progress data for charts"""
    totals = {
        category: sum(entry['duration'] for entry in sessions)
        for category, sessions in workouts.items()
    }
    return jsonify(totals)

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
    total_calories = sum(
        sum(entry.get('calories', 0) for entry in sessions)
        for sessions in workouts.values()
    )
    return render_template('summary_v1.3.html', workouts=workouts, 
                         total_time=total_time, total_calories=round(total_calories, 1),
                         user_info=user_info)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'version': '1.3'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

