#!/usr/bin/env python3
from googleapiclient import discovery

API_KEY = 'AIzaSyBVqH00y4Ta4Iw5oavrkdP3e04ixJOtL_M'
SPREADSHEET_ID = '1pO0-3Px5GStwT0vGqXiN6Z1Bjp2Vczwg2peXwITXGiY'

service = discovery.build('sheets', 'v4', developerKey=API_KEY)

# Get spreadsheet metadata to see all sheet names
metadata = service.spreadsheets().get(
    spreadsheetId=SPREADSHEET_ID
).execute()

print("Sheet names:")
print("-" * 50)
for sheet in metadata.get('sheets', []):
    title = sheet['properties']['title']
    print(f"  - {title}")
