# Overlay Annotator V3.4.2 - Startup Crash Fix

**Release Date:** November 3, 2025  
**Type:** 🔥 Critical Hotfix  
**Download:** [overlay_annotator_v3.4.2.zip](computer:///mnt/user-data/outputs/overlay_annotator_v3.4.2.zip)

## 🐛 CRITICAL BUG FIXED

### **App Crashes on Startup** ✅ FIXED

**Error:**
```
TypeError: AnnotationCanvas.__init__() got an unexpected keyword argument 'parent'
```

**Cause:** 
AnnotationCanvas.__init__() didn't accept parent parameter

**Fix:**
```python
# Before (BROKEN):
def __init__(self):
    super().__init__()

# After (FIXED):
def __init__(self, parent=None):
    super().__init__(parent)
```

**Result:** App starts successfully!

## 🚀 Installation

```bash
unzip overlay_annotator_v3.4.2.zip
cd overlay_annotator_v3
python -m app.main
```

## 📥 Download

- [**overlay_annotator_v3.4.2.zip**](computer:///mnt/user-data/outputs/overlay_annotator_v3.4.2.zip) ⭐ **WORKS!**

**V3.4.1 was broken - use V3.4.2!**
