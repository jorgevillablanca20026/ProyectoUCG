import streamlit as st
from auth import auth_router
from crud import create_product, get_all, delete_product, update_stock

st.set_page_config(
    page_title="Inventario Pro",
    page_icon="📦",
    layout="wide"
)

# ================= LOGIN =================
state = auth_router()

if state != "ok":
    st.stop()

# ================= HEADER =================
st.markdown(
    """
    <style>
        .main-title {
            font-size: 34px;
            font-weight: bold;
            color: #1f4e79;
        }
        .subtitle {
            font-size: 16px;
            color: gray;
        }
        .card {
            padding: 15px;
            border-radius: 12px;
            background-color: #f5f7fa;
            box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
        }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns([8,1])

with col1:
    st.markdown('<div class="main-title">📦 Inventario Profesional</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">Usuario: {st.session_state.user}</div>', unsafe_allow_html=True)

with col2:
    if st.button("🚪 Logout"):
        st.session_state.auth = False
        st.session_state.user = ""
        st.session_state.page = "login"
        st.rerun()

st.markdown("---")

# ================= DATA =================
df = get_all()

# ================= SIDEBAR =================
menu = st.sidebar.radio(
    "📌 Menú",
    ["📊 Dashboard", "➕ Crear", "✏️ Editar", "🗑️ Eliminar"]
)

# ================= DASHBOARD =================
if menu == "📊 Dashboard":

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="card">📦 Total productos<br><h2>{}</h2></div>'.format(len(df)), unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">💰 Valor total stock<br><h2>{}</h2></div>'.format(df["stock"].sum() if len(df)>0 else 0), unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card">📂 Categorías<br><h2>{}</h2></div>'.format(df["categoria"].nunique() if len(df)>0 else 0), unsafe_allow_html=True)

    st.markdown("### 📋 Inventario")
    st.dataframe(df, use_container_width=True)

    st.markdown("### 📊 Productos por categoría")

    if len(df) > 0:
        st.bar_chart(df["categoria"].value_counts())

# ================= CREATE =================
elif menu == "➕ Crear":

    st.subheader("➕ Nuevo producto")

    col1, col2 = st.columns(2)

    with col1:
        n = st.text_input("Nombre")
        p = st.number_input("Precio", min_value=0.0)

    with col2:
        d = st.text_input("Descripción")
        s = st.number_input("Stock", min_value=0)

    c = st.selectbox("Categoría", ["Periféricos","Audio","Laptops","Otro"])

    if st.button("💾 Guardar producto"):
        nuevo = {
            "id": int(df["id"].max()+1) if len(df)>0 else 1,
            "nombre": n,
            "descripcion": d,
            "precio": p,
            "stock": s,
            "categoria": c
        }

        create_product(nuevo)
        st.success("Producto agregado correctamente")
        st.rerun()

# ================= EDIT =================
elif menu == "✏️ Editar":

    st.subheader("✏️ Actualizar stock")

    id_ = st.number_input("ID producto", min_value=1)
    stock = st.number_input("Nuevo stock", min_value=0)

    if st.button("Actualizar"):
        update_stock(id_, stock)
        st.success("Actualizado")
        st.rerun()

# ================= DELETE =================
elif menu == "🗑️ Eliminar":

    st.subheader("🗑️ Eliminar producto")

    id_ = st.number_input("ID producto", min_value=1)

    if st.button("Eliminar"):
        delete_product(id_)
        st.success("Eliminado")
        st.rerun()
