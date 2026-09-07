#-----------------------------------------------------------------------------  
#IMPORTAR LIBRERIAS
#-----------------------------------------------------------------------------

import streamlit as st
import pandas as pd 
import plotly.express as px 

#-----------------------------------------------------------------------------
#CONFIGURACION DE LA PÁGINA
#-----------------------------------------------------------------------------

st.set_page_config(
    page_title="Dashboar Ventas de Chocolate 2022 - 2023",
    page_icon=":bar_chart:",
    )

#-----------------------------------------------------------------
#CARGAR LOS DATOS
#-----------------------------------------------------------------

def load_data():
    df = pd.read_csv('Chocolate_Sales.csv')
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], errors='coerce')
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    return df

df = load_data()

products = df['Product'].dropna().unique()
countries = df['Country'].dropna().unique()
channels = df['Channel'].dropna().unique()

#-----------------------------------------------------------------
#LIMPIAR FILTROS 
#-----------------------------------------------------------------

def limpiar_filtros():
    st.session_state["Order_ID"] = ""
    st.session_state["Product"] = list(products)
    st.session_state["Country"] = list(countries)
    st.session_state["Channel"] = list(channels)

#----------------------------------------------------------------------------
#TITULO DEL DASHBOARD
#----------------------------------------------------------------------------

st.title("Dashboard Ventas de Chocolate")

#----------------------------------------------------------------------------
#INFORMACIÓN SOBRE LOS DATOS
#----------------------------------------------------------------------------

st.write("""Este conjunto de datos recoge la actividad de ventas a nivel de pedido de 
una marca de chocolate que opera en varios países y canales de venta entre enero 
de 2022 y diciembre de 2023.""")

#-----------------------------------------------------------------
#BARRA LATERAL BOTON (SIDEBAR) PARA FILTROS 
#-----------------------------------------------------------------

st.sidebar.header("Filtros de Búsqueda")
st.sidebar.button("Limpiar Filtros", on_click=limpiar_filtros)

#---------------------------------------------------------------------------
#TITULO
#---------------------------------------------------------------------------

st.sidebar.title("Filtros")

#-----------------------------------------------------------------
#FILTROS
#-----------------------------------------------------------------

#FILTRO DE FECHA
fecha_inicio = st.sidebar.date_input(
    "Fecha de Inicio", value=pd.to_datetime(df["Order_Date"].min()), key="fecha_inicio")

fecha_fin = st.sidebar.date_input(
    "Fecha de Fin", value=pd.to_datetime(df["Order_Date"].max()), key="fecha_fin")

#FILTRO ORDER_ID
order_id_query = st.sidebar.text_input("Order ID", key="Order_ID")

#FILTRO PRODUCT
selected_products = st.sidebar.multiselect(
    "Product", options=products, default=products, key="Product")

#FILTRO COUNTRY
selected_countries = st.sidebar.multiselect(
    "Country", options=countries, default=countries, key="Country")

#FILTRO CHANNEL
selected_channels = st.sidebar.multiselect(
    "Channel", options=channels, default=channels, key="Channel")

# APLICACIÓN DE FILTROS
filtered_df = df.copy()

#FILTRO POR:

if fecha_inicio and fecha_fin:
    filtered_df = filtered_df[
        (filtered_df["Order_Date"].dt.date >= fecha_inicio) & 
        (filtered_df["Order_Date"].dt.date <= fecha_fin)
    ]

# Filtrado por Order ID
if order_id_query:
    filtered_df = filtered_df[filtered_df['Order_ID'].astype(str).str.contains(order_id_query, case=False, na=False)]

# Filtrado por Productos
if selected_products:
    filtered_df = filtered_df[filtered_df['Product'].isin(selected_products)]

# Filtrado por Países
if selected_countries:
    filtered_df = filtered_df[filtered_df['Country'].isin(selected_countries)]

# Filtrado por Canales
if selected_channels:
    filtered_df = filtered_df[filtered_df['Channel'].isin(selected_channels)]


#---------------------------------------------------------------------------
#MÉTRICAS CLAVE (KPI)
#---------------------------------------------------------------------------

if filtered_df.empty:
    st.warning("Sin datos disponibles.")
    st.stop()

#---------------------------------------------------------------------------
#TITULO
#---------------------------------------------------------------------------

st.subheader("Métricas Clave")

#---------------------------------------------------------------------------
#ORGANIZAR EN COLUMNAS LOS KPI
#---------------------------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

#---------------------------------------------------------------------------
#CALCULO DE METRICAS
#---------------------------------------------------------------------------

col1.metric("Ingresos Totales", f"${filtered_df['Amount'].sum():,.2f}")
col2.metric("Precio promedio por caja", f"${filtered_df['Price_per_Box'].mean():,.2f}")
col3.metric("Precio máximo por caja", f"${filtered_df['Price_per_Box'].max():,.2f}")
col4.metric("Precio mínimo por caja", f"${filtered_df['Price_per_Box'].min():,.2f}")

#---------------------------------------------------------------------------
#ORGANIZAR EN COLUMNAS LOS KPI
#---------------------------------------------------------------------------

col5, col6, col7 = st.columns(3)

#---------------------------------------------------------------------------
#CALCULO DE METRICAS
#---------------------------------------------------------------------------

col5.metric("Total de cajas vendidas", f"{filtered_df['Boxes_Shipped'].sum():,.0f}")
col6.metric("Total gasto de marketing", f"${filtered_df['Marketing_Spend'].sum():,.0f}")
col7.metric("Cantidad de órdenes ejecutadas", f"{len(filtered_df):,}")

#---------------------------------------------------------------------------
#ANALISIS VISUAL - GRÁFICOS USANDO PLOTLY EXPRESS
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------
#TITULO
#---------------------------------------------------------------------------

st.subheader("Análisis Visual")

#---------------------------------------------------------------------------
#DEFINICION DEL ESPACIO PARA UBICAR LOS GRÁFICOS 
#---------------------------------------------------------------------------

col8, = st.columns(1)

#---------------------------------------------------------------------------
#1ER GRÁFICO - VENTAS POR PRODUCTO - DE BARRAS
#---------------------------------------------------------------------------

with col8:
    st.markdown("**Ventas por Producto**")

#Paso 1

ventas_por_producto = (
    filtered_df.groupby("Product")['Amount']
    .sum()
    .reset_index()
    .sort_values(by="Amount", ascending=True)  
    )

#Paso 2

fig_bar_ventas_por_producto = px.bar(
    ventas_por_producto,
    x="Amount",
    y="Product",
    orientation = "h",
    color="Amount",
    color_continuous_scale="Oranges",
    )

#Paso 3

st.plotly_chart(fig_bar_ventas_por_producto, use_container_width=True)

#---------------------------------------------------------------------------
#DEFINICION DEL ESPACIO PARA UBICAR LOS GRÁFICOS 
#---------------------------------------------------------------------------

col9, col10 = st.columns(2)

#---------------------------------------------------------------------------
#2DO GRÁFICO - GASTO DE MARKETING - DE BARRAS
#---------------------------------------------------------------------------

with col9:
    st.markdown("**Gasto de Marketing**")

    gasto_de_marketing = (
        filtered_df.groupby(["Country", "Channel"])["Marketing_Spend"]
        .sum()
        .reset_index()
        .sort_values(by="Marketing_Spend", ascending=True)
    )

    fig_bar_gasto_de_marketing = px.bar(
        gasto_de_marketing,
        x="Country",
        y="Marketing_Spend",
        color= "Channel",
        barmode="group",
    )

    st.plotly_chart(fig_bar_gasto_de_marketing, use_container_width=True)
#---------------------------------------------------------------------------
#3ER GRÁFICO - VENTAS POR PAÌS - DE TORTA
#---------------------------------------------------------------------------

with col10:
   st.markdown("**Ventas por País**")

#Paso 1

ventas_por_país =(
    filtered_df.groupby("Country") ['Amount']
    .sum()
    .reset_index()
    .sort_values(by="Amount", ascending=False))

#Paso 2

pie_chart_ventas_por_país = px.pie(
    ventas_por_país, 
    values="Amount", 
    names="Country",
    hole=0.5,
    color_discrete_sequence=px.colors.sequential.Greens_r,
    )

#Paso 3

st.plotly_chart(pie_chart_ventas_por_país, use_container_width=True)

#---------------------------------------------------------------------------
#DEFINICION DEL ESPACIO PARA UBICAR LOS GRÁFICOS 
#---------------------------------------------------------------------------

col11, = st.columns(1)

#---------------------------------------------------------------------------
#4TO GRÁFICO - COMPORTAMIENTO DE LAS VENTAS  - LINEA DE TIEMPO
#---------------------------------------------------------------------------

with col11:

   st.markdown("**Comportamiento de las Ventas**")

unidad_tiempo = st.selectbox(
        "Seleccione la unidad de tiempo para visualizar el comportamiento de las ventas",
        options=[ "Día", "Semana","Mes", "Año"],
        key="unidad_tiempo",)

frecuencias = {
        "Día": "D",
        "Semana": "W",
        "Mes": "ME",
        "Año": "YE" 
        }

ventas_por_fecha = (
        filtered_df.groupby(
            pd.Grouper(
                key="Order_Date", 
                freq=frecuencias[unidad_tiempo]),
        )["Amount"]
        .sum()
        .reset_index()
        .sort_values(by="Order_Date", ascending=True))

fig_line_fecha = px.line(
        ventas_por_fecha,
        x="Order_Date",
        y="Amount",
        markers=True,)

st.plotly_chart(fig_line_fecha, use_container_width=True)

#--------------------------------------------------------------
#DESCARGA DE DATOS
#--------------------------------------------------------------

st.subheader("Base de Datos Ventas de Chocolate 2022 - 2023")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

csv = filtered_df.to_csv(index=False) .encode("utf-8")

st.download_button(
    label="Descargar CSV",
    data=csv, 
    file_name="datos_procesados.csv", 
    mime="text/csv",)

#-------------------------------------------------------------
#PIE DE PÁGINA
#-------------------------------------------------------------

st.divider()
st.markdown("**Fuente:**") 
st.caption("https://www.kaggle.com/datasets/arjunmehta1992/chocolate-sales-in-20222023")
