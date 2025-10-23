@echo off
echo ========================================
echo    CHATBOT PSICOSOCIAL - MODO ESCRITORIO
echo ========================================

echo Verificando Python...
python --version
if errorlevel 1 (
    echo ERROR: Python no encontrado
    echo Instala Python desde: https://python.org
    pause
    exit
)

echo Instalando dependencias...
pip install -r requirements.txt

echo Ejecutando aplicacion...
echo 🌐 La app se abrira en: http://localhost:8501
echo 💡 Manten esta ventana abierta mientras uses la app

streamlit run app.py

pause