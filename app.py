import streamlit as st
import pandas as pd

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Dashboard Incendios Forestales", 
    layout="wide", 
    page_icon="🔥"
)

# 2. ESTILOS CSS PARA IMITAR LA REFERENCIA DE GOOGLE ANALYTICS
st.markdown("""
    <style>
    /* Fondo general gris claro */
    .stApp {
        background-color: #f4f6f8;
    }
    /* Barra superior para el Título del Reporte */
    .header-bar {
        background-color: #37474f;
        padding: 18px 25px;
        border-radius: 4px;
        border-left: 6px solid #00bfa5;
        margin-bottom: 25px;
    }
    .header-title {
        color: white !important;
        margin: 0 !important;
        font-family: 'Roboto', sans-serif;
        font-weight: 400;
        letter-spacing: 0.5px;
    }
    /* Contenedores tipo tarjeta blanca con sombra sutil */
    .analytics-card {
        background-color: white;
        padding: 22px;
        border-radius: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
    }
    .card-label {
        color: #70757a;
        font-size: 13px;
        text-transform: uppercase;
        font-weight: bold;
        letter-spacing: 0.5px;
        margin-bottom: 10px;
    }
    .card-value {
        color: #202124;
        font-size: 38px;
        font-weight: 400;
        margin-bottom: 5px;
    }
    .card-subtext {
        font-size: 13px;
        font-weight: bold;
    }
    .text-green { color: #00bfa5; }
    .text-orange { color: #ff6d00; }
    </style>
    """, unsafe_allow_html=True)

# 3. BARRA DE TÍTULO PRINCIPAL
st.markdown('<div class="header-bar"><h2 class="header-title">TRAFFIC OVERVIEW — INCENDIOS FORESTALES</h2></div>', unsafe_allow_html=True)

# 4. CARGA DE DATOS SEGURO
@st.cache_data
def cargar_datos_seguro():
    try:
        # Volvemos a usar pandas normal sin requerir la librería pyproj de mapas
        return pd.read_excel("DATOS DUROS 2025-2026 WEB_2.xlsx", sheet_name="Invest. IF")
    except Exception as e:
        st.error(f"Error cargando el archivo: {e}")
        return pd.DataFrame()

df = cargar_datos_seguro()

if not df.empty:
    # 5. FILTROS EN LA BARRA LATERAL (Sidebar)
    st.sidebar.header("⚙️ Filtros del Reporte")
    
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
        
    grupo_sel = st.sidebar.selectbox("Grupo de Causa", ["Todos"] + sorted(list(df_filtrado["Grupo de causas"].dropna().unique()))) if "Grupo de causas" in df.columns else "Todos"
    if grupo_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Grupo de causas"] == grupo_sel]

    # 6. GRÁFICO CENTRAL DE ANÁLISIS (Ocupa todo el ancho superior como en tu referencia)
    st.markdown('<div class="analytics-card">'
                '<div class="card-label">📊 Hectáreas Afectadas por Causa General</div>', unsafe_allow_html=True)
    if "Causa General" in df_filtrado.columns and "Sup" in df_filtrado.columns and not df_filtrado.empty:
        df_causas_sup = df_filtrado.groupby("Causa General")["Sup"].sum().sort_values(ascending=False)
        st.bar_chart(df_causas_sup, use_container_width=True)
    else:
        st.info("Sin datos para graficar.")
    st.markdown('</div>', unsafe_allow_html=True)

    # 7. BLOQUE DE MÉTRICAS (Fila intermedia con tarjetas)
    col_met1, col_met2, col_met3 = st.columns(3)
    
    with col_met1:
        total_focos = len(df_filtrado)
        st.markdown(f"""
            <div class="analytics-card">
                <div class="card-label">Total Incendios</div>
                <div class="card-value">{total_focos:,}</div>
                <div class="card-subtext"><span class="text-green">★ Monitoreados</span> en la temporada</div>
            </div>
            """, unsafe_allow_html=True)
            
    with col_met2:
        total_sup = df_filtrado["Sup"].sum() if "Sup" in df_filtrado.columns else 0
        st.markdown(f"""
            <div class="analytics-card">
                <div class="card-label">Superficie Afectada</div>
                <div class="card-value">{total_sup:,.1f} <span style="font-size:20px;">Ha</span></div>
                <div class="card-subtext"><span class="text-orange">▲ Impacto</span> Rural/Forestal</div>
            </div>
            """, unsafe_allow_html=True)
            
    with col_met3:
        causa_top = df_filtrado["Causa General"].mode()[0] if "Causa General" in df_filtrado.columns and not df_filtrado.empty else "N/A"
        st.markdown(f"""
            <div class="analytics-card">
                <div class="card-label">Causa más Frecuente</div>
                <div class="card-value" style="font-size: 24px; padding-top: 15px; padding-bottom: 10px;">{causa_top}</div>
                <div class="card-subtext"><span class="text-orange">⚠️ Alerta</span> Incidencias</div>
            </div>
            """, unsafe_allow_html=True)

    # 8. TABLA INFERIOR DETALLADA
    st.markdown('<div class="analytics-card">'
                '<div class="card-label">📋 Resumen de Registros Filtrados</div>', unsafe_allow_html=True)
    columnas_deseadas = ["ID", "Temporada", "Comuna", "Nombre incendio", "Causa General", "Sup"]
    columnas_visibles = [c for c in columnas_deseadas if c in df_filtrado.columns]
    st.dataframe(df_filtrado[columnas_visibles], use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.warning("Verifica que el archivo se llame exactamente 'DATOS DUROS 2025-2026 WEB_2.xlsx' en tu repositorio.")
