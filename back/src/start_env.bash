#!/bin/bash
echo "Python dependencies installed successfully."
if [ -d "venv" ]; then
  echo "Virtual environment 'venv' already exists. Skipping creation."
else
  python -m venv venv
  echo "Virtual environment 'venv' created."
fi
VENV_DIR="venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment $VENV_DIR not found."
    exit 1
fi
source "$VENV_DIR/bin/activate"

echo "Virtual environment $VENV_DIR activated."
REQUIREMENTS_FILE="requirements.txt"
if [ ! -f "$REQUIREMENTS_FILE" ]; then
    echo "Error: $REQUIREMENTS_FILE not found."
    exit 1
fi
pip install -r "$REQUIREMENTS_FILE"
source venv/bin/activate