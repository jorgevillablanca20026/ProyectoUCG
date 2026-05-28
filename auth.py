import streamlit as st

USUARIO = "admin"
PASSWORD = "1234"


def init_auth():
    if "auth" not in st.session_state:
        st.session_state["auth"] = False


def login():
    st.title("🔐 Login")

    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        if user == USUARIO and password == PASSWORD:
            st.session_state["auth"] = True
            st.rerun()
        else:
            st.error("Credenciales incorrectas")


def logout():
    if st.sidebar.button("Cerrar sesión"):
        st.session_state["auth"] = False
        st.rerun()


def is_authenticated():
    init_auth()
    return st.session_state["auth"]
