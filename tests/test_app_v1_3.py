"""
Unit tests for ACEest Fitness Flask Application Version 1.3
"""
import pytest
import json

def test_health_check_v1_3(client_v1_3):
    """Test health endpoint for version 1.3"""
    response = client_v1_3.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['version'] == '1.3'

def test_calorie_calculation(v1_3_functions):
    """Test calorie calculation function"""
    calories = v1_3_functions['calculate_calories'](70, 6.0, 30)
    assert calories > 0
    assert isinstance(calories, float)

def test_bmi_calculation(v1_3_functions):
    """Test BMI calculation function"""
    bmi = v1_3_functions['calculate_bmi'](175, 70)
    assert bmi > 0
    assert isinstance(bmi, float)

def test_bmr_calculation(v1_3_functions):
    """Test BMR calculation function"""
    bmr_male = v1_3_functions['calculate_bmr'](70, 175, 30, 'M')
    bmr_female = v1_3_functions['calculate_bmr'](70, 175, 30, 'F')
    assert bmr_male > 0
    assert bmr_female > 0
    assert bmr_male != bmr_female

def test_save_user_info(client_v1_3):
    """Test saving user information"""
    user_data = {
        'name': 'Test User',
        'regn_id': 'REG001',
        'age': 30,
        'gender': 'M',
        'height': 175,
        'weight': 70
    }
    response = client_v1_3.post('/api/user',
                         data=json.dumps(user_data),
                         content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'bmi' in data['user_info']
    assert 'bmr' in data['user_info']

def test_workout_with_calories(client_v1_3):
    """Test workout includes calorie calculation"""
    # First save user info
    user_data = {
        'name': 'Test User',
        'regn_id': 'REG001',
        'age': 30,
        'gender': 'M',
        'height': 175,
        'weight': 70
    }
    client_v1_3.post('/api/user',
               data=json.dumps(user_data),
               content_type='application/json')
    
    # Then add workout
    workout_data = {
        'category': 'Workout',
        'exercise': 'Running',
        'duration': 30
    }
    response = client_v1_3.post('/api/workouts',
                         data=json.dumps(workout_data),
                         content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'calories' in data['workout']
    assert data['workout']['calories'] > 0

def test_get_progress(client_v1_3):
    """Test progress endpoint"""
    response = client_v1_3.get('/api/progress')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, dict)

