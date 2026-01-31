#!/usr/bin/env python3
from googleapiclient import discovery

API_KEY = 'AIzaSyBVqH00y4Ta4Iw5oavrkdP3e04ixJOtL_M'
RUBRIC_SPREADSHEET_ID = '1vLwSqajfazSB8OYBJhK_OEwn2w5xVB-gbTsh_VjBMVI'

service = discovery.build('sheets', 'v4', developerKey=API_KEY)

# Get the Auto Scoring Rubric sheet
print("Auto Scoring Rubric (First 50 rows):")
print("=" * 70)

result = service.spreadsheets().values().get(
    spreadsheetId=RUBRIC_SPREADSHEET_ID,
    range='Auto Scoring Rubric!A1:Z50'
).execute()

values = result.get('values', [])
if values:
    for i, row in enumerate(values):
        print(f"Row {i+1}: {row}")
