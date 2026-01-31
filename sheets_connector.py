import os
from googleapiclient import discovery

class GoogleSheetsConnector:
    def __init__(self, api_key):
        """
        Initialize the Google Sheets connector using API Key.
        
        Args:
            api_key: Your Google API Key for read-only access
        """
        self.api_key = api_key
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Google Sheets API using API Key."""
        # Build the service with API key (read-only)
        self.service = discovery.build('sheets', 'v4', developerKey=self.api_key)
    
    def get_values(self, spreadsheet_id, range_name):
        """
        Read values from a Google Sheet.
        
        Args:
            spreadsheet_id: The ID of the spreadsheet
            range_name: The A1 notation of the range (e.g., 'Sheet1!A1:D10')
        
        Returns:
            List of lists containing the cell values
        """
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            values = result.get('values', [])
            return values
        except Exception as e:
            print(f"Error reading from sheet: {e}")
            return None
    
    def write_values(self, spreadsheet_id, range_name, values):
        """
        Write values to a Google Sheet.
        
        Args:
            spreadsheet_id: The ID of the spreadsheet
            range_name: The A1 notation of the range
            values: List of lists containing the values to write
        
        Returns:
            The response from the API
        """
        try:
            body = {'values': values}
            result = self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            print(f"Updated {result.get('updatedCells')} cells")
            return result
        except Exception as e:
            print(f"Error writing to sheet: {e}")
            return None
    
    def append_values(self, spreadsheet_id, range_name, values):
        """
        Append values to a Google Sheet.
        
        Args:
            spreadsheet_id: The ID of the spreadsheet
            range_name: The A1 notation of the range
            values: List of lists containing the values to append
        
        Returns:
            The response from the API
        """
        try:
            body = {'values': values}
            result = self.service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            print(f"Appended {result.get('updates').get('updatedRows')} rows")
            return result
        except Exception as e:
            print(f"Error appending to sheet: {e}")
            return None


# Example usage
if __name__ == '__main__':
    # Initialize connector with your API Key
    api_key = 'YOUR_API_KEY'  # Replace with your Google API Key
    connector = GoogleSheetsConnector(api_key)
    
    # Example: Read data from a public Google Sheet
    # Replace with your actual spreadsheet ID
    spreadsheet_id = 'YOUR_SPREADSHEET_ID'  # From the URL: /d/{SPREADSHEET_ID}/edit
    range_name = 'Sheet1!A1:D10'
    
    # values = connector.get_values(spreadsheet_id, range_name)
    # if values:
    #     for row in values:
    #         print(row)
    
    print("To use this connector:")
    print("1. Set api_key to your Google API Key")
    print("2. Set spreadsheet_id to your Google Sheet's ID")
    print("3. Make sure the sheet is shared publicly or with 'Anyone with link'")
