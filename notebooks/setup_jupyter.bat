@echo off
REM Setup script for Jupyter notebook analysis (Windows)

echo ==========================================
echo Jupyter Notebook Setup
echo ==========================================

REM Install required packages
echo.
echo Installing required packages...
pip install rdflib pandas matplotlib networkx pyvis plotly openpyxl jupyter

if %ERRORLEVEL% EQU 0 (
    echo [OK] Packages installed successfully
) else (
    echo [ERROR] Installation failed
    exit /b 1
)

REM Start Jupyter
echo.
echo ==========================================
echo Starting Jupyter Notebook...
echo ==========================================
echo.
echo Instructions:
echo 1. Create a new notebook in the notebooks/ directory
echo 2. Copy cells from ontology_visualization.py
echo 3. Run cells sequentially
echo.
echo Press Ctrl+C to stop Jupyter when done
echo.

jupyter notebook
