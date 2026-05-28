import streamlit as st
import pandas as pd
from data import load_users, save_users


def init_auth():
    if "auth" not in st.session_state:
        st.session_state.auth = False
    if "page" not in st.session_state:
        st.session_state.page = "login"
    if "user" not in st.session_state:
        st.session_state.user = None


# ---------------- LOGIN ----------------
def login_view():
    st.title("🔐 Bienvenido")

    st.subheader("Inicia sesión")

    users = load_users()

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Entrar"):
            ok = users[(users["usuario"] == usuario) & (users["password"] == password)]

            if not ok.empty:
                st.session_state.auth = True
                st.session_state.user = usuario
                st.rerun()
            else:
                st.error("Credenciales incorrectas")

    with col2:
        if st.button("🆕 Registrarte"):
            st.session_state.page = "register"
            st.rerun()


# ---------------- REGISTRO ----------------
def register_view():
    st.title("🆕 Crear cuenta")

    users = load_users()

    new_user = st.text_input("Nuevo usuario")
    new_pass = st.text_input("Nueva contraseña", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Crear cuenta"):
            if new_user == "" or new_pass == "":
                st.error("Completa todos los campos")
                return

            if new_user in users["usuario"].values:
                st.error("Usuario ya existe")
                return

            nuevo = pd.DataFrame([{
                "usuario": new_user,
                "password": new_pass
            }])

            users = pd.concat([users, nuevo], ignore_index=True)
            save_users(users)

            st.success("Usuario creado")
            st.session_state.page = "login"
            st.rerun()

    with col2:
        if st.button("⬅ Volver"):
            st.session_state.page = "login"
            st.rerun()


# ---------------- LOGOUT ----------------
def logout():
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.auth = False
        st.session_state.user = None
        st.rerun()


# ---------------- CONTROL ----------------
def auth_router():
    init_auth()

    if st.session_state.auth:
        return "ok"

    if st.session_state.page == "login":
        login_view()
    else:
        register_view()

    return "stop"
