from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import os
import json

def get_service_account_info() -> dict:
    """Fetches the service account information from the environment variable."""
    return json.loads(os.environ['GCP_SERVICE_ACCOUNT_KEY'])

def service(scope: list) -> build:
    """Builds and returns the Google Sheets API service."""
    credentials = service_account.Credentials.from_service_account_info(
        get_service_account_info(), scopes=scope
    )
    return build('sheets', 'v4', credentials=credentials)

def okoservice() -> build:
    """Returns the Google Sheets API service with predefined scopes."""
    return service(['https://www.googleapis.com/auth/spreadsheets'])

service = okoservice()

def get_values(spreadsheet_id: str, sheetname: str, range_: str, service=service) -> list:
    """Fetches values from a specified Google Sheets range."""
    range_name = f"{sheetname}!{range_}"
    try:
        result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        return result.get("values", [])
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

def dffromsheet(data: list) -> pd.DataFrame:
    """Converts a list of lists to a pandas DataFrame."""
    if data:
        return pd.DataFrame(data[1:], columns=data[0])
    return pd.DataFrame()

def sheetfromdf(df: pd.DataFrame) -> list:
    """Converts a pandas DataFrame to a list of lists suitable for Google Sheets API."""
    columns = df.columns.tolist()
    rows = df.values.tolist()
    return [columns] + rows

def write_values(spreadsheet_id: str, sheetname: str, range_: str, values: list, service=service, value_input_option="USER_ENTERED") -> list:
    """Writes values to a specified Google Sheets range."""
    range_name = f"{sheetname}!{range_}"
    body = {'values': values}
    try:
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption=value_input_option,
            body=body
        ).execute()
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

# Example usage:
if __name__ == "__main__":
    SPREADSHEET_ID = '1H29_v1hU5H6wSAJj29QgyltHvletdJp8CFim1QXJrc4'
    SHEET_NAME = 'Maj'
    
    # Read values from the sheet
    values = get_values(SPREADSHEET_ID, SHEET_NAME, 'A1:D5')
    print("Values from the sheet:", values)
    
    # Convert to DataFrame
    df = dffromsheet(values)
    print("DataFrame from sheet values:", df.head())