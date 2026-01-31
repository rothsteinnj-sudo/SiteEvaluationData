#!/usr/bin/env python3
from googleapiclient import discovery

api_key = 'AIzaSyBVqH00y4Ta4Iw5oavrkdP3e04ixJOtL_M'
service = discovery.build('sheets', 'v4', developerKey=api_key)

# Get the header row
result = service.spreadsheets().values().get(
    spreadsheetId='1pO0-3Px5GStwT0vGqXiN6Z1Bjp2Vczwg2peXwITXGiY',
    range='Responses_Raw!1:1'
).execute()

headers = result.get('values', [[]])[0]
print(f"Total header columns: {len(headers)}")

if len(headers) > 118:
    print(f"Column index 118 header: '{headers[118]}'")
    
# Get response data
result2 = service.spreadsheets().values().get(
    spreadsheetId='1pO0-3Px5GStwT0vGqXiN6Z1Bjp2Vczwg2peXwITXGiY',
    range='Responses_Raw!2:5'
).execute()

responses = result2.get('values', [])
print(f"\nResponses loaded: {len(responses)}")

for idx, resp in enumerate(responses, start=2):
    if len(resp) > 118:
        value = resp[118]
        print(f"Response {idx}, Column DO (index 118): '{value}'")
    else:
        print(f"Response {idx} only has {len(resp)} columns")
