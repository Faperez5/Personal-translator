@echo off
echo Starting Language Learning Platform Frontend...
echo.

cd frontend

echo Frontend will be available at http://localhost:3000
echo.
echo Opening browser...
echo Press Ctrl+C to stop the server
echo.

start http://localhost:3000

python -m http.server 3000
