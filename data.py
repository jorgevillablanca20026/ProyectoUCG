import pandas as pd
import os

FILE = "data.csv"

def load_data():
    if not os.path.exists(FILE):
        df = pd.DataFrame(columns=[
            "id", "nombre", "descripcion", "precio", "stock", "categoria"
        ])
        df.to_csv(FILE, index=False)
        return df

    return pd.read_csv(FILE)


def save_data(df):
    df.to_csv(FILE, index=False)
