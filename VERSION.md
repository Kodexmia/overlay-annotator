# Overlay Annotator - Version History

## Version 3.0 - Stable Release (2025-11-01)

**Status:** ✅ STABLE - All major issues resolved

### What's New
- **Replaced pynput with pyqthotkey** - Eliminated Windows hook crashes
- **Thread-safe painting** - QMutex protection for canvas rendering
- **Deep image copy** - Prevents dangling buffer crashes
- **Software rendering** - GPU driver workaround enabled
- **Comprehensive logging** - Full error traces with faulthandler
- **Capture button fixed** - Works reliably alongside hotkey

### Fixed Issues
1. ✅ pynput Windows hook access violations
2. ✅ Dangling buffer Qt crashes
3. ✅ Thread race conditions in paintEvent
4. ✅ Capture button not triggering overlay
5. ✅ Evernote auto-opening temp files
6. ✅ Python 3.13 dataclass compatibility
7. ✅ Cross-platform temp file paths
8. ✅ Import path issues

### Installation
```bash
# IMPORTANT: Uninstall old dependency
pip uninstall pynput

# Install new dependencies
pip install -r requirements.txt

# Run
python -m app.main
```

### Requirements
- Python 3.8-3.13
- pyqt6
- mss
- pillow
- pydantic
- jinja2
- markdown
- **pyqthotkey** (new - replaces pynput)

---

## Version 2.x - Development Versions (Deprecated)

### Version 2.5
- Added error logging system
- Enhanced error handling in paintEvent
- Added toolbar parent references

### Version 2.4
- Fixed Evernote popup issue
- In-memory image conversion
- Removed temp file usage

### Version 2.3
- Fixed dangling buffer crash
- Added deep copy for QImage
- RGBA format conversion

### Version 2.2
- Enhanced crash diagnostics
- Added faulthandler
- Better error messages

### Version 2.1
- Fixed Python 3.13 compatibility
- Fixed import paths
- Fixed Windows temp paths

### Version 2.0
- Initial refactor
- Multiple stability issues

---

## Version 1.0 - Original (Not Included)

Initial prototype version with basic functionality.

---

## Version Naming Convention

- **V3.x** = Stable releases (production-ready)
- **V2.x** = Development/testing versions (deprecated)
- **V1.x** = Original prototype

---

## Current Version: 3.0

**Download:** overlay_annotator_v3.0.zip

**Key Features:**
- ✅ Stable on Windows with Python 3.13
- ✅ No crashes during image capture
- ✅ No pynput thread issues
- ✅ Thread-safe rendering
- ✅ Comprehensive error logging
- ✅ Both button and hotkey work reliably

---

## Upgrade Guide: V2.x → V3.0

### Breaking Changes
1. **pynput removed** - Install pyqthotkey instead
2. **App instance** - MainWindow now requires app_instance parameter

### Migration Steps
```bash
# 1. Uninstall old dependency
pip uninstall pynput

# 2. Install new version
pip install -r requirements.txt

# 3. No code changes needed for end users
python -m app.main
```

---

## Known Issues (V3.0)

None currently reported. 

If you encounter issues:
1. Check log file: `~/overlay_annotator_logs/`
2. Verify pyqthotkey installed: `pip list | grep hotkey`
3. Report with log excerpt

---

## Future Roadmap (V3.1+)

Potential enhancements:
- [ ] Multi-monitor support
- [ ] Custom hotkey configuration
- [ ] Plugin system for custom annotations
- [ ] Cloud sync for sessions
- [ ] Dark/light theme toggle
- [ ] Export to PDF
- [ ] Video annotation support

---

## Support

- **Log Location:** `~/overlay_annotator_logs/`
- **Report Issues:** Include last 50 lines of log file
- **System Info Needed:** Python version, OS, screen resolution

---

## Credits

Built with:
- PyQt6 - GUI framework
- mss - Fast screenshot library
- Pillow - Image processing
- pyqthotkey - System-wide hotkeys
- Pydantic - Data validation
- Jinja2 - Template engine
