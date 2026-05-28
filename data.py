import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

USERS_FILE = os.path.join(BASE_DIR, "users1.csv")
DATA_FILE = os.path.join(BASE_DIR, "data1.csv")


# ================= USERS =================
def load_users():
    try:
        return pd.read_csv(USERS_FILE, encoding="utf-8")
    except:
        df = pd.DataFrame(columns=["usuario", "password"])
        df.to_csv(USERS_FILE, index=False, encoding="utf-8")
        return df


def save_users(df):
    # 🔥 esto garantiza escritura real
    df.to_csv(USERS_FILE, index=False, encoding="utf-8")


# ================= PRODUCTS =================
def load_data():
    try:
        return pd.read_csv(DATA_FILE, encoding="utf-8")
    except:
        df = pd.DataFrame(columns=["id","nombre","descripcion","precio","stock","categoria"])
        df.to_csv(DATA_FILE, index=False, encoding="utf-8")
        return df


def save_data(df):
    df.to_csv(DATA_FILE, index=False, encoding="utf-8")
