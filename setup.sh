#!/bin/sh

# Create & source virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Update pip
pip install -U pip

# Install bot
pip install -r requirements.txt