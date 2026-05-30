import streamlit as st
from database import get_db


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

        db = get_db()

        try:
            res = db.table("users") \
                .select("*") \
                .eq("usuario", u) \
                .eq("password", p) \
                .execute()

            if res.data:
                st.session_state.auth = True
                st.session_state.user = u
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

        except Exception as e:
            st.error(f"Error login: {e}")


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

        db = get_db()

        try:
            # verificar usuario
            check = db.table("users") \
                .select("*") \
                .eq("usuario", u) \
                .execute()

            if check.data:
                st.error("El usuario ya existe")
                return

            # insertar usuario
            db.table("users").insert({
                "usuario": u,
                "password": p
            }).execute()

            st.success("Usuario creado correctamente")
            st.session_state.page = "login"
            st.rerun()

        except Exception as e:
            st.error(f"Error registro: {e}")


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
