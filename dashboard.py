import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuración de página (debe ser la primera llamada a Streamlit)
st.set_page_config(
    page_title="Dashboard de Rentabilidad | Maderera",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS Premium Adicionales
st.markdown("""
<style>
    /* Estilizar las métricas */
    div[data-testid="metric-container"] {
        background-color: #1E222A;
        border: 1px solid #2B303B;
        padding: 5% 5% 5% 10%;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease-in-out;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        border-color: #00D4FF;
    }
    /* Títulos de la app */
    .app-title {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: -webkit-linear-gradient(45deg, #00D4FF, #00FFD4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Función para cargar datos (con caché para rendimiento)
@st.cache_data
def load_data():
    data_path = os.path.join("data", "gold", "dm_rentabilidad", "rentabilidad.csv")
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    else:
        st.error(f"No se encontró el archivo de datos en: {data_path}. Asegúrate de ejecutar el pipeline de la Capa Gold.")
        return pd.DataFrame()

# Cargar los datos
df = load_data()

if not df.empty:
    # --- BARRA LATERAL (FILTROS) ---
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1042/1042079.png", width=100) # Icono de madera temporal
    st.sidebar.markdown("## 🌲 Maderera BI")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Filtros de Análisis")
    
    # Filtro de Año
    anios_disponibles = sorted(df['anio'].unique().tolist(), reverse=True)
    anio_seleccionado = st.sidebar.selectbox("Seleccionar Año", ["Todos"] + anios_disponibles)
    
    # Filtro de Especie
    especies_disponibles = sorted(df['especie'].unique().tolist())
    especie_seleccionada = st.sidebar.multiselect("Seleccionar Especie(s)", especies_disponibles, default=especies_disponibles)
    
    # Aplicar Filtros
    df_filtrado = df.copy()
    if anio_seleccionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['anio'] == anio_seleccionado]
    if especie_seleccionada:
        df_filtrado = df_filtrado[df_filtrado['especie'].isin(especie_seleccionada)]

    # --- CUERPO PRINCIPAL ---
    st.markdown('<h1 class="app-title">Análisis de Rentabilidad Comercial</h1>', unsafe_allow_html=True)
    st.markdown("Monitor de ventas, volúmenes y transacciones por especie de madera.")
    
    st.markdown("---")

    # KPIs Principales
    col1, col2, col3 = st.columns(3)
    
    ingresos_totales = df_filtrado['ingresos_totales'].sum()
    volumen_total = df_filtrado['volumen_piezas_vendidas'].sum()
    transacciones_totales = df_filtrado['transacciones_totales'].sum()
    
    col1.metric("Ingresos Totales (PEN)", f"S/ {ingresos_totales:,.2f}")
    col2.metric("Volumen Vendido (Piezas)", f"{volumen_total:,.0f}")
    col3.metric("Transacciones Totales", f"{transacciones_totales:,.0f}")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Gráficos
    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        st.markdown("### Ingresos por Especie")
        df_especie_ingresos = df_filtrado.groupby('especie')['ingresos_totales'].sum().reset_index()
        fig_pie = px.pie(
            df_especie_ingresos, 
            values='ingresos_totales', 
            names='especie',
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Tealgrn_r
        )
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig_pie, use_container_width=True)

    with row1_col2:
        st.markdown("### Tendencia de Ingresos Mensuales")
        # Asegurar orden correcto de meses
        meses_orden = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        df_tendencia = df_filtrado.groupby(['mes', 'nombre_mes'])['ingresos_totales'].sum().reset_index().sort_values('mes')
        
        fig_line = px.line(
            df_tendencia, 
            x='nombre_mes', 
            y='ingresos_totales',
            markers=True,
            line_shape='spline'
        )
        fig_line.update_traces(line_color='#00D4FF', marker_color='#00FFD4')
        fig_line.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color="white",
            xaxis_title="Mes",
            yaxis_title="Ingresos (S/)"
        )
        st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")
    
    # Tabla de Datos
    st.markdown("### Detalle Analítico")
    st.dataframe(
        df_filtrado.sort_values(by='ingresos_totales', ascending=False),
        use_container_width=True,
        hide_index=True,
        column_config={
            "anio": st.column_config.NumberColumn("Año", format="%d"),
            "mes": "Nº Mes",
            "ingresos_totales": st.column_config.NumberColumn("Ingresos (S/)", format="%.2f"),
            "volumen_piezas_vendidas": "Volumen (pzs)",
            "transacciones_totales": "Transacciones"
        }
    )
else:
    st.info("Esperando datos para renderizar el dashboard.")
