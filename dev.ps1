# Simple development script
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -e .[test]
python -m pytest tests/
python examples/simple.py