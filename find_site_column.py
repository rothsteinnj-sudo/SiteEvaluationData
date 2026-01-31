#!/usr/bin/env python3
from googleapiclient import discovery

api_key = 'AIzaSyBVqH00y4Ta4Iw5oavrkdP3e04ixJOtL_M'
service = discovery.build('sheets', 'v4', developerKey=api_key)

# Get header row
result = service.spreadsheets().values().get(
    spreadsheetId='1pO0-3Px5GStwT0vGqXiN6Z1Bjp2Vczwg2peXwITXGiY',
    range='Responses_Raw!1:1'
).execute()

headers = result.get('values', [[]])[0]
print(f"Total columns: {len(headers)}\n")

# Find columns with "site" or "name" in header
for i, header in enumerate(headers):
    if any(word in header.lower() for word in ['site', 'name', 'owner']):
        print(f"Index {i}: {header}")

# Now get first data row to see what's in each
print("\n--- Data in first response ---")
result2 = service.spreadsheets().values().get(
    spreadsheetId='1pO0-3Px5GStwT0vGqXiN6Z1Bjp2Vczwg2peXwITXGiY',
    range='Responses_Raw!2:2'
).execute()

row = result2.get('values', [[]])[0] if result2.get('values') else []

# Show what's in those columns
for i, header in enumerate(headers):
    if any(word in header.lower() for word in ['site', 'name', 'owner']):
        val = row[i] if i < len(row) else '(empty)'
        print(f"Index {i}: [{val}]")
