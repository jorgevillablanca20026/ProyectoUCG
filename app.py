import streamlit as st

from auth import auth_router, logout
from crud import create_product, delete_product, update_stock, get_all

st.set_page_config(page_title="Inventario", layout="wide")

state = auth_router()

if state != "ok":
    st.stop()

logout()

st.title(f"📦 Inventario - {st.session_state.user}")

menu = st.sidebar.selectbox("Menú", ["Ver", "Crear", "Editar", "Eliminar"])

df = get_all()

# ---------------- VER ----------------
if menu == "Ver":
    st.dataframe(df, use_container_width=True)

# ---------------- CREAR ----------------
elif menu == "Crear":
    st.subheader("➕ Nuevo producto")

    nombre = st.text_input("Nombre")
    descripcion = st.text_input("Descripción")
    precio = st.number_input("Precio", min_value=0.0)
    stock = st.number_input("Stock", min_value=0)
    categoria = st.selectbox("Categoría", ["Periféricos", "Laptops", "Audio", "Otro"])

    if st.button("Guardar"):
        nuevo = {
            "id": int(df["id"].max() + 1) if len(df) > 0 else 1,
            "nombre": nombre,
            "descripcion": descripcion,
            "precio": precio,
            "stock": stock,
            "categoria": categoria
        }

        create_product(nuevo)
        st.success("Creado")
        st.rerun()

# ---------------- EDITAR ----------------
elif menu == "Editar":
    st.subheader("✏️ Editar stock")

    id_ = st.number_input("ID", min_value=1)
    stock = st.number_input("Nuevo stock", min_value=0)

    if st.button("Actualizar"):
        update_stock(id_, stock)
        st.success("Actualizado")
        st.rerun()

# ---------------- ELIMINAR ----------------
elif menu == "Eliminar":
    st.subheader("❌ Eliminar")

    id_ = st.number_input("ID", min_value=1)

    if st.button("Eliminar"):
        delete_product(id_)
        st.success("Eliminado")
        st.rerun()
