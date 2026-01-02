@echo off
setlocal

REM Ir a la carpeta del proyecto (la misma donde está este .bat)
cd /d "%~dp0"

REM Ejecutar el pipeline con el python del venv
"%~dp0venv\Scripts\python.exe" "%~dp0run_pipeline.py" >> "%~dp0outputs\run_pipeline_task.txt" 2>&1

endlocal
