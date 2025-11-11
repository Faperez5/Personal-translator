@echo off
echo Starting Language Learning Platform Backend...
echo.

cd backend

if not exist "..\venv\" (
    echo Virtual environment not found. Creating one...
    python -m venv ..\venv
    echo.
)

echo Activating virtual environment...
call ..\venv\Scripts\activate

echo.
echo Installing/Updating dependencies...
pip install -r requirements.txt

echo.
echo Starting Flask server...
echo Backend will be available at http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

python run.py
