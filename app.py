import streamlit as st
from auth import auth_router
from crud import create_product, get_all, delete_product, update_stock

st.set_page_config(page_title="Inventario", layout="wide")

state = auth_router()

if state != "ok":
    st.stop()

st.title(f"📦 Inventario - {st.session_state.user}")

# 🔥 LOGOUT REAL
col1, col2 = st.columns([8,1])

with col2:
    if st.button("🚪 Salir"):
        st.session_state.auth = False
        st.session_state.user = ""
        st.session_state.page = "login"
        st.rerun()

menu = st.sidebar.selectbox("Menú", ["Ver", "Crear", "Editar", "Eliminar"])

df = get_all()

# ---------------- VER ----------------
if menu == "Ver":
    st.dataframe(df)

    if len(df) > 0:
        st.subheader("📊 Categorías")
        st.bar_chart(df["categoria"].value_counts())

# ---------------- CREAR ----------------
elif menu == "Crear":
    n = st.text_input("Nombre")
    d = st.text_input("Descripción")
    p = st.number_input("Precio", min_value=0.0)
    s = st.number_input("Stock", min_value=0)
    c = st.selectbox("Categoría", ["Periféricos","Audio","Laptops","Otro"])

    if st.button("Guardar"):
        nuevo = {
            "id": int(df["id"].max()+1) if len(df)>0 else 1,
            "nombre": n,
            "descripcion": d,
            "precio": p,
            "stock": s,
            "categoria": c
        }

        create_product(nuevo)
        st.success("Guardado")
        st.rerun()

# ---------------- EDITAR ----------------
elif menu == "Editar":
    id_ = st.number_input("ID", min_value=1)
    stock = st.number_input("Stock nuevo", min_value=0)

    if st.button("Actualizar"):
        update_stock(id_, stock)
        st.success("Actualizado")
        st.rerun()

# ---------------- ELIMINAR ----------------
elif menu == "Eliminar":
    id_ = st.number_input("ID", min_value=1)

    if st.button("Eliminar"):
        delete_product(id_)
        st.success("Eliminado")
        st.rerun()
