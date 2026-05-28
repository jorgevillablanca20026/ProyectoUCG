import streamlit as st
import pandas as pd

from database import init_db
from auth_sqlite import auth_router
from crud_sqlite import create_product, get_all, update_stock, delete_product

# ---------------- INIT ----------------
init_db()

# ---------------- NAV STATE ----------------
if "menu" not in st.session_state:
    st.session_state.menu = "Ver productos"

# ---------------- MENSAJE FORMAL ----------------
if st.session_state.get("created"):
    st.success("Producto registrado correctamente.")
    st.session_state["created"] = False

# ---------------- AUTH ----------------
state = auth_router()

if state != "ok":
    st.stop()

# ---------------- HEADER ----------------
st.title(f"Inventario - {st.session_state.user}")

# ---------------- LOGOUT ----------------
if st.button("Cerrar sesión"):
    st.session_state.auth = False
    st.session_state.user = ""
    st.session_state.page = "login"
    st.rerun()

# ---------------- MENU ----------------
menu = st.selectbox(
    "Opciones",
    ["Ver productos", "Registrar producto", "Editar stock", "Eliminar producto"],
    index=["Ver productos", "Registrar producto", "Editar stock", "Eliminar producto"].index(
        st.session_state.menu
    )
)

# ---------------- DATA ----------------
rows = get_all()
df = pd.DataFrame(rows, columns=["id", "nombre", "descripcion", "precio", "stock", "categoria"])

# ---------------- VER ----------------
if menu == "Ver productos":
    st.dataframe(df)

    if len(df) > 0:
        st.bar_chart(df["categoria"].value_counts())

# ---------------- CREAR ----------------
elif menu == "Registrar producto":

    nombre = st.text_input("Nombre")
    descripcion = st.text_input("Descripción")
    precio = st.number_input("Precio", min_value=0.0)
    stock = st.number_input("Stock", min_value=0)
    categoria = st.selectbox("Categoría", ["Periféricos", "Audio", "Laptops", "Otro"])

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

            st.session_state.created = True
            st.session_state.menu = "Ver productos"
            st.rerun()

# ---------------- EDITAR ----------------
elif menu == "Editar stock":

    id_ = st.number_input("ID del producto", min_value=1)
    stock = st.number_input("Nuevo stock", min_value=0)

    if st.button("Actualizar"):

        update_stock(id_, stock)
        st.success("Stock actualizado correctamente.")
        st.rerun()

# ---------------- ELIMINAR ----------------
elif menu == "Eliminar producto":

    id_ = st.number_input("ID del producto", min_value=1)

    if st.button("Eliminar"):

        delete_product(id_)
        st.session_state.menu = "Ver productos"
        st.success("Producto eliminado correctamente.")
        st.rerun()
