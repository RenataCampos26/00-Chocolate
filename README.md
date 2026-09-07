# 00-Chocolate
Creación de un DashBoard con Python 

Aplicación de análisis y visualización de datos construida con Panda, Plotly y Sreamlit

Descripción 

Este proyecto permite:
•	Cargar y transformar datos con Pandas.
•	Presentar métricas clave de forma interactiva.
•	Visualizar resultados con gráficos dinámicos en Plotly.
•	Publicar un dashboard con Streamlit. 

Está pensado como base para proyectos de analítica, monitoreo y reporting rápido. 

Características

•	Limpieza y preparación de datos tabulares. 
•	Filtros interactivos por categorías, fechas y otras variables. 
•	Gráficos de líneas, barras, y tablas resumen. 
•	KPIs principales en una interfaz simple y clara. 

Tecnologías

•	Python 3.10+
•	Pandas
•	Plotly
•	Streamlit

Estructura de Datos

El proyecto asume una tabla principal en formato CSV como: 

COLUMNA	         TIPO DE DATO	      DESCRIPCION
Order_ID          	Texto	          Número de Orden 
Channel             Texto	          Canal de venta 
Discount_Pct        Texto	          Porcentaje de descuento 
Boxes_Shipped       Texto	          Cant de Cajas Vendidas
Country             Texto	          País
Order_Date          Flotante	      Fecha de la Orden
Marketing_Spend     Flotante	      Gasto de Marketing
Product             Texto          	Producto
Salesperson         Texto	          Vendedor
Price_per_Box       Flotante	      Precio por Caja 
Amount              Flotante	      Monto de la Venta

