import locale

def format_dk(number):
    # Set the locale to Danish
    locale.setlocale(locale.LC_NUMERIC, 'da_DK.UTF-8')

    # Format the number using locale
    formatted_number = locale.format_string("%.2f", number, grouping=True) + " kr."

    # Reset the locale to default
    locale.setlocale(locale.LC_NUMERIC, '')

    return formatted_number


def to_float(formatted_number):
    # Set the locale to Danish
    locale.setlocale(locale.LC_NUMERIC, 'da_DK.UTF-8')

    # Remove any non-numeric characters except for '.' and ','
    cleaned_number = ''.join(char for char in formatted_number if char.isnumeric() or char in ['.', ','])

    # Replace ',' with '.' and convert to float
    float_number = float(cleaned_number.replace(',', '.'))

    # Reset the locale to default
    locale.setlocale(locale.LC_NUMERIC, '')

    return float_number

import streamlit as st
import pandas as pd
import requests
from io import StringIO

def read_sheet():
    months = ["Januar", "Februar"]

    sheet_id = "1H29_v1hU5H6wSAJj29QgyltHvletdJp8CFim1QXJrc4"
    col1, col2, col3 = st.columns(3)
    with col1:
        sheet_name = st.selectbox("Måned", months)
    
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    
    with col2:
        st.link_button("Google Sheet", url.replace("gviz/tq?tqx=out:csv&sheet=", "edit#gid="))

    # Use requests to download the CSV data
    response = requests.get(url, verify=True)  # Set verify to True to enable SSL certificate verification

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Use StringIO to convert the CSV content to a file-like object
        csv_data = StringIO(response.text)

        # Read the CSV data into a Pandas DataFrame
        df = pd.read_csv(csv_data, usecols=list(range(10)))
        return df, sheet_name

    else:
        return st.error(f"Failed to retrieve data. Status code: {response.status_code}")


from datetime import datetime
def getthismonth():
    today = datetime.now()
    month_number = today.month
    danish_month_names = {
    1: "januar",
    2: "februar",
    3: "marts",
    4: "april",
    5: "maj",
    6: "juni",
    7: "juli",
    8: "august",
    9: "september",
    10: "oktober",
    11: "november",
    12: "december",
    }
    return danish_month_names[month_number]

