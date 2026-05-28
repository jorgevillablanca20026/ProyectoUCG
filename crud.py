import pandas as pd
from data import load_data, save_data


def create_product(producto):
    df = load_data()
    df = pd.concat([df, pd.DataFrame([producto])], ignore_index=True)
    save_data(df)


def delete_product(id_producto):
    df = load_data()
    df = df[df["id"] != id_producto]
    save_data(df)


def update_stock(id_producto, stock):
    df = load_data()
    df.loc[df["id"] == id_producto, "stock"] = stock
    save_data(df)


def get_all():
    return load_data()
