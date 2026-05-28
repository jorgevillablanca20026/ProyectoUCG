import streamlit as st
from auth import login, check_auth
from data import load_data
from crud import add_product, delete_product, update_stock

st.set_page_config(page_title="Inventario", layout="wide")

# ---------------- LOGIN ----------------
if not check_auth():
    login()
    st.stop()

# ---------------- APP ----------------
st.title("📦 Sistema de Inventario")

menu = st.sidebar.selectbox("Menú", ["Ver", "Agregar", "Editar", "Eliminar"])

df = load_data()

# ---------------- VER ----------------
if menu == "Ver":
    st.subheader("📋 Productos")
    st.dataframe(df)

# ---------------- AGREGAR ----------------
elif menu == "Agregar":
    st.subheader("➕ Agregar producto")

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

        add_product(nuevo)
        st.success("Producto agregado")
        st.rerun()

# ---------------- EDITAR ----------------
elif menu == "Editar":
    st.subheader("✏️ Editar stock")

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