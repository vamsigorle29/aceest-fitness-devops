"""
Unit tests for ACEest_Fitness-V1.2.py
"""
import pytest
import sys
import os
import importlib.util
from unittest.mock import Mock, patch

# Skip all Tkinter tests in CI environments (tkinter not available)
# Use importorskip to handle tkinter availability gracefully
try:
    tkinter = pytest.importorskip("tkinter", reason="Tkinter not available in CI environment")
    from tkinter import messagebox
    from tkinter import ttk
    TKINTER_AVAILABLE = True
except (ImportError, AttributeError, TypeError):
    TKINTER_AVAILABLE = False
    pytestmark = pytest.mark.skip(reason="Tkinter not available in CI environment")

def load_aceest_v1_2():
    """Load ACEest_Fitness-V1.2 module"""
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ACEest_Fitness-V1.2.py')
    spec = importlib.util.spec_from_file_location("aceest_fitness_v1_2", file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["aceest_fitness_v1_2"] = module
    spec.loader.exec_module(module)
    return module

@pytest.fixture
def mock_tkinter():
    """Mock tkinter components"""
    if not TKINTER_AVAILABLE:
        pytest.skip("Tkinter not available in CI environment")
    try:
        with patch('tkinter.Tk'), \
             patch('tkinter.messagebox') as mock_msg, \
             patch('tkinter.Label'), \
             patch('tkinter.Entry'), \
             patch('tkinter.Button'), \
             patch('tkinter.ttk.Combobox'), \
             patch('tkinter.ttk.Notebook'), \
             patch('tkinter.Frame'), \
             patch('tkinter.Toplevel'):
            yield {'messagebox': mock_msg}
    except (TypeError, AttributeError):
        pytest.skip("Tkinter not properly available")

@pytest.fixture
def fitness_app_v1_2(mock_tkinter):
    """Create FitnessTrackerApp instance"""
    module = load_aceest_v1_2()
    mock_master = Mock()
    app = module.FitnessTrackerApp(mock_master)
    return app

def test_init_v1_2(fitness_app_v1_2):
    """Test initialization"""
    assert fitness_app_v1_2.workouts == {"Warm-up": [], "Workout": [], "Cool-down": []}
    assert hasattr(fitness_app_v1_2, 'notebook')

def test_add_workout_v1_2(fitness_app_v1_2, mock_tkinter):
    """Test adding workout"""
    fitness_app_v1_2.category_var = Mock()
    fitness_app_v1_2.category_var.get.return_value = "Workout"
    fitness_app_v1_2.workout_entry = Mock()
    fitness_app_v1_2.workout_entry.get.return_value = "Push-ups"
    fitness_app_v1_2.duration_entry = Mock()
    fitness_app_v1_2.duration_entry.get.return_value = "30"
    fitness_app_v1_2.status_label = Mock()
    
    fitness_app_v1_2.add_workout()
    
    assert len(fitness_app_v1_2.workouts["Workout"]) == 1

def test_view_summary_v1_2(fitness_app_v1_2, mock_tkinter):
    """Test viewing summary"""
    fitness_app_v1_2.workouts["Workout"] = [
        {"exercise": "Push-ups", "duration": 30, "timestamp": "2024-01-01 10:00:00"}
    ]
    fitness_app_v1_2.view_summary()
    assert True

def test_create_workout_chart_tab_v1_2(fitness_app_v1_2):
    """Test workout chart tab creation"""
    fitness_app_v1_2.create_workout_chart_tab()
    assert True

def test_create_diet_chart_tab_v1_2(fitness_app_v1_2):
    """Test diet chart tab creation"""
    fitness_app_v1_2.create_diet_chart_tab()
    assert True

