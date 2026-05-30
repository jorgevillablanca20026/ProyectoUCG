import streamlit as st
import pandas as pd

from auth_sqlite import auth_router
from crud_sqlite import create_product, get_all, update_stock, delete_product

# ---------------- AUTH ----------------
state = auth_router()
if state != "ok":
    st.stop()

st.set_page_config(page_title="Inventario", layout="wide")

st.title(f"📦 Sistema de Inventario - {st.session_state.user}")

# ---------------- DATA ----------------
def normalizar(rows):
    if not rows:
        return pd.DataFrame()

    if isinstance(rows[0], dict):
        return pd.DataFrame(rows)

    return pd.DataFrame(rows, columns=["id", "nombre", "descripcion", "precio", "stock", "categoria"])


rows = get_all()
df = normalizar(rows)

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard",
    "➕ Crear",
    "✏️ Editar stock",
    "🗑️ Eliminar"
])

# ================= DASHBOARD =================
with tab1:
    st.subheader("Resumen del inventario")

    col1, col2, col3 = st.columns(3)

    if not df.empty:
        col1.metric("Productos", len(df))
        col2.metric("Stock total", int(pd.to_numeric(df["stock"], errors="coerce").sum()))
        col3.metric("Categorías", df["categoria"].nunique())

        st.divider()

        colA, colB = st.columns(2)

        with colA:
            st.write("📊 Productos por categoría")
            st.bar_chart(df["categoria"].value_counts())

        with colB:
            st.write("📦 Stock por producto")
            chart = df.groupby("nombre")["stock"].sum()
            st.bar_chart(chart)

        st.divider()
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No hay productos registrados")

# ================= CREAR =================
with tab2:
    st.subheader("Registrar producto")

    col1, col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre")
        precio = st.number_input("Precio", min_value=0.0)

    with col2:
        stock = st.number_input("Stock", min_value=0)
        categoria = st.selectbox(
            "Categoría",
            ["Periféricos", "Audio", "Laptops", "Celular", "Televisor", "Otro"]
        )

    descripcion = st.text_area("Descripción")

    if st.button("💾 Guardar producto"):
        if nombre.strip():
            create_product({
                "nombre": nombre,
                "descripcion": descripcion,
                "precio": precio,
                "stock": stock,
                "categoria": categoria
            })
            st.success("Producto creado correctamente")
            st.rerun()
        else:
            st.error("El nombre es obligatorio")

# ================= EDITAR =================
with tab3:
    st.subheader("Actualizar stock")

    col1, col2 = st.columns(2)

    with col1:
        id_ = st.number_input("ID del producto", min_value=1)

    with col2:
        stock = st.number_input("Nuevo stock", min_value=0)

    if st.button("Actualizar stock"):
        update_stock(id_, stock)
        st.success("Stock actualizado")
        st.rerun()

# ================= ELIMINAR =================
with tab4:
    st.subheader("Eliminar producto")

    col1, col2 = st.columns([2, 1])

    with col1:
        id_ = st.number_input("ID del producto", min_value=1)

    with col2:
        st.write("")
        st.write("")
        if st.button("🗑️ Eliminar"):
            delete_product(id_)
            st.success("Producto eliminado")
            st.rerun()
