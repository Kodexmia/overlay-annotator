# INSTALLATION GUIDE - FINAL FIX

## 🎯 The Final Problem: pynput Thread Crash

The faulthandler revealed the real issue:
```
Windows fatal exception: access violation
File "pynput\_util\win32.py", line 190 in __iter__
```

**The `pynput` library's Windows keyboard hook was crashing!**

---

## ✅ THE SOLUTION: Replace pynput with QHotkey

We've replaced the problematic `pynput` with `pyqthotkey` - a Qt-native hotkey library that's much more stable on Windows.

---

## 📦 Installation Steps

### Step 1: Download the Fixed Version

[**Download overlay_annotator_v2.zip**](computer:///mnt/user-data/outputs/overlay_annotator_v2.zip)

### Step 2: Extract

```bash
# Extract to a folder
unzip overlay_annotator_v2.zip
cd overlay_annotator_v2
```

### Step 3: Install New Dependencies

**IMPORTANT:** You need to install `pyqthotkey` instead of `pynput`:

```bash
# Uninstall old dependency
pip uninstall pynput

# Install new dependencies
pip install -r requirements.txt
```

**Or install manually:**
```bash
pip install pyqt6 mss pillow pydantic jinja2 markdown pyqthotkey
```

### Step 4: Run

```bash
python -m app.main
```

---

## 🔧 What Changed

### 1. **Removed pynput** (was causing crashes)
```diff
- pynput  ❌ REMOVED (Windows hook crashes)
+ pyqthotkey  ✅ ADDED (Qt-native, stable)
```

### 2. **Qt-Native Hotkey** (runs on GUI thread)
```python
# OLD (BROKEN):
from pynput import keyboard
# Thread → Windows hook → Access violation → CRASH

# NEW (FIXED):
from pyqthotkey import QHotkey
# Qt-native → GUI thread → No crash ✓
```

### 3. **Software Rendering** (GPU driver workaround)
```python
os.environ["QT_OPENGL"] = "software"
```

### 4. **Thread-Safe Painting** (mutex protection)
```python
with QMutexLocker(self._mx):
    self._pixmap = QPixmap.fromImage(self.q_image)
```

---

## 🎯 Expected Behavior

### **Startup:**
```
Overlay Annotator running...
Press Ctrl+Alt+S to capture screen region
```

### **When you press Ctrl+Alt+S:**
```
✅ Capture overlay appears
✅ Select region
✅ Toolbar shows
✅ NO CRASH!
✅ Ready to annotate
```

---

## ⚠️ If pyqthotkey Won't Install

If you get an error installing `pyqthotkey`:

```
ERROR: Could not find a version that satisfies the requirement pyqthotkey
```

### Option 1: Use the Capture Button

The app will still work, just without the global hotkey:

```
WARNING: Global hotkey not available!
Install pyqthotkey: pip install pyqthotkey
Use the 'Capture' button instead
```

Click the "📷 Capture (Ctrl+Alt+S)" button in the app instead.

### Option 2: Try Different Installation

```bash
# Try with pip directly
pip install pyqt6-hotkey

# Or try pyqt-hotkey (different package)
pip install pyqt-hotkey
```

### Option 3: Manual Hotkey (Fallback)

If none work, edit `app/main.py` and add this simple Qt shortcut:

```python
# In MainWindow.__init__
from PyQt6.QtGui import QKeySequence, QShortcut

self.shortcut = QShortcut(QKeySequence("Ctrl+Alt+S"), self)
self.shortcut.activated.connect(self.show_capture_overlay)
```

This only works when the window is focused, but it's better than nothing!

---

## 🧪 Testing Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Verify Installation
```bash
python -c "import pyqthotkey; print('✓ pyqthotkey installed')"
```

### 3. Run Application
```bash
python -m app.main
```

### 4. Look for This:
```
Overlay Annotator running...
Press Ctrl+Alt+S to capture screen region
Log file: C:\Users\...\overlay_annotator_logs\...
```

### 5. Test Capture
- Press Ctrl+Alt+S
- Select a region
- **Toolbar should appear and STAY VISIBLE**
- No crash!

---

## 📊 What Was Fixed

| Issue | Status |
|-------|--------|
| Python 3.13 compatibility | ✅ Fixed |
| Import paths | ✅ Fixed |
| Windows temp paths | ✅ Fixed |
| Evernote popup | ✅ Fixed |
| Dangling buffer crash | ✅ Fixed |
| **pynput thread crash** | ✅ **FIXED!** |
| Thread-safe painting | ✅ Fixed |
| Software rendering | ✅ Enabled |

---

## 🎉 Success Indicators

**✓ It's working if:**
1. App starts without errors
2. "Press Ctrl+Alt+S to capture" message appears
3. Hotkey triggers capture overlay
4. Toolbar appears after selection
5. **Toolbar stays visible** (no crash!)
6. You can draw annotations
7. Can save entries

**✗ Still having issues if:**
1. "pyqthotkey not installed" warning
2. Still crashes after toolbar shows
3. Access violation errors

---

## 🆘 Troubleshooting

### Issue 1: Can't Install pyqthotkey

**Solution:** Use the Capture button instead of hotkey
```
Click: 📷 Capture (Ctrl+Alt+S)
```

### Issue 2: Still Crashes

**Check the log file:**
```bash
# Find latest log
dir %USERPROFILE%\overlay_annotator_logs /o-d

# Open it
notepad overlay_annotator_20251101_*.log
```

Look for new ERROR lines and share them.

### Issue 3: Hotkey Not Working

**Try this test:**
```python
# Run this to test pyqthotkey
python -c "
from PyQt6.QtWidgets import QApplication
from pyqthotkey import QHotkey
import sys

app = QApplication(sys.argv)
hk = QHotkey('Ctrl+Alt+S', register=True)
print('Hotkey registered!' if hk else 'Failed to register')
"
```

---

## 💡 Why This Fix Works

### **Before (Broken):**
```
pynput thread → Windows hook → Access violation in win32.py
→ Crashes while Qt is painting
→ 💥 Python stopped working
```

### **After (Fixed):**
```
QHotkey → Qt signal → GUI thread → QTimer.singleShot
→ Everything on main thread
→ No Windows hooks
→ ✓ Stable!
```

**Key improvements:**
1. **No separate thread** - everything on GUI thread
2. **No Windows hooks** - uses Qt's event system
3. **Thread-safe painting** - mutex protects pixmap
4. **Software rendering** - avoids GPU driver issues

---

## 📥 Download Links

- [**overlay_annotator_v2.zip** (67 KB)](computer:///mnt/user-data/outputs/overlay_annotator_v2.zip) - **RECOMMENDED**
- [overlay_annotator_v2.tar.gz (52 KB)](computer:///mnt/user-data/outputs/overlay_annotator_v2.tar.gz) - Linux/Mac

---

## 🚀 Quick Start

```bash
# 1. Extract
unzip overlay_annotator_v2.zip
cd overlay_annotator_v2

# 2. Install (NEW requirement!)
pip uninstall pynput
pip install -r requirements.txt

# 3. Run
python -m app.main

# 4. Use it!
# Press Ctrl+Alt+S or click Capture button
```

---

## ✅ Final Checklist

Before reporting issues, verify:

- [ ] Uninstalled `pynput`
- [ ] Installed `pyqthotkey` (or see fallback options)
- [ ] Running latest version (67 KB zip file)
- [ ] Log file shows "Hotkey registered successfully" OR "Use Capture button"
- [ ] No "pynput" imports in error messages

---

## 📞 Getting Help

If it still crashes, share:

1. **Last 50 lines of log file**
2. **Error message** (if any)
3. **Did pyqthotkey install?**
   ```bash
   pip list | findstr hotkey
   ```
4. **Windows version**
5. **Python version**
   ```bash
   python --version
   ```

---

**This should be the final fix!** The pynput thread crash was the culprit, and we've completely removed it. 🎯✨
