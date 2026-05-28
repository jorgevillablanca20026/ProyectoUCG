import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(BASE_DIR, "data.csv")
USERS_FILE = os.path.join(BASE_DIR, "users.csv")


def load_data():
    try:
        return pd.read_csv(DATA_FILE, encoding="utf-8")
    except:
        return pd.DataFrame(columns=[
            "id", "nombre", "descripcion", "precio", "stock", "categoria"
        ])


def save_data(df):
    df.to_csv(DATA_FILE, index=False, encoding="utf-8")


def load_users():
    try:
        return pd.read_csv(USERS_FILE, encoding="utf-8")
    except:
        return pd.DataFrame(columns=["usuario", "password"])


def save_users(df):
    df.to_csv(USERS_FILE, index=False, encoding="utf-8")
