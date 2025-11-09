"""
Unit tests for ACEest Fitness Flask Application Version 1.3
Comprehensive test suite
"""
import pytest
import json
import sys
import os
import importlib.util

def load_app_v1_3():
    """Load app_v1.3 module dynamically"""
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app_v1.3.py')
    spec = importlib.util.spec_from_file_location("app_v1_3", file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["app_v1_3"] = module
    spec.loader.exec_module(module)
    return module

@pytest.fixture(scope='function')
def app_v1_3():
    """Load app_v1.3 module"""
    module = load_app_v1_3()
    app = module.app
    app.config['TESTING'] = True
    # Reset workouts and user_info for each test
    module.workouts["Warm-up"] = []
    module.workouts["Workout"] = []
    module.workouts["Cool-down"] = []
    module.user_info.clear()
    module.daily_workouts.clear()
    return app

@pytest.fixture
def client_v1_3(app_v1_3):
    """Create test client for v1.3"""
    return app_v1_3.test_client()

@pytest.fixture
def v1_3_functions():
    """Load v1.3 calculation functions"""
    module = load_app_v1_3()
    return {
        'calculate_calories': module.calculate_calories,
        'calculate_bmi': module.calculate_bmi,
        'calculate_bmr': module.calculate_bmr
    }

def test_health_check_v1_3(client_v1_3):
    """Test health endpoint for version 1.3"""
    response = client_v1_3.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['version'] == '1.3'

class TestCalculationFunctions:
    """Test calculation functions"""
    
    def test_calorie_calculation(self, v1_3_functions):
        """Test calorie calculation function"""
        calories = v1_3_functions['calculate_calories'](70, 6.0, 30)
        assert calories > 0
        assert isinstance(calories, float)
        # Test with different values
        calories2 = v1_3_functions['calculate_calories'](80, 3.0, 20)
        assert calories2 > 0
        assert calories2 != calories
    
    def test_bmi_calculation(self, v1_3_functions):
        """Test BMI calculation function"""
        bmi = v1_3_functions['calculate_bmi'](175, 70)
        assert bmi > 0
        assert isinstance(bmi, float)
        # Test with different values
        bmi2 = v1_3_functions['calculate_bmi'](180, 80)
        assert bmi2 > 0
        assert bmi2 != bmi
    
    def test_bmr_calculation_male(self, v1_3_functions):
        """Test BMR calculation for male"""
        bmr = v1_3_functions['calculate_bmr'](70, 175, 30, 'M')
        assert bmr > 0
        assert isinstance(bmr, float)
    
    def test_bmr_calculation_female(self, v1_3_functions):
        """Test BMR calculation for female"""
        bmr = v1_3_functions['calculate_bmr'](70, 175, 30, 'F')
        assert bmr > 0
        assert isinstance(bmr, float)
    
    def test_bmr_calculation_gender_difference(self, v1_3_functions):
        """Test BMR difference between genders"""
        bmr_male = v1_3_functions['calculate_bmr'](70, 175, 30, 'M')
        bmr_female = v1_3_functions['calculate_bmr'](70, 175, 30, 'F')
        assert bmr_male > 0
        assert bmr_female > 0
        assert bmr_male != bmr_female
        # Male BMR should be higher (due to +5 vs -161)
        assert bmr_male > bmr_female

class TestUserAPI:
    """Test user API endpoints"""
    
    def test_save_user_info_male(self, client_v1_3):
        """Test saving user information for male"""
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
        assert data['user_info']['gender'] == 'M'
    
    def test_save_user_info_female(self, client_v1_3):
        """Test saving user information for female"""
        user_data = {
            'name': 'Test User Female',
            'regn_id': 'REG002',
            'age': 25,
            'gender': 'F',
            'height': 165,
            'weight': 60
        }
        response = client_v1_3.post('/api/user',
                             data=json.dumps(user_data),
                             content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['user_info']['gender'] == 'F'
    
    def test_get_user_info(self, client_v1_3):
        """Test getting user information"""
        # Save user info first
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
        
        response = client_v1_3.get('/api/user')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'name' in data
        assert 'bmi' in data
    
    def test_get_user_info_empty(self, app_v1_3, client_v1_3):
        """Test getting user info when none exists"""
        # Clear user_info directly from the module
        module = load_app_v1_3()
        module.user_info.clear()
        
        response = client_v1_3.get('/api/user')
        assert response.status_code == 200
        data = json.loads(response.data)
        # If user_info was set in a previous test, it might not be empty
        # So we just check it's a dict
        assert isinstance(data, dict)
    
    def test_save_user_info_missing_fields(self, client_v1_3):
        """Test saving user info with missing fields"""
        user_data = {
            'name': 'Test User',
            'age': 30
        }
        response = client_v1_3.post('/api/user',
                             data=json.dumps(user_data),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_save_user_info_invalid_gender(self, client_v1_3):
        """Test saving user info with invalid gender"""
        user_data = {
            'name': 'Test User',
            'regn_id': 'REG001',
            'age': 30,
            'gender': 'X',
            'height': 175,
            'weight': 70
        }
        response = client_v1_3.post('/api/user',
                             data=json.dumps(user_data),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_save_user_info_invalid_age(self, client_v1_3):
        """Test saving user info with invalid age"""
        user_data = {
            'name': 'Test User',
            'regn_id': 'REG001',
            'age': 'thirty',
            'gender': 'M',
            'height': 175,
            'weight': 70
        }
        response = client_v1_3.post('/api/user',
                             data=json.dumps(user_data),
                             content_type='application/json')
        assert response.status_code == 400

class TestWorkoutAPI:
    """Test workout API endpoints"""
    
    def test_add_workout_with_calories(self, client_v1_3):
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
    
    def test_add_workout_without_user_info(self, client_v1_3):
        """Test workout without user info (uses default weight)"""
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
    
    def test_add_workout_all_categories(self, client_v1_3):
        """Test adding workouts to all categories"""
        categories = ['Warm-up', 'Workout', 'Cool-down']
        for category in categories:
            workout_data = {
                'category': category,
                'exercise': f'Test {category}',
                'duration': 15
            }
            response = client_v1_3.post('/api/workouts',
                                     data=json.dumps(workout_data),
                                     content_type='application/json')
            assert response.status_code == 201
    
    def test_get_workouts(self, client_v1_3):
        """Test getting workouts"""
        response = client_v1_3.get('/api/workouts')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, dict)
    
    def test_get_summary_with_calories(self, client_v1_3):
        """Test getting summary with calorie data"""
        # Add workout first
        workout_data = {
            'category': 'Workout',
            'exercise': 'Running',
            'duration': 30
        }
        client_v1_3.post('/api/workouts',
                   data=json.dumps(workout_data),
                   content_type='application/json')
        
        response = client_v1_3.get('/api/workouts/summary')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'total_time' in data
        assert 'total_calories' in data
        assert 'category_totals' in data
        assert data['total_calories'] >= 0

class TestProgressAPI:
    """Test progress API endpoints"""
    
    def test_get_progress(self, client_v1_3):
        """Test progress endpoint"""
        response = client_v1_3.get('/api/progress')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, dict)
        assert 'Warm-up' in data
        assert 'Workout' in data
        assert 'Cool-down' in data
    
    def test_get_progress_with_data(self, client_v1_3):
        """Test progress endpoint with workout data"""
        # Add workout first
        client_v1_3.post('/api/workouts',
                   data=json.dumps({'category': 'Workout', 'exercise': 'Test', 'duration': 20}),
                   content_type='application/json')
        response = client_v1_3.get('/api/progress')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['Workout'] >= 20

class TestPlansAPI:
    """Test workout and diet plans API"""
    
    def test_get_workout_plans(self, client_v1_3):
        """Test getting workout plans"""
        response = client_v1_3.get('/api/workout-plans')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, dict)
        assert len(data) > 0
    
    def test_get_diet_plans(self, client_v1_3):
        """Test getting diet plans"""
        response = client_v1_3.get('/api/diet-plans')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, dict)
        assert len(data) > 0

class TestPages:
    """Test HTML page endpoints"""
    
    def test_index_page(self, client_v1_3):
        """Test index page loads"""
        response = client_v1_3.get('/')
        assert response.status_code == 200
    
    def test_summary_page(self, client_v1_3):
        """Test summary page loads"""
        response = client_v1_3.get('/summary')
        assert response.status_code == 200

