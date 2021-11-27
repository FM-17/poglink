#!/bin/sh

# Create & source virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install bot
pip install -r requirements.txt