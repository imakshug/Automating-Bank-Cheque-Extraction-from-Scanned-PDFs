@echo off
cd /d "%~dp0"
call .\venv_new\Scripts\Activate.ps1
echo Starting Flask Web Server...
echo.
echo Dashboard will be available at: http://localhost:5000
echo.
python flask_app.py
pause
