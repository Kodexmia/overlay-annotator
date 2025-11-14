# Error Logging & Recovery Guide

## 🆕 New Feature: Automatic Error Logging

The latest version now includes comprehensive error logging to help diagnose crashes!

---

## 📝 Where Are the Logs?

**Log Location:**
```
Windows: C:\Users\YourName\overlay_annotator_logs\
Linux:   /home/yourname/overlay_annotator_logs/
Mac:     /Users/yourname/overlay_annotator_logs/
```

**Log Files:**
```
overlay_annotator_20251101_153045.log  ← Timestamp in filename
overlay_annotator_20251101_154123.log
overlay_annotator_20251101_160245.log
```

---

## 🔍 What Gets Logged?

### Application Events:
- ✅ Startup and initialization
- ✅ Session creation
- ✅ Screen captures
- ✅ Annotation actions
- ✅ File operations
- ✅ Export generation

### Errors & Crashes:
- ✅ Full exception details
- ✅ Stack traces
- ✅ System information
- ✅ Memory state
- ✅ Failed operations

### Debug Information:
- ✅ Image dimensions
- ✅ Conversion steps
- ✅ File paths
- ✅ User actions

---

## 📖 How to Read a Log File

### Example Log Entry:

```
2025-11-01 15:30:45 - OverlayAnnotator - INFO - Application Started
2025-11-01 15:30:45 - OverlayAnnotator - INFO - Log file: C:\Users\Admin\overlay_annotator_logs\overlay_annotator_20251101_153045.log
2025-11-01 15:30:45 - OverlayAnnotator - INFO - Python version: 3.13.0
2025-11-01 15:30:45 - OverlayAnnotator - INFO - Platform: win32
2025-11-01 15:30:46 - OverlayAnnotator - INFO - Application initialized successfully
2025-11-01 15:30:46 - OverlayAnnotator - INFO - Starting hotkey listener...
2025-11-01 15:30:46 - OverlayAnnotator - INFO - Hotkey listener started - Ctrl+Alt+S active
2025-11-01 15:30:48 - OverlayAnnotator - DEBUG - Hotkey pressed (Ctrl+Alt+S)
2025-11-01 15:30:48 - OverlayAnnotator - INFO - Showing capture overlay...
2025-11-01 15:30:48 - OverlayAnnotator.CaptureOverlay - DEBUG - CaptureOverlay initialized
2025-11-01 15:30:48 - OverlayAnnotator.CaptureOverlay - INFO - Starting screen capture...
2025-11-01 15:30:48 - OverlayAnnotator.CaptureOverlay - DEBUG - Monitor: {'left': 0, 'top': 0, 'width': 1920, 'height': 1080}
2025-11-01 15:30:48 - OverlayAnnotator.CaptureOverlay - INFO - Captured: 1920x1080
2025-11-01 15:30:49 - OverlayAnnotator.CaptureOverlay - INFO - QPixmap loaded: 1920x1080
2025-11-01 15:30:52 - OverlayAnnotator - INFO - Region selected: 800x600
2025-11-01 15:30:52 - OverlayAnnotator - INFO - Image loaded successfully
```

### If There's an Error:

```
2025-11-01 15:30:48 - OverlayAnnotator.CaptureOverlay - ERROR - Screen capture failed
Traceback (most recent call last):
  File "app/ui/capture_overlay.py", line 58, in capture_screen
    img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
  File "/usr/lib/python3/site-packages/PIL/Image.py", line 3012, in frombytes
    ...
ValueError: not enough image data

2025-11-01 15:30:48 - OverlayAnnotator - CRITICAL - Unhandled exception:
...full stack trace...
```

---

## 🐛 When Application Crashes

### Step 1: Find the Log File

```bash
# Windows
cd %USERPROFILE%\overlay_annotator_logs
dir /o-d  # Lists newest first

# Linux/Mac
cd ~/overlay_annotator_logs
ls -lt  # Lists newest first
```

### Step 2: Open the Latest Log

```bash
# Windows
notepad overlay_annotator_20251101_153045.log

# Linux
gedit overlay_annotator_20251101_153045.log

# Mac
open -a TextEdit overlay_annotator_20251101_153045.log
```

### Step 3: Look for ERROR or CRITICAL Lines

Search for:
- `ERROR`
- `CRITICAL`
- `Exception`
- `Traceback`

### Step 4: Read the Stack Trace

Example:
```
ERROR - Screen capture failed
Traceback (most recent call last):
  File "app/ui/capture_overlay.py", line 58
    ↑ File where error occurred
  
    img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
    ↑ Line that failed
  
ValueError: not enough image data
↑ What went wrong
```

---

## 🔧 Common Errors & Solutions

### Error 1: "not enough image data"

**Log shows:**
```
ValueError: not enough image data
```

**Cause:** Screen capture returned incomplete data

**Solutions:**
1. Lower screen resolution temporarily
2. Capture smaller regions
3. Update graphics drivers
4. Disable hardware acceleration

---

### Error 2: "QPixmap is null"

**Log shows:**
```
ERROR - Failed to load QPixmap
```

**Cause:** Image conversion failed

**Solutions:**
1. Check available RAM (need 500MB+ free)
2. Restart the application
3. Try capturing smaller regions first

---

### Error 3: "Permission denied"

**Log shows:**
```
PermissionError: [Errno 13] Permission denied
```

**Cause:** Can't write to session folder

**Solutions:**
1. Choose a different session folder
2. Run as administrator (Windows)
3. Check folder permissions

---

### Error 4: "Module not found"

**Log shows:**
```
ModuleNotFoundError: No module named 'X'
```

**Cause:** Missing dependency

**Solutions:**
```bash
pip install -r requirements.txt
# Or install specific module:
pip install pyqt6
pip install mss
pip install pillow
```

---

## 📊 Analyzing Performance Issues

### Check Timing Information

Look for slow operations:
```
2025-11-01 15:30:48 - INFO - Starting screen capture...
2025-11-01 15:30:58 - INFO - Captured: 1920x1080
                      ↑ 10 seconds! Too slow!
```

**Normal times:**
- Screen capture: < 0.5 seconds
- Image conversion: < 0.2 seconds
- Canvas loading: < 0.1 seconds

**If slow:**
- Your screen resolution might be too high
- Not enough RAM
- Graphics drivers need update

---

## 🛠️ Debug Mode

### Run with Extra Debugging

```bash
# Windows
set PYTHONVERBOSE=1
python -m app.main

# Linux/Mac
PYTHONVERBOSE=1 python -m app.main
```

This shows even more detailed information!

---

## 📤 Sharing Logs for Help

If you need help debugging:

### Step 1: Find the Latest Log

```bash
cd ~/overlay_annotator_logs
ls -lt | head -1  # Shows newest file
```

### Step 2: Copy Last 100 Lines

```bash
# Windows
powershell "Get-Content overlay_annotator_*.log -Tail 100"

# Linux/Mac
tail -100 overlay_annotator_*.log
```

### Step 3: Share the Output

Copy and paste the last 100 lines when asking for help.

**Include:**
- What you were doing when it crashed
- Your screen resolution
- Python version (`python --version`)
- Operating system

---

## 🧹 Log Maintenance

### Cleaning Old Logs

Logs accumulate over time. Clean them periodically:

```bash
# Windows
cd %USERPROFILE%\overlay_annotator_logs
del /q overlay_annotator_*.log

# Linux/Mac
rm ~/overlay_annotator_logs/overlay_annotator_*.log
```

### Automatic Cleanup (Advanced)

Add to your system's task scheduler to run weekly:

```bash
# Delete logs older than 30 days
find ~/overlay_annotator_logs -name "*.log" -mtime +30 -delete
```

---

## 📈 Log Statistics

### Check Log Size

```bash
# Windows
cd %USERPROFILE%\overlay_annotator_logs
dir

# Linux/Mac
du -sh ~/overlay_annotator_logs
```

**Typical sizes:**
- Normal session: 50-200 KB
- With errors: 500 KB - 1 MB
- Many crashes: 5-10 MB

If logs are huge (>10 MB), something is wrong!

---

## 🎯 What to Do If Still Crashing

### 1. **Check the Log First**
Always read the log file to see what failed

### 2. **Look for Patterns**
Does it crash:
- At startup? → Installation issue
- During capture? → Graphics/memory issue
- During save? → Disk/permission issue

### 3. **Try Safe Mode**
Reduce complexity:
```bash
# Use smaller regions
# Lower screen resolution
# Close other applications
# Free up RAM
```

### 4. **Collect Debug Info**

Run this command and save output:
```bash
python -m app.main 2>&1 | tee debug_output.txt
```

Then try to reproduce the crash.

### 5. **Share Debug Info**
Post:
- Last 100 lines of log file
- Debug output
- System specs (RAM, screen resolution, OS)
- What you were doing

---

## 💡 Pro Tips

### Tip 1: Keep Logs Small
Start fresh application each session to avoid huge logs.

### Tip 2: Watch Console and Log
Run in terminal to see real-time errors while also logging to file.

### Tip 3: Set Log Level
Edit `app/core/logger.py` to change logging detail:
```python
level=logging.DEBUG   # Very detailed
level=logging.INFO    # Normal (default)
level=logging.WARNING # Only warnings/errors
```

### Tip 4: Timestamp Analysis
Compare timestamps to find slow operations:
```
15:30:48 - Start capture
15:30:58 - Capture complete
         = 10 seconds (TOO SLOW!)
```

---

## ✅ Success Indicators

### Good Log File:
```
INFO - Application Started
INFO - Application initialized successfully
INFO - Hotkey listener started
DEBUG - Hotkey pressed
INFO - Starting screen capture...
INFO - Captured: 1920x1080
INFO - QPixmap loaded: 1920x1080
INFO - Image loaded successfully
INFO - Entry saved
INFO - Report exported
```

No ERROR or CRITICAL lines = Everything working!

---

## 🆘 Emergency Recovery

### If Application Won't Start:

1. **Delete config:**
   ```bash
   rm ~/.overlay_annotator_config
   ```

2. **Clear logs:**
   ```bash
   rm -rf ~/overlay_annotator_logs
   ```

3. **Reinstall dependencies:**
   ```bash
   pip uninstall -y pyqt6 mss pillow pydantic jinja2 pynput
   pip install -r requirements.txt
   ```

4. **Fresh download:**
   Download clean copy of application

---

## 📞 Getting Help

When reporting issues, always include:

1. **Log file** (last 100 lines)
2. **What you did** (steps to reproduce)
3. **System info:**
   - OS: Windows 11 / Ubuntu 22.04 / macOS 13
   - Python version: 3.13.0
   - Screen resolution: 1920x1080
   - RAM: 8 GB

4. **Error message** (from log)

---

**With logging enabled, we can now diagnose any crash!** 📝🔍

Check `~/overlay_annotator_logs/` after each crash to see what went wrong.
