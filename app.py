import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="GEOPIF - Panel de Incendios", 
    layout="wide", 
    page_icon="🌲"
)

# 2. ESTILOS CSS CON COLORES INSTITUCIONALES (Verde CONAF, Fondo Gris, Detalles Amarillo Fuego)
st.markdown("""
    <style>
    /* Fondo general gris de la aplicación */
    .stApp {
        background-color: #ebedef;
    }
    /* Barra superior - Verde Oscuro Institucional CONAF */
    .header-bar {
        background-color: #1b5e20;
        padding: 16px 25px;
        border-radius: 4px;
        border-bottom: 4px solid #fbc02d; /* Línea de acento amarilla */
        margin-bottom: 25px;
    }
    .header-title {
        color: white !important;
        margin: 0 !important;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: bold;
        letter-spacing: 0.5px;
    }
    /* Tarjetas blancas institucionales para los gráficos y métricas */
    .analytics-card {
        background-color: white;
        padding: 20px;
        border-radius: 4px;
        border: 1px solid #dcdcdc;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .card-label {
        color: #2e7d32; /* Texto secundario verde */
        font-size: 13px;
        text-transform: uppercase;
        font-weight: bold;
        letter-spacing: 0.5px;
        margin-bottom: 15px;
        border-bottom: 1px solid #eeeeee;
        padding-bottom: 5px;
    }
    /* Estilos específicos para las tarjetas de métricas */
    .metric-value {
        color: #1b5e20;
        font-size: 34px;
        font-weight: bold;
    }
    .metric-sub {
        color: #555555;
        font-size: 12px;
        margin-top: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA DE TÍTULO INSTITUCIONAL
st.markdown('<div class="header-bar"><h2 class="header-title">🌲 GEOPIF — SISTEMA DE MONITOREO DE INCENDIOS FORESTALES</h2></div>', unsafe_allow_html=True)

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
    # 5. FILTROS EN LA BARRA LATERAL (Sidebar Institucional)
    st.sidebar.markdown("<h2 style='color:#1b5e20;'>🔍 Parámetros de Filtro</h2>", unsafe_allow_html=True)
    
    region_sel = st.sidebar.selectbox("Filtro por Región", ["Todas"] + sorted(list(df["Región"].dropna().unique()))) if "Región" in df.columns else "Todas"
    df_filtrado = df.copy()
    if region_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Región"] == region_sel]
        
    provincia_sel = st.sidebar.selectbox("Filtro por Provincia", ["Todas"] + sorted(list(df_filtrado["Provincia"].dropna().unique()))) if "Provincia" in df.columns else "Todas"
    if provincia_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Provincia"] == provincia_sel]
        
    comuna_sel = st.sidebar.selectbox("Filtro por Comuna", ["Todas"] + sorted(list(df_filtrado["Comuna"].dropna().unique()))) if "Comuna" in df.columns else "Todas"
    if comuna_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Comuna"] == comuna_sel]

    # 6. FILA SUPERIOR: GRÁFICOS PARALELOS (Distribución Punto 4 Lado a Lado)
    col_graf1, col_graf2 = st.columns([6, 4]) # 60% para barras y 40% para el circular

    with col_graf1:
        st.markdown('<div class="analytics-card" style="min-height: 400px;"><div class="card-label">📊 Frecuencia de Incendios por Causa General (Mayor a Menor)</div>', unsafe_allow_html=True)
        if "Causa General" in df_filtrado.columns and not df_filtrado.empty:
            df_causas_frecuencia = df_filtrado["Causa General"].value_counts().sort_values(ascending=False)
            st.bar_chart(df_causas_frecuencia, use_container_width=True)
        else:
            st.info("Sin datos para graficar causas.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_graf2:
        st.markdown('<div class="analytics-card" style="min-height: 400px;"><div class="card-label">🍕 Distribución Porcentual por Grupo de Causas</div>', unsafe_allow_html=True)
        if "Grupo de causas" in df_filtrado.columns and not df_filtrado.empty:
            df_grupo_counts = df_filtrado["Grupo de causas"].value_counts()
            
            # Gráfico de torta con colores que complementan la marca (verdes, amarillos y tierras)
            fig, ax = plt.subplots(figsize=(6, 4.2), facecolor='white')
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
        else:
            st.info("Sin registros para generar gráfico circular.")
        st.markdown('</div>', unsafe_allow_html=True)

    # 7. FILA INTERMEDIA: TARJETAS DE MÉTRICAS HORIZONTALES
    col_m1, col_m2, col_m3 = st.columns(3)
    
    with col_m1:
        total_focos = len(df_filtrado)
        st.markdown(f"""
            <div class="analytics-card">
                <div class="card-label">🚨 Volumen de Ocurrencia</div>
                <div class="metric-value">{total_focos:,}</div>
                <div class="metric-sub">Siniestros bajo investigación técnica</div>
            </div>
            """, unsafe_allow_html=True)
            
    with col_m2:
        total_sup = df_filtrado["Sup"].sum() if "Sup" in df_filtrado.columns else 0
        st.markdown(f"""
            <div class="analytics-card">
                <div class="card-label">📐 Magnitud del Daño</div>
                <div class="metric-value">{total_sup:,.1f} <span style="font-size:18px;">Ha</span></div>
                <div class="metric-sub">Superficie afectada consolidada</div>
            </div>
            """, unsafe_allow_html=True)
            
    with col_m3:
        causa_top = df_filtrado["Causa General"].mode()[0] if "Causa General" in df_filtrado.columns and not df_filtrado.empty else "N/A"
        st.markdown(f"""
            <div class="analytics-card">
                <div class="card-label">⚠️ Factor Crítico Principal</div>
                <div class="metric-value" style="font-size: 20px; padding-top: 8px; padding-bottom: 5px;">{causa_top}</div>
                <div class="metric-sub">Mayor tendencia de origen registrada</div>
            </div>
            """, unsafe_allow_html=True)

    # 8. TABLA INFERIOR DETALLADA
    st.markdown('<div class="analytics-card"><div class="card-label">📋 Registros Históricos Filtrados — Detalle General</div>', unsafe_allow_html=True)
    columnas_deseadas = ["ID", "Temporada", "Comuna", "Nombre incendio", "Causa General", "Grupo de causas", "Sup"]
    columnas_visibles = [c for c in columnas_deseadas if c in df_filtrado.columns]
    
    df_tabla_ordenada = df_filtrado[columnas_visibles].sort_values(by="Sup", ascending=False) if "Sup" in df_filtrado.columns else df_filtrado[columnas_visibles]
    st.dataframe(df_tabla_ordenada, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.warning("Verifica que el archivo se llame exactamente 'DATOS DUROS 2025-2026 WEB_2.xlsx' en tu repositorio.")
