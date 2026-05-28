import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(BASE_DIR, "data1.csv")
USERS_FILE = os.path.join(BASE_DIR, "users1.csv")


def load_data():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["id","nombre","descripcion","precio","stock","categoria"])
        df.to_csv(DATA_FILE, index=False, encoding="utf-8")
        return df

    return pd.read_csv(DATA_FILE, encoding="utf-8")


def save_data(df):
    df.to_csv(DATA_FILE, index=False, encoding="utf-8")


def load_users():
    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame(columns=["usuario","password"])
        df.to_csv(USERS_FILE, index=False, encoding="utf-8")
        return df

    return pd.read_csv(USERS_FILE, encoding="utf-8")


def save_users(df):
    df.to_csv(USERS_FILE, index=False, encoding="utf-8")
