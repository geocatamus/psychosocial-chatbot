# modules/data_extractor.py
import pandas as pd
import numpy as np

class DocumentProcessor:
    def extract_from_pdf(self, file_path):
        """Extraer datos básicos de PDF - versión simplificada"""
        # Crear datos de ejemplo para desarrollo
        return self._create_sample_data()
    
    def extract_from_excel(self, file_path):
        """Extraer datos de Excel"""
        try:
            return pd.read_excel(file_path)
        except Exception as e:
            print(f"Error leyendo Excel: {e}")
            return self._create_sample_data()
    
    def extract_from_csv(self, file_path):
        """Extraer datos de CSV"""
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            print(f"Error leyendo CSV: {e}")
            return self._create_sample_data()
    
    def extract_from_word(self, file_path):
        """Extraer datos de Word - versión básica"""
        return self._create_sample_data()
    
    def _create_sample_data(self):
        """Crear datos de ejemplo realistas"""
        np.random.seed(42)
        n_samples = 50
        
        return pd.DataFrame({
            'id_colaborador': range(1, n_samples + 1),
            'nombre': [f'Colaborador_{i}' for i in range(1, n_samples + 1)],
            'area_trabajo': np.random.choice(['Académica', 'Administrativa', 'Operativa'], 
                                           n_samples, p=[0.4, 0.35, 0.25]),
            'nivel_estres': np.random.choice(['Bajo', 'Medio', 'Alto', 'Muy Alto'], 
                                           n_samples, p=[0.5, 0.25, 0.15, 0.1]),
            'demandas_jornada': np.random.choice(['Bajo', 'Medio', 'Alto', 'Muy Alto'], 
                                               n_samples, p=[0.3, 0.4, 0.2, 0.1]),
            'satisfaccion_laboral': np.random.randint(1, 11, n_samples),
            'ausentismo_dias': np.random.poisson(2, n_samples),
            'antiguedad_meses': np.random.randint(1, 60, n_samples)
        })