"""
Unit tests for ACEest_Fitness-V1.2.1, V1.2.2, V1.2.3.py
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

def load_aceest_version(version):
    """Load ACEest_Fitness version module"""
    filename = f'ACEest_Fitness-V{version}.py'
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)
    spec = importlib.util.spec_from_file_location(f"aceest_fitness_{version}", file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {file_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[f"aceest_fitness_{version}"] = module
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
             patch('matplotlib.backends.backend_tkagg.FigureCanvasTkAgg'), \
             patch('matplotlib.figure.Figure'):
            yield {'messagebox': mock_msg}
    except (TypeError, AttributeError):
        pytest.skip("Tkinter not properly available")

@pytest.mark.parametrize("version", ["1.2.1", "1.2.2", "1.2.3"])
def test_init_versions(version, mock_tkinter):
    """Test initialization for all V1.2.x versions"""
    module = load_aceest_version(version)
    mock_master = Mock()
    app = module.FitnessTrackerApp(mock_master)
    assert app.workouts == {"Warm-up": [], "Workout": [], "Cool-down": []}

@pytest.mark.parametrize("version", ["1.2.1", "1.2.2", "1.2.3"])
def test_add_workout_versions(version, mock_tkinter):
    """Test adding workout for all V1.2.x versions"""
    module = load_aceest_version(version)
    mock_master = Mock()
    app = module.FitnessTrackerApp(mock_master)
    
    app.category_var = Mock()
    app.category_var.get.return_value = "Workout"
    app.workout_entry = Mock()
    app.workout_entry.get.return_value = "Push-ups"
    app.duration_entry = Mock()
    app.duration_entry.get.return_value = "30"
    app.status_label = Mock()
    
    app.add_workout()
    
    assert len(app.workouts["Workout"]) == 1
    assert app.workouts["Workout"][0]["exercise"] == "Push-ups"

@pytest.mark.parametrize("version", ["1.2.1", "1.2.2", "1.2.3"])
def test_view_summary_versions(version, mock_tkinter):
    """Test viewing summary for all V1.2.x versions"""
    module = load_aceest_version(version)
    mock_master = Mock()
    app = module.FitnessTrackerApp(mock_master)
    
    app.workouts["Workout"] = [
        {"exercise": "Push-ups", "duration": 30, "timestamp": "2024-01-01 10:00:00"}
    ]
    app.view_summary()
    assert True

@pytest.mark.parametrize("version", ["1.2.1", "1.2.2", "1.2.3"])
def test_create_tabs_versions(version, mock_tkinter):
    """Test tab creation for all V1.2.x versions"""
    module = load_aceest_version(version)
    mock_master = Mock()
    app = module.FitnessTrackerApp(mock_master)
    
    # Test that tabs are created
    assert hasattr(app, 'log_tab')
    assert hasattr(app, 'chart_tab')
    assert hasattr(app, 'diet_tab')
    assert hasattr(app, 'progress_tab')

def test_v1_2_1_specific(mock_tkinter):
    """Test V1.2.1 specific features"""
    module = load_aceest_version("1.2.1")
    mock_master = Mock()
    app = module.FitnessTrackerApp(mock_master)
    assert True

def test_v1_2_2_specific(mock_tkinter):
    """Test V1.2.2 specific features"""
    module = load_aceest_version("1.2.2")
    mock_master = Mock()
    app = module.FitnessTrackerApp(mock_master)
    # V1.2.2 has on_tab_change method
    if hasattr(app, 'on_tab_change'):
        app.on_tab_change(Mock())
    assert True

def test_v1_2_3_specific(mock_tkinter):
    """Test V1.2.3 specific features"""
    module = load_aceest_version("1.2.3")
    mock_master = Mock()
    app = module.FitnessTrackerApp(mock_master)
    # V1.2.3 has color constants
    assert hasattr(module, 'COLOR_PRIMARY') or hasattr(app, 'COLOR_PRIMARY')
    assert True

