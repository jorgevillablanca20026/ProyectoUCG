import streamlit as st
import pandas as pd

from database import init_db
from auth_sqlite import auth_router
from crud_sqlite import create_product, get_all, update_stock, delete_product

# ---------------- INIT ----------------
init_db()

# ---------------- STATE DEFAULTS ----------------
if "menu" not in st.session_state:
    st.session_state.menu = "Ver"

if "msg" not in st.session_state:
    st.session_state.msg = ""

# ---------------- MENSAJE ----------------
if st.session_state.msg:
    st.success(st.session_state.msg)
    st.session_state.msg = ""

# ---------------- AUTH ----------------
state = auth_router()

if state != "ok":
    st.stop()

st.title(f"Inventario - {st.session_state.user}")

# ---------------- LOGOUT ----------------
if st.button("Cerrar sesión"):
    st.session_state.auth = False
    st.session_state.user = ""
    st.session_state.page = "login"
    st.rerun()

# ---------------- SIDEBAR (ESTO ARREGLA TODO) ----------------
st.sidebar.title("Menú")

if st.sidebar.button("Ver productos"):
    st.session_state.menu = "Ver"

if st.sidebar.button("Registrar producto"):
    st.session_state.menu = "Crear"

if st.sidebar.button("Editar stock"):
    st.session_state.menu = "Editar"

if st.sidebar.button("Eliminar producto"):
    st.session_state.menu = "Eliminar"

menu = st.session_state.menu

# ---------------- DATA ----------------
rows = get_all()
df = pd.DataFrame(rows, columns=["id","nombre","descripcion","precio","stock","categoria"])

# ---------------- VER ----------------
if menu == "Ver":
    st.dataframe(df)

# ---------------- CREAR ----------------
elif menu == "Crear":

    nombre = st.text_input("Nombre")
    descripcion = st.text_input("Descripción")
    precio = st.number_input("Precio", min_value=0.0)
    stock = st.number_input("Stock", min_value=0)
    categoria = st.selectbox("Categoría", ["Periféricos","Audio","Laptops","Otro"])

    if st.button("Guardar"):

        if nombre.strip() == "":
            st.error("El nombre es obligatorio.")
        else:
            create_product({
                "nombre": nombre,
                "descripcion": descripcion,
                "precio": precio,
                "stock": stock,
                "categoria": categoria
            })

            # 🔥 MENSAJE GARANTIZADO
            st.session_state.msg = "Producto registrado correctamente."
            st.session_state.menu = "Ver"

            st.rerun()

# ---------------- EDITAR ----------------
elif menu == "Editar":

    id_ = st.number_input("ID", min_value=1)
    stock = st.number_input("Stock", min_value=0)

    if st.button("Actualizar"):
        update_stock(id_, stock)
        st.session_state.msg = "Stock actualizado correctamente."
        st.session_state.menu = "Ver"
        st.rerun()

# ---------------- ELIMINAR ----------------
elif menu == "Eliminar":

    id_ = st.number_input("ID", min_value=1)

    if st.button("Eliminar"):
        delete_product(id_)
        st.session_state.msg = "Producto eliminado correctamente."
        st.session_state.menu = "Ver"
        st.rerun()
