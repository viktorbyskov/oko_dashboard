import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, date

conn = st.connection("gsheets", type=GSheetsConnection)
olddf = conn.read(worksheet="Kur",
                    usecols=['Dato', 'Salat', 'Løb', 'Km', 'Kmsnit'],
                    ttl=0).dropna(subset=["Dato"])

st.dataframe(olddf)

st.dataframe(olddf.dtypes)

today = date.today()

with st.form("my_form"):
    dato = st.date_input("When's your birthday", today)
    mad = st.selectbox("Kun salat?", ["Ja", "Nej", "Løb"])
    lob = st.selectbox("Løb", ["Ja", "Nej", "Andet"])
    km = st.number_input("Hvor langt?")
    submitted = st.form_submit_button("Submit")
    if submitted:
        newdict = {"Dato": dato,
                "Salat": mad,
                "Løb": lob,
                "Km": km}
        newdata = pd.DataFrame(newdict, index=[0])
        newdf = pd.concat([olddf, newdata], axis=0).reset_index(drop=True)
        newdf["Kmsnit"] = newdf["Km"].cumsum() / len(newdf)
        conn.update(worksheet="Kur", data=newdf)
        st.write("Success!")

st.dataframe(newdf)
st.dataframe(newdf.dtypes)
