import streamlit as st
import pandas as pd
import requests
from io import StringIO
from funcs import format_dk, to_float, getthismonth
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

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet=sheet_name,
        usecols=['måned', 'fast_var', 'kredit_debit', 'Kategori', 'Ind_ud', 'Navn', 'beløb_måned', 'beløb_kvartal', 'beløb_år', "beløb"],
        ttl=0)
df = df.dropna(subset=["måned"])

df["beløb"] = df["beløb"].replace(",", "", regex=True).astype(float)
df_ulon = df[df["Kategori"] != "løn"]
df_ulon_ustatus = df_ulon[df_ulon["Kategori"] != "status"]

col1, col2, col3 = st.columns(3)
with col1:
    # Get the specific value from the dataframe
    value = df[df["Navn"] == "til udbetaling"]["beløb"].values[0]
    # Format the value using f-string and swap comma and period
    formatted_value = format_dk(value)
    # Create the metric using the formatted value
    st.metric("Løn udbetalt", formatted_value, delta=None, delta_color="normal", help=None, label_visibility="visible")
with col2:
    udgifter = df[(df['Ind_ud'] == 'ud') & (df['Kategori'] != 'løn')]['beløb'].sum()
    # Format the value using f-string and swap comma and period
    udgifter_form = format_dk(udgifter)
    # Create the metric using the formatted value
    st.metric("Udgifter", udgifter_form, delta=None, delta_color="normal", help=None, label_visibility="visible")
with col3:
    resultat = value - udgifter
    # Format the value using f-string and swap comma and period
    resultat_form = format_dk(resultat)
    # Create the metric using the formatted value
    st.metric("Resultat", resultat_form, delta=None, delta_color="normal", help=None, label_visibility="visible")

col1, col2, col3 = st.columns(3)
with col1:
    # Get the specific value from the dataframe
    value = df_ulon_ustatus[df_ulon_ustatus["fast_var"] == "fast"]["beløb"].sum()
    # Format the value using f-string and swap comma and period
    formatted_value = format_dk(value)
    # Create the metric using the formatted value
    st.metric("Faste udgifter", formatted_value, delta=None, delta_color="normal", help=None, label_visibility="visible")
with col2:
    # Get the specific value from the dataframe
    value = df_ulon_ustatus[df_ulon_ustatus["fast_var"] == "var"]["beløb"].sum()
    # Format the value using f-string and swap comma and period
    formatted_value = format_dk(value)
    # Create the metric using the formatted value
    st.metric("Månedens udgifter", formatted_value, delta=None, delta_color="normal", help=None, label_visibility="visible")

import plotly.express as px

fig = px.bar(df_ulon_ustatus, x='Navn', y='beløb', color='fast_var')
fig.update_layout(
    height=400,
    xaxis_title="",
)
config = {'displayModeBar': False}
st.plotly_chart(fig, use_container_width=True, config=config)

col1, col2 = st.columns(2)
with col2:
    fast_var = st.selectbox("Vælg kategory", df_ulon_ustatus['fast_var'].unique())
    df_ulon_ustatus_var = df_ulon_ustatus[df_ulon_ustatus["fast_var"] == fast_var]

col1, col2 = st.columns(2)
with col1:
    fig = px.pie(df_ulon_ustatus, values='beløb', names='fast_var')
    fig.update_traces(textposition='inside', textinfo='value+label')
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig = px.bar(df_ulon_ustatus_var, x='Navn', y='beløb', color='Kategori')
    fig.update_layout(
        xaxis_title="")
    st.plotly_chart(fig, use_container_width=True, config=config)

col1, col2 = st.columns(2)
with col2:
    category = st.selectbox("Vælg kategory", df_ulon_ustatus['Kategori'].unique())

col1, col2 = st.columns(2)
with col1:
    fig = px.pie(df_ulon_ustatus, values='beløb', names='Kategori')
    fig.update_traces(textposition='inside', textinfo='value+label')
    st.plotly_chart(fig, use_container_width=True)
with col2:
    df_ulon_ustatus_kat = df_ulon_ustatus[df_ulon["Kategori"] == category]
    fig = px.bar(df_ulon_ustatus_kat, x='Navn', y='beløb', color='fast_var')
    fig.update_layout(
        xaxis_title="")
    st.plotly_chart(fig, use_container_width=True, config=config)