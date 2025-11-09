"""
Unit tests for ACEest_Fitness.py (Tkinter GUI application)
Tests the core logic without requiring GUI display
"""
import pytest
import sys
import os
import importlib.util
from unittest.mock import Mock, patch, MagicMock

# Skip all Tkinter tests in CI environments (tkinter not available)
# Use importorskip to handle tkinter availability gracefully
try:
    tkinter = pytest.importorskip("tkinter", reason="Tkinter not available in CI environment")
    from tkinter import messagebox
    TKINTER_AVAILABLE = True
except (ImportError, AttributeError, TypeError):
    TKINTER_AVAILABLE = False
    pytestmark = pytest.mark.skip(reason="Tkinter not available in CI environment")

def load_aceest_module():
    """Load ACEest_Fitness module dynamically"""
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ACEest_Fitness.py')
    spec = importlib.util.spec_from_file_location("aceest_fitness", file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["aceest_fitness"] = module
    spec.loader.exec_module(module)
    return module

@pytest.fixture
def mock_tkinter():
    """Mock tkinter components"""
    if not TKINTER_AVAILABLE:
        pytest.skip("Tkinter not available in CI environment")
    try:
        with patch('tkinter.Tk') as mock_tk, \
             patch('tkinter.messagebox') as mock_msg, \
             patch('tkinter.Label') as mock_label, \
             patch('tkinter.Entry') as mock_entry, \
             patch('tkinter.Button') as mock_button:
            yield {
                'tk': mock_tk,
                'messagebox': mock_msg,
                'Label': mock_label,
                'Entry': mock_entry,
                'Button': mock_button
            }
    except (TypeError, AttributeError):
        pytest.skip("Tkinter not properly available")

@pytest.fixture
def fitness_app(mock_tkinter):
    """Create FitnessTrackerApp instance with mocked tkinter"""
    module = load_aceest_module()
    mock_master = Mock()
    app = module.FitnessTrackerApp(mock_master)
    return app

def test_fitness_app_init(fitness_app):
    """Test FitnessTrackerApp initialization"""
    assert fitness_app.master is not None
    assert fitness_app.workouts == []

def test_add_workout_valid(fitness_app, mock_tkinter):
    """Test adding a valid workout"""
    fitness_app.workout_entry = Mock()
    fitness_app.workout_entry.get.return_value = "Push-ups"
    fitness_app.duration_entry = Mock()
    fitness_app.duration_entry.get.return_value = "30"
    
    fitness_app.add_workout()
    
    assert len(fitness_app.workouts) == 1
    assert fitness_app.workouts[0]["workout"] == "Push-ups"
    assert fitness_app.workouts[0]["duration"] == 30

def test_add_workout_empty_fields(fitness_app, mock_tkinter):
    """Test adding workout with empty fields"""
    fitness_app.workout_entry = Mock()
    fitness_app.workout_entry.get.return_value = ""
    fitness_app.duration_entry = Mock()
    fitness_app.duration_entry.get.return_value = ""
    
    fitness_app.add_workout()
    
    assert len(fitness_app.workouts) == 0
    mock_tkinter['messagebox'].showerror.assert_called()

def test_add_workout_invalid_duration(fitness_app, mock_tkinter):
    """Test adding workout with invalid duration"""
    fitness_app.workout_entry = Mock()
    fitness_app.workout_entry.get.return_value = "Push-ups"
    fitness_app.duration_entry = Mock()
    fitness_app.duration_entry.get.return_value = "not_a_number"
    
    fitness_app.add_workout()
    
    assert len(fitness_app.workouts) == 0
    mock_tkinter['messagebox'].showerror.assert_called()

def test_view_workouts_empty(fitness_app, mock_tkinter):
    """Test viewing workouts when none exist"""
    fitness_app.view_workouts()
    mock_tkinter['messagebox'].showinfo.assert_called()

def test_view_workouts_with_data(fitness_app, mock_tkinter):
    """Test viewing workouts with data"""
    fitness_app.workouts = [
        {"workout": "Push-ups", "duration": 30},
        {"workout": "Squats", "duration": 20}
    ]
    fitness_app.view_workouts()
    mock_tkinter['messagebox'].showinfo.assert_called()

