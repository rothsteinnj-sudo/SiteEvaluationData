#!/usr/bin/env python3
"""
Script to highlight example data rows in Google Sheets with yellow background.
This marks rows with made-up data (2023, 2024, 2025) for easy identification.
"""

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Spreadsheet and sheet information
SPREADSHEET_ID = '1pO0-3Px5GStwT0vGqXiN6Z1Bjp2Vczwg2peXwITXGiY'
SHEET_NAME = 'Yearly Averages'  # Adjust if your sheet has a different name

# Yellow color (RGB format for Google Sheets API)
YELLOW_COLOR = {
    "red": 1.0,
    "green": 1.0,
    "blue": 0.0,  # Yellow: Red=1, Green=1, Blue=0
    "alpha": 1.0
}

def authenticate():
    """Authenticate with Google Sheets API using OAuth 2.0"""
    creds = None
    
    # Check if token.json exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If no valid credentials, prompt for login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # You'll need credentials.json from Google Cloud Console
            if not os.path.exists('credentials.json'):
                print("ERROR: credentials.json not found!")
                print("Please run setup_credentials.py first to set up OAuth 2.0 credentials.")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def highlight_example_data():
    """Highlight example data rows in yellow"""
    creds = authenticate()
    
    if not creds:
        print("Failed to authenticate. Cannot highlight data.")
        return False
    
    try:
        service = build('sheets', 'v4', credentials=creds)
        
        # Get sheet ID for the tab
        spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        sheets = spreadsheet.get('sheets', [])
        
        sheet_id = None
        for sheet in sheets:
            if sheet['properties']['title'] == SHEET_NAME:
                sheet_id = sheet['properties']['sheetId']
                break
        
        if sheet_id is None:
            print(f"Sheet '{SHEET_NAME}' not found. Available sheets:")
            for sheet in sheets:
                print(f"  - {sheet['properties']['title']}")
            return False
        
        # Example years to highlight
        example_years = [2023, 2024, 2025]
        
        # Build batch update requests to highlight rows with example data
        requests = []
        
        # We need to find the rows with these years first
        # For now, we'll apply formatting to a range that covers typical year data
        # Adjust row numbers based on your actual sheet structure
        
        for year in example_years:
            # Create a request to highlight the row with this year
            # Adjust these row indices based on your sheet structure
            row_index = None
            if year == 2025:
                row_index = 1  # Adjust based on actual position
            elif year == 2024:
                row_index = 2
            elif year == 2023:
                row_index = 3
            
            if row_index is not None:
                requests.append({
                    "updateCells": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": row_index,
                            "endRowIndex": row_index + 1,
                            "startColumnIndex": 0,
                            "endColumnIndex": 10  # Columns A through J
                        },
                        "rows": [
                            {
                                "values": [
                                    {
                                        "userEnteredFormat": {
                                            "backgroundColor": YELLOW_COLOR
                                        }
                                    }
                                    for _ in range(10)
                                ]
                            }
                        ],
                        "fields": "userEnteredFormat.backgroundColor"
                    }
                })
        
        if not requests:
            print("No rows to highlight. Check your sheet structure and row indices.")
            return False
        
        # Execute the batch update
        body = {'requests': requests}
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=body
        ).execute()
        
        print(f"✓ Successfully highlighted {len(example_years)} rows with yellow background")
        print(f"  Years marked: {', '.join(map(str, example_years))}")
        return True
        
    except Exception as e:
        print(f"Error highlighting data: {e}")
        return False

def main():
    print("=" * 70)
    print("Google Sheets Example Data Highlighter")
    print("=" * 70)
    print()
    print("This script will highlight example data rows in yellow.")
    print(f"Spreadsheet: {SPREADSHEET_ID}")
    print(f"Sheet: {SHEET_NAME}")
    print()
    
    if highlight_example_data():
        print()
        print("✓ Highlighting complete!")
    else:
        print()
        print("✗ Failed to highlight data.")

if __name__ == '__main__':
    main()
