from google.oauth2 import service_account
from googleapiclient.discovery import build
from credsdict import creds
import pandas as pd

def service(creds: str, scope: list):

  SERVICE_ACCOUNT_FILE = creds
  SCOPES = scope
  
  credentials = service_account.Credentials.from_service_account_file(
          SERVICE_ACCOUNT_FILE, scopes=SCOPES)
  
  service = build('sheets', 'v4', credentials=credentials)

  return service

def okoservice():
  return service(creds["serviceacc"],['https://www.googleapis.com/auth/spreadsheets'])

service = okoservice()

def get_values(spreadsheet_id: str, sheetname:str, range: str, service = service):
  range_name = f"{sheetname}!{range}"
  try:
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=range_name)
        .execute()
    )
    rows = result.get("values", [])
    return rows

  except HttpError as error:
    print(f"An error occurred: {error}")
    return error

def dffromsheet(data: list):
  df = pd.DataFrame(data[1:], columns=data[0])
  return df

def sheetfromdf(df: pd.DataFrame) -> list:
  if df.empty:
    return []
    # Convert DataFrame to list of lists
    data = df.values.tolist()
    # Add column names as the first row
    data.insert(0, df.columns.tolist())
    return data
