import streamlit as st

from auth import login, logout, is_authenticated
from crud import create_product, delete_product, update_stock, get_all

st.set_page_config(page_title="Inventario", layout="wide")

# ---------------- AUTH ----------------
if not is_authenticated():
    login()
    st.stop()

logout()

# ---------------- APP ----------------
st.title("📦 Sistema de Inventario")

menu = st.sidebar.selectbox("Menú", ["Ver", "Crear", "Editar", "Eliminar"])

df = get_all()

# ---------------- VER ----------------
if menu == "Ver":
    st.subheader("📋 Productos")
    st.dataframe(df)

# ---------------- CREAR ----------------
elif menu == "Crear":
    st.subheader("➕ Crear producto")

    nombre = st.text_input("Nombre")
    descripcion = st.text_input("Descripción")
    precio = st.number_input("Precio", min_value=0.0)
    stock = st.number_input("Stock", min_value=0)
    categoria = st.text_input("Categoría")

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
        st.success("Producto creado")
        st.rerun()

# ---------------- EDITAR ----------------
elif menu == "Editar":
    st.subheader("✏️ Actualizar stock")

    id_edit = st.number_input("ID producto", min_value=1)
    stock = st.number_input("Nuevo stock", min_value=0)

    if st.button("Actualizar"):
        update_stock(id_edit, stock)
        st.success("Stock actualizado")
        st.rerun()

# ---------------- ELIMINAR ----------------
elif menu == "Eliminar":
    st.subheader("❌ Eliminar producto")

    id_del = st.number_input("ID producto", min_value=1)

    if st.button("Eliminar"):
        delete_product(id_del)
        st.success("Producto eliminado")
        st.rerun()
        st.rerun()
