import streamlit as st
import pandas as pd
import requests
from io import StringIO
from funcs import getthismonth
from streamlit_gsheets import GSheetsConnection

# Import functions
import sys
sys.path.append('googledrive_api')
from googledrive_api.quickstart import get_values, creds, dffromsheet, sheetfromdf

# Page config
st.set_page_config(
    page_title="Økonomisk overblik",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Start
range_nr = "A:Z"
months = ["Januar", "Februar", "Marts", "April", "Maj"]

col1, col2, col3 = st.columns(3)
with col1:
    sheet_name = st.selectbox("Måned", months)
with col2:
    st.link_button("Google Sheet", "https://docs.google.com/spreadsheets/d/1H29_v1hU5H6wSAJj29QgyltHvletdJp8CFim1QXJrc4/")
data = get_values(creds["sheetid"], sheet_name,range_nr)
df = dffromsheet(data)

st.data_editor(df)
st.write(df)

st.markdown(sheetfromdf(df))