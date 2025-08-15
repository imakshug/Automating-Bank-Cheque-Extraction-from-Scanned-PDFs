@echo off
cd /d "%~dp0"
call .\venv_new\Scripts\Activate.ps1
streamlit run streamlit_app.py --server.port 8501
pause
