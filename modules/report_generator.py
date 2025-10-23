# modules/report_generator.py
import pandas as pd
from datetime import datetime

class ReportGenerator:
    def generate_complete_report(self, results, data, app_selection):
        """Generar reporte básico"""
        report_content = f"""
        REPORTE PSICOSOCIAL - {datetime.now().strftime('%Y-%m-%d')}
        =============================================
        
        Resumen del Análisis:
        - Total colaboradores analizados: {len(data)}
        - Aplicaciones ejecutadas: {len(app_selection)}
        - Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        
        Resultados Principales:
        """
        
        for app_name in app_selection:
            report_content += f"\n- {app_name}: Completado"
        
        # Guardar reporte simple
        report_path = f"reporte_psicosocial_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return report_path