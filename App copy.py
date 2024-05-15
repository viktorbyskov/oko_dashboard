import streamlit as st
import pandas as pd
import requests
from io import StringIO
from funcs import getthismonth
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_title="Økonomisk overblik",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

months = ["Januar", "Februar", "Marts", "April", "Maj"]
thismonth = getthismonth().capitalize()
index_of_thismonth = months.index(thismonth)
months = [thismonth] + months

col1, col2, col3 = st.columns(3)
with col1:
    sheet_name = st.selectbox("Måned", months)
with col2:
    st.link_button("Google Sheet", "https://docs.google.com/spreadsheets/d/1H29_v1hU5H6wSAJj29QgyltHvletdJp8CFim1QXJrc4/")