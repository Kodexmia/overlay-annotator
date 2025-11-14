"""
Main application window with session management
"""
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QFileDialog, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QTextEdit, QComboBox, QListWidget, 
    QSplitter, QMessageBox, QStatusBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut
from PIL import Image

from app.core.storage import SessionStore
from app.core.models import Entry, ImageModel
from app.ui.annotation_canvas import AnnotationCanvas, ToolType
from app.ui.annotation_toolbar import AnnotationToolbar


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, project_root: Path, logger=None, app_instance=None):
        super().__init__()
        self.setWindowTitle("Overlay Annotator v2")
        self.resize(1400, 900)
        self.project_root = project_root
        self.logger = logger
        self.app_instance = app_instance  # Reference to OverlayAnnotatorApp
        self.session_path = None
        self.store = None
        self.annotation_toolbar = None
        
        if self.logger:
            self.logger.debug("MainWindow initializing...")
        
        self.setup_ui()
        self.setup_shortcuts()
        self.show_welcome_message()
    
    def setup_ui(self):
        """Setup main UI components"""
        # Left panel: Session and entry list
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Session controls
        self.btn_new_session = QPushButton("📁 New Session")
        self.btn_new_session.clicked.connect(self.choose_session_folder)
        left_layout.addWidget(self.btn_new_session)
        
        self.btn_capture = QPushButton("📷 Capture (Ctrl+Alt+S)")
        self.btn_capture.clicked.connect(self.trigger_capture)
        self.btn_capture.setEnabled(False)
        left_layout.addWidget(self.btn_capture)
        
        left_layout.addWidget(QLabel("Entries:"))
        self.entry_list = QListWidget()
        self.entry_list.itemClicked.connect(self.load_entry)
        left_layout.addWidget(self.entry_list)
        
        # Export button
        self.btn_export = QPushButton("📤 Export Report")
        self.btn_export.clicked.connect(self.export_report)
        self.btn_export.setEnabled(False)
        left_layout.addWidget(self.btn_export)
        
        left_panel.setLayout(left_layout)
        
        # Center panel: Canvas
        center_panel = QWidget()
        center_layout = QVBoxLayout()
        
        # CRITICAL FIX: Set main window as canvas parent so text tool can call back
        self.canvas = AnnotationCanvas(parent=self)
        center_layout.addWidget(self.canvas)
        
        # Annotation controls
        controls_layout = QHBoxLayout()
        
        self.btn_show_toolbar = QPushButton("🎨 Show Toolbar")
        self.btn_show_toolbar.clicked.connect(self.show_annotation_toolbar)
        self.btn_show_toolbar.setEnabled(False)
        controls_layout.addWidget(self.btn_show_toolbar)
        
        self.btn_undo = QPushButton("↶ Undo")
        self.btn_undo.clicked.connect(self.canvas.undo_last)
        self.btn_undo.setEnabled(False)
        controls_layout.addWidget(self.btn_undo)
        
        self.btn_clear = QPushButton("🗑 Clear")
        self.btn_clear.clicked.connect(self.canvas.clear_annotations)
        self.btn_clear.setEnabled(False)
        controls_layout.addWidget(self.btn_clear)
        
        controls_layout.addStretch()
        center_layout.addLayout(controls_layout)
        
        center_panel.setLayout(center_layout)
        
        # Right panel: Metadata
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        right_layout.addWidget(QLabel("Layout:"))
        self.layout_select = QComboBox()
        self.layout_select.addItems(["image-left", "image-top"])
        right_layout.addWidget(self.layout_select)
        
        right_layout.addWidget(QLabel("Title:"))
        self.title_edit = QTextEdit()
        self.title_edit.setPlaceholderText("Enter title...")
        self.title_edit.setMaximumHeight(60)
        right_layout.addWidget(self.title_edit)
        
        right_layout.addWidget(QLabel("Notes:"))
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Enter notes...")
        right_layout.addWidget(self.notes_edit)
        
        self.btn_save = QPushButton("💾 Save Entry")
        self.btn_save.clicked.connect(self.save_entry)
        self.btn_save.setEnabled(False)
        right_layout.addWidget(self.btn_save)
        
        right_layout.addStretch()
        right_panel.setLayout(right_layout)
        
        # Main splitter
        splitter = QSplitter()
        splitter.addWidget(left_panel)
        splitter.addWidget(center_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        splitter.setStretchFactor(2, 1)
        
        # Central widget
        container = QWidget()
        main_layout = QHBoxLayout()
        main_layout.addWidget(splitter)
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status("Ready. Press Ctrl+Alt+S to capture screen region.")
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Save shortcut
        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self.save_entry)
        
        # Tool shortcuts
        arrow_shortcut = QShortcut(QKeySequence("A"), self)
        arrow_shortcut.activated.connect(lambda: self.canvas.set_tool(ToolType.ARROW))
        
        box_shortcut = QShortcut(QKeySequence("B"), self)
        box_shortcut.activated.connect(lambda: self.canvas.set_tool(ToolType.BOX))
        
        pen_shortcut = QShortcut(QKeySequence("P"), self)
        pen_shortcut.activated.connect(lambda: self.canvas.set_tool(ToolType.PEN))
        
        blur_shortcut = QShortcut(QKeySequence("U"), self)
        blur_shortcut.activated.connect(lambda: self.canvas.set_tool(ToolType.BLUR))
    
    def show_welcome_message(self):
        """Show welcome message"""
        self.update_status("Welcome! Create a session to begin capturing.")
    
    def choose_session_folder(self):
        """Choose or create session folder"""
        default_dir = str(self.project_root / "sessions")
        Path(default_dir).mkdir(exist_ok=True)
        
        path = QFileDialog.getExistingDirectory(
            self,
            "Choose Session Folder",
            default_dir
        )
        
        if not path:
            return
        
        self.session_path = Path(path)
        self.session_path.mkdir(parents=True, exist_ok=True)
        (self.session_path / "images").mkdir(exist_ok=True)
        (self.session_path / "metadata").mkdir(exist_ok=True)
        
        self.store = SessionStore(self.session_path)
        self.load_session_entries()
        
        # Enable buttons
        self.btn_capture.setEnabled(True)
        self.btn_export.setEnabled(True)
        
        self.update_status(f"Session loaded: {self.session_path.name}")
    
    def load_session_entries(self):
        """Load existing entries from session"""
        if not self.store:
            return
        
        self.entry_list.clear()
        entries = self.store.load_entries()
        
        for entry in entries:
            self.entry_list.addItem(f"{entry.id} — {entry.title}")
    
    def load_entry(self, item):
        """Load selected entry into canvas"""
        if not self.store:
            return
        
        entry_id = item.text().split(" — ")[0]
        entries = self.store.load_entries()
        
        for entry in entries:
            if entry.id == entry_id:
                # Load image
                img_path = self.session_path / entry.image.path
                if img_path.exists():
                    pil_img = Image.open(img_path)
                    self.canvas.load_pil(pil_img)
                    
                    # Load metadata
                    self.title_edit.setPlainText(entry.title)
                    self.notes_edit.setPlainText(entry.notes)
                    self.layout_select.setCurrentText(entry.layout)
                    
                    self.update_status(f"Loaded entry: {entry.title}")
                break
    
    def trigger_capture(self):
        """Manually trigger capture (for testing without hotkey)"""
        if self.app_instance:
            if self.logger:
                self.logger.debug("Capture button clicked - triggering overlay")
            self.app_instance.show_capture_overlay()
        else:
            self.update_status("Error: Capture overlay not available")
            if self.logger:
                self.logger.error("App instance not set - cannot trigger capture")
    
    def handle_captured_region(self, pil_img: Image.Image):
        """Handle captured screen region"""
        try:
            if self.logger:
                self.logger.info(f"Handling captured region: {pil_img.width}x{pil_img.height}")
            
            if not self.store:
                if self.logger:
                    self.logger.warning("No session - cannot handle captured region")
                QMessageBox.warning(self, "No Session", "Please create a session first.")
                return
            
            # Load into canvas
            if self.logger:
                self.logger.debug("Loading image into canvas...")
            self.canvas.load_pil(pil_img)
            
            # Enable annotation controls
            self.btn_show_toolbar.setEnabled(True)
            self.btn_undo.setEnabled(True)
            self.btn_clear.setEnabled(True)
            self.btn_save.setEnabled(True)
            
            # Auto-show toolbar
            self.show_annotation_toolbar()
            
            self.update_status("Image captured! Annotate and save.")
            if self.logger:
                self.logger.info("Image loaded successfully, ready for annotation")
                
        except Exception as e:
            if self.logger:
                self.logger.error("Error handling captured region", exc_info=True)
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to load captured image:\n{str(e)}"
            )
    
    def show_annotation_toolbar(self):
        """Show floating annotation toolbar"""
        try:
            if self.logger:
                self.logger.debug("Showing annotation toolbar...")
            
            if self.annotation_toolbar is None:
                if self.logger:
                    self.logger.debug("Creating new annotation toolbar")
                # CRITICAL: Set parent to prevent orphaned widget crashes
                self.annotation_toolbar = AnnotationToolbar(parent=self)
                
                # Connect signals
                self.annotation_toolbar.tool_selected.connect(self.canvas.set_tool)
                self.annotation_toolbar.save_requested.connect(self.save_entry)
                self.annotation_toolbar.cancel_requested.connect(self.cancel_annotation)
                self.annotation_toolbar.text_requested.connect(self.canvas.add_text_annotation)
                self.annotation_toolbar.undo_btn.clicked.connect(self.canvas.undo_last)
                
                if self.logger:
                    self.logger.debug("Toolbar created and signals connected")
            
            # Position toolbar near top center
            toolbar_x = self.x() + (self.width() - self.annotation_toolbar.width()) // 2
            toolbar_y = self.y() + 100
            self.annotation_toolbar.move(toolbar_x, toolbar_y)
            
            if self.logger:
                self.logger.debug(f"Toolbar positioned at {toolbar_x}, {toolbar_y}")
            
            self.annotation_toolbar.show()
            self.annotation_toolbar.raise_()
            
            if self.logger:
                self.logger.info("Annotation toolbar shown successfully")
                
        except Exception as e:
            if self.logger:
                self.logger.error("Error showing annotation toolbar", exc_info=True)
            QMessageBox.warning(
                self,
                "Toolbar Error",
                f"Failed to show annotation toolbar:\n{str(e)}"
            )
    
    def cancel_annotation(self):
        """Cancel current annotation"""
        self.canvas.clear_annotations()
        if self.annotation_toolbar:
            self.annotation_toolbar.hide()
        self.update_status("Annotation cancelled")
    
    def request_text_for_annotation(self):
        """Request text input from toolbar when canvas is clicked with text tool"""
        if self.annotation_toolbar:
            text = self.annotation_toolbar.request_text_input()
            if text:
                self.canvas.add_text_annotation(text)
                # Switch back to arrow tool after placing text
                from app.ui.annotation_canvas import ToolType
                self.canvas.set_tool(ToolType.ARROW)
                self.annotation_toolbar.select_tool(ToolType.ARROW)
    
    def save_entry(self):
        """Save annotated entry"""
        if not self.store or self.canvas.pil_image is None:
            self.update_status("Nothing to save")
            return
        
        # Render annotated image
        pil = self.canvas.render_annotated()
        
        # Save image
        img_rel_path = self.store.save_image(pil)
        
        # Create entry
        entry = Entry.new(
            title=self.title_edit.toPlainText().strip() or "Untitled",
            notes=self.notes_edit.toPlainText().strip(),
            layout=self.layout_select.currentText(),
            image=ImageModel(
                path=str(img_rel_path),
                width=pil.width,
                height=pil.height,
                quality=None,
                hires=False
            ),
        )
        
        # Save entry
        self.store.save_entry(entry)
        
        # Update list
        self.entry_list.addItem(f"{entry.id} — {entry.title}")
        
        # Clear form
        self.title_edit.clear()
        self.notes_edit.clear()
        self.canvas.clear_annotations()
        
        # Hide toolbar
        if self.annotation_toolbar:
            self.annotation_toolbar.hide()
        
        self.update_status(f"Entry saved: {entry.title}")
        
        QMessageBox.information(
            self,
            "Saved",
            f"Entry '{entry.title}' saved successfully!"
        )
    
    def export_report(self):
        """Export session report as both Markdown and HTML"""
        if not self.store:
            return
        
        try:
            # Export both formats
            md_path = self.store.export_markdown()
            html_path = self.store.export_html()
            
            self.update_status(f"Reports exported: {md_path.name} & {html_path.name}")
            
            # Ask user which one to open
            reply = QMessageBox.question(
                self,
                "Export Complete",
                f"Reports exported successfully!\n\n"
                f"📄 Markdown: {md_path}\n"
                f"🌐 HTML: {html_path}\n\n"
                f"Open HTML report in browser?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                import webbrowser
                webbrowser.open(str(html_path.absolute()))
                
        except Exception as e:
            if self.logger:
                self.logger.error("Export failed", exc_info=True)
            QMessageBox.critical(
                self,
                "Export Failed",
                f"Failed to export report:\n{str(e)}"
            )
    
    def update_status(self, message: str):
        """Update status bar"""
        self.status_bar.showMessage(message)
    
    def closeEvent(self, event):
        """Handle window close"""
        if self.annotation_toolbar:
            self.annotation_toolbar.close()
        event.accept()
