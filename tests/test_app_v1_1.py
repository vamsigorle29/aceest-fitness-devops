"""
Unit tests for ACEest Fitness Flask Application Version 1.1
"""
import pytest
import json

def test_health_check_v1_1(client_v1_1):
    """Test health endpoint for version 1.1"""
    response = client_v1_1.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
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

