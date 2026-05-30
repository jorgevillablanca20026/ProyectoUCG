import streamlit as st
import pandas as pd

from auth_sqlite import auth_router
from crud_sqlite import create_product, get_all, update_stock, delete_product

# ---------------- AUTH ----------------
state = auth_router()
if state != "ok":
    st.stop()

st.title(f"Sistema de Inventario - {st.session_state.user}")

# ---------------- STATE ----------------
if "menu" not in st.session_state:
    st.session_state.menu = "Ver"

if "msg" not in st.session_state:
    st.session_state.msg = ""

if st.session_state.msg:
    st.success(st.session_state.msg)
    st.session_state.msg = ""

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 Menú")

if st.sidebar.button("Ver productos"):
    st.session_state.menu = "Ver"

if st.sidebar.button("Crear producto"):
    st.session_state.menu = "Crear"

if st.sidebar.button("Editar stock"):
    st.session_state.menu = "Editar"

if st.sidebar.button("Eliminar"):
    st.session_state.menu = "Eliminar"

if st.sidebar.button("Cerrar sesión"):
    st.session_state.auth = False
    st.session_state.user = ""
    st.session_state.page = "login"
    st.rerun()

# ================= VER =================
if st.session_state.menu == "Ver":

    rows = get_all()

    # 🔥 PROTECCIÓN TOTAL
    if not rows:
        st.warning("No hay datos")
        st.stop()

    df = pd.DataFrame(rows)
    df = df.fillna("")

    st.subheader("Productos")
    st.dataframe(df.reset_index(drop=True))

    # ================= GRÁFICO CATEGORÍAS =================
    if "categoria" in df.columns:
        st.subheader("Por categoría")

        try:
            data = df["categoria"].astype(str).value_counts()
            st.bar_chart(data)
        except:
            st.warning("No se pudo graficar categorías")

    # ================= GRÁFICO STOCK =================
    if "nombre" in df.columns and "stock" in df.columns:
        st.subheader("Stock")

        try:
            df["stock"] = pd.to_numeric(df["stock"], errors="coerce")
            chart = df.dropna(subset=["stock"]).groupby("nombre")["stock"].sum()
            st.bar_chart(chart)
        except:
            st.warning("No se pudo graficar stock")

# ================= CREAR =================
elif st.session_state.menu == "Crear":

    st.subheader("Nuevo producto")

    nombre = st.text_input("Nombre")
    descripcion = st.text_input("Descripción")
    precio = st.number_input("Precio", min_value=0.0)
    stock = st.number_input("Stock", min_value=0)

    categoria = st.selectbox(
        "Categoría",
        ["Periféricos", "Audio", "Laptops", "Celular", "Televisor", "Otro"]
    )

    if st.button("Guardar"):

        if nombre.strip():
            create_product({
                "nombre": nombre,
                "descripcion": descripcion,
                "precio": precio,
                "stock": stock,
                "categoria": categoria
            })

            st.session_state.msg = "Producto creado"
            st.session_state.menu = "Ver"
            st.rerun()

        else:
            st.error("Nombre obligatorio")

# ================= EDITAR =================
elif st.session_state.menu == "Editar":

    st.subheader("Editar stock")

    id_ = st.number_input("ID", min_value=1)
    stock = st.number_input("Nuevo stock", min_value=0)

    if st.button("Actualizar"):
        update_stock(id_, stock)
        st.session_state.msg = "Actualizado"
        st.session_state.menu = "Ver"
        st.rerun()

# ================= ELIMINAR =================
elif st.session_state.menu == "Eliminar":

    st.subheader("Eliminar")

    id_ = st.number_input("ID", min_value=1)

    if st.button("Eliminar"):
        delete_product(id_)
        st.session_state.msg = "Eliminado"
        st.session_state.menu = "Ver"
        st.rerun()
