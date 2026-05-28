import streamlit as st
from database import get_conn


def init_session():
    if "auth" not in st.session_state:
        st.session_state.auth = False
    if "user" not in st.session_state:
        st.session_state.user = ""
    if "page" not in st.session_state:
        st.session_state.page = "login"


# ================= LOGIN =================
def login():
    st.title("🔐 Login")

    u = st.text_input("Usuario")
    p = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        conn = get_conn()
        c = conn.cursor()

        c.execute(
            "SELECT * FROM users WHERE usuario=? AND password=?",
            (u, p)
        )
        data = c.fetchone()
        conn.close()

        if data:
            st.session_state.auth = True
            st.session_state.user = u
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

    # 🔥 BOTÓN DE REGISTRO (LO QUE TE FALTABA)
    st.markdown("---")
    st.write("¿No tienes cuenta?")

    if st.button("🆕 Registrarse"):
        st.session_state.page = "register"
        st.rerun()


# ================= REGISTER =================
def register():
    st.title("🆕 Registro")

    u = st.text_input("Nuevo usuario")
    p = st.text_input("Contraseña", type="password")

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

            # volver a login
            st.session_state.page = "login"
            st.rerun()

        except:
            st.error("El usuario ya existe")


# ================= ROUTER =================
def auth_router():
    init_session()

    if st.session_state.auth:
        return "ok"

    if st.session_state.page == "register":
        register()
    else:
        login()

    return "stop"
