"""
Unit tests for ACEest Fitness Flask Application Version 1.1
Comprehensive test suite
"""
import pytest
import json
import sys
import os
import importlib.util

def load_app_v1_1():
    """Load app_v1.1 module dynamically"""
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app_v1.1.py')
    spec = importlib.util.spec_from_file_location("app_v1_1", file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["app_v1_1"] = module
    spec.loader.exec_module(module)
    return module

@pytest.fixture(scope='module')
def app_v1_1():
    """Load app_v1.1 module"""
    module = load_app_v1_1()
    app = module.app
    app.config['TESTING'] = True
    # Reset workouts
    module.workouts["Warm-up"] = []
    module.workouts["Workout"] = []
    module.workouts["Cool-down"] = []
    return app

@pytest.fixture
def client_v1_1(app_v1_1):
    """Create test client for v1.1"""
    return app_v1_1.test_client()

def test_health_check_v1_1(client_v1_1):
    """Test health endpoint for version 1.1"""
    response = client_v1_1.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['version'] == '1.1'

def test_workout_with_timestamp(client_v1_1):
    """Test workout includes timestamp"""
    workout_data = {
        'category': 'Warm-up',
        'exercise': 'Jogging',
        'duration': 10
    }
    response = client_v1_1.post('/api/workouts',
                         data=json.dumps(workout_data),
                         content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'timestamp' in data['workout']
    assert 'exercise' in data['workout']
    assert 'duration' in data['workout']

def test_get_workouts_v1_1(client_v1_1):
    """Test getting workouts in v1.1"""
    response = client_v1_1.get('/api/workouts')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, dict)

def test_add_workout_all_categories_v1_1(client_v1_1):
    """Test adding workouts to all categories in v1.1"""
    categories = ['Warm-up', 'Workout', 'Cool-down']
    for category in categories:
        workout_data = {
            'category': category,
            'exercise': f'Test {category}',
            'duration': 15
        }
        response = client_v1_1.post('/api/workouts',
                                 data=json.dumps(workout_data),
                                 content_type='application/json')
        assert response.status_code == 201

def test_get_summary_v1_1(client_v1_1):
    """Test getting summary in v1.1"""
    # Add workout first
    client_v1_1.post('/api/workouts',
               data=json.dumps({'category': 'Workout', 'exercise': 'Test', 'duration': 20}),
               content_type='application/json')
    response = client_v1_1.get('/api/workouts/summary')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'total_time' in data
    assert 'category_totals' in data

def test_invalid_workout_v1_1(client_v1_1):
    """Test invalid workout in v1.1"""
    workout_data = {
        'category': 'Invalid',
        'exercise': 'Test',
        'duration': 10
    }
    response = client_v1_1.post('/api/workouts',
                         data=json.dumps(workout_data),
                         content_type='application/json')
    assert response.status_code == 400

def test_missing_fields_v1_1(client_v1_1):
    """Test missing fields in v1.1"""
    workout_data = {
        'category': 'Workout'
    }
    response = client_v1_1.post('/api/workouts',
                         data=json.dumps(workout_data),
                         content_type='application/json')
    assert response.status_code == 400

def test_index_page_v1_1(client_v1_1):
    """Test index page loads in v1.1"""
    response = client_v1_1.get('/')
    assert response.status_code == 200

def test_summary_page_v1_1(client_v1_1):
    """Test summary page loads in v1.1"""
    response = client_v1_1.get('/summary')
    assert response.status_code == 200

