@echo off
cd /d "%~dp0"
call .\venv_new\Scripts\Activate.ps1
python main.py
pause
