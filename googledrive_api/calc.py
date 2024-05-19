import pandas as pd

def calculate_belob(row):
    belob_kvartal = pd.to_numeric(row['beløb_kvartal'], errors='coerce')
    belob_aar = pd.to_numeric(row['beløb_år'], errors='coerce')
    belob_maaned = pd.to_numeric(row['beløb_måned'], errors='coerce')

    if not pd.isna(belob_kvartal):
        result = belob_kvartal / 3
    elif not pd.isna(belob_aar):
        result = belob_aar / 12
    else:
        result = belob_maaned
    
    return str(result) if not pd.isna(result) else None