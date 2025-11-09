"""
Pytest configuration and fixtures for ACEest Fitness tests
"""
import pytest
import sys
import os
import importlib.util

def load_app_module(version):
    """Load app module dynamically based on version"""
    version_map = {
        '1.1': 'app_v1.1.py',
        '1.2': 'app_v1.2.py',
        '1.3': 'app_v1.3.py'
    }
    
    if version not in version_map:
        raise ValueError(f"Unknown version: {version}")
    
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), version_map[version])
    module_name = f"app_v1_{version.replace('.', '_')}"
    
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load module from {file_path}")
    
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

@pytest.fixture(scope='module')
def app_v1_1():
    """Load app_v1.1 module"""
    module = load_app_module('1.1')
    app = module.app
    app.config['TESTING'] = True
    return app

@pytest.fixture(scope='module')
def app_v1_3():
    """Load app_v1.3 module"""
    module = load_app_module('1.3')
    app = module.app
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client_v1_1(app_v1_1):
    """Create test client for v1.1"""
    return app_v1_1.test_client()

@pytest.fixture
def client_v1_3(app_v1_3):
    """Create test client for v1.3"""
    return app_v1_3.test_client()

@pytest.fixture
def v1_3_functions():
    """Load v1.3 calculation functions"""
    module = load_app_module('1.3')
    return {
        'calculate_calories': module.calculate_calories,
        'calculate_bmi': module.calculate_bmi,
        'calculate_bmr': module.calculate_bmr
    }

