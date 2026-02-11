import streamlit as st
import pandas as pd
from datetime import date

# Configuración de página
st.set_page_config(page_title="Examen I Parcial", page_icon="💳", layout="wide")

# --- COLORES ---
st.markdown("""
    <style>
    /* Fondo principal oscuro */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Títulos en amarillo */
    h1, h2, h3, label, .stMarkdown p {
        color: #f1c40f !important;
    }

    /* Contenedores de inputs */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>div>input, .stDateInput>div>div>input {
        background-color: #262730 !important;
        color: white !important;
        border: 1px solid #f1c40f !important;
    }

    /* Botón Generar Factura (Amarillo) */
    .stButton>button {
        background-color: #f1c40f !important;
        color: #0e1117 !important;
        font-weight: bold !important;
        width: 100%;
        border-radius: 10px;
        border: none;
    }

    /* Tablas */
    .stTable {
        background-color: #1a1c24;
        border-radius: 10px;
    }
    
    /* Líneas divisorias */
    hr {
        border-top: 1px solid #f1c40f !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. TÍTULO DE LA TIENDA (Requisito D)
st.title("Tienda de Electrodomésticos (Examen I parcial)")
st.markdown("---")

# Base de datos (Mínimo 8 productos - Requisito A)
productos = [
    {"Nombre": "Refrigeradora", "Precio": 18500.0, "Categoría": "Línea Blanca"},
    {"Nombre": "Lavadora", "Precio": 12400.0, "Categoría": "Línea Blanca"},
    {"Nombre": "Microondas", "Precio": 3200.0, "Categoría": "Cocina"},
    {"Nombre": "Licuadora", "Precio": 1500.0, "Categoría": "Cocina"},
    {"Nombre": "Aire Acondicionado", "Precio": 15800.0, "Categoría": "Climatización"},
    {"Nombre": "Plancha", "Precio": 850.0, "Categoría": "Hogar"},
    {"Nombre": "Televisor", "Precio": 9500.0, "Categoría": "Electrónica"},
    {"Nombre": "Cafetera", "Precio": 2100.0, "Categoría": "Cocina"},
]
df_prods = pd.DataFrame(productos)

# 2. SELECCIÓN DE PRODUCTO (selectbox - Requisito A/3)
st.header("1. Selección de producto")
producto_nombre = st.selectbox("Elija un producto del catálogo:", df_prods["Nombre"])
datos_prod = df_prods[df_prods["Nombre"] == producto_nombre].iloc[0]

# 3. FILTRO POR PRECIO (slider - Requisito D/4)
st.header("2. Filtro por precio")
precio_max = st.slider("Verificar presupuesto máximo (Lps):", 0, 25000, 20000)
if datos_prod["Precio"] > precio_max:
    st.warning(f"El producto seleccionado excede su filtro de precio (Lps. {precio_max})")
else:
    st.success(f"El producto está dentro del rango de precio.")

# 4. CANTIDAD Y CARRITO (Requisito B/5)
st.header("3. Cantidad y carrito")
col_c1, col_c2 = st.columns(2)
with col_c1:
    cantidad = st.number_input("Ingrese la cantidad:", min_value=1, value=1, step=1)
with col_c2:
    subtotal_item = datos_prod["Precio"] * cantidad
    st.write("**Resumen de Selección:**")
    st.write(f"- Producto: {producto_nombre}")
    st.write(f"- Precio Unitario: Lps. {datos_prod['Precio']:,.2f}")
    st.write(f"- Subtotal: Lps. {subtotal_item:,.2f}")

st.markdown("---")

# 5. DATOS DEL CLIENTE (Requisito C/7)
st.header("4. Datos del cliente")
col_d1, col_d2 = st.columns(2)
with col_d1:
    nombre_cliente = st.text_input("Nombre completo:")
    rtn_cliente = st.text_input("RTN / Identidad:")
with col_d2:
    fecha_factura = st.date_input("Fecha de facturación:", date.today())

st.markdown("---")

# 6. RESUMEN DE FACTURACIÓN (Requisito C/8)
st.header("5. Resumen de facturación")

if st.button("GENERAR FACTURA"):
    if nombre_cliente and rtn_cliente:
        # Cálculos finales
        isv = subtotal_item * 0.15
        total_pagar = subtotal_item + isv
        
        # Mostrar Factura
        st.subheader("DETALLE DE LA COMPRA")
        
        # Tabla detallada (Requisito B/C)
        detalle_data = {
            "Cliente": [nombre_cliente],
            "Producto": [producto_nombre],
            "Cantidad": [cantidad],
            "Precio Unit.": [f"Lps. {datos_prod['Precio']:,.2f}"],
            "Subtotal": [f"Lps. {subtotal_item:,.2f}"]
        }
        st.table(pd.DataFrame(detalle_data))
        
        # Totales
        col_t1, col_t2 = st.columns(2)
        with col_t2:
            st.write(f"**Subtotal General:** Lps. {subtotal_item:,.2f}")
            st.write(f"**ISV (15%):** Lps. {isv:,.2f}")
            st.markdown(f"### **Total a Pagar: Lps. {total_pagar:,.2f}**")
            
        st.info(f"Factura generada para el RTN: {rtn_cliente} el {fecha_factura}")
        st.balloons()
    else:
        st.error("Por favor, ingrese los datos del cliente antes de facturar.")

# Nombre Completo: Cristian Roberto Diaz