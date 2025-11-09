"""
Unit tests for ACEest Fitness Flask Application
"""
import pytest
import json
from app import app as flask_app

@pytest.fixture
def app():
    """Create application instance for testing"""
    flask_app.config['TESTING'] = True
    return flask_app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create test CLI runner"""
    return app.test_cli_runner()

class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_check(self, client):
        """Test health endpoint returns 200"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'version' in data

class TestWorkoutAPI:
    """Test workout API endpoints"""
    
    def test_get_workouts_empty(self, client):
        """Test getting workouts when none exist"""
        response = client.get('/api/workouts')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, dict)
    
    def test_add_workout_success(self, client):
        """Test adding a valid workout"""
        workout_data = {
            'category': 'Workout',
            'exercise': 'Push-ups',
            'duration': 30
        }
        response = client.post('/api/workouts',
                             data=json.dumps(workout_data),
                             content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['message'] == 'Workout added successfully'
        assert 'workout' in data
    
    def test_add_workout_missing_fields(self, client):
        """Test adding workout with missing fields"""
        workout_data = {
            'category': 'Workout'
        }
        response = client.post('/api/workouts',
                             data=json.dumps(workout_data),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_add_workout_invalid_duration(self, client):
        """Test adding workout with invalid duration"""
        workout_data = {
            'category': 'Workout',
            'exercise': 'Push-ups',
            'duration': -10
        }
        response = client.post('/api/workouts',
                             data=json.dumps(workout_data),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_add_workout_invalid_category(self, client):
        """Test adding workout with invalid category"""
        workout_data = {
            'category': 'Invalid',
            'exercise': 'Push-ups',
            'duration': 30
        }
        response = client.post('/api/workouts',
                             data=json.dumps(workout_data),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_get_summary(self, client):
        """Test getting workout summary"""
        # Add a workout first
        workout_data = {
            'category': 'Workout',
            'exercise': 'Squats',
            'duration': 20
        }
        client.post('/api/workouts',
                   data=json.dumps(workout_data),
                   content_type='application/json')
        
        response = client.get('/api/workouts/summary')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'total_time' in data
        assert 'category_totals' in data
        assert data['total_time'] >= 20

class TestPages:
    """Test HTML page endpoints"""
    
    def test_index_page(self, client):
        """Test index page loads"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'ACEest Fitness' in response.data
    
    def test_summary_page(self, client):
        """Test summary page loads"""
        response = client.get('/summary')
        assert response.status_code == 200
        assert b'Summary' in response.data

