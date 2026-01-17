@echo off
echo Waiting for Flask to reload...
timeout /t 5 /nobreak >nul
echo.
python check_backend.py
