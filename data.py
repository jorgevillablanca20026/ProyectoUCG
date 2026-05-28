import pandas as pd
import os

BASE_DIR = "."

USERS_FILE = os.path.join(BASE_DIR, "users1.csv")
DATA_FILE = os.path.join(BASE_DIR, "data1.csv")


def load_users():
    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame(columns=["usuario", "password"])
        df.to_csv(USERS_FILE, index=False)
        return df
    return pd.read_csv(USERS_FILE)


def save_users(df):
    df.to_csv(USERS_FILE, index=False)


def load_data():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["id","nombre","descripcion","precio","stock","categoria"])
        df.to_csv(DATA_FILE, index=False)
        return df
    return pd.read_csv(DATA_FILE)


def save_data(df):
    df.to_csv(DATA_FILE, index=False)
