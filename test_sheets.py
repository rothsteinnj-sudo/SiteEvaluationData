#!/usr/bin/env python3
"""
Test script to verify Google Sheets API connection
"""

from sheets_connector import GoogleSheetsConnector

# Your credentials
API_KEY = 'AIzaSyBVqH00y4Ta4Iw5oavrkdP3e04ixJOtL_M'
SPREADSHEET_ID = '1pO0-3Px5GStwT0vGqXiN6Z1Bjp2Vczwg2peXwITXGiY'

def main():
    print("=" * 70)
    print("Testing Google Sheets API Connection")
    print("=" * 70)
    print()
    
    # Initialize connector
    print("Initializing connector...")
    try:
        connector = GoogleSheetsConnector(API_KEY)
        print("✓ Connected successfully!")
        print()
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False
    
    # Try to read data
    print("Reading data from spreadsheet...")
    print(f"Spreadsheet ID: {SPREADSHEET_ID}")
    print()
    
    try:
        # Read the first sheet
        values = connector.get_values(SPREADSHEET_ID, 'Sheet1!A1:Z50')
        
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
            return True
        else:
            print("⚠ Sheet is empty or not accessible")
            return False
            
    except Exception as e:
        print(f"✗ Error reading data: {e}")
        print()
        print("Troubleshooting:")
        print("1. Make sure the spreadsheet is shared publicly or 'Anyone with link'")
        print("2. Verify the spreadsheet ID is correct")
        print("3. Check that the API Key has access to Google Sheets API")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
