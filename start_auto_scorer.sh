#!/bin/bash
# Start Automated Scoring Service

echo "=================================="
echo "Automated Scoring Service"
echo "=================================="
echo ""
echo "Starting background scoring..."
echo "Press Ctrl+C to stop"
echo ""

cd /Users/nina/Desktop/site_data

/Users/nina/opt/anaconda3/bin/python3 auto_scorer.py

echo ""
echo "Service stopped."
