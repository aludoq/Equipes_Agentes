@echo off
TITLE Painel Varejo Insight - Squad Insight
echo ==========================================
echo   INICIANDO DASHBOARD VAREJO INSIGHT
echo ==========================================
echo Ativando ambiente virtual...
if not exist .venv (
    echo [ERRO] Ambiente .venv nao encontrado!
    pause
    exit
)
echo Abrindo navegador...
.venv\Scripts\python.exe -m streamlit run squads\varejo-insight\app_python\main.py
pause
