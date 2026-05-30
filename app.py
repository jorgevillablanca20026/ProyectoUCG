import streamlit as st
import pandas as pd

from auth_sqlite import auth_router
from crud_sqlite import create_product, get_all, update_stock, delete_product

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Inventario Pro", layout="wide")

# 🔥 ESTILO VISUAL (CSS SIMPLE)
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    div[data-testid="metric-container"] {
        background-color: #0f172a;
        border-radius: 12px;
        padding: 12px;
        color: white;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.2);
    }

    h1, h2, h3 {
        color: #1f2937;
    }

    .stDataFrame {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- AUTH ----------------
state = auth_router()
if state != "ok":
    st.stop()

st.title(f"📦 Inventario Profesional - {st.session_state.user}")

# ---------------- DATA ----------------
def normalizar(rows):
    if not rows:
        return pd.DataFrame()

    if isinstance(rows[0], dict):
        return pd.DataFrame(rows)

    return pd.DataFrame(rows, columns=[
        "id", "nombre", "descripcion", "precio", "stock", "categoria"
    ])

df = normalizar(get_all())

# ---------------- TABS ----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard",
    "➕ Crear",
    "✏️ Editar",
    "🗑️ Eliminar"
])

# ================= DASHBOARD =================
with tab1:

    st.markdown("## 📊 Panel de control")

    if not df.empty:

        # --------- CARDS / MÉTRICAS ---------
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("📦 Productos", len(df))

        with col2:
            total_precio = pd.to_numeric(df["precio"], errors="coerce").sum()
            st.metric("💰 Total precios", round(total_precio, 2))

        with col3:
            stock_total = pd.to_numeric(df["stock"], errors="coerce").sum()
            st.metric("📊 Stock total", int(stock_total))

        with col4:
            st.metric("🏷️ Categorías", df["categoria"].nunique())

        st.divider()

        # --------- TABLA (ARRIBA) ---------
        with st.container():
            st.markdown("### 📋 Inventario")
            st.dataframe(df, use_container_width=True, height=260)

        st.divider()

        # --------- GRÁFICOS ---------
        st.markdown("### 📊 Análisis")

        colA, colB = st.columns(2)

        with colA:
            st.markdown("#### Categorías")
            st.bar_chart(df["categoria"].value_counts())

        with colB:
            st.markdown("#### Stock por producto")
            st.bar_chart(df.groupby("nombre")["stock"].sum())

    else:
        st.warning("No hay productos registrados")

# ================= CREAR =================
with tab2:

    st.markdown("## ➕ Nuevo producto")

    with st.container():

        col1, col2 = st.columns(2)

        with col1:
            nombre = st.text_input("Nombre", key="create_nombre")
            precio = st.number_input("Precio", min_value=0.0, key="create_precio")

        with col2:
            stock = st.number_input("Stock", min_value=0, key="create_stock")
            categoria = st.selectbox(
                "Categoría",
                ["Periféricos", "Audio", "Laptops", "Celular", "Televisor", "Otro"],
                key="create_categoria"
            )

        descripcion = st.text_area("Descripción", key="create_desc")

        if st.button("💾 Guardar", key="create_btn"):
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

                st.success("Producto creado")
                st.rerun()

# ================= EDITAR =================
with tab3:

    st.markdown("## ✏️ Actualizar stock")

    col1, col2 = st.columns(2)

    with col1:
        id_ = st.number_input("ID producto", min_value=1, key="edit_id")

    with col2:
        stock = st.number_input("Nuevo stock", min_value=0, key="edit_stock")

    if st.button("Actualizar", key="edit_btn"):
        update_stock(id_, stock)
        st.success("Stock actualizado")
        st.rerun()

# ================= ELIMINAR =================
with tab4:

    st.markdown("## 🗑️ Eliminar producto")

    col1, col2 = st.columns([2, 1])

    with col1:
        id_ = st.number_input("ID producto", min_value=1, key="delete_id")

    with col2:
        st.write("")
        if st.button("Eliminar", key="delete_btn"):
            delete_product(id_)
            st.success("Producto eliminado")
            st.rerun()
