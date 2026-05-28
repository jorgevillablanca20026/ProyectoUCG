import streamlit as st
import pandas as pd

from database import init_db
from auth_sqlite import auth_router
from crud_sqlite import create_product, get_all, update_stock, delete_product

# ---------------- INIT DB ----------------
init_db()

# ---------------- ALERTA POST CREACIÓN ----------------
if st.session_state.get("created"):
    st.success("🎉 Producto creado correctamente")
    st.balloons()
    st.session_state["created"] = False

# ---------------- AUTH ----------------
state = auth_router()

if state != "ok":
    st.stop()

# ---------------- HEADER ----------------
st.title(f"📦 Inventario - {st.session_state.user}")

# ---------------- LOGOUT ----------------
if st.button("🚪 Cerrar sesión"):
    st.session_state.auth = False
    st.session_state.user = ""
    st.session_state.page = "login"
    st.rerun()

# ---------------- MENU ----------------
menu = st.selectbox("Menú", ["Ver", "Crear", "Editar", "Eliminar"])

# ---------------- DATA ----------------
rows = get_all()
df = pd.DataFrame(
    rows,
    columns=["id", "nombre", "descripcion", "precio", "stock", "categoria"]
)

# ---------------- VER ----------------
if menu == "Ver":
    st.dataframe(df)

    # 📊 GRAFICO DE CATEGORÍAS
    if len(df) > 0:
        st.subheader("📊 Productos por categoría")
        st.bar_chart(df["categoria"].value_counts())

# ---------------- CREAR ----------------
elif menu == "Crear":

    n = st.text_input("Nombre")
    d = st.text_input("Descripción")
    p = st.number_input("Precio", 0.0)
    s = st.number_input("Stock", 0)
    c = st.selectbox("Categoría", ["Periféricos", "Audio", "Laptops", "Otro"])

    if st.button("Guardar producto"):

        if n == "":
            st.error("El nombre es obligatorio")
        else:
            create_product({
                "nombre": n,
                "descripcion": d,
                "precio": p,
                "stock": s,
                "categoria": c
            })

            # 🔥 FLAG PARA ALERTA
            st.session_state["created"] = True

            st.rerun()

# ---------------- EDITAR ----------------
elif menu == "Editar":

    id_ = st.number_input("ID producto", min_value=1)
    stock = st.number_input("Nuevo stock", min_value=0)

    if st.button("Actualizar stock"):
        update_stock(id_, stock)
        st.success("Stock actualizado")
        st.rerun()

# ---------------- ELIMINAR ----------------
elif menu == "Eliminar":

    id_ = st.number_input("ID producto", min_value=1)

    if st.button("Eliminar"):
        delete_product(id_)
        st.success("Producto eliminado")
        st.rerun()
