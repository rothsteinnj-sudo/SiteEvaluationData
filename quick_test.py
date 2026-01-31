#!/usr/bin/env python3
from googleapiclient import discovery

# Your credentials
API_KEY = 'AIzaSyBVqH00y4Ta4Iw5oavrkdP3e04ixJOtL_M'
SPREADSHEET_ID = '1pO0-3Px5GStwT0vGqXiN6Z1Bjp2Vczwg2peXwITXGiY'

print("=" * 70)
print("Testing Google Sheets API Connection")
print("=" * 70)
print()

# Build the service with API key
service = discovery.build('sheets', 'v4', developerKey=API_KEY)

print("✓ Connected successfully!")
print()
print("Reading data from spreadsheet...")
print(f"Spreadsheet ID: {SPREADSHEET_ID}")
print()

try:
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='Responses_Raw!A1:Z50'
    ).execute()
    
    values = result.get('values', [])
    
    if values:
        print(f"✓ Successfully read {len(values)} rows!")
        print()
        print("First 10 rows:")
        print("-" * 70)
        for i, row in enumerate(values[:10]):
            print(f"Row {i+1}: {row}")
        print()
        print("=" * 70)
        print("✓ All tests passed! Google Sheets API is working.")
        print("=" * 70)
    else:
        print("⚠ Sheet is empty or not accessible")
        
except Exception as e:
    print(f"✗ Error reading data: {e}")
