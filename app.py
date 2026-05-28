import streamlit as st
import pandas as pd

from database import init_db
from auth_sqlite import auth_router
from crud_sqlite import create_product, get_all, update_stock, delete_product

init_db()

# 🔥 MOSTRAR MENSAJE PERSISTENTE (IMPORTANTE)
if "msg" in st.session_state:
    st.success(st.session_state.msg)
    del st.session_state.msg


state = auth_router()

if state != "ok":
    st.stop()

st.title(f"Inventario - {st.session_state.user}")

if st.button("Cerrar sesión"):
    st.session_state.auth = False
    st.session_state.user = ""
    st.session_state.page = "login"
    st.rerun()

menu = st.selectbox("Menú", ["Ver", "Crear", "Editar", "Eliminar"])

rows = get_all()
df = pd.DataFrame(rows, columns=["id","nombre","descripcion","precio","stock","categoria"])

# ---------------- VER ----------------
if menu == "Ver":
    st.dataframe(df)

# ---------------- CREAR ----------------
elif menu == "Crear":

    n = st.text_input("Nombre")
    d = st.text_input("Descripción")
    p = st.number_input("Precio", 0.0)
    s = st.number_input("Stock", 0)
    c = st.selectbox("Categoría", ["Periféricos","Audio","Laptops","Otro"])

    if st.button("Guardar"):

        create_product({
            "nombre": n,
            "descripcion": d,
            "precio": p,
            "stock": s,
            "categoria": c
        })

        # 🔥 MENSAJE QUE SÍ SE VE (ARREGLADO)
        st.session_state.msg = "Su producto fue registrado correctamente"

        st.rerun()

# ---------------- EDITAR ----------------
elif menu == "Editar":

    id_ = st.number_input("ID", 1)
    stock = st.number_input("Stock", 0)

    if st.button("Actualizar"):
        update_stock(id_, stock)
        st.success("Actualizado")
        st.rerun()

# ---------------- ELIMINAR ----------------
elif menu == "Eliminar":

    id_ = st.number_input("ID", 1)

    if st.button("Eliminar"):
        delete_product(id_)
        st.success("Eliminado")
        st.rerun()
