#!/usr/bin/env python3
from googleapiclient import discovery

API_KEY = 'AIzaSyBVqH00y4Ta4Iw5oavrkdP3e04ixJOtL_M'
RUBRIC_SPREADSHEET_ID = '1vLwSqajfazSB8OYBJhK_OEwn2w5xVB-gbTsh_VjBMVI'

service = discovery.build('sheets', 'v4', developerKey=API_KEY)

# Get all sheets in the rubric spreadsheet
metadata = service.spreadsheets().get(
    spreadsheetId=RUBRIC_SPREADSHEET_ID
).execute()

print("Rubric Spreadsheet Sheets:")
print("-" * 50)
for sheet in metadata.get('sheets', []):
    title = sheet['properties']['title']
    print(f"  - {title}")

print("\n" + "=" * 70)
print("Fetching first few sheets to understand rubric structure...")
print("=" * 70 + "\n")

# Get data from each sheet
for sheet_name in ['Sheet1', 'Rubric', 'Scoring']:
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=RUBRIC_SPREADSHEET_ID,
            range=f'{sheet_name}!A1:Z100'
        ).execute()
        
        values = result.get('values', [])
        if values:
            print(f"\n{sheet_name}:")
            print("-" * 70)
            for i, row in enumerate(values[:15]):  # Show first 15 rows
                print(f"Row {i+1}: {row}")
    except:
        pass
