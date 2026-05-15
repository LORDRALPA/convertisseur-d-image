@echo off
REM ============================================
REM Convertisseur d'Images - Lanceur de contrôle
REM ============================================

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "PYTHON_EXE=D:\DEV\.venv\Scripts\python.exe"
set "REQUIREMENTS=!SCRIPT_DIR!requirements.txt"

REM Vérifier si Python est accessible
if not exist "!PYTHON_EXE!" (
    echo [ERREUR] Python introuvable: !PYTHON_EXE!
    echo.
    echo Veuillez vous assurer que l'environnement virtuel est configuré.
    pause
    exit /b 1
)

REM Vérifier et installer les dépendances si nécessaire
echo [INFO] Vérification des dépendances...
"!PYTHON_EXE!" -m pip show PyQt5 >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installation des dépendances...
    "!PYTHON_EXE!" -m pip install -r "!REQUIREMENTS!" >nul 2>&1
    if errorlevel 1 (
        echo [ERREUR] Impossible d'installer les dépendances
        pause
        exit /b 1
    )
)

echo [INFO] Lancement du Convertisseur d'Images...
echo.

REM Lancer l'application GUI
"!PYTHON_EXE!" "!SCRIPT_DIR!converter_gui.py"

if errorlevel 1 (
    echo [ERREUR] L'application s'est fermée avec une erreur
    pause
    exit /b 1
)

exit /b 0