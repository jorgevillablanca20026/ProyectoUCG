from data import load_data, save_data
import pandas as pd


def create_product(p):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([p])], ignore_index=True)
    save_data(df)


def delete_product(id_):
    df = load_data()
    df = df[df["id"] != id_]
    save_data(df)


def update_stock(id_, stock):
    df = load_data()
    df.loc[df["id"] == id_, "stock"] = stock
    save_data(df)


def get_all():
    return load_data()
