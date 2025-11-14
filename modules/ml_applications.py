# modules/ml_applications.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
import streamlit as st

class PsychosocialAnalyzer:
    def __init__(self):
        self.le = LabelEncoder()
    
    def alerta_temprana(self, data):
        """App 1: Sistema de alerta temprana de comportamientos de riesgo"""
        df = data.copy()
        
        # Crear variable objetivo simulada
        if 'nivel_estres' in df.columns:
            df['riesgo_alto'] = np.where(
                df['nivel_estres'].str.contains('Alto|Muy Alto', na=False), 1, 0
            )
        else:
            df['riesgo_alto'] = np.random.choice([0, 1], len(df), p=[0.7, 0.3])
        
        return df
    
    def recomendador_intervenciones(self, data):
        """App 5: Recomendador de intervenciones personalizadas"""
        df = data.copy()
        
        def generar_recomendacion(fila):
            recomendaciones = []
            
            # Basado en nivel de estrés
            if fila.get('nivel_estres', '') in ['Alto', 'Muy Alto']:
                recomendaciones.append('Capacitación manejo de estrés')
            
            # Basado en demandas de trabajo
            if fila.get('demandas_jornada', '') in ['Alto', 'Muy Alto']:
                recomendaciones.append('Revisión carga laboral')
            
            # Basado en satisfacción
            if fila.get('satisfaccion_laboral', 5) < 5:
                recomendaciones.append('Programa de reconocimiento')
            
            return ', '.join(recomendaciones) if recomendaciones else 'Monitoreo periódico'
        
        if len(df) > 0:
            df['recomendacion'] = df.apply(generar_recomendacion, axis=1)
        
        return df
    
    def patrones_estres(self, data):
        """App 3: Detección de patrones de estrés por clustering"""
        df = data.copy()
        
        try:
            # Preparar datos para clustering
            features_for_cluster = []
            
            if 'nivel_estres' in df.columns:
                df['estres_encoded'] = self.le.fit_transform(df['nivel_estres'].astype(str))
                features_for_cluster.append('estres_encoded')
            
            if 'demandas_jornada' in df.columns:
                df['demandas_encoded'] = self.le.fit_transform(df['demandas_jornada'].astype(str))
                features_for_cluster.append('demandas_encoded')
            
            if len(features_for_cluster) >= 2:
                # Aplicar K-Means
                kmeans = KMeans(n_clusters=3, random_state=42)
                cluster_data = df[features_for_cluster].fillna(0)
                df['cluster'] = kmeans.fit_predict(cluster_data)
            else:
                df['cluster'] = 0
                
        except Exception as e:
            st.warning(f"Clustering no disponible: {e}")
            df['cluster'] = 0
        
        return df
    
    def modelo_rotacion(self, data):
        """App 2: Modelo de rotación voluntaria"""
        df = data.copy()
        
        # Simular riesgo de rotación
        if 'satisfaccion_laboral' in df.columns:
            df['riesgo_rotacion'] = np.where(df['satisfaccion_laboral'] < 5, 1, 0)
        else:
            df['riesgo_rotacion'] = np.random.choice([0, 1], len(df), p=[0.8, 0.2])
        
        df['probabilidad_rotacion'] = np.random.uniform(0, 1, len(df))
        
        return df
    
    def predictor_incidentes(self, data):
        """App 4: Predictor de incidentes"""
        df = data.copy()
        
        # Simular predictor de incidentes
        if 'nivel_estres' in df.columns:
            df['riesgo_incidentes'] = np.where(
                df['nivel_estres'].str.contains('Alto|Muy Alto', na=False), 1, 0
            )
        else:
            df['riesgo_incidentes'] = np.random.choice([0, 1], len(df), p=[0.85, 0.15])
        
        return df
    
    def perfiles_resiliencia(self, data):
        """App 6: Perfiles de resiliencia"""
        df = data.copy()
        
        # Calcular score de resiliencia simple
        df['score_resiliencia'] = np.random.randint(1, 10, len(df))
        df['perfil_resiliencia'] = pd.cut(df['score_resiliencia'], 
                                        bins=3, 
                                        labels=['Baja', 'Media', 'Alta'])
        
        return df
    
    def efectividad_intervenciones(self, data):
        """App 7: Efectividad de intervenciones"""
        df = data.copy()
        
        # Simular datos históricos y efectividad
        df['mejora_esperada'] = np.random.uniform(0.1, 0.8, len(df))
        df['intervencion_recomendada'] = np.random.choice(
            ['Capacitación', 'Rediseño puesto', 'Apoyo psicológico', 'Flexibilidad horaria'], 
            len(df)
        )
        
        return df

    # =============================================
    # NUEVAS FUNCIONES CON SISTEMA DE COLORES
    # =============================================

    def detector_enfermedades_colores(self, data):
        """
        Versión simple con sistema de colores para enfermedades laborales
        """
        df = data.copy()
        
        # Sistema simple de scoring
        score = 0
        
        # Factor 1: Estrés alto
        if 'nivel_estres' in df.columns:
            df['punto_estres'] = df['nivel_estres'].isin(['Alto', 'Muy Alto']).astype(int)
            score += df['punto_estres']
        
        # Factor 2: Demandas excesivas
        if 'demandas_jornada' in df.columns:
            df['punto_demandas'] = df['demandas_jornada'].isin(['Alto', 'Muy Alto']).astype(int)
            score += df['punto_demandas']
        
        # Factor 3: Baja satisfacción
        if 'satisfaccion_laboral' in df.columns:
            df['punto_satisfaccion'] = (df['satisfaccion_laboral'] < 5).astype(int)
            score += df['punto_satisfaccion']
        
        # Factor 4: Alto ausentismo
        if 'ausentismo_dias' in df.columns:
            df['punto_ausentismo'] = (df['ausentismo_dias'] > 5).astype(int)
            score += df['punto_ausentismo']
        
        # Asignar niveles de riesgo con colores
        df['riesgo_enfermedad'] = pd.cut(score, 
                                       bins=[-1, 1, 2, 4], 
                                       labels=['🟢 Bajo', '🟡 Medio', '🔴 Alto'])
        
        # Detección específica
        df['alerta_depresion'] = np.where(score >= 2, '🔴 Alta', '🟢 Baja')
        df['alerta_ansiedad'] = np.where(score >= 2, '🔴 Alta', '🟢 Baja')
        
        return df

    def predictor_rotacion_colores(self, data):
        """
        Versión simple con sistema de colores para rotación
        """
        df = data.copy()
        
        score = 0
        
        # Factor 1: Baja satisfacción
        if 'satisfaccion_laboral' in df.columns:
            df['punto_rot_satisfaccion'] = (df['satisfaccion_laboral'] < 4).astype(int)
            score += df['punto_rot_satisfaccion']
        
        # Factor 2: Estrés alto
        if 'nivel_estres' in df.columns:
            df['punto_rot_estres'] = df['nivel_estres'].isin(['Alto', 'Muy Alto']).astype(int)
            score += df['punto_rot_estres']
        
        # Factor 3: Poca antigüedad
        if 'antiguedad_meses' in df.columns:
            df['punto_rot_antiguedad'] = (df['antiguedad_meses'] < 12).astype(int)
            score += df['punto_rot_antiguedad']
        
        # Sistema de colores para rotación
        df['riesgo_rotacion'] = pd.cut(score,
                                     bins=[-1, 0, 1, 3],
                                     labels=['🟢 Bajo', '🟡 Medio', '🔴 Alto'])
        
        return df
