@echo off
REM Quick patch for Windows temp file paths

echo Patching capture_overlay.py for Windows compatibility...

cd app\ui

REM Backup original
copy capture_overlay.py capture_overlay.py.backup > nul 2>&1

REM Add tempfile import
powershell -Command "$content = Get-Content capture_overlay.py; $content = $content -replace 'from typing import Callable, Optional', 'from typing import Callable, Optional`nimport tempfile`nimport os'; $content | Set-Content capture_overlay.py"

REM Fix /tmp/ paths to use tempfile
powershell -Command "$content = Get-Content capture_overlay.py -Raw; $content = $content -replace \"img\.save\('/tmp/screenshot_temp\.png'\)\s+self\.screenshot = QPixmap\('/tmp/screenshot_temp\.png'\)\", \"temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)`n            temp_path = temp_file.name`n            temp_file.close()`n            `n            img.save(temp_path)`n            self.screenshot = QPixmap(temp_path)`n            `n            # Clean up temp file`n            try:`n                os.unlink(temp_path)`n            except:`n                pass\"; $content | Set-Content capture_overlay.py"

powershell -Command "$content = Get-Content capture_overlay.py -Raw; $content = $content -replace \"cropped\.save\('/tmp/cropped_temp\.png'\)\s+pil_img = Image\.open\('/tmp/cropped_temp\.png'\)\", \"temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)`n                    temp_path = temp_file.name`n                    temp_file.close()`n                    `n                    cropped.save(temp_path)`n                    pil_img = Image.open(temp_path)`n                    `n                    # Clean up temp file`n                    try:`n                        os.unlink(temp_path)`n                    except:`n                        pass\"; $content | Set-Content capture_overlay.py"

cd ..\..

echo.
echo ================================
echo Patch applied successfully!
echo ================================
echo.
echo Backup saved as: app\ui\capture_overlay.py.backup
echo.
echo Now run: start.bat
pause
