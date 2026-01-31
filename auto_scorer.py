#!/usr/bin/env python3
"""
Automated Scoring Service
Monitors Google Forms for new submissions and automatically scores them
Writes results back to Scores_Summary sheet
"""

from googleapiclient import discovery
import time
from datetime import datetime
import json

API_KEY = 'AIzaSyBVqH00y4Ta4Iw5oavrkdP3e04ixJOtL_M'
FORM_SPREADSHEET_ID = '1pO0-3Px5GStwT0vGqXiN6Z1Bjp2Vczwg2peXwITXGiY'
RUBRIC_SPREADSHEET_ID = '1vLwSqajfazSB8OYBJhK_OEwn2w5xVB-gbTsh_VjBMVI'

from scorer import SiteEvaluationScorer

class AutomatedScoringService:
    def __init__(self, api_key, poll_interval=300):
        """
        Initialize the automated scoring service
        
        Args:
            api_key: Google API key
            poll_interval: Seconds between checking for new submissions (default: 5 minutes)
        """
        self.api_key = api_key
        self.service = discovery.build('sheets', 'v4', developerKey=api_key)
        self.poll_interval = poll_interval
        self.last_checked = None
        self.last_response_count = 0
        self.scorer = SiteEvaluationScorer(api_key)
    
    def get_response_count(self):
        """Get the current number of responses"""
        result = self.service.spreadsheets().values().get(
            spreadsheetId=FORM_SPREADSHEET_ID,
            range='Responses_Raw!A:A'
        ).execute()
        
        values = result.get('values', [])
        # Subtract 1 for header
        return len(values) - 1
    
    def score_and_write_results(self):
        """Score all responses and write to Scores_Summary sheet"""
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Scoring all responses...")
        
        # Load and score
        if not self.scorer.load_responses(FORM_SPREADSHEET_ID):
            print("  ⚠ Failed to load responses")
            return False
        
        all_scores = []
        for i, response in enumerate(self.scorer.responses, 1):
            score = self.scorer.score_response(response, i)
            score['timestamp'] = response[0] if response else ''
            all_scores.append(score)
        
        # Prepare data for writing back
        score_data = [['Response #', 'Timestamp', 'Study Capabilities', 'Phase Capabilities', 'Key Personnel', 'Total Score']]
        
        for score in all_scores:
            row = [
                score['response_num'],
                score['timestamp'],
                score['category_totals'].get('Study Capabilities', 0),
                score['category_totals'].get('Phase Capabilities', 0),
                score['category_totals'].get('Key Personnel', 0),
                score['total_score']
            ]
            score_data.append(row)
        
        # Write to Scores_Summary sheet
        try:
            self.service.spreadsheets().values().update(
                spreadsheetId=FORM_SPREADSHEET_ID,
                range='Scores_Summary!A1',
                valueInputOption='USER_ENTERED',
                body={'values': score_data}
            ).execute()
            
            print(f"  ✓ Scored and written {len(all_scores)} responses to Scores_Summary")
            return True
            
        except Exception as e:
            print(f"  ✗ Error writing scores: {e}")
            return False
    
    def check_for_new_submissions(self):
        """Check if there are new form submissions"""
        current_count = self.get_response_count()
        
        if self.last_response_count == 0:
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Initial count: {current_count} responses")
            self.last_response_count = current_count
            return False
        
        if current_count > self.last_response_count:
            new_count = current_count - self.last_response_count
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✓ Found {new_count} new response(s)!")
            self.last_response_count = current_count
            return True
        
        return False
    
    def run(self):
        """Run the monitoring service"""
        print("=" * 70)
        print("AUTOMATED SITE EVALUATION SCORING SERVICE")
        print("=" * 70)
        print(f"\nConfiguration:")
        print(f"  Poll interval: {self.poll_interval} seconds")
        print(f"  Form ID: {FORM_SPREADSHEET_ID}")
        print(f"  Checking for new submissions...")
        print("\nPress Ctrl+C to stop the service\n")
        
        try:
            iteration = 0
            while True:
                iteration += 1
                
                # Check for new submissions
                if self.check_for_new_submissions():
                    # Score and write results
                    self.score_and_write_results()
                else:
                    status = "No changes" if iteration > 1 else "Initializing"
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {status} | Responses: {self.last_response_count} | Next check in {self.poll_interval}s")
                
                # Wait before next check
                time.sleep(self.poll_interval)
                
        except KeyboardInterrupt:
            print("\n\n✓ Service stopped")
            print("=" * 70)

def main():
    # Use 5-minute poll interval (300 seconds)
    service = AutomatedScoringService(API_KEY, poll_interval=300)
    service.run()

if __name__ == '__main__':
    main()
