import streamlit as st
import pandas as pd

from auth_sqlite import auth_router
from crud_sqlite import create_product, get_all, update_stock, delete_product

# ---------------- STATE ----------------
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

# ---------------- HEADER ----------------
st.title(f"Sistema de Inventario - {st.session_state.user}")

# ---------------- DATA ----------------
rows = get_all()

df = pd.DataFrame(rows)

if df.empty:
    st.warning("No hay productos registrados")
    st.stop()

df = df.fillna("")

if "stock" in df.columns:
    df["stock"] = pd.to_numeric(df["stock"], errors="coerce")

# ================= VER =================
if st.session_state.menu == "Ver":

    st.subheader("Inventario de productos")
    st.dataframe(df.reset_index(drop=True))

    # 🔥 GRÁFICO CATEGORÍAS (FORZADO)
    if "categoria" in df.columns and len(df) > 0:
        st.subheader("Productos por categoría")
        st.bar_chart(df.groupby("categoria").size())

    # 🔥 GRÁFICO STOCK (FORZADO)
    if "nombre" in df.columns and "stock" in df.columns:
        st.subheader("Stock por producto")

        chart_df = df.groupby("nombre")["stock"].sum()

        if len(chart_df) > 0:
            st.bar_chart(chart_df)

# ================= CREAR =================
elif st.session_state.menu == "Crear":

    st.subheader("Registrar producto")

    nombre = st.text_input("Nombre")
    descripcion = st.text_input("Descripción")
    precio = st.number_input("Precio", min_value=0.0)
    stock = st.number_input("Stock", min_value=0)

    categoria = st.selectbox(
        "Categoría",
        ["Periféricos", "Audio", "Laptops", "Celular", "Televisor", "Otro"]
    )

    if st.button("Guardar producto"):

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

            st.session_state.msg = "Producto registrado correctamente."
            st.session_state.menu = "Ver"
            st.rerun()

# ================= EDITAR =================
elif st.session_state.menu == "Editar":

    st.subheader("Editar stock")

    id_ = st.number_input("ID del producto", min_value=1)
    stock = st.number_input("Nuevo stock", min_value=0)

    if st.button("Actualizar"):
        update_stock(id_, stock)
        st.session_state.msg = "Stock actualizado"
        st.session_state.menu = "Ver"
        st.rerun()

# ================= ELIMINAR =================
elif st.session_state.menu == "Eliminar":

    st.subheader("Eliminar producto")

    id_ = st.number_input("ID del producto", min_value=1)

    if st.button("Eliminar"):
        delete_product(id_)
        st.session_state.msg = "Producto eliminado"
        st.session_state.menu = "Ver"
        st.rerun()
