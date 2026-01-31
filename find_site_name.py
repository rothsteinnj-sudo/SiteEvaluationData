#!/usr/bin/env python3
from googleapiclient import discovery

api_key = 'AIzaSyBVqH00y4Ta4Iw5oavrkdP3e04ixJOtL_M'
service = discovery.build('sheets', 'v4', developerKey=api_key)

result = service.spreadsheets().values().get(
    spreadsheetId='1pO0-3Px5GStwT0vGqXiN6Z1Bjp2Vczwg2peXwITXGiY',
    range='Responses_Raw!A1:AF2'
).execute()

values = result.get('values', [])
if len(values) > 1:
    headers = values[0]
    response = values[1]
    
    print("Looking for site name column...")
    for i in range(len(headers)):
        h = headers[i]
        if i < len(response):
            print(f"[{i}] {h[:60]}")
            print(f"    → {response[i][:60]}")
        else:
            print(f"[{i}] {h[:60]}")
            print(f"    → (empty)")
        if 'site' in h.lower() or 'name' in h.lower():
            print(f"    ✓ MATCH FOUND AT INDEX {i}")
