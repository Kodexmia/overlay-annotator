# Crash Recovery & Troubleshooting Guide

## 🐛 Issue: Python Stopped Working / Application Crash

### Symptoms You're Seeing:
- "Python has stopped working" dialog
- "Not Responding" in title bar
- Corrupted/garbled image display (colorful noise)
- Application freezes

### Root Causes:

1. **Memory Issue** - Large screen resolution causing memory problems
2. **Image Conversion Bug** - PIL to QPixmap conversion failing
3. **Graphics Driver Issue** - Qt struggling with hardware acceleration

---

## 🔧 Quick Fixes (Try These First)

### Fix 1: Reduce Screen Resolution
**Temporary workaround:**
1. Lower your screen resolution
2. Try capturing smaller regions
3. Restart the application

### Fix 2: Download Patched Version
I've created fixes for the image handling issues.

**Download the fixed version:**
[Download patched overlay_annotator_v2.zip](computer:///mnt/user-data/outputs/overlay_annotator_v2.zip)

**What was fixed:**
- ✅ Added error handling for image capture
- ✅ Image validation before display
- ✅ Better PIL → Qt conversion
- ✅ Memory safety checks
- ✅ Detailed error logging

### Fix 3: Manual Patch (If You Don't Want to Re-download)

**Edit `app/ui/capture_overlay.py`:**

Find line 45 and replace the `capture_screen` method with:

```python
def capture_screen(self):
    """Capture full screen using mss"""
    try:
        with mss() as sct:
            monitor = sct.monitors[1]  # Primary monitor
            screenshot = sct.grab(monitor)
            
            # Convert to PIL Image
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
            
            # Validate image
            if img.width == 0 or img.height == 0:
                print("Error: Invalid image dimensions")
                return
            
            print(f"Captured: {img.width}x{img.height}")
            
            # Convert PIL to QPixmap via temporary file
            temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            temp_path = temp_file.name
            temp_file.close()
            
            # Save with explicit PNG format
            img.save(temp_path, 'PNG')
            
            # Load QPixmap
            self.screenshot = QPixmap(temp_path)
            
            # Validate QPixmap loaded successfully
            if self.screenshot.isNull():
                print("Error: Failed to load QPixmap")
                return
            
            print(f"QPixmap loaded: {self.screenshot.width()}x{self.screenshot.height()}")
            
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except Exception as e:
                print(f"Warning: Could not delete temp file: {e}")
                
    except Exception as e:
        print(f"Error capturing screen: {e}")
        import traceback
        traceback.print_exc()
```

**Edit `app/ui/annotation_canvas.py`:**

Find line 54 and replace the `load_pil` method with:

```python
def load_pil(self, pil_img: Image.Image):
    """Load PIL image into canvas"""
    try:
        if pil_img is None:
            print("Error: Cannot load None image")
            return
        
        # Validate image
        if pil_img.width == 0 or pil_img.height == 0:
            print("Error: Invalid image dimensions")
            return
        
        print(f"Loading image: {pil_img.width}x{pil_img.height}, mode: {pil_img.mode}")
        
        # Ensure RGB mode
        if pil_img.mode != 'RGB':
            print(f"Converting from {pil_img.mode} to RGB")
            pil_img = pil_img.convert('RGB')
        
        self.pil_image = pil_img.copy()
        self.annotations.clear()
        self.current_annotation = None
        
        # Convert PIL to QImage for display
        try:
            image_qt = ImageQt.ImageQt(self.pil_image)
            self.q_image = QImage(image_qt)
            
            # Validate QImage
            if self.q_image.isNull():
                print("Error: QImage is null after conversion")
                return
                
            print(f"QImage created: {self.q_image.width()}x{self.q_image.height()}")
            
        except Exception as e:
            print(f"Error converting to QImage: {e}")
            import traceback
            traceback.print_exc()
            return
        
        self.update()
        
    except Exception as e:
        print(f"Error loading PIL image: {e}")
        import traceback
        traceback.print_exc()
```

---

## 🔍 Debugging: What to Check

### Check Terminal Output
When you run the app, watch for these messages:

**Good output:**
```
Captured: 1920x1080
QPixmap loaded: 1920x1080
Loading image: 1920x1080, mode: RGB
QImage created: 1920x1080
```

**Bad output (indicates problem):**
```
Error: Invalid image dimensions
Error: Failed to load QPixmap
Error capturing screen: [error message]
```

### Check Your Screen Resolution
```bash
# Windows
wmic path Win32_VideoController get CurrentHorizontalResolution,CurrentVerticalResolution

# The app might struggle with:
# - 4K displays (3840x2160)
# - Ultra-wide monitors (3440x1440)
# - Multi-monitor setups with high total resolution
```

---

## 🛡️ Prevention Tips

### 1. Start Small
- Create session first
- Capture small regions initially
- Test with 800x600 region before full screen

### 2. Monitor Memory
- Close other applications
- Watch Task Manager during capture
- If Python.exe uses >500MB, restart app

### 3. Use Manual Capture First
- Click "📷 Capture" button instead of Ctrl+Alt+S
- This gives you more control
- Easier to troubleshoot

---

## 🔄 Recovery Steps If Crashed

### Step 1: Close Everything
```bash
# Kill any stuck Python processes
# Windows: Task Manager → End Process for Python.exe
# Or close terminal window
```

### Step 2: Clean Temp Files
```bash
# Windows
del %TEMP%\tmp*.png

# Check your session folder for partial files
# Delete any 0-byte images
```

### Step 3: Restart with Debugging
```bash
# Run with verbose output
python -m app.main 2>&1 | tee debug.log

# Now you'll see all error messages
```

### Step 4: Try Safe Mode
Create a test with small image:

```python
# test_simple.py
from PIL import Image
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap
import sys

app = QApplication(sys.argv)

# Create small test image
img = Image.new('RGB', (800, 600), color='red')
img.save('test.png')

# Try loading
pixmap = QPixmap('test.png')
print(f"Loaded: {pixmap.width()}x{pixmap.height()}")
print(f"Is null: {pixmap.isNull()}")
```

---

## 💡 Alternative Workarounds

### Option 1: Use Smaller Captures
Instead of full screen:
1. Press Ctrl+Alt+S
2. Select only a small region (not full screen)
3. This uses less memory

### Option 2: Reduce Color Depth
Edit `app/ui/capture_overlay.py` line 51:

```python
# Before
img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)

# After (uses less memory)
img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
img = img.resize((img.width // 2, img.height // 2), Image.LANCZOS)  # Half size
```

### Option 3: Use Different Screenshot Library
Replace MSS with PIL's ImageGrab (Windows only):

```python
# In capture_overlay.py
from PIL import ImageGrab

def capture_screen(self):
    try:
        img = ImageGrab.grab()  # Simpler, might be more reliable
        # ... rest of code
```

---

## 📊 System Requirements Check

### Minimum Requirements:
- **RAM:** 4GB (8GB recommended)
- **Python:** 3.8-3.13
- **Screen:** Any resolution
- **OS:** Windows 10+, Ubuntu 20.04+, macOS 10.14+

### Known Issues:
- **4K displays:** May cause memory issues
- **Multi-monitor:** Primary monitor only (currently)
- **High DPI:** Scaling issues possible
- **Old graphics drivers:** Update recommended

---

## 🆘 Still Crashing?

### Collect Debug Info:

1. **What's your screen resolution?**
   ```bash
   # Check in Display Settings
   ```

2. **Run this diagnostic:**
   ```bash
   python -m app.main > debug.log 2>&1
   # Try to capture
   # Check debug.log for errors
   ```

3. **Check Python version:**
   ```bash
   python --version
   # Make sure it's 3.8-3.13
   ```

4. **Share the error:**
   - Copy error message from terminal
   - Copy debug.log contents
   - Note your screen resolution
   - Share here for specific help

---

## ✅ After Applying Fixes

### Test Procedure:

1. **Restart the app:**
   ```bash
   python -m app.main
   ```

2. **Create session**

3. **Try small capture first:**
   - Press Ctrl+Alt+S
   - Select just a small 400x300 region
   - See if it works

4. **Watch terminal output:**
   - Look for "Captured: WxH" messages
   - Check for error messages

5. **If successful, try larger:**
   - Gradually increase capture size
   - Find your system's limits

---

## 📥 Download Patched Version

The fixed version is ready with all improvements:

[**Download Fixed overlay_annotator_v2.zip**](computer:///mnt/user-data/outputs/overlay_annotator_v2.zip)

**Changes in patched version:**
- ✅ Comprehensive error handling
- ✅ Image validation
- ✅ Better logging
- ✅ Memory safety checks
- ✅ Graceful failure instead of crashes

---

## 🎯 Expected Behavior After Fix

**Before fix:**
- Captures → Garbled pixels → Crash

**After fix:**
- Captures → Shows debug info → Validates → Either displays correctly OR shows error message without crashing

**Terminal output you should see:**
```
Captured: 1920x1080
QPixmap loaded: 1920x1080
Loading image: 1920x1080, mode: RGB
QImage created: 1920x1080
```

If you see errors, they'll now be clear messages instead of silent crashes.

---

**Download the fixed version and try again!** 🔧✨
