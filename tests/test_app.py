"""
Unit tests for ACEest Fitness Flask Application
Comprehensive test suite for 85%+ coverage
"""
import pytest
import json
from app import app as flask_app, workouts

@pytest.fixture
def app():
    """Create application instance for testing"""
    flask_app.config['TESTING'] = True
    # Reset workouts for each test
    workouts["Warm-up"] = []
    workouts["Workout"] = []
    workouts["Cool-down"] = []
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
        assert data['version'] == '1.0'

class TestWorkoutAPI:
    """Test workout API endpoints"""
    
    def test_get_workouts_empty(self, client):
        """Test getting workouts when none exist"""
        response = client.get('/api/workouts')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, dict)
        assert 'Warm-up' in data
        assert 'Workout' in data
        assert 'Cool-down' in data
    
    def test_get_workouts_with_data(self, client):
        """Test getting workouts with existing data"""
        # Add workouts first
        client.post('/api/workouts',
                   data=json.dumps({'category': 'Workout', 'exercise': 'Test', 'duration': 10}),
                   content_type='application/json')
        response = client.get('/api/workouts')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['Workout']) > 0
    
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
        assert data['workout']['exercise'] == 'Push-ups'
        assert data['workout']['duration'] == 30
        assert 'timestamp' in data['workout']
    
    def test_add_workout_all_categories(self, client):
        """Test adding workouts to all categories"""
        categories = ['Warm-up', 'Workout', 'Cool-down']
        for category in categories:
            workout_data = {
                'category': category,
                'exercise': f'Test {category}',
                'duration': 15
            }
            response = client.post('/api/workouts',
                                 data=json.dumps(workout_data),
                                 content_type='application/json')
            assert response.status_code == 201
    
    def test_add_workout_default_category(self, client):
        """Test adding workout with default category"""
        workout_data = {
            'exercise': 'Running',
            'duration': 20
        }
        response = client.post('/api/workouts',
                             data=json.dumps(workout_data),
                             content_type='application/json')
        assert response.status_code == 201
    
    def test_add_workout_missing_exercise(self, client):
        """Test adding workout with missing exercise"""
        workout_data = {
            'category': 'Workout',
            'duration': 30
        }
        response = client.post('/api/workouts',
                             data=json.dumps(workout_data),
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_add_workout_missing_duration(self, client):
        """Test adding workout with missing duration"""
        workout_data = {
            'category': 'Workout',
            'exercise': 'Push-ups'
        }
        response = client.post('/api/workouts',
                             data=json.dumps(workout_data),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_add_workout_empty_exercise(self, client):
        """Test adding workout with empty exercise"""
        workout_data = {
            'category': 'Workout',
            'exercise': '   ',
            'duration': 30
        }
        response = client.post('/api/workouts',
                             data=json.dumps(workout_data),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_add_workout_invalid_duration_negative(self, client):
        """Test adding workout with negative duration"""
        workout_data = {
            'category': 'Workout',
            'exercise': 'Push-ups',
            'duration': -10
        }
        response = client.post('/api/workouts',
                             data=json.dumps(workout_data),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_add_workout_invalid_duration_zero(self, client):
        """Test adding workout with zero duration"""
        workout_data = {
            'category': 'Workout',
            'exercise': 'Push-ups',
            'duration': 0
        }
        response = client.post('/api/workouts',
                             data=json.dumps(workout_data),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_add_workout_invalid_duration_string(self, client):
        """Test adding workout with string duration"""
        workout_data = {
            'category': 'Workout',
            'exercise': 'Push-ups',
            'duration': 'thirty'
        }
        response = client.post('/api/workouts',
                             data=json.dumps(workout_data),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_add_workout_invalid_duration_float(self, client):
        """Test adding workout with float duration (should convert)"""
        workout_data = {
            'category': 'Workout',
            'exercise': 'Push-ups',
            'duration': 30.5
        }
        response = client.post('/api/workouts',
                             data=json.dumps(workout_data),
                             content_type='application/json')
        # Should convert to int or fail
        assert response.status_code in [201, 400]
    
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
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_add_workout_no_json(self, client):
        """Test adding workout without JSON data"""
        response = client.post('/api/workouts',
                             data='not json',
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_get_summary_empty(self, client):
        """Test getting summary when no workouts exist"""
        response = client.get('/api/workouts/summary')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['total_time'] == 0
        assert data['category_totals']['Warm-up'] == 0
        assert data['category_totals']['Workout'] == 0
        assert data['category_totals']['Cool-down'] == 0
    
    def test_get_summary_with_workouts(self, client):
        """Test getting workout summary with data"""
        # Add multiple workouts
        workouts_to_add = [
            {'category': 'Warm-up', 'exercise': 'Jogging', 'duration': 10},
            {'category': 'Workout', 'exercise': 'Squats', 'duration': 20},
            {'category': 'Cool-down', 'exercise': 'Stretching', 'duration': 5}
        ]
        for workout in workouts_to_add:
            client.post('/api/workouts',
                       data=json.dumps(workout),
                       content_type='application/json')
        
        response = client.get('/api/workouts/summary')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['total_time'] == 35
        assert data['category_totals']['Warm-up'] == 10
        assert data['category_totals']['Workout'] == 20
        assert data['category_totals']['Cool-down'] == 5
        assert 'workouts' in data

class TestPages:
    """Test HTML page endpoints"""
    
    def test_index_page(self, client):
        """Test index page loads"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'ACEest Fitness' in response.data or b'fitness' in response.data.lower()
    
    def test_summary_page_empty(self, client):
        """Test summary page loads with no data"""
        response = client.get('/summary')
        assert response.status_code == 200
        assert b'Summary' in response.data or b'summary' in response.data.lower()
    
    def test_summary_page_with_data(self, client):
        """Test summary page loads with workout data"""
        # Add a workout first
        client.post('/api/workouts',
                   data=json.dumps({'category': 'Workout', 'exercise': 'Test', 'duration': 15}),
                   content_type='application/json')
        response = client.get('/summary')
        assert response.status_code == 200

class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_invalid_route(self, client):
        """Test accessing non-existent route"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
    
    def test_post_to_get_endpoint(self, client):
        """Test POST to GET-only endpoint"""
        response = client.post('/api/workouts/summary')
        assert response.status_code == 405
    
    def test_get_to_post_endpoint(self, client):
        """Test GET to POST-only endpoint (should work for workouts)"""
        response = client.get('/api/workouts')
        assert response.status_code == 200
    
    def test_malformed_json(self, client):
        """Test sending malformed JSON"""
        response = client.post('/api/workouts',
                             data='{"invalid": json}',
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_workout_with_whitespace_exercise(self, client):
        """Test workout with exercise that has whitespace (should be stripped)"""
        workout_data = {
            'category': 'Workout',
            'exercise': '  Push-ups  ',
            'duration': 30
        }
        response = client.post('/api/workouts',
                             data=json.dumps(workout_data),
                             content_type='application/json')
        # Should either strip or reject
        assert response.status_code in [201, 400]

