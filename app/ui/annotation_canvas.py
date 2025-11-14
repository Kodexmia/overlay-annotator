from typing import Optional, List, Tuple
from enum import Enum
from dataclasses import dataclass
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QMouseEvent, QFont, QImage, QPixmap
from PyQt6.QtCore import Qt, QPoint, QRect, QMutex, QMutexLocker
from PIL import Image, ImageDraw, ImageFont, ImageFilter


class ToolType(Enum):
    """Available annotation tools"""
    ARROW = "arrow"
    BOX = "box"
    TEXT = "text"
    BLUR = "blur"
    PEN = "pen"


@dataclass
class Annotation:
    """Single annotation element"""
    tool: ToolType
    start: QPoint
    end: Optional[QPoint] = None
    color: Optional[QColor] = None
    text: Optional[str] = None
    width: int = 3
    
    def __post_init__(self):
        if self.color is None:
            self.color = QColor(255, 0, 0)


class AnnotationCanvas(QWidget):
    """Canvas for drawing annotations on captured images"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pil_image: Optional[Image.Image] = None
        self.q_image: Optional[QImage] = None  # Immutable backing image
        self._pixmap: Optional[QPixmap] = None  # Fast paint source
        self._mx = QMutex()  # Guard image swap for thread safety
        self.annotations: List[Annotation] = []
        self.current_annotation: Optional[Annotation] = None
        self.active_tool = ToolType.ARROW
        self.tool_color = QColor(255, 0, 0)
        self.tool_width = 3
        self.is_drawing = False
        
        # For text tool
        self.pending_text = False
        self.text_position: Optional[QPoint] = None
        
        self.setMinimumSize(400, 300)
    
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
            
            # CRITICAL FIX: Ensure RGBA mode and create deep copy
            # This prevents the dangling buffer crash that was killing Qt
            if pil_img.mode != 'RGBA':
                print(f"Converting from {pil_img.mode} to RGBA")
                pil_img = pil_img.convert('RGBA')
            
            # Store PIL image (keeps it alive)
            self.pil_image = pil_img.copy()
            self.annotations.clear()
            self.current_annotation = None
            
            # Method: Safe conversion with deep copy and mutex protection
            # Extract raw bytes and dimensions
            width, height = self.pil_image.size
            img_data = self.pil_image.tobytes("raw", "RGBA")
            bytes_per_line = width * 4  # RGBA = 4 bytes per pixel
            
            # Create QImage from bytes
            q_img = QImage(
                img_data, 
                width, 
                height, 
                bytes_per_line,
                QImage.Format.Format_RGBA8888
            )
            
            # CRITICAL: Force deep copy so Qt owns the memory
            # This is what prevents the crash!
            q_img = q_img.copy()
            
            # Validate QImage
            if q_img.isNull():
                print("Error: QImage is null after conversion")
                return
                
            print(f"QImage created: {q_img.width()}x{q_img.height()}")
            print("Deep copy successful - Qt now owns the image buffer")
            
            # THREAD SAFETY: Use mutex when swapping images
            with QMutexLocker(self._mx):
                self.q_image = q_img
                # Create QPixmap for fast painting
                self._pixmap = QPixmap.fromImage(self.q_image)
            
            # Keep the byte data alive too (extra safety)
            self._img_data = img_data
            
            self.update()
            
        except Exception as e:
            print(f"Error loading PIL image: {e}")
            import traceback
            traceback.print_exc()
    
    def set_tool(self, tool: ToolType, color: QColor = None, width: int = None):
        """Set active drawing tool"""
        self.active_tool = tool
        if color:
            self.tool_color = color
        if width:
            self.tool_width = width
    
    def mousePressEvent(self, event: QMouseEvent):
        """Start drawing annotation"""
        if event.button() == Qt.MouseButton.LeftButton and self.pil_image:
            pos = event.pos()
            
            if self.active_tool == ToolType.TEXT:
                # Text tool: mark position and request text input from parent
                self.text_position = pos
                self.pending_text = True
                self.update()
                
                # Request text input from toolbar/parent
                # This will be handled by the main window
                self.parent().request_text_for_annotation()
            else:
                # Other tools: start annotation
                self.current_annotation = Annotation(
                    tool=self.active_tool,
                    start=pos,
                    end=pos,
                    color=self.tool_color,
                    width=self.tool_width
                )
                self.is_drawing = True
                self.update()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Update annotation while drawing"""
        if self.is_drawing and self.current_annotation:
            self.current_annotation.end = event.pos()
            self.update()
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Finish annotation"""
        if event.button() == Qt.MouseButton.LeftButton and self.is_drawing:
            if self.current_annotation:
                self.current_annotation.end = event.pos()
                
                # Apply blur immediately if blur tool
                if self.active_tool == ToolType.BLUR:
                    self._apply_blur_to_image(self.current_annotation)
                    self.current_annotation = None
                else:
                    self.annotations.append(self.current_annotation)
                    self.current_annotation = None
                
            self.is_drawing = False
            self.update()
    
    def add_text_annotation(self, text: str):
        """Add text annotation at pending position"""
        if self.pending_text and self.text_position and text:
            annotation = Annotation(
                tool=ToolType.TEXT,
                start=self.text_position,
                color=self.tool_color,
                text=text,
                width=self.tool_width
            )
            self.annotations.append(annotation)
            self.pending_text = False
            self.text_position = None
            self.update()
    
    def _apply_blur_to_image(self, annotation: Annotation):
        """Apply blur effect directly to the image"""
        if not self.pil_image or not annotation.start or not annotation.end:
            return
        
        # Calculate region coordinates
        x1 = min(annotation.start.x(), annotation.end.x())
        y1 = min(annotation.start.y(), annotation.end.y())
        x2 = max(annotation.start.x(), annotation.end.x())
        y2 = max(annotation.start.y(), annotation.end.y())
        
        # Scale to image coordinates
        scale_x = self.pil_image.width / self.width()
        scale_y = self.pil_image.height / self.height()
        
        img_x1 = int(x1 * scale_x)
        img_y1 = int(y1 * scale_y)
        img_x2 = int(x2 * scale_x)
        img_y2 = int(y2 * scale_y)
        
        # Crop, blur, and paste back
        if img_x2 > img_x1 and img_y2 > img_y1:
            region = self.pil_image.crop((img_x1, img_y1, img_x2, img_y2))
            blurred = region.filter(ImageFilter.GaussianBlur(radius=15))
            self.pil_image.paste(blurred, (img_x1, img_y1))
            
            # Update display
            self.q_image = QImage(ImageQt.ImageQt(self.pil_image))
    
    def undo_last(self):
        """Remove last annotation"""
        if self.annotations:
            self.annotations.pop()
            self.update()
    
    def clear_annotations(self):
        """Clear all annotations"""
        self.annotations.clear()
        self.update()
    
    def paintEvent(self, event):
        """Draw image and annotations"""
        painter = QPainter(self)
        try:
            # THREAD SAFETY: Lock mutex when accessing pixmap
            with QMutexLocker(self._mx):
                if not self._pixmap:
                    return
                pixmap_copy = self._pixmap  # Get reference inside lock
            
            # Draw the image (scaled to fit)
            target_rect = self.rect()
            
            # Validate rect
            if target_rect.width() <= 0 or target_rect.height() <= 0:
                print(f"Warning: Invalid target rect: {target_rect.width()}x{target_rect.height()}")
                return
            
            # QUALITY FIX: Enable smooth scaling/anti-aliasing
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
            
            # Use QPixmap for faster painting than QImage
            painter.drawPixmap(target_rect, pixmap_copy)
            
            # Draw all completed annotations
            for annotation in self.annotations:
                try:
                    self._draw_annotation(painter, annotation)
                except Exception as e:
                    print(f"Warning: Failed to draw annotation: {e}")
            
            # Draw current annotation being created
            if self.current_annotation:
                try:
                    self._draw_annotation(painter, self.current_annotation)
                except Exception as e:
                    print(f"Warning: Failed to draw current annotation: {e}")
            
            # Draw text cursor if pending
            if self.pending_text and self.text_position:
                try:
                    pen = QPen(self.tool_color, 2, Qt.PenStyle.DashLine)
                    painter.setPen(pen)
                    painter.drawEllipse(self.text_position, 5, 5)
                except Exception as e:
                    print(f"Warning: Failed to draw text cursor: {e}")
                    
        except Exception as e:
            print(f"ERROR in paintEvent: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # CRITICAL: Always end the painter
            painter.end()
    
    def _draw_annotation(self, painter: QPainter, annotation: Annotation):
        """Draw a single annotation"""
        pen = QPen(annotation.color, annotation.width)
        painter.setPen(pen)
        
        if annotation.tool == ToolType.ARROW:
            self._draw_arrow(painter, annotation)
        elif annotation.tool == ToolType.BOX:
            self._draw_box(painter, annotation)
        elif annotation.tool == ToolType.PEN:
            self._draw_line(painter, annotation)
        elif annotation.tool == ToolType.TEXT:
            self._draw_text(painter, annotation)
    
    def _draw_arrow(self, painter: QPainter, annotation: Annotation):
        """Draw arrow annotation"""
        if not annotation.start or not annotation.end:
            return
        
        # Draw line
        painter.drawLine(annotation.start, annotation.end)
        
        # Draw arrowhead
        angle = QPoint.dotProduct(
            annotation.end - annotation.start,
            QPoint(1, 0)
        )
        # Simplified arrowhead
        dx = annotation.end.x() - annotation.start.x()
        dy = annotation.end.y() - annotation.start.y()
        length = (dx**2 + dy**2)**0.5
        
        if length > 0:
            # Normalize
            dx, dy = dx/length, dy/length
            # Arrowhead points
            arrow_size = 15
            left_x = annotation.end.x() - arrow_size * (dx + dy*0.5)
            left_y = annotation.end.y() - arrow_size * (dy - dx*0.5)
            right_x = annotation.end.x() - arrow_size * (dx - dy*0.5)
            right_y = annotation.end.y() - arrow_size * (dy + dx*0.5)
            
            painter.setBrush(QBrush(annotation.color))
            painter.drawPolygon([
                annotation.end,
                QPoint(int(left_x), int(left_y)),
                QPoint(int(right_x), int(right_y))
            ])
    
    def _draw_box(self, painter: QPainter, annotation: Annotation):
        """Draw box annotation"""
        if not annotation.start or not annotation.end:
            return
        
        # CRITICAL FIX: Clear brush so box is not filled
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        x1 = min(annotation.start.x(), annotation.end.x())
        y1 = min(annotation.start.y(), annotation.end.y())
        x2 = max(annotation.start.x(), annotation.end.x())
        y2 = max(annotation.start.y(), annotation.end.y())
        
        painter.drawRect(x1, y1, x2 - x1, y2 - y1)
    
    def _draw_line(self, painter: QPainter, annotation: Annotation):
        """Draw freehand line"""
        if not annotation.start or not annotation.end:
            return
        painter.drawLine(annotation.start, annotation.end)
    
    def _draw_text(self, painter: QPainter, annotation: Annotation):
        """Draw text annotation"""
        if not annotation.start or not annotation.text:
            return
        
        font = QFont("Arial", 14, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QPen(annotation.color))
        
        # Draw background
        metrics = painter.fontMetrics()
        text_rect = metrics.boundingRect(annotation.text)
        text_rect.moveTo(annotation.start)
        text_rect.adjust(-5, -5, 5, 5)
        
        painter.fillRect(text_rect, QColor(255, 255, 255, 200))
        painter.drawText(annotation.start, annotation.text)
    
    def render_annotated(self) -> Image.Image:
        """Render final image with all annotations burned in at high quality"""
        if not self.pil_image:
            return Image.new("RGB", (1, 1), "white")
        
        output = self.pil_image.copy()
        draw = ImageDraw.Draw(output)
        
        # Scale factors
        w, h = output.size
        scale_x = w / (self.width() or 1)
        scale_y = h / (self.height() or 1)
        
        # QUALITY FIX: Use higher base width for better visibility
        min_width = max(3, int(3 * scale_x))  # At least 3px, scaled up for large images
        
        # Draw each annotation on PIL image
        for annotation in self.annotations:
            if annotation.tool == ToolType.TEXT and annotation.text:
                # Draw text
                x = int(annotation.start.x() * scale_x)
                y = int(annotation.start.y() * scale_y)
                
                # QUALITY FIX: Use larger font size scaled to image
                font_size = max(24, int(32 * scale_y))  # Scale font with image
                
                # Try to load a good font
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    try:
                        # Try common font locations
                        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
                    except:
                        # Fallback to default (will be small)
                        font = ImageFont.load_default()
                
                # Draw white background for text
                bbox = draw.textbbox((x, y), annotation.text, font=font)
                draw.rectangle(bbox, fill=(255, 255, 255, 220))
                
                # Draw text with color
                color = (annotation.color.red(), annotation.color.green(), annotation.color.blue())
                draw.text((x, y), annotation.text, fill=color, font=font)
            
            elif annotation.tool in [ToolType.ARROW, ToolType.BOX, ToolType.PEN]:
                if not annotation.start or not annotation.end:
                    continue
                
                x1 = int(annotation.start.x() * scale_x)
                y1 = int(annotation.start.y() * scale_y)
                x2 = int(annotation.end.x() * scale_x)
                y2 = int(annotation.end.y() * scale_y)
                
                # CRITICAL FIX: Normalize coordinates so x1 <= x2 and y1 <= y2
                # This prevents "x1 must be greater than or equal to x0" error
                x1, x2 = min(x1, x2), max(x1, x2)
                y1, y2 = min(y1, y2), max(y1, y2)
                
                color = (annotation.color.red(), annotation.color.green(), annotation.color.blue())
                
                # QUALITY FIX: Scale width properly and ensure minimum visibility
                width = max(min_width, int(annotation.width * max(scale_x, scale_y)))
                
                if annotation.tool == ToolType.BOX:
                    draw.rectangle([x1, y1, x2, y2], outline=color, width=width)
                elif annotation.tool in [ToolType.ARROW, ToolType.PEN]:
                    draw.line([x1, y1, x2, y2], fill=color, width=width)
                    
                    # Add arrowhead for arrows
                    if annotation.tool == ToolType.ARROW:
                        dx = x2 - x1
                        dy = y2 - y1
                        length = (dx**2 + dy**2)**0.5
                        if length > 0:
                            dx, dy = dx/length, dy/length
                            # QUALITY FIX: Scale arrow size with image
                            arrow_size = max(20, int(30 * scale_x))
                            pts = [
                                (x2, y2),
                                (int(x2 - arrow_size * (dx + dy*0.5)), int(y2 - arrow_size * (dy - dx*0.5))),
                                (int(x2 - arrow_size * (dx - dy*0.5)), int(y2 - arrow_size * (dy + dx*0.5)))
                            ]
                            draw.polygon(pts, fill=color)
        
        return output
