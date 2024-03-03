import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_title="Økonomisk overblik",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(worksheet="Januar")
st.dataframe(data)

st.markdown(data.columns)