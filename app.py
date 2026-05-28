import streamlit as st
import pandas as pd

from database import init_db
from auth_sqlite import auth_router
from crud_sqlite import create_product, get_all, update_stock, delete_product

# ---------------- INIT ----------------
init_db()

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

# ---------------- LOGOUT ----------------
if st.button("Cerrar sesión"):
    st.session_state.auth = False
    st.session_state.user = ""
    st.session_state.page = "login"
    st.rerun()

# ---------------- SIDEBAR ACORDEÓN ----------------
st.sidebar.title("Panel de control")

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
st.sidebar.info("Sistema de inventario con SQLite + Streamlit")

menu = st.session_state.menu

# ---------------- DATA ----------------
rows = get_all()
df = pd.DataFrame(
    rows,
    columns=["id", "nombre", "descripcion", "precio", "stock", "categoria"]
)

# ================= VER =================
if menu == "Ver":

    st.subheader("Inventario de productos")
    st.dataframe(df)

    if len(df) > 0:
        st.subheader("Productos por categoría")
        st.bar_chart(df["categoria"].value_counts())

        st.subheader("Stock por producto")
        st.bar_chart(df.set_index("nombre")["stock"])

# ================= CREAR =================
elif menu == "Crear":

    st.subheader("Registrar producto")

    nombre = st.text_input("Nombre")
    descripcion = st.text_input("Descripción")
    precio = st.number_input("Precio", min_value=0.0)
    stock = st.number_input("Stock", min_value=0)

    # 🔥 AQUÍ ESTÁ EL CAMBIO
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
elif menu == "Editar":

    st.subheader("Editar stock")

    id_ = st.number_input("ID del producto", min_value=1)
    stock = st.number_input("Nuevo stock", min_value=0)

    if st.button("Actualizar"):

        update_stock(id_, stock)
        st.session_state.msg = "Stock actualizado correctamente."
        st.session_state.menu = "Ver"
        st.rerun()

# ================= ELIMINAR =================
elif menu == "Eliminar":

    st.subheader("Eliminar producto")

    id_ = st.number_input("ID del producto", min_value=1)

    if st.button("Eliminar"):

        delete_product(id_)
        st.session_state.msg = "Producto eliminado correctamente."
        st.session_state.menu = "Ver"
        st.rerun()
