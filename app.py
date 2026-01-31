#!/usr/bin/env python3
"""
Site Evaluation Scoring Web Interface
Flask app for viewing and managing scores with automated scoring
"""

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from googleapiclient import discovery
import json
import os
from datetime import datetime
import threading
import time

API_KEY = 'AIzaSyBVqH00y4Ta4Iw5oavrkdP3e04ixJOtL_M'
FORM_SPREADSHEET_ID = '1pO0-3Px5GStwT0vGqXiN6Z1Bjp2Vczwg2peXwITXGiY'

app = Flask(__name__)
CORS(app)

# Import the scorer
from scorer import SiteEvaluationScorer

# Store cached scores
scored_responses = []
headers = []
last_response_count = 0
auto_scoring_enabled = True
last_updated = None

def get_sheets_service():
    """Get Google Sheets service"""
    return discovery.build('sheets', 'v4', developerKey=API_KEY)

def write_scores_to_sheets(scores):
    """Write calculated scores back to the Scores_ItemLevel sheet
    Note: API keys can only read, not write. This function would need OAuth2 credentials.
    For now, scores are only displayed in the dashboard.
    """
    try:
        # Note: This would require OAuth2 credentials, not an API key
        # For now, we just return True and scores are available via API
        return True
    except Exception as e:
        print(f"Info: Scores stored in memory/dashboard (write to sheets requires OAuth2): {e}")
        return True

def load_and_score_all():
    """Load all responses and score them"""
    global scored_responses, headers, last_response_count, last_updated
    
    try:
        scorer = SiteEvaluationScorer(API_KEY)
        
        # Load responses
        if not scorer.load_responses(FORM_SPREADSHEET_ID):
            return False
        
        headers = scorer.headers
        
        # Score all responses
        scored_responses = []
        for i, response in enumerate(scorer.responses, 1):
            score = scorer.score_response(response, i)
            # Add the response data to the score
            score['timestamp'] = response[0] if response else 'N/A'
            
            # Extract site name from column DO (index 118)
            site_name = 'Unknown Site'
            if len(response) > 118:
                value = response[118]
                if value and isinstance(value, str) and value.strip():
                    site_name = value.strip()
            
            score['site_name'] = site_name
            # Generate link to view raw response in Google Sheet (row i+1 because row 1 is headers)
            sheet_row = i + 1
            score['form_link'] = f'https://docs.google.com/spreadsheets/d/{FORM_SPREADSHEET_ID}/edit#gid=0&range=A{sheet_row}:DZ{sheet_row}'
            scored_responses.append(score)
        
        # Check if there are new responses
        if len(scored_responses) > last_response_count:
            new_count = len(scored_responses) - last_response_count
            print(f"✓ {new_count} new response(s) detected and scored!")
            # Write scores back to sheets
            write_scores_to_sheets(scored_responses)
        
        last_response_count = len(scored_responses)
        last_updated = datetime.now().isoformat()
        
        return True
    except Exception as e:
        print(f"Error loading/scoring: {e}")
        return False

def auto_score_worker():
    """Background worker for automatic scoring"""
    global auto_scoring_enabled
    
    while auto_scoring_enabled:
        try:
            load_and_score_all()
            # Check every 30 seconds for new submissions
            time.sleep(30)
        except Exception as e:
            print(f"Error in auto-scoring worker: {e}")
            time.sleep(30)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/scores', methods=['GET'])
def get_scores():
    """Get all scores"""
    if not scored_responses:
        load_and_score_all()
    
    return jsonify({
        'success': True,
        'count': len(scored_responses),
        'last_updated': last_updated,
        'scores': scored_responses
    })

@app.route('/api/score/<int:response_id>', methods=['GET'])
def get_score(response_id):
    """Get a specific score"""
    if not scored_responses:
        load_and_score_all()
    
    if 0 <= response_id - 1 < len(scored_responses):
        return jsonify({
            'success': True,
            'score': scored_responses[response_id - 1]
        })
    
    return jsonify({'success': False, 'error': 'Score not found'}), 404

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get scoring statistics"""
    if not scored_responses:
        load_and_score_all()
    
    if not scored_responses:
        return jsonify({
            'success': False,
            'error': 'No scores available'
        }), 404
    
    total_scores = [s['total_score'] for s in scored_responses]
    study_scores = [s['category_totals']['Study Capabilities'] for s in scored_responses]
    phase_scores = [s['category_totals']['Phase Capabilities'] for s in scored_responses]
    personnel_scores = [s['category_totals']['Key Personnel'] for s in scored_responses]
    
    return jsonify({
        'success': True,
        'total_responses': len(scored_responses),
        'average_score': sum(total_scores) / len(total_scores) if total_scores else 0,
        'highest_score': max(total_scores) if total_scores else 0,
        'lowest_score': min(total_scores) if total_scores else 0,
        'category_averages': {
            'Study Capabilities': sum(study_scores) / len(study_scores) if study_scores else 0,
            'Phase Capabilities': sum(phase_scores) / len(phase_scores) if phase_scores else 0,
            'Key Personnel': sum(personnel_scores) / len(personnel_scores) if personnel_scores else 0
        }
    })

@app.route('/api/refresh', methods=['POST'])
def refresh_scores():
    """Refresh scores from Google Sheets"""
    success = load_and_score_all()
    
    return jsonify({
        'success': success,
        'message': f'Loaded and scored {len(scored_responses)} responses',
        'timestamp': datetime.now().isoformat(),
        'auto_scoring': auto_scoring_enabled
    })

@app.route('/api/auto-scoring', methods=['GET', 'POST'])
def toggle_auto_scoring():
    """Get or toggle auto-scoring status"""
    global auto_scoring_enabled
    
    if request.method == 'POST':
        data = request.get_json()
        auto_scoring_enabled = data.get('enabled', auto_scoring_enabled)
    
    return jsonify({
        'success': True,
        'auto_scoring_enabled': auto_scoring_enabled,
        'last_updated': last_updated
    })

@app.route('/api/export', methods=['GET'])
def export_scores():
    """Export scores as JSON"""
    if not scored_responses:
        load_and_score_all()
    
    return jsonify({
        'export_date': datetime.now().isoformat(),
        'total_responses': len(scored_responses),
        'scores': scored_responses
    })

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Server error', 'message': str(e)}), 500

if __name__ == '__main__':
    print("=" * 70)
    print("Site Evaluation Scoring Dashboard")
    print("=" * 70)
    
    print("\nLoading initial scores...")
    load_and_score_all()
    print(f"✓ Loaded {len(scored_responses)} responses")
    
    # Start auto-scoring worker thread
    print("✓ Starting auto-scoring worker...")
    worker_thread = threading.Thread(target=auto_score_worker, daemon=True)
    worker_thread.start()
    
    print("\n" + "=" * 70)
    print("Web Dashboard: http://localhost:5000")
    print("=" * 70)
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(debug=True, port=5000, use_reloader=False)
