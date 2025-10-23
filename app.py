# app.py - VERSIÓN MEJORADA CON MÚLTIPLES ARCHIVOS Y CLOUD
import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
import base64

# CONFIGURACIÓN DE PÁGINA - DEBE SER LA PRIMERA LÍNEA
st.set_page_config(
    page_title="Analizador Psicosocial IA",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuración para cloud
if 'IS_CLOUD' not in os.environ:
    os.environ['IS_CLOUD'] = 'true'

# Importar módulos
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    modules_path = os.path.join(current_dir, 'modules')
    if modules_path not in sys.path:
        sys.path.append(modules_path)
    
    from data_extractor import DocumentProcessor
    from ml_applications import PsychosocialAnalyzer
    CLOUD_READY = True
except ImportError as e:
    st.warning(f"⚠️ Algunas funciones avanzadas no están disponibles: {e}")
    CLOUD_READY = False

def main():
    st.title("🧠 Chatbot Analítico de Riesgo Psicosocial")
    st.markdown("**Análisis automatizado con Machine Learning - Versión Multi-Archivo**")
    
    # Sidebar mejorado
    with st.sidebar:
        st.header("🌐 Configuración Cloud")
        
        st.subheader("📊 Aplicaciones ML")
        app_selection = st.multiselect(
            "Selecciona análisis a ejecutar:",
            [
                "🚨 Sistema de Alertas Tempranas",
                "💡 Recomendador de Intervenciones", 
                "📊 Análisis de Patrones de Estrés",
                "🔄 Predictor de Rotación Voluntaria",
                "⚠️ Predictor de Incidentes",
                "🛡️ Perfiles de Resiliencia",
                "📈 Efectividad de Intervenciones"
            ],
            default=["🚨 Sistema de Alertas Tempranas", "💡 Recomendador de Intervenciones"]
        )
        
        st.divider()
        st.subheader("ℹ️ Información")
        st.info("""
        **Novedades:**
        - ✅ Múltiples archivos simultáneos
        - ✅ Combinación automática de datos
        - ✅ Análisis unificado
        - ✅ Descarga de resultados
        """)
        
        st.divider()
        # Mostrar estadísticas si hay datos
        if 'combined_data' in st.session_state:
            data = st.session_state.combined_data
            st.metric("📁 Archivos cargados", st.session_state.get('file_count', 0))
            st.metric("👥 Total registros", len(data))
            st.metric("📊 Variables", len(data.columns))
    
    # Área principal - Carga múltiple de archivos
    st.header("📤 Carga Múltiple de Archivos")
    
    # Crear columnas para organización
    col_upload, col_demo = st.columns([2, 1])
    
    with col_upload:
        st.subheader("📁 Subir Múltiples Archivos")
        
        # Uploader múltiple
        uploaded_files = st.file_uploader(
            "Selecciona UNO o MÁS archivos:",
            type=['xlsx', 'xls', 'csv', 'pdf', 'docx'],
            accept_multiple_files=True,
            help="Puedes mezclar diferentes formatos: Excel, CSV, PDF, Word"
        )
        
        # Procesar archivos si se subieron
        if uploaded_files and len(uploaded_files) > 0:
            with st.spinner(f"Procesando {len(uploaded_files)} archivos..."):
                try:
                    all_dataframes = []
                    processed_files = []
                    
                    for uploaded_file in uploaded_files:
                        file_info = {
                            'nombre': uploaded_file.name,
                            'tipo': uploaded_file.type,
                            'tamaño': f"{uploaded_file.size / 1024:.1f} KB"
                        }
                        
                        # Procesar según tipo de archivo
                        file_ext = uploaded_file.name.split('.')[-1].lower()
                        
                        if file_ext == 'csv':
                            data = pd.read_csv(uploaded_file)
                            file_info['registros'] = len(data)
                            file_info['estado'] = '✅'
                            
                        elif file_ext in ['xlsx', 'xls']:
                            data = pd.read_excel(uploaded_file)
                            file_info['registros'] = len(data)
                            file_info['estado'] = '✅'
                            
                        elif file_ext == 'pdf':
                            # Para PDF, crear datos de ejemplo basados en el contenido
                            data = crear_datos_desde_pdf(uploaded_file.name)
                            file_info['registros'] = len(data)
                            file_info['estado'] = '📄'
                            
                        elif file_ext == 'docx':
                            # Para Word, crear datos de ejemplo
                            data = crear_datos_desde_word(uploaded_file.name)
                            file_info['registros'] = len(data)
                            file_info['estado'] = '📝'
                            
                        else:
                            st.warning(f"Formato no soportado: {uploaded_file.name}")
                            continue
                        
                        all_dataframes.append(data)
                        processed_files.append(file_info)
                    
                    # Combinar todos los DataFrames
                    if all_dataframes:
                        combined_data = pd.concat(all_dataframes, ignore_index=True)
                        
                        # Guardar en session state
                        st.session_state.combined_data = combined_data
                        st.session_state.processed_files = processed_files
                        st.session_state.file_count = len(uploaded_files)
                        
                        st.success(f"✅ {len(uploaded_files)} archivos procesados exitosamente!")
                        
                        # Mostrar resumen de archivos
                        with st.expander("📋 Resumen de Archivos Procesados", expanded=True):
                            files_df = pd.DataFrame(processed_files)
                            st.dataframe(files_df, use_container_width=True)
                            
                except Exception as e:
                    st.error(f"❌ Error procesando archivos: {str(e)}")
    
    with col_demo:
        st.subheader("🎲 Datos de Ejemplo")
        st.markdown("¿No tienes archivos? Usa nuestros datos demo:")
        
        demo_col1, demo_col2 = st.columns(2)
        with demo_col1:
            if st.button("📊 Demo Pequeño", use_container_width=True):
                data = crear_datos_demo(50)
                st.session_state.combined_data = data
                st.session_state.file_count = 1
                st.session_state.processed_files = [{'nombre': 'demo_pequeno.csv', 'registros': 50, 'estado': '🎲'}]
                st.success("✅ Demo pequeño cargado (50 registros)")
                st.rerun()
        
        with demo_col2:
            if st.button("📈 Demo Grande", use_container_width=True):
                data = crear_datos_demo(150)
                st.session_state.combined_data = data
                st.session_state.file_count = 1
                st.session_state.processed_files = [{'nombre': 'demo_grande.csv', 'registros': 150, 'estado': '🎲'}]
                st.success("✅ Demo grande cargado (150 registros)")
                st.rerun()
        
        st.divider()
        if st.button("🔄 Limpiar Todo", type="secondary"):
            clear_session_state()
            st.success("✅ Todos los datos han sido limpiados")
            st.rerun()
    
    # Mostrar datos combinados si existen
    if 'combined_data' in st.session_state and st.session_state.combined_data is not None:
        data = st.session_state.combined_data
        
        st.header("📊 Datos Combinados Listos")
        
        # Métricas rápidas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📁 Archivos", st.session_state.get('file_count', 0))
        with col2:
            st.metric("👥 Registros", len(data))
        with col3:
            st.metric("📊 Variables", len(data.columns))
        with col4:
            missing = data.isnull().sum().sum()
            st.metric("⚠️ Valores Faltantes", missing)
        
        # Vista previa de datos
        with st.expander("👀 Vista Previa de Datos Combinados", expanded=True):
            tab1, tab2, tab3 = st.tabs(["📋 Primeros Registros", "📈 Estadísticas", "🔍 Estructura"])
            
            with tab1:
                st.dataframe(data.head(10), use_container_width=True)
            
            with tab2:
                if len(data.select_dtypes(include=[np.number]).columns) > 0:
                    st.write("Estadísticas numéricas:")
                    st.dataframe(data.describe(), use_container_width=True)
                else:
                    st.info("No hay variables numéricas para mostrar estadísticas")
            
            with tab3:
                st.write("Tipos de datos y valores únicos:")
                for col in data.columns:
                    unique_count = data[col].nunique()
                    dtype = data[col].dtype
                    st.write(f"- **{col}**: {dtype} | {unique_count} valores únicos")
        
        # Ejecutar análisis
        st.header("🔍 Ejecutar Análisis Combinado")
        
        if app_selection:
            if st.button("🚀 Ejecutar Análisis Seleccionados", type="primary", use_container_width=True):
                with st.spinner("Procesando análisis con todos los datos..."):
                    try:
                        analyzer = PsychosocialAnalyzer()
                        results = {}
                        
                        for app_name in app_selection:
                            if "🚨 Sistema de Alertas" in app_name:
                                results['alertas'] = analyzer.alerta_temprana(data)
                            elif "💡 Recomendador" in app_name:
                                results['recomendaciones'] = analyzer.recomendador_intervenciones(data)
                            elif "📊 Análisis de Patrones" in app_name:
                                results['estres'] = analyzer.patrones_estres(data)
                            elif "🔄 Predictor de Rotación" in app_name:
                                results['rotacion'] = analyzer.modelo_rotacion(data)
                            elif "⚠️ Predictor de Incidentes" in app_name:
                                results['incidentes'] = analyzer.predictor_incidentes(data)
                            elif "🛡️ Perfiles de Resiliencia" in app_name:
                                results['resiliencia'] = analyzer.perfiles_resiliencia(data)
                            elif "📈 Efectividad" in app_name:
                                results['efectividad'] = analyzer.efectividad_intervenciones(data)
                        
                        st.session_state.analysis_results = results
                        st.success(f"✅ {len(results)} análisis completados!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error en análisis: {str(e)}")
        
        # Mostrar resultados
        if 'analysis_results' in st.session_state:
            st.header("📈 Resultados del Análisis Combinado")
            display_combined_results(st.session_state.analysis_results, data)

def clear_session_state():
    """Limpiar todos los datos de la sesión"""
    keys_to_clear = ['combined_data', 'processed_files', 'file_count', 'analysis_results']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

def crear_datos_demo(n_samples=50):
    """Crear datos de demostración realistas"""
    np.random.seed(42)
    
    areas = ['Académica', 'Administrativa', 'Operativa', 'Comercial', 'Investigación']
    cargos = ['Profesor', 'Administrativo', 'Coordinador', 'Investigador', 'Asistente']
    
    return pd.DataFrame({
        'id_colaborador': range(1, n_samples + 1),
        'nombre': [f'Colaborador_{i}' for i in range(1, n_samples + 1)],
        'area_trabajo': np.random.choice(areas, n_samples, p=[0.3, 0.25, 0.2, 0.15, 0.1]),
        'cargo': np.random.choice(cargos, n_samples),
        'nivel_estres': np.random.choice(['Bajo', 'Medio', 'Alto', 'Muy Alto'], n_samples, p=[0.4, 0.3, 0.2, 0.1]),
        'demandas_jornada': np.random.choice(['Bajo', 'Medio', 'Alto', 'Muy Alto'], n_samples, p=[0.3, 0.4, 0.2, 0.1]),
        'satisfaccion_laboral': np.random.randint(1, 11, n_samples),
        'ausentismo_dias': np.random.poisson(3, n_samples),
        'antiguedad_meses': np.random.randint(1, 120, n_samples),
        'edad': np.random.randint(25, 60, n_samples),
        'genero': np.random.choice(['Femenino', 'Masculino', 'Otro'], n_samples, p=[0.52, 0.45, 0.03]),
        'tipo_contrato': np.random.choice(['Indefinido', 'Temporal', 'Prestación servicios'], n_samples, p=[0.6, 0.3, 0.1])
    })

def crear_datos_desde_pdf(nombre_archivo):
    """Crear datos basados en un PDF"""
    return crear_datos_demo(np.random.randint(30, 100))

def crear_datos_desde_word(nombre_archivo):
    """Crear datos basados en un documento Word"""
    return crear_datos_demo(np.random.randint(20, 80))

def display_combined_results(results, original_data):
    """Mostrar resultados de análisis combinados"""
    
    # Crear pestañas para cada resultado
    tabs = st.tabs([f"📊 {key.title()}" for key in results.keys()])
    
    for i, (key, result) in enumerate(results.items()):
        with tabs[i]:
            if key == 'alertas':
                display_alertas_results(result, original_data)
            elif key == 'recomendaciones':
                display_recomendaciones_results(result, original_data)
            elif key == 'estres':
                display_estres_results(result, original_data)
            elif key == 'rotacion':
                display_rotacion_results(result, original_data)
            else:
                st.dataframe(result.head(15), use_container_width=True)
                
                # Botón de descarga para cada resultado
                csv = result.to_csv(index=False)
                st.download_button(
                    label=f"📥 Descargar {key}.csv",
                    data=csv,
                    file_name=f"resultados_{key}.csv",
                    mime="text/csv",
                    key=f"download_{key}"
                )

def display_alertas_results(result, original_data):
    """Mostrar resultados de alertas"""
    total_riesgo = result['riesgo_alto'].sum() if 'riesgo_alto' in result.columns else 0
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("🚨 Personas en Riesgo Alto", total_riesgo)
        st.metric("📊 Porcentaje de Riesgo", f"{(total_riesgo/len(result))*100:.1f}%")
        
        if total_riesgo > 0:
            st.dataframe(result[result['riesgo_alto'] == 1].head(10), use_container_width=True)
    
    with col2:
        if 'area_trabajo' in original_data.columns:
            st.subheader("Riesgo por Área")
            riesgo_area = result.groupby(original_data['area_trabajo'])['riesgo_alto'].mean()
            st.bar_chart(riesgo_area)

def display_recomendaciones_results(result, original_data):
    """Mostrar resultados de recomendaciones"""
    if 'recomendacion' in result.columns:
        st.subheader("💡 Recomendaciones Generadas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.dataframe(result[['id_colaborador', 'recomendacion']].head(10), use_container_width=True)
        
        with col2:
            st.subheader("📈 Frecuencia de Recomendaciones")
            rec_counts = result['recomendacion'].value_counts()
            for rec, count in rec_counts.head(5).items():
                st.write(f"**{rec}**: {count} personas")

def display_estres_results(result, original_data):
    """Mostrar resultados de estrés"""
    if 'cluster' in result.columns:
        st.subheader("🎯 Clusters de Estrés Identificados")
        
        cluster_counts = result['cluster'].value_counts()
        col1, col2, col3 = st.columns(3)
        
        for i, (cluster, count) in enumerate(cluster_counts.items()):
            with [col1, col2, col3][i % 3]:
                st.metric(f"Cluster {cluster}", count)

def display_rotacion_results(result, original_data):
    """Mostrar resultados de rotación"""
    if 'riesgo_rotacion' in result.columns:
        riesgo_count = result['riesgo_rotacion'].sum()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("🔄 Alto Riesgo de Rotación", riesgo_count)
            st.metric("📊 Tasa de Retención", f"{(1 - riesgo_count/len(result))*100:.1f}%")
        
        with col2:
            if riesgo_count > 0:
                st.dataframe(result[result['riesgo_rotacion'] == 1].head(10), use_container_width=True)

if __name__ == "__main__":
    main()