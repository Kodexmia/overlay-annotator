# Overlay Annotator v3.4.2

A versatile desktop overlay tool for rapid screenshot capture, annotation, documentation, and structured evidence generation. Designed for developers, QA testers, cybersecurity analysts, trainers, content creators, internal teams, and client-facing workflows.

Overlay Annotator turns everyday screenshots into **professional documentation** with minimal effort.

---

## Why It’s More Than a Screenshot Tool

Overlay Annotator is built as a **full evidence pipeline**:

Capture → Annotate → Save → Export (Markdown/HTML)

This makes it ideal for:

- Software QA and bug reporting  
- Cybersecurity incident documentation  
- Technical walkthroughs and SOPs  
- UI/UX design notes  
- Audit trails  
- Developer onboarding  
- Client project delivery  
- Training and learning modules  

Every capture becomes a structured entry with:

- Screenshot  
- Title  
- Notes  
- Annotations  
- Timestamps  
- Export-ready formatting  


## Installation

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the application
python -m app.main
```

### Quick Start

1. **Create Session**: Click "📁 New Session" and select/create a folder
2. **Capture**: Press `Ctrl+Alt+S` or click "📷 Capture"
3. **Select Region**: Click and drag to select the area
4. **Annotate**: Use the floating toolbar to add annotations
   - Arrow: Draw directional arrows
   - Box: Draw rectangles
   - Pen: Freehand drawing
   - Blur: Blur sensitive areas
   - Text: Add text labels
5. **Save**: Add title and notes, then click "💾 Save Entry"
6. **Export**: Click "📤 Export Report" to generate Markdown report

### Keyboard Shortcuts

- `Ctrl+Alt+S` - Capture screen region
- `Ctrl+S` - Save entry
- `A` - Arrow tool
- `B` - Box tool
- `P` - Pen tool
- `U` - Blur tool
- `Esc` - Cancel capture/annotation

## Project Structure

```
overlay_annotator_v2/
├── app/
│   ├── main.py                 # Entry point with hotkey support
│   ├── ui/
│   │   ├── main_window.py      # Main application window
│   │   ├── capture_overlay.py  # Transparent capture overlay
│   │   ├── annotation_canvas.py # Annotation canvas with tools
│   │   └── annotation_toolbar.py # Floating toolbar
│   └── core/
│       ├── models.py           # Data models
│       └── storage.py          # Session storage
├── sessions/                   # Default session storage
├── requirements.txt
└── README.md
```

## Session Structure

Each session folder contains:

```
session_name/
├── images/                     # Captured and annotated images
├── metadata/                   # JSON metadata for each entry
├── _templates/                 # Report templates
└── report.md                   # Generated report
```

## Tips

- **Drag Toolbar**: Click and drag anywhere on the toolbar to reposition
- **Quick Save**: Use `Ctrl+S` after annotating
- **Color Picker**: Click the color button (●) to choose annotation colors
- **Multiple Monitors**: Works with primary monitor (multi-monitor coming soon)

## Troubleshooting

**Hotkey not working:**
- Check if another application is using `Ctrl+Alt+S`
- Try restarting the application
- Use manual capture button as fallback

**Canvas appears black:**
- This is normal - it shows after you capture something
- Create a session first, then capture

**Annotations not showing:**
- Make sure toolbar is visible (click "🎨 Show Toolbar")
- Check that you're selecting a tool (should be highlighted)

## Roadmap

- [ ] Multi-monitor support
- [ ] Window-specific capture
- [ ] Customizable hotkeys
- [ ] Video recording
- [ ] PDF/ODT export
- [ ] Cloud sync
- [ ] Team collaboration

## License

MIT License
