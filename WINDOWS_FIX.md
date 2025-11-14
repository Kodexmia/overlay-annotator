# Quick Fix for Windows Temp Path Error

## The Problem
The app tries to use `/tmp/` which doesn't exist on Windows.

## Easy Fix: Edit One File

Open: `app/ui/capture_overlay.py`

### Step 1: Add imports (at top, around line 10)
Add these two lines after the other imports:
```python
import tempfile
import os
```

### Step 2: Find and replace line 51
Replace:
```python
            img.save('/tmp/screenshot_temp.png')
            self.screenshot = QPixmap('/tmp/screenshot_temp.png')
```

With:
```python
            temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            temp_path = temp_file.name
            temp_file.close()
            
            img.save(temp_path)
            self.screenshot = QPixmap(temp_path)
            
            try:
                os.unlink(temp_path)
            except:
                pass
```

### Step 3: Find and replace around line 74
Replace:
```python
                    cropped.save('/tmp/cropped_temp.png')
                    pil_img = Image.open('/tmp/cropped_temp.png')
```

With:
```python
                    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                    temp_path = temp_file.name
                    temp_file.close()
                    
                    cropped.save(temp_path)
                    pil_img = Image.open(temp_path)
                    
                    try:
                        os.unlink(temp_path)
                    except:
                        pass
```

### Step 4: Save and run
Save the file and run `start.bat` again.

## Or Just Download Fixed Version
[Download overlay_annotator_v2.zip](https://claude.ai) (already fixed)
