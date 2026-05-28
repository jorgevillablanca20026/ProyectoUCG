import streamlit as st
from data import load_users, save_users


def init_auth():
    if "auth" not in st.session_state:
        st.session_state["auth"] = False
        st.session_state["user"] = None


def login():
    st.title("🔐 Login")

    users = load_users()

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        user_ok = users[
            (users["usuario"] == usuario) &
            (users["password"] == password)
        ]

        if not user_ok.empty:
            st.session_state["auth"] = True
            st.session_state["user"] = usuario
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

    st.markdown("---")
    st.subheader("🆕 Registrarse")

    new_user = st.text_input("Nuevo usuario")
    new_pass = st.text_input("Nueva contraseña", type="password")

    if st.button("Crear cuenta"):
        if new_user == "" or new_pass == "":
            st.error("Completa los campos")
            return

        users = load_users()

        if new_user in users["usuario"].values:
            st.error("Usuario ya existe")
            return

        new_row = {
            "usuario": new_user,
            "password": new_pass
        }

        users = pd.concat([users, pd.DataFrame([new_row])], ignore_index=True)
        save_users(users)

        st.success("Usuario creado")


def logout():
    if st.sidebar.button("Cerrar sesión"):
        st.session_state["auth"] = False
        st.session_state["user"] = None
        st.rerun()


def is_authenticated():
    init_auth()
    return st.session_state["auth"]
