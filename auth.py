import streamlit as st
import pandas as pd
from data import load_users, save_users


def init():
    if "auth" not in st.session_state:
        st.session_state.auth = False
    if "user" not in st.session_state:
        st.session_state.user = ""
    if "page" not in st.session_state:
        st.session_state.page = "login"


# LOGIN
def login():
    st.title("🔐 Login")

    users = load_users()

    u = st.text_input("Usuario")
    p = st.text_input("Password", type="password")

    if st.button("Entrar"):
        ok = users[(users["usuario"] == u) & (users["password"] == p)]

        if not ok.empty:
            st.session_state.auth = True
            st.session_state.user = u
            st.rerun()
        else:
            st.error("Incorrecto")

    if st.button("Registrarse"):
        st.session_state.page = "register"
        st.rerun()


# REGISTRO (GUARDA EN users1.csv)
def register():
    st.title("🆕 Registro")

    users = load_users()

    u = st.text_input("Nuevo usuario")
    p = st.text_input("Nueva password", type="password")

    if st.button("Crear usuario"):
        if u == "" or p == "":
            st.error("Completa campos")
            return

        if u in users["usuario"].values:
            st.error("Usuario ya existe")
            return

        new_user = pd.DataFrame([{"usuario": u, "password": p}])

        users = pd.concat([users, new_user], ignore_index=True)

        save_users(users)  # 🔥 GUARDA EN users1.csv

        st.success("Usuario creado")
        st.session_state.page = "login"
        st.rerun()


def auth_router():
    init()

    if st.session_state.auth:
        return "ok"

    if st.session_state.page == "register":
        register()
    else:
        login()

    return "stop"
