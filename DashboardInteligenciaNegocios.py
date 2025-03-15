import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos reales
st.set_page_config(page_title="Dashboard de Ventas", layout="wide")
st.title("📊 Dashboard de Ventas")

@st.cache_data
def cargar_datos():
    file_path = r"DatosDeVentasLimpios.xlsx"
    df = pd.read_excel(file_path, sheet_name='Sheet1')
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    df_enero = df[df["Fecha"].dt.month == 1]  # Filtrar enero
    return df_enero

df = cargar_datos()

# Sidebar para filtros
st.sidebar.header("Filtros")
region_seleccionada = st.sidebar.selectbox("Selecciona una Región", df["Region"].unique())
df = df[df["Region"] == region_seleccionada]

# Región con más ventas
df_region = df.groupby("Region")["Ventas"].sum().reset_index()
region_mas_ventas = df_region.sort_values(by="Ventas", ascending=False).iloc[0]

st.metric(label="🏆 Región con más ventas en enero", value=region_mas_ventas["Region"], delta=int(region_mas_ventas["Ventas"]))

# Gráfico de ventas por región
fig_region = px.bar(df_region, x="Region", y="Ventas", title="📍 Ventas Totales por Región", color="Ventas", text_auto=True)
st.plotly_chart(fig_region, use_container_width=True)

# Gráfico de ventas por día
df_ventas_diarias = df.groupby("Fecha")["Ventas"].sum().reset_index()
fig_ventas_dia = px.line(df_ventas_diarias, x="Fecha", y="Ventas", title="📅 Ventas por Día en Enero")
st.plotly_chart(fig_ventas_dia, use_container_width=True)

# Productos más y menos vendidos
df_productos = df.groupby("Producto")["Ventas"].sum().reset_index()
producto_mas_vendido = df_productos.sort_values(by="Ventas", ascending=False).iloc[0]
producto_menos_vendido = df_productos.sort_values(by="Ventas", ascending=True).iloc[0]

st.metric(label="🔥 Producto más vendido", value=producto_mas_vendido["Producto"], delta=int(producto_mas_vendido["Ventas"]))
st.metric(label="❄️ Producto menos vendido", value=producto_menos_vendido["Producto"], delta=int(producto_menos_vendido["Ventas"]))

# Gráfico de ventas por producto
fig_productos = px.bar(df_productos, x="Producto", y="Ventas", title="🛒 Ventas por Producto", color="Ventas", text_auto=True)
st.plotly_chart(fig_productos, use_container_width=True)

# Distribución de precios de productos
fig_precios = px.box(df, x="Producto", y="Ventas", title="💰 Distribución de Precios de Productos", points="all")
st.plotly_chart(fig_precios, use_container_width=True)

# Top 10 vendedores
df_vendedores = df.groupby("Vendedor")["Ventas"].sum().reset_index()
df_vendedores = df_vendedores.sort_values(by="Ventas", ascending=False).head(10)
fig_vendedores = px.bar(df_vendedores, x="Vendedor", y="Ventas", title="🏅 Top 10 Vendedores", color="Ventas", text_auto=True)
st.plotly_chart(fig_vendedores, use_container_width=True)
