#!/usr/bin/env python3
"""
Setup script to create OAuth 2.0 credentials for Google Sheets API.
This will open a browser for you to authorize the application.
"""

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def create_credentials():
    """Create OAuth 2.0 credentials interactively."""
    
    print("=" * 70)
    print("Google Sheets OAuth 2.0 Credential Setup")
    print("=" * 70)
    print()
    
    print("To set up OAuth 2.0 credentials, follow these steps:")
    print()
    print("1. Go to: https://console.cloud.google.com/")
    print("2. Create a new project (name it 'Site Evaluation Data')")
    print("3. Go to APIs & Services > Library")
    print("4. Search for 'Google Sheets API' and enable it")
    print("5. Go to APIs & Services > Credentials")
    print("6. Click 'Create Credentials' > 'OAuth 2.0 Client IDs'")
    print("7. Choose 'Desktop application'")
    print("8. Click 'Create'")
    print("9. Download the JSON file and save it as 'credentials.json'")
    print("   in this directory (/Users/nina/Desktop/site_data/)")
    print()
    print("-" * 70)
    print()
    
    if os.path.exists('credentials.json'):
        print("✓ Found credentials.json - proceeding with authorization...")
        print()
        
        try:
            # Create the flow from the credentials file
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            
            # Run the local server for OAuth (using port 0 for automatic selection)
            creds = flow.run_local_server(port=0)
            
            # Save the credentials
            import pickle
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
            
            print()
            print("=" * 70)
            print("✓ SUCCESS! Credentials have been saved.")
            print("=" * 70)
            print()
            print("You can now use the GoogleSheetsConnector in your Python code!")
            print()
            
        except Exception as e:
            print(f"✗ Error during authorization: {e}")
            print()
            print("Make sure you clicked 'Allow' in the browser window.")
            return False
    else:
        print("✗ credentials.json not found!")
        print()
        print("Please download the OAuth 2.0 credentials JSON file from Google Cloud Console")
        print("and save it as 'credentials.json' in this directory.")
        print()
        return False
    
    return True

if __name__ == '__main__':
    success = create_credentials()
    exit(0 if success else 1)
