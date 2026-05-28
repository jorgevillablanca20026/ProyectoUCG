import streamlit as st
from database import get_conn


# ---------------- INIT ----------------
def init():
    if "auth" not in st.session_state:
        st.session_state.auth = False
    if "user" not in st.session_state:
        st.session_state.user = ""
    if "page" not in st.session_state:
        st.session_state.page = "login"


# ---------------- LOGIN ----------------
def login():

    st.title("Sistema de Inventario")
    st.caption("Inicia sesión para continuar")

    u = st.text_input("Usuario")
    p = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):

        conn = get_conn()
        c = conn.cursor()

        c.execute(
            "SELECT * FROM users WHERE usuario=? AND password=?",
            (u, p)
        )

        user = c.fetchone()
        conn.close()

        if user:
            st.session_state.auth = True
            st.session_state.user = u
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

    st.markdown("---")

    if st.button("Registrarse"):
        st.session_state.page = "register"
        st.rerun()


# ---------------- REGISTER ----------------
def register():

    st.title("Registro de usuario")

    u = st.text_input("Nuevo usuario")
    p = st.text_input("Nueva contraseña", type="password")

    if st.button("Crear cuenta"):

        conn = get_conn()
        c = conn.cursor()

        try:
            c.execute(
                "INSERT INTO users (usuario, password) VALUES (?, ?)",
                (u, p)
            )
            conn.commit()
            conn.close()

            st.success("Usuario creado correctamente")
            st.session_state.page = "login"
            st.rerun()

        except:
            conn.close()
            st.error("El usuario ya existe")

    st.markdown("---")

    if st.button("Volver al login"):
        st.session_state.page = "login"
        st.rerun()


# ---------------- ROUTER ----------------
def auth_router():

    init()

    if st.session_state.auth:
        return "ok"

    if st.session_state.page == "register":
        register()
    else:
        login()

    return "stop"
