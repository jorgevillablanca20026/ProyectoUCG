import streamlit as st
import matplotlib.pyplot as plt

from auth import auth_router
from crud import create_product, get_all, delete_product, update_stock

st.set_page_config(page_title="Inventario", layout="wide")

state = auth_router()

if state != "ok":
    st.stop()

st.title(f"📦 Inventario - {st.session_state.user}")

menu = st.sidebar.selectbox("Menú", ["Ver", "Crear", "Editar", "Eliminar"])

df = get_all()

# ---------------- VER ----------------
if menu == "Ver":
    st.subheader("📋 Productos")
    st.dataframe(df)

    st.markdown("---")
    st.subheader("📊 Productos por categoría")

    if len(df) > 0:
        data = df["categoria"].value_counts()

        fig, ax = plt.subplots()
        data.plot(kind="bar", ax=ax, color="skyblue")

        ax.set_xlabel("Categoría")
        ax.set_ylabel("Cantidad")
        ax.set_title("Inventario por categoría")

        st.pyplot(fig)
    else:
        st.info("No hay productos")

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
    stock = st.number_input("Nuevo stock", min_value=0)

    if st.button("Actualizar"):
        update_stock(id_, stock)
        st.rerun()

# ---------------- ELIMINAR ----------------
elif menu == "Eliminar":
    id_ = st.number_input("ID", min_value=1)

    if st.button("Eliminar"):
        delete_product(id_)
        st.rerun()
