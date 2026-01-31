#!/bin/bash
# Start the Site Evaluation Scoring Web Application

cd "$(dirname "$0")" || exit

# Suppress warnings for cleaner output
export PYTHONWARNINGS="ignore"

# Run the Flask app with the correct Python interpreter
/Users/nina/opt/anaconda3/bin/python3 app.py 2>&1 | grep -v "FutureWarning\|deprecated\|warnings.warn"
