import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

data = ""

with st.form("my_form"):
    maned = st.selectbox("Måned", ["Marts"])
    fast_var = st.selectbox("Fast eller variabel udgift", ["var", "fast", "Status"])
    kredit_debit = st.selectbox("Kredit elelr Debit", ["kredit", "debit"])
    kategori = st.text_input(label="Kategori")
    indud = st.selectbox("Indtægt eller udgift?", ["ud", "ind"])
    navn = st.text_input(label="Navn")
    belob_m = st.text_input(label="Beløb pr. måned")
    belob_k = st.text_input(label="Beløb pr. kvartal")
    belob_a = st.text_input(label="Beløb pr. år")
    belob = belob_m
    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        data = {'måned': maned.lower(),
                'fast_var': fast_var,
                'kredit_debit': kredit_debit,
                'Kategori': kategori,
                'Ind_ud': indud,
                'Navn': navn,
                'beløb_måned': belob_m,
                'beløb_kvartal': belob_k,
                'beløb_år': belob_a,
                'beløb': belob
        }
        conn = st.connection("gsheets", type=GSheetsConnection)
        olddf = conn.read(worksheet=maned, usecols=['måned', 'fast_var', 'kredit_debit', 'Kategori', 'Ind_ud', 'Navn', 'beløb_måned', 'beløb_kvartal', 'beløb_år', "beløb"])
        olddf = olddf.dropna(subset=["måned"])
        newdata = pd.DataFrame(data, index=[0])
        newdf = pd.concat([olddf, newdata], axis=0).reset_index(drop=True)
        conn.update(worksheet=maned, data=newdf)
        st.write("Success!")


# st.dataframe(olddf)

# st.dataframe(newdata)

# newdf = pd.concat([olddf, newdata], axis=0).reset_index(drop=True)

# st.dataframe(newdf)