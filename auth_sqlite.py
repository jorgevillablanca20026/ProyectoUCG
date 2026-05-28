import streamlit as st
from database import get_conn


# ---------------- INIT STATE ----------------
def init():
    if "auth" not in st.session_state:
        st.session_state.auth = False
    if "user" not in st.session_state:
        st.session_state.user = ""
    if "page" not in st.session_state:
        st.session_state.page = "login"


# ---------------- LOGIN UI ----------------
def login():
    st.markdown(
        """
        <style>
        .login-box {
            max-width: 400px;
            margin: auto;
            padding: 2rem;
            border-radius: 12px;
            background-color: #111827;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
        }

        .title {
            text-align: center;
            color: white;
            font-size: 28px;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.markdown("<div class='title'>Sistema de Inventario</div>", unsafe_allow_html=True)

    u = st.text_input("Usuario")
    p = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        conn = get_conn()
        c = conn.cursor()

        c.execute("SELECT * FROM users WHERE usuario=? AND password=?", (u, p))
        user = c.fetchone()
        conn.close()

        if user:
            st.session_state.auth = True
            st.session_state.user = u
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

    st.markdown("---")

    if st.button("Crear cuenta"):
        st.session_state.page = "register"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------- REGISTER ----------------
def register():
    st.title("Registro de usuario")

    u = st.text_input("Nuevo usuario")
    p = st.text_input("Nueva contraseña", type="password")

    if st.button("Registrar"):
        conn = get_conn()
        c = conn.cursor()

        try:
            c.execute("INSERT INTO users (usuario, password) VALUES (?, ?)", (u, p))
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
