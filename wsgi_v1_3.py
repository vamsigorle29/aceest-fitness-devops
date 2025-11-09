"""
WSGI entry point for app_v1.3.py
This wrapper allows gunicorn to load modules with dots in their names
"""
import sys
import os
import importlib.util

# Load the app module dynamically
file_path = os.path.join(os.path.dirname(__file__), 'app_v1.3.py')
spec = importlib.util.spec_from_file_location("app_v1_3", file_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Cannot load module from {file_path}")

app_module = importlib.util.module_from_spec(spec)
sys.modules["app_v1_3"] = app_module
spec.loader.exec_module(app_module)

# Export the app object for gunicorn
app = app_module.app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

