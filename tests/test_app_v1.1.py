"""
Unit tests for ACEest Fitness Flask Application Version 1.1
"""
import pytest
import json
import sys
import importlib.util
spec = importlib.util.spec_from_file_location("app_v1_1", "app_v1.1.py")
app_v1_1 = importlib.util.module_from_spec(spec)
sys.modules["app_v1_1"] = app_v1_1
spec.loader.exec_module(app_v1_1)
flask_app = app_v1_1.app

@pytest.fixture
def app():
    """Create application instance for testing"""
    flask_app.config['TESTING'] = True
    return flask_app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

def test_health_check_v1_1(client):
    """Test health endpoint for version 1.1"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['version'] == '1.1'

def test_workout_with_timestamp(client):
    """Test workout includes timestamp"""
    workout_data = {
        'category': 'Warm-up',
        'exercise': 'Jogging',
        'duration': 10
    }
    response = client.post('/api/workouts',
                         data=json.dumps(workout_data),
                         content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'timestamp' in data['workout']

