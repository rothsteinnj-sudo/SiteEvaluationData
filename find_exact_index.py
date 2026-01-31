#!/usr/bin/env python3
from googleapiclient import discovery

api_key = 'AIzaSyBVqH00y4Ta4Iw5oavrkdP3e04ixJOtL_M'
service = discovery.build('sheets', 'v4', developerKey=api_key)

# Get headers and first response
result = service.spreadsheets().values().get(
    spreadsheetId='1pO0-3Px5GStwT0vGqXiN6Z1Bjp2Vczwg2peXwITXGiY',
    range='Responses_Raw!A1:AZ2'
).execute()

values = result.get('values', [])
if len(values) > 1:
    headers = values[0]
    response = values[1]
    
    print("Looking for 'site name' or 'enter' in questions...")
    for i, h in enumerate(headers):
        if 'enter' in h.lower() and 'site' in h.lower():
            print(f"FOUND AT [{i}]: {h}")
            print(f"  Value: {response[i] if i < len(response) else 'EMPTY'}")
    
    print(f"\nCurrent index 2 contains:")
    print(f"  Header: {headers[2]}")
    print(f"  Value: {response[2] if len(response) > 2 else 'EMPTY'}")
