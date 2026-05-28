import pandas as pd

FILE = "data.csv"

def load_data():
    return pd.read_csv(FILE)

def save_data(df):
    df.to_csv(FILE, index=False)