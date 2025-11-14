# Overlay Annotator v2 - Getting Started Guide

## 🎯 What You Built

A working desktop overlay tool with:

✅ **Global Hotkey** - Ctrl+Alt+S triggers capture from anywhere
✅ **Transparent Overlay** - Dimmed screen with region selection
✅ **Island Toolbar** - Floating, draggable annotation toolbar
✅ **5 Annotation Tools** - Arrow, Box, Pen, Blur, Text
✅ **Session Management** - Organized capture storage
✅ **Markdown Export** - Auto-generated reports

## 📦 What's Included

```
overlay_annotator_v2/
├── app/
│   ├── main.py                    # Entry point with hotkey
│   ├── ui/
│   │   ├── main_window.py         # Main app window
│   │   ├── capture_overlay.py     # Transparent capture overlay
│   │   ├── annotation_canvas.py   # Annotation engine with tools
│   │   └── annotation_toolbar.py  # Floating island toolbar
│   └── core/
│       ├── models.py              # Entry and session models
│       └── storage.py             # File storage system
├── requirements.txt               # Dependencies
├── start.sh                       # Linux/Mac launcher
├── start.bat                      # Windows launcher
├── test_quick.py                  # Quick verification
└── README.md                      # Documentation
```

## 🚀 Installation & Launch

### Windows
```cmd
1. Double-click start.bat
   (It will auto-install dependencies and launch)

OR manually:
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python -m app.main
```

### Linux/Mac
```bash
1. Run: ./start.sh
   (It will auto-install dependencies and launch)

OR manually:
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python -m app.main
```

## 📸 How to Use

### First Time Setup

1. **Launch Application**
   - Run `start.bat` (Windows) or `./start.sh` (Linux/Mac)
   - Main window opens

2. **Create Session**
   - Click "📁 New Session"
   - Choose/create a folder (e.g., "QA_Reports")
   - Session loaded ✓

### Capturing & Annotating

1. **Trigger Capture**
   - Press `Ctrl+Alt+S` (anywhere on your system)
   - OR click "📷 Capture" button

2. **Select Region**
   - Screen dims with transparent overlay
   - Click and drag to select area
   - Release to capture
   - Press `Esc` to cancel

3. **Annotate**
   - Floating toolbar appears automatically
   - Select tool:
     - ➔ **Arrow** (A) - Draw directional arrows
     - ▭ **Box** (B) - Draw rectangles
     - ✎ **Pen** (P) - Freehand drawing
     - ⊙ **Blur** (U) - Blur sensitive areas
     - **T Text** (T) - Add text labels
   - Click color button (●) to change colors
   - Draw on the captured image

4. **Save Entry**
   - Add title and notes in right panel
   - Choose layout (image-left or image-top)
   - Click "💾 Save Entry" or press `Ctrl+S`
   - Entry saved to session ✓

5. **Export Report**
   - Click "📤 Export Report"
   - Markdown file generated with all entries
   - Located in session folder as `report.md`

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Alt+S` | Capture screen region |
| `Ctrl+S` | Save current entry |
| `A` | Switch to Arrow tool |
| `B` | Switch to Box tool |
| `P` | Switch to Pen tool |
| `U` | Switch to Blur tool |
| `Esc` | Cancel capture/annotation |

## 🎨 Toolbar Features

**Draggable**: Click and drag toolbar to reposition

**Tools**:
- **Arrow** - Draw directional pointers
- **Box** - Highlight regions with rectangles
- **Pen** - Free drawing for custom annotations
- **Blur** - Redact sensitive information
- **Text** - Add labels (prompts for text input)

**Actions**:
- **Color Button (●)** - Pick annotation color
- **Undo (↶)** - Remove last annotation
- **Save (✓)** - Save entry
- **Cancel (✕)** - Discard annotations

## 📁 Session Structure

Each session folder contains:

```
Session_Folder/
├── images/
│   ├── entry_20251031_143022.jpg
│   ├── entry_20251031_143045.jpg
│   └── ...
├── metadata/
│   ├── 5f3a7b21.json
│   ├── 8c2d9e45.json
│   └── ...
├── _templates/
│   └── report.md.j2
└── report.md                    # Generated report
```

## 🔧 Customization

### Change Hotkey
Edit `app/main.py` line 50:
```python
with keyboard.GlobalHotKeys({
    '<ctrl>+<alt>+s': self.on_hotkey_pressed  # Change this
}) as listener:
```

### Modify Report Template
Edit `session_folder/_templates/report.md.j2`:
```markdown
# Custom Report Header

{% for e in entries %}
## {{ e.title }}
...
{% endfor %}
```

### Add New Annotation Colors
Edit `app/ui/annotation_toolbar.py`:
```python
self.color_presets = [
    QColor(255, 0, 0),    # Red
    QColor(0, 255, 0),    # Green
    QColor(0, 0, 255),    # Blue
    # Add more...
]
```

## 🐛 Troubleshooting

### Hotkey Not Working
**Problem**: Ctrl+Alt+S doesn't trigger capture

**Solutions**:
1. Check if another app uses this hotkey
2. Run as administrator (Windows)
3. Use manual "📷 Capture" button
4. Change hotkey in code (see Customization)

### Black Canvas
**Problem**: Canvas shows nothing

**Solution**:
- This is normal when no image is loaded
- Create session first, then capture
- Check that capture completed (watch for toolbar)

### Toolbar Not Showing
**Problem**: Floating toolbar doesn't appear

**Solutions**:
1. Click "🎨 Show Toolbar" button
2. Check if hidden behind main window
3. Close and reopen application

### Dependencies Failed to Install
**Problem**: pip install errors

**Solutions**:
```bash
# Update pip first
python -m pip install --upgrade pip

# Install one by one
pip install pyqt6
pip install mss
pip install pillow
pip install pydantic
pip install jinja2
pip install markdown
pip install pynput
```

### Annotations Not Saving
**Problem**: Annotations disappear

**Solution**:
- Make sure to click "💾 Save Entry"
- Don't close toolbar before saving
- Check that session folder is writable

## 🎯 Best Practices

1. **Organize Sessions by Project**
   - Create separate sessions for different projects
   - Use descriptive folder names

2. **Use Meaningful Titles**
   - Add clear titles to each entry
   - Include context in notes

3. **Color Code Annotations**
   - Red for errors/issues
   - Blue for information
   - Green for success/working features

4. **Blur Sensitive Data**
   - Always use blur tool on passwords, keys, tokens
   - Review images before exporting

5. **Regular Exports**
   - Export reports frequently
   - Keep backups of session folders

## 🚧 Known Limitations (MVP)

- ❌ Single monitor only (primary display)
- ❌ Full screen capture only (no window picker)
- ❌ No undo for blur tool
- ❌ No annotation history/edit
- ❌ Markdown export only (no PDF/ODT yet)
- ❌ No cloud sync

## 🔮 Coming Soon (v2.1)

- [ ] Multi-monitor support
- [ ] Window selection (click to capture specific window)
- [ ] More shapes (circle, callout, numbered pins)
- [ ] Annotation presets
- [ ] PDF export
- [ ] Undo blur
- [ ] Session templates
- [ ] Dark mode

## 💡 Tips & Tricks

**Quick Workflow**:
1. Set up session once
2. Use Ctrl+Alt+S → Select → Annotate → Ctrl+S
3. Repeat for all captures
4. Export report at end

**Efficient Annotation**:
- Learn keyboard shortcuts (A, B, P, U)
- Keep toolbar in same position
- Use consistent color coding

**Professional Reports**:
- Add detailed notes
- Include context (browser, resolution, etc.)
- Use descriptive titles
- Export regularly

**Collaboration**:
- Share session folders via network/USB
- Export Markdown for wikis/docs
- Screenshots are portable

## 📞 Support

**Issues?**
1. Check Troubleshooting section
2. Verify Python 3.8+ installed
3. Ensure all dependencies installed
4. Check console output for errors

**Enhancement Ideas?**
- Fork the project
- Add your features
- Share improvements

## 📄 License

MIT License - Use freely, modify as needed

---

**Ready to capture!** 📸

Press `Ctrl+Alt+S` and start documenting!
