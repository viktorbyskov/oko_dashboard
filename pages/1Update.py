import streamlit as st
import pandas as pd

# Import functions
import sys
sys.path.append('googledrive_api')
from googledrive_api.quickstart import get_values, creds, dffromsheet, sheetfromdf, write_values
from calc import calculate_belob

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
data = get_values(creds["sheetid"], sheet_name, range_nr)
df = dffromsheet(data)
original_df = df.copy()  # Create a copy of the original DataFrame

col1, col2, col3 = st.columns(3)
with col1:
    column_filter = st.selectbox("Filter Column", ["None"] + list(df.columns) if not df.empty else ["None"])
with col2:
    filter_value = st.text_input("Filter Value") if column_filter != "None" else None

if column_filter != "None" and filter_value:
    filtered_df = df[df[column_filter].astype(str).str.contains(filter_value, case=False, na=False)]
else:
    filtered_df = df

# Remove the 'beløb' column before displaying the editor
filtered_df_for_editing = filtered_df.drop(columns=['beløb'])

# Display the editor without the 'beløb' column
edited_df = st.data_editor(filtered_df_for_editing, num_rows="dynamic")

if st.button("Send data", type="primary"):
    # Update the original DataFrame with the changes made in the filtered DataFrame
    for idx, row in edited_df.iterrows():
        for col in edited_df.columns:
            original_df.at[idx, col] = row[col]
    # Recalculate the 'beløb' column
    original_df['beløb'] = original_df.apply(calculate_belob, axis=1)
    # Convert df to lists
    list_of_lists = sheetfromdf(original_df)
    # Write data
    write_values(creds["sheetid"], sheet_name, range_nr, list_of_lists)
    # Success
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("Data updated")