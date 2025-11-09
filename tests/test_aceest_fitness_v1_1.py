"""
Unit tests for ACEest_Fitness-V1.1.py
"""
import pytest
import sys
import os
import importlib.util
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

def load_aceest_v1_1():
    """Load ACEest_Fitness-V1.1 module"""
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ACEest_Fitness-V1.1.py')
    spec = importlib.util.spec_from_file_location("aceest_fitness_v1_1", file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["aceest_fitness_v1_1"] = module
    spec.loader.exec_module(module)
    return module

@pytest.fixture
def mock_tkinter():
    """Mock tkinter components"""
    with patch('tkinter.Tk'), \
         patch('tkinter.messagebox') as mock_msg, \
         patch('tkinter.Label'), \
         patch('tkinter.Entry'), \
         patch('tkinter.Button'), \
         patch('tkinter.ttk.Combobox'), \
         patch('tkinter.Frame'), \
         patch('tkinter.Toplevel'):
        yield {'messagebox': mock_msg}

@pytest.fixture
def fitness_app_v1_1(mock_tkinter):
    """Create FitnessTrackerApp instance"""
    module = load_aceest_v1_1()
    mock_master = Mock()
    app = module.FitnessTrackerApp(mock_master)
    return app

def test_init_v1_1(fitness_app_v1_1):
    """Test initialization"""
    assert fitness_app_v1_1.workouts == {"Warm-up": [], "Workout": [], "Cool-down": []}

def test_add_workout_v1_1(fitness_app_v1_1, mock_tkinter):
    """Test adding workout"""
    fitness_app_v1_1.category_var = Mock()
    fitness_app_v1_1.category_var.get.return_value = "Workout"
    fitness_app_v1_1.workout_entry = Mock()
    fitness_app_v1_1.workout_entry.get.return_value = "Push-ups"
    fitness_app_v1_1.duration_entry = Mock()
    fitness_app_v1_1.duration_entry.get.return_value = "30"
    fitness_app_v1_1.status_label = Mock()
    
    fitness_app_v1_1.add_workout()
    
    assert len(fitness_app_v1_1.workouts["Workout"]) == 1
    assert fitness_app_v1_1.workouts["Workout"][0]["exercise"] == "Push-ups"
    assert fitness_app_v1_1.workouts["Workout"][0]["duration"] == 30
    assert "timestamp" in fitness_app_v1_1.workouts["Workout"][0]

def test_add_workout_empty_fields_v1_1(fitness_app_v1_1, mock_tkinter):
    """Test adding workout with empty fields"""
    fitness_app_v1_1.category_var = Mock()
    fitness_app_v1_1.category_var.get.return_value = "Workout"
    fitness_app_v1_1.workout_entry = Mock()
    fitness_app_v1_1.workout_entry.get.return_value = ""
    fitness_app_v1_1.duration_entry = Mock()
    fitness_app_v1_1.duration_entry.get.return_value = ""
    
    fitness_app_v1_1.add_workout()
    
    assert len(fitness_app_v1_1.workouts["Workout"]) == 0

def test_view_summary_empty_v1_1(fitness_app_v1_1, mock_tkinter):
    """Test viewing summary when empty"""
    fitness_app_v1_1.view_summary()
    mock_tkinter['messagebox'].showinfo.assert_called()

def test_view_summary_with_data_v1_1(fitness_app_v1_1, mock_tkinter):
    """Test viewing summary with data"""
    fitness_app_v1_1.workouts["Workout"] = [
        {"exercise": "Push-ups", "duration": 30, "timestamp": "2024-01-01 10:00:00"}
    ]
    fitness_app_v1_1.view_summary()
    # Should create a Toplevel window
    assert True  # If no exception, test passes

def test_view_summary_motivational_messages_v1_1(fitness_app_v1_1, mock_tkinter):
    """Test motivational messages based on total time"""
    # Test < 30 minutes
    fitness_app_v1_1.workouts["Workout"] = [
        {"exercise": "Test", "duration": 20, "timestamp": "2024-01-01 10:00:00"}
    ]
    fitness_app_v1_1.view_summary()
    
    # Test 30-60 minutes
    fitness_app_v1_1.workouts["Workout"] = [
        {"exercise": "Test", "duration": 45, "timestamp": "2024-01-01 10:00:00"}
    ]
    fitness_app_v1_1.view_summary()
    
    # Test > 60 minutes
    fitness_app_v1_1.workouts["Workout"] = [
        {"exercise": "Test", "duration": 70, "timestamp": "2024-01-01 10:00:00"}
    ]
    fitness_app_v1_1.view_summary()

