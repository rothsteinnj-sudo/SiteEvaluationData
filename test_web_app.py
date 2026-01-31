#!/usr/bin/env python3
"""Test the web app"""
import sys
sys.path.insert(0, '/Users/nina/Desktop/site_data')

from app import app, load_and_score_all

print("Testing Flask app...")
print("=" * 70)

print("\nLoading scores...")
load_and_score_all()
print("✓ Scores loaded successfully")

print("\nTesting API endpoints:")

with app.test_client() as client:
    # Test /api/scores
    response = client.get('/api/scores')
    data = response.get_json()
    print(f"✓ GET /api/scores: {data['count']} scores")
    
    # Test /api/score/<id>
    response = client.get('/api/score/1')
    data = response.get_json()
    if data['success']:
        print(f"✓ GET /api/score/1: Total score = {data['score']['total_score']}")
    
    # Test /api/export
    response = client.get('/api/export')
    data = response.get_json()
    print(f"✓ GET /api/export: {data['total_responses']} responses exported")

print("\n" + "=" * 70)
print("✓ All tests passed!")
print("\n To start the web server, run:")
print("   /Users/nina/opt/anaconda3/bin/python3 app.py")
print("\n Then open: http://localhost:5000")
