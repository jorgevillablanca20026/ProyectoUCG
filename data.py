import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

USERS_FILE = os.path.join(BASE_DIR, "users1.csv")
DATA_FILE = os.path.join(BASE_DIR, "data1.csv")


def load_users():
    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame(columns=["usuario", "password"])
        df.to_csv(USERS_FILE, index=False)
        return df
    return pd.read_csv(USERS_FILE)


def save_users(df):
    # 🔥 escritura segura (evita pérdida en Streamlit)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        df.to_csv(f, index=False)
        f.flush()


def load_data():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["id","nombre","descripcion","precio","stock","categoria"])
        df.to_csv(DATA_FILE, index=False)
        return df
    return pd.read_csv(DATA_FILE)


def save_data(df):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        df.to_csv(f, index=False)
        f.flush()
