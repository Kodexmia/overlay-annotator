@echo off
REM Quick fix for import errors in Overlay Annotator v2

echo Fixing import paths...

cd app

REM Create __init__.py if missing
if not exist "__init__.py" (
    echo # App package > __init__.py
    echo Created app/__init__.py
)

REM Fix main.py
powershell -Command "(Get-Content main.py) -replace 'from ui\.', 'from app.ui.' -replace 'from core\.', 'from app.core.' | Set-Content main.py"
echo Fixed app/main.py

REM Fix main_window.py
cd ui
powershell -Command "(Get-Content main_window.py) -replace 'from core\.', 'from app.core.' -replace 'from ui\.', 'from app.ui.' | Set-Content main_window.py"
echo Fixed app/ui/main_window.py

REM Fix annotation_toolbar.py
powershell -Command "(Get-Content annotation_toolbar.py) -replace 'from ui\.annotation_canvas', 'from app.ui.annotation_canvas' | Set-Content annotation_toolbar.py"
echo Fixed app/ui/annotation_toolbar.py

cd ..\core

REM Fix storage.py
powershell -Command "(Get-Content storage.py) -replace 'from core\.models', 'from app.core.models' | Set-Content storage.py"
echo Fixed app/core/storage.py

cd ..\..

REM Fix test_quick.py
powershell -Command "(Get-Content test_quick.py) -replace 'from ui\.', 'from app.ui.' -replace 'from core\.', 'from app.core.' | Set-Content test_quick.py"
echo Fixed test_quick.py

echo.
echo ================================
echo All imports fixed!
echo ================================
echo.
echo Now run: start.bat
pause
