"""
Unit tests for ACEest Fitness Flask Application Version 1.2
Comprehensive test suite
"""
import pytest
import json
import sys
import os
import importlib.util

def load_app_v1_2():
    """Load app_v1.2 module dynamically"""
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app_v1.2.py')
    spec = importlib.util.spec_from_file_location("app_v1_2", file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["app_v1_2"] = module
    spec.loader.exec_module(module)
    return module

@pytest.fixture(scope='module')
def app_v1_2():
    """Load app_v1.2 module"""
    module = load_app_v1_2()
    app = module.app
    app.config['TESTING'] = True
    # Reset workouts
    module.workouts["Warm-up"] = []
    module.workouts["Workout"] = []
    module.workouts["Cool-down"] = []
    return app

@pytest.fixture
def client_v1_2(app_v1_2):
    """Create test client for v1.2"""
    return app_v1_2.test_client()

@pytest.fixture
def v1_2_module():
    """Get the v1.2 module"""
    return load_app_v1_2()

def test_health_check_v1_2(client_v1_2):
    """Test health endpoint for version 1.2"""
    response = client_v1_2.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['version'] == '1.2'

def test_get_workout_plans(client_v1_2):
    """Test getting workout plans"""
    response = client_v1_2.get('/api/workout-plans')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, dict)
    assert 'Warm-up (5-10 min)' in data
    assert 'Workout (45-60 min)' in data
    assert 'Cool-down (5 min)' in data

def test_get_diet_plans(client_v1_2):
    """Test getting diet plans"""
    response = client_v1_2.get('/api/diet-plans')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, dict)
    assert 'Weight Loss' in data
    assert 'Muscle Gain' in data
    assert 'Endurance' in data

def test_add_workout_v1_2(client_v1_2):
    """Test adding workout in v1.2"""
    workout_data = {
        'category': 'Workout',
        'exercise': 'Push-ups',
        'duration': 30
    }
    response = client_v1_2.post('/api/workouts',
                         data=json.dumps(workout_data),
                         content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'timestamp' in data['workout']

def test_get_workouts_v1_2(client_v1_2):
    """Test getting workouts in v1.2"""
    response = client_v1_2.get('/api/workouts')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, dict)

def test_get_summary_v1_2(client_v1_2):
    """Test getting summary in v1.2"""
    # Add workout first
    client_v1_2.post('/api/workouts',
               data=json.dumps({'category': 'Workout', 'exercise': 'Test', 'duration': 20}),
               content_type='application/json')
    response = client_v1_2.get('/api/workouts/summary')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'total_time' in data

def test_index_page_v1_2(client_v1_2):
    """Test index page loads in v1.2"""
    response = client_v1_2.get('/')
    assert response.status_code == 200

def test_summary_page_v1_2(client_v1_2):
    """Test summary page loads in v1.2"""
    response = client_v1_2.get('/summary')
    assert response.status_code == 200

def test_workout_plans_structure(v1_2_module):
    """Test workout plans data structure"""
    plans = v1_2_module.WORKOUT_PLANS
    assert isinstance(plans, dict)
    assert len(plans) > 0
    for plan_name, exercises in plans.items():
        assert isinstance(exercises, list)
        assert len(exercises) > 0

def test_diet_plans_structure(v1_2_module):
    """Test diet plans data structure"""
    plans = v1_2_module.DIET_PLANS
    assert isinstance(plans, dict)
    assert len(plans) > 0
    for plan_name, meals in plans.items():
        assert isinstance(meals, list)
        assert len(meals) > 0

def test_add_workout_all_categories_v1_2(client_v1_2):
    """Test adding workouts to all categories in v1.2"""
    categories = ['Warm-up', 'Workout', 'Cool-down']
    for category in categories:
        workout_data = {
            'category': category,
            'exercise': f'Test {category}',
            'duration': 15
        }
        response = client_v1_2.post('/api/workouts',
                                 data=json.dumps(workout_data),
                                 content_type='application/json')
        assert response.status_code == 201

def test_invalid_workout_v1_2(client_v1_2):
    """Test invalid workout in v1.2"""
    workout_data = {
        'category': 'Invalid',
        'exercise': 'Test',
        'duration': 10
    }
    response = client_v1_2.post('/api/workouts',
                         data=json.dumps(workout_data),
                         content_type='application/json')
    assert response.status_code == 400

