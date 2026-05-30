import streamlit as st
import pandas as pd
import altair as alt

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

# ---------------- SIDEBAR (ACORDEÓN) ----------------
st.sidebar.title("📊 Panel de control")

with st.sidebar.expander("📦 Inventario", expanded=True):
    if st.button("Ver productos"):
        st.session_state.menu = "Ver"

with st.sidebar.expander("➕ Productos"):
    if st.button("Registrar producto"):
        st.session_state.menu = "Crear"

with st.sidebar.expander("✏️ Gestión"):
    if st.button("Editar stock"):
        st.session_state.menu = "Editar"

    if st.button("Eliminar producto"):
        st.session_state.menu = "Eliminar"

st.sidebar.markdown("---")

if st.sidebar.button("🚪 Cerrar sesión"):
    st.session_state.auth = False
    st.session_state.user = ""
    st.session_state.page = "login"
    st.rerun()

# ================= VER =================
if st.session_state.menu == "Ver":

    rows = get_all()
    df = pd.DataFrame(rows)

    st.subheader("Inventario de productos")
    st.dataframe(df)

    if df.empty:
        st.warning("No hay productos registrados")
        st.stop()

    df = df.fillna("")

    # ================= GRÁFICO CATEGORÍAS (CON COLORES) =================
    if "categoria" in df.columns:

        st.subheader("Productos por categoría")

        cat = df["categoria"].astype(str).value_counts().reset_index()
        cat.columns = ["categoria", "cantidad"]

        chart = (
            alt.Chart(cat)
            .mark_bar()
            .encode(
                x=alt.X("categoria", sort=None),
                y="cantidad",
                color="categoria"
            )
        )

        st.altair_chart(chart, use_container_width=True)

    # ================= GRÁFICO STOCK =================
    if "nombre" in df.columns and "stock" in df.columns:

        st.subheader("Stock por producto")

        df["stock"] = pd.to_numeric(df["stock"], errors="coerce")

        chart_df = df.dropna(subset=["nombre", "stock"])
        chart_df = chart_df.groupby("nombre")["stock"].sum()

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

    if st.button("Guardar"):

        if nombre.strip() == "":
            st.error("Nombre obligatorio")
        else:
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

# ================= EDITAR =================
elif st.session_state.menu == "Editar":

    st.subheader("Editar stock")

    id_ = st.number_input("ID", min_value=1)
    stock = st.number_input("Nuevo stock", min_value=0)

    if st.button("Actualizar"):
        update_stock(id_, stock)
        st.session_state.msg = "Stock actualizado"
        st.session_state.menu = "Ver"
        st.rerun()

# ================= ELIMINAR =================
elif st.session_state.menu == "Eliminar":

    st.subheader("Eliminar producto")

    id_ = st.number_input("ID", min_value=1)

    if st.button("Eliminar"):
        delete_product(id_)
        st.session_state.msg = "Producto eliminado"
        st.session_state.menu = "Ver"
        st.rerun()
