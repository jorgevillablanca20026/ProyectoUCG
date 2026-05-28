import streamlit as st
import pandas as pd
from data import load_users, save_users


def init_auth():
    if "auth" not in st.session_state:
        st.session_state.auth = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "page" not in st.session_state:
        st.session_state.page = "login"


def login_view():
    st.title("🔐 Login")

    users = load_users()

    u = st.text_input("Usuario")
    p = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        ok = users[(users["usuario"] == u) & (users["password"] == p)]

        if not ok.empty:
            st.session_state.auth = True
            st.session_state.user = u
            st.rerun()
        else:
            st.error("Incorrecto")

    st.markdown("---")

    if st.button("🆕 Registrarse"):
        st.session_state.page = "register"
        st.rerun()


def register_view():
    st.title("🆕 Registro")

    users = load_users()

    u = st.text_input("Nuevo usuario")
    p = st.text_input("Contraseña", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Crear"):
            if u == "" or p == "":
                st.error("Completa campos")
                return

            if u in users["usuario"].values:
                st.error("Ya existe")
                return

            new = pd.DataFrame([{"usuario": u, "password": p}])
            users = pd.concat([users, new], ignore_index=True)
            save_users(users)

            st.success("Creado")
            st.session_state.page = "login"
            st.rerun()

    with col2:
        if st.button("Volver"):
            st.session_state.page = "login"
            st.rerun()


def auth_router():
    init_auth()

    if st.session_state.auth:
        return "ok"

    if st.session_state.page == "register":
        register_view()
    else:
        login_view()

    return "stop"
