@echo off
echo Stopping any existing servers...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *uvicorn*" 2>nul
timeout /t 2 /nobreak >nul

echo Starting FastAPI server...
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

pause
