"""
Unit tests for ACEest_Fitness-V1.3.py
"""
import pytest
import sys
import os
import importlib.util
from unittest.mock import Mock, patch, MagicMock
from datetime import date

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

def load_aceest_v1_3():
    """Load ACEest_Fitness-V1.3 module"""
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ACEest_Fitness-V1.3.py')
    spec = importlib.util.spec_from_file_location("aceest_fitness_v1_3", file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["aceest_fitness_v1_3"] = module
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
             patch('tkinter.ttk.Button'), \
             patch('tkinter.ttk.Style'), \
             patch('tkinter.Frame'), \
             patch('tkinter.Toplevel'), \
             patch('tkinter.Text'), \
             patch('tkinter.ttk.Scrollbar'), \
             patch('matplotlib.backends.backend_tkagg.FigureCanvasTkAgg'), \
             patch('matplotlib.figure.Figure'), \
             patch('reportlab.pdfgen.canvas'):
            yield {'messagebox': mock_msg}
    except (TypeError, AttributeError):
        pytest.skip("Tkinter not properly available")

@pytest.fixture
def fitness_app_v1_3(mock_tkinter):
    """Create FitnessTrackerApp instance"""
    module = load_aceest_v1_3()
    mock_master = Mock()
    app = module.FitnessTrackerApp(mock_master)
    return app

def test_init_v1_3(fitness_app_v1_3):
    """Test initialization"""
    assert fitness_app_v1_3.workouts == {"Warm-up": [], "Workout": [], "Cool-down": []}
    assert fitness_app_v1_3.user_info == {}
    assert fitness_app_v1_3.daily_workouts == {}

def test_save_user_info_male(fitness_app_v1_3, mock_tkinter):
    """Test saving user info for male"""
    fitness_app_v1_3.name_entry = Mock()
    fitness_app_v1_3.name_entry.get.return_value = "Test User"
    fitness_app_v1_3.regn_entry = Mock()
    fitness_app_v1_3.regn_entry.get.return_value = "REG001"
    fitness_app_v1_3.age_entry = Mock()
    fitness_app_v1_3.age_entry.get.return_value = "30"
    fitness_app_v1_3.gender_entry = Mock()
    fitness_app_v1_3.gender_entry.get.return_value = "M"
    fitness_app_v1_3.height_entry = Mock()
    fitness_app_v1_3.height_entry.get.return_value = "175"
    fitness_app_v1_3.weight_entry = Mock()
    fitness_app_v1_3.weight_entry.get.return_value = "70"
    
    fitness_app_v1_3.save_user_info()
    
    assert fitness_app_v1_3.user_info["gender"] == "M"
    assert "bmi" in fitness_app_v1_3.user_info
    assert "bmr" in fitness_app_v1_3.user_info

def test_save_user_info_female(fitness_app_v1_3, mock_tkinter):
    """Test saving user info for female"""
    fitness_app_v1_3.name_entry = Mock()
    fitness_app_v1_3.name_entry.get.return_value = "Test User"
    fitness_app_v1_3.regn_entry = Mock()
    fitness_app_v1_3.regn_entry.get.return_value = "REG002"
    fitness_app_v1_3.age_entry = Mock()
    fitness_app_v1_3.age_entry.get.return_value = "25"
    fitness_app_v1_3.gender_entry = Mock()
    fitness_app_v1_3.gender_entry.get.return_value = "F"
    fitness_app_v1_3.height_entry = Mock()
    fitness_app_v1_3.height_entry.get.return_value = "165"
    fitness_app_v1_3.weight_entry = Mock()
    fitness_app_v1_3.weight_entry.get.return_value = "60"
    
    fitness_app_v1_3.save_user_info()
    
    assert fitness_app_v1_3.user_info["gender"] == "F"

def test_add_workout_v1_3(fitness_app_v1_3, mock_tkinter):
    """Test adding workout with calorie calculation"""
    fitness_app_v1_3.user_info = {"weight": 70}
    fitness_app_v1_3.category_var = Mock()
    fitness_app_v1_3.category_var.get.return_value = "Workout"
    fitness_app_v1_3.workout_entry = Mock()
    fitness_app_v1_3.workout_entry.get.return_value = "Running"
    fitness_app_v1_3.duration_entry = Mock()
    fitness_app_v1_3.duration_entry.get.return_value = "30"
    fitness_app_v1_3.status_label = Mock()
    
    fitness_app_v1_3.add_workout()
    
    assert len(fitness_app_v1_3.workouts["Workout"]) == 1
    assert "calories" in fitness_app_v1_3.workouts["Workout"][0]
    assert fitness_app_v1_3.workouts["Workout"][0]["calories"] > 0

def test_add_workout_invalid_duration_v1_3(fitness_app_v1_3, mock_tkinter):
    """Test adding workout with invalid duration"""
    fitness_app_v1_3.category_var = Mock()
    fitness_app_v1_3.category_var.get.return_value = "Workout"
    fitness_app_v1_3.workout_entry = Mock()
    fitness_app_v1_3.workout_entry.get.return_value = "Test"
    fitness_app_v1_3.duration_entry = Mock()
    fitness_app_v1_3.duration_entry.get.return_value = "-10"
    
    fitness_app_v1_3.add_workout()
    
    assert len(fitness_app_v1_3.workouts["Workout"]) == 0

def test_view_summary_v1_3(fitness_app_v1_3, mock_tkinter):
    """Test viewing summary"""
    fitness_app_v1_3.workouts["Workout"] = [
        {"exercise": "Running", "duration": 30, "calories": 100.0, "timestamp": "2024-01-01 10:00:00"}
    ]
    fitness_app_v1_3.view_summary()
    assert True

def test_update_progress_charts_empty(fitness_app_v1_3):
    """Test updating progress charts with no data"""
    fitness_app_v1_3.chart_container = Mock()
    fitness_app_v1_3.chart_container.winfo_children.return_value = []
    fitness_app_v1_3.update_progress_charts()
    assert True

def test_update_progress_charts_with_data(fitness_app_v1_3):
    """Test updating progress charts with data"""
    fitness_app_v1_3.workouts["Workout"] = [
        {"exercise": "Test", "duration": 30, "calories": 100.0, "timestamp": "2024-01-01 10:00:00"}
    ]
    fitness_app_v1_3.chart_container = Mock()
    fitness_app_v1_3.chart_container.winfo_children.return_value = []
    fitness_app_v1_3.chart_canvas = None
    fitness_app_v1_3.update_progress_charts()
    assert True

def test_export_weekly_report_no_user_info(fitness_app_v1_3, mock_tkinter):
    """Test exporting report without user info"""
    fitness_app_v1_3.user_info = {}
    fitness_app_v1_3.export_weekly_report()
    mock_tkinter['messagebox'].showerror.assert_called()

def test_export_weekly_report_with_data(fitness_app_v1_3, mock_tkinter):
    """Test exporting report with data"""
    fitness_app_v1_3.user_info = {
        "name": "Test User",
        "regn_id": "REG001",
        "age": 30,
        "gender": "M",
        "height": 175,
        "weight": 70,
        "bmi": 22.9,
        "bmr": 1700
    }
    fitness_app_v1_3.workouts["Workout"] = [
        {"exercise": "Running", "duration": 30, "calories": 100.0, "timestamp": "2024-01-01 10:00:00"}
    ]
    fitness_app_v1_3.export_weekly_report()
    mock_tkinter['messagebox'].showinfo.assert_called()

def test_on_tab_change(fitness_app_v1_3):
    """Test tab change handler"""
    fitness_app_v1_3.notebook = Mock()
    fitness_app_v1_3.notebook.select.return_value = "tab_id"
    fitness_app_v1_3.notebook.tab.return_value = {"text": "📈 Progress Tracker"}
    fitness_app_v1_3.update_progress_charts = Mock()
    
    event = Mock()
    fitness_app_v1_3.on_tab_change(event)
    
    fitness_app_v1_3.update_progress_charts.assert_called()

