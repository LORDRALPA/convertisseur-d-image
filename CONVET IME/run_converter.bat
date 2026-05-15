@echo off
setlocal

REM Lance le convertisseur GUI avec le Python du projet.
set "SCRIPT_DIR=%~dp0"
set "PYTHON_EXE=D:\DEV\.venv\Scripts\python.exe"

if not exist "%PYTHON_EXE%" (
    echo Python introuvable dans l'environnement virtuel: %PYTHON_EXE%
    pause
    exit /b 1
)

REM Lance l'interface GUI
"%PYTHON_EXE%" "%SCRIPT_DIR%converter_gui.py"
exit /b 0