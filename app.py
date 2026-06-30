import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Causas de Incendios Forestales Investigados", 
    layout="wide", 
    page_icon="🌲"
)

# 2. ESTILOS CSS CON COLORES INSTITUCIONALES Y DISEÑO COMPACTO (SIN ESPACIOS EN BLANCO)
st.markdown("""
    <style>
    /* Fondo general gris de la aplicación */
    .stApp {
        background-color: #ebedef;
    }
    /* Reducir espacios en blanco nativos de Streamlit */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    /* Barra superior - Verde Oscuro Institucional CONAF */
    .header-bar {
        background-color: #1b5e20;
        padding: 14px 20px;
        border-radius: 4px;
        border-bottom: 4px solid #fbc02d; /* Línea de acento amarilla */
        margin-bottom: 15px;
    }
    .header-title {
        color: white !important;
        margin: 0 !important;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: bold;
        font-size: 24px;
        letter-spacing: 0.5px;
    }
    /* Títulos de los gráficos sobre las tarjetas */
    .section-title {
        color: #1b5e20;
        font-size: 16px;
        text-transform: uppercase;
        font-weight: bold;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
        margin-top: 5px;
    }
    /* Tarjetas blancas institucionales ajustadas (sin padding excesivo) */
    .analytics-card {
        background-color: white;
        padding: 12px 15px;
        border-radius: 4px;
        border: 1px solid #dcdcdc;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    /* Estilos específicos para las tarjetas de métricas */
    .metric-label {
        color: #555555;
        font-size: 12px;
        text-transform: uppercase;
        font-weight: bold;
        margin-bottom: 4px;
    }
    .metric-value {
        color: #1b5e20;
        font-size: 28px;
        font-weight: bold;
        line-height: 1.1;
    }
    .metric-sub {
        color: #777777;
        font-size: 11px;
        margin-top: 2px;
    }
    /* Ajuste de margen inferior en elementos de Streamlit */
    .stSelectbox, .stDataFrame {
        margin-bottom: 0px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA DE TÍTULO SOLICITADO
st.markdown('<div class="header-bar"><h2 class="header-title">Causas de Incendios Forestales Investigados, Temporada 2025-2026</h2></div>', unsafe_allow_html=True)

# 4. CARGA DE DATOS SEGURO
@st.cache_data
def cargar_datos_seguro():
    try:
        return pd.read_excel("DATOS DUROS 2025-2026 WEB_2.xlsx", sheet_name="Invest. IF")
    except Exception as e:
        st.error(f"Error cargando el archivo: {e}")
        return pd.DataFrame()

df = cargar_datos_seguro()

if not df.empty:
    # 5. FILTROS EN LA BARRA LATERAL
    st.sidebar.markdown("<h3 style='color:#1b5e20; margin-top:0;'>🔍 Filtros</h3>", unsafe_allow_html=True)
    
    region_sel = st.sidebar.selectbox("Región", ["Todas"] + sorted(list(df["Región"].dropna().unique()))) if "Región" in df.columns else "Todas"
    df_filtrado = df.copy()
    if region_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Región"] == region_sel]
        
    provincia_sel = st.sidebar.selectbox("Provincia", ["Todas"] + sorted(list(df_filtrado["Provincia"].dropna().unique()))) if "Provincia" in df.columns else "Todas"
    if provincia_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Provincia"] == provincia_sel]
        
    comuna_sel = st.sidebar.selectbox("Comuna", ["Todas"] + sorted(list(df_filtrado["Comuna"].dropna().unique()))) if "Comuna" in df.columns else "Todas"
    if comuna_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Comuna"] == comuna_sel]

    # 6. FILA SUPERIOR: GRÁFICOS PARALELOS CON TÍTULOS SOBRE ELLOS
    col_graf1, col_graf2 = st.columns([6, 4])

    with col_graf1:
        st.markdown('<div class="section-title">📊 Frecuencia de Incendios por Causa General (Mayor a Menor)</div>', unsafe_allow_html=True)
        st.markdown('<div class="analytics-card" style="min-height: 350px;">', unsafe_allow_html=True)
        if "Causa General" in df_filtrado.columns and not df_filtrado.empty:
            df_causas_frecuencia = df_filtrado["Causa General"].value_counts().sort_values(ascending=False)
            st.bar_chart(df_causas_frecuencia, use_container_width=True)
        else:
            st.info("Sin datos para graficar causas.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_graf2:
        st.markdown('<div class="section-title">🍕 Distribución Porcentual por Grupo de Causas</div>', unsafe_allow_html=True)
        st.markdown('<div class="analytics-card" style="min-height: 350px;">', unsafe_allow_html=True)
        if "Grupo de causas" in df_filtrado.columns and not df_filtrado.empty:
            df_grupo_counts = df_filtrado["Grupo de causas"].value_counts()
            
            fig, ax = plt.subplots(figsize=(6, 3.8), facecolor='white')
            colores_institucionales = ['#2e7d32', '#fbc02d', '#ef6c00', '#c62828', '#4e342e', '#00838f']
            
            ax.pie(
                df_grupo_counts, 
                labels=df_grupo_counts.index, 
                autopct='%1.1f%%', 
                startangle=140, 
                colors=colores_institucionales[:len(df_grupo_counts)],
                textprops={'fontsize': 9, 'color': '#212121'}
            )
            ax.axis('equal')
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.info("Sin registros para generar gráfico circular.")
        st.markdown('</div>', unsafe_allow_html=True)

    # 7. FILA INTERMEDIA: TARJETAS DE MÉTRICAS HORIZONTALES COMPACTAS
    col_m1, col_m2, col_m3 = st.columns(3)
    
    with col_m1:
        total_focos = len(df_filtrado)
        st.markdown(f"""
            <div class="analytics-card">
                <div class="metric-label">🚨 Volumen de Ocurrencia</div>
                <div class="metric-value">{total_focos:,}</div>
                <div class="metric-sub">Siniestros bajo investigación técnica</div>
            </div>
            """, unsafe_allow_html=True)
            
    with col_m2:
        total_sup = df_filtrado["Sup"].sum() if "Sup" in df_filtrado.columns else 0
        st.markdown(f"""
            <div class="analytics-card">
                <div class="metric-label">📐 Magnitud del Daño</div>
                <div class="metric-value">{total_sup:,.1f} <span style="font-size:16px;">Ha</span></div>
                <div class="metric-sub">Superficie afectada consolidada</div>
            </div>
            """, unsafe_allow_html=True)
            
    with col_m3:
        causa_top = df_filtrado["Causa General"].mode()[0] if "Causa General" in df_filtrado.columns and not df_filtrado.empty else "N/A"
        st.markdown(f"""
            <div class="analytics-card">
                <div class="metric-label">⚠️ Factor Crítico Principal</div>
                <div class="metric-value" style="font-size: 18px; padding-top: 4px;">{causa_top}</div>
                <div class="metric-sub">Mayor tendencia de origen registrada</div>
            </div>
            """, unsafe_allow_html=True)

    # 8. TABLA INFERIOR DETALLADA COMPACTA
    st.markdown('<div class="section-title">📋 Registros Históricos Filtrados — Detalle General</div>', unsafe_allow_html=True)
    st.markdown('<div class="analytics-card" style="margin-bottom:0;">', unsafe_allow_html=True)
    columnas_deseadas = ["ID", "Temporada", "Comuna", "Nombre incendio", "Causa General", "Grupo de causas", "Sup"]
    columnas_visibles = [c for c in columnas_deseadas if c in df_filtrado.columns]
    
    df_tabla_ordenada = df_filtrado[columnas_visibles].sort_values(by="Sup", ascending=False) if "Sup" in df_filtrado.columns else df_filtrado[columnas_visibles]
    st.dataframe(df_tabla_ordenada, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.warning("Verifica que el archivo se llame exactamente 'DATOS DUROS 2025-2026 WEB_2.xlsx' en tu repositorio.")
