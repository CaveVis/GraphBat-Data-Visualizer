# In your ui/src/draw_tool.py

# --- Imports ---
from PySide6.QtWidgets import QWidget, QSizePolicy # Make sure QSizePolicy is imported
from PySide6.QtGui import QPainter, QColor, QMouseEvent, QImage, QPixmap
from PySide6.QtCore import Qt, QRect, QSize, QPointF # Make sure QSize, QPointF are imported

import numpy as np

alp = QColor.fromRgbF(0.0, 0.0, 0.0, 0.0)
black = QColor.fromRgbF(0.0, 0.0, 0.0, 1.0)

class PaintGrid(QWidget):
    def __init__(self, brush_size=5, background=None, parent=None):
        super().__init__(parent)
        self.brush_size = brush_size
        self.is_drawing = False
        self.draw_value = 1

        self.background_pixmap = None
        self.image = None
        self._original_image_size = QSize(500, 500) # Default/fallback size

        # --- Load background and determine base size ---
        if background:
            temp_pixmap = QPixmap(background)
            if not temp_pixmap.isNull():
                self.background_pixmap = temp_pixmap
                self._original_image_size = self.background_pixmap.size() # Store original size
            else:
                print(f"Warning: Failed to load background image: {background}")
                # Keep default _original_image_size

        # --- Setup the drawing canvas based on original size ---
        self._setup_canvas(self._original_image_size)

        # --- Set Size Policy ---
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(100, 100) # Prevent collapsing
        self.updateGeometry()

    def _setup_canvas(self, size):
        """Initializes or reinitializes the drawing QImage."""
        if size.isEmpty() or not size.isValid():
            size = QSize(100, 100) # Ensure a valid size
        self.image = QImage(size, QImage.Format.Format_ARGB32_Premultiplied)
        self.image.fill(alp)

    def sizeCheck(self):
        if self._original_image_size.isValid() and self._original_image_size.width() > 0 and self._original_image_size.height() > 0:
             return self._original_image_size
        else:
             return QSize(500, 500) 


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        widget_rect = self.rect()
        target_rect = self._get_target_rect(widget_rect)

        if self.background_pixmap:
             painter.drawPixmap(target_rect, self.background_pixmap)
        if self.image:
             painter.drawImage(target_rect, self.image)

    def _get_target_rect(self, container_rect):
        """Calculates the centered rectangle within container_rect to draw the content."""
        original_size = self.sizeHint() # Use sizeHint to get the base size
        if original_size.isEmpty() or original_size.width() <= 0 or original_size.height() <= 0:
             return container_rect # Fallback if size is invalid

        aspect_ratio = original_size.width() / original_size.height()
        container_ratio = container_rect.width() / container_rect.height()

        target_size = QSize()
        if container_ratio > aspect_ratio:
            target_size.setHeight(container_rect.height())
            target_size.setWidth(int(container_rect.height() * aspect_ratio))
        else:
            target_size.setWidth(container_rect.width())
            target_size.setHeight(int(container_rect.width() / aspect_ratio))

        x_offset = (container_rect.width() - target_size.width()) / 2
        y_offset = (container_rect.height() - target_size.height()) / 2

        return QRect(int(container_rect.left() + x_offset),
                     int(container_rect.top() + y_offset),
                     max(1, target_size.width()),   # Ensure width >= 1
                     max(1, target_size.height())) # Ensure height >= 1


    def _map_widget_to_image(self, widget_pos: QPointF):
        if not self.image or self.image.isNull(): return None
        original_size = self.sizeHint() # Use base size for mapping
        if original_size.isEmpty() or original_size.width() <= 0 or original_size.height() <= 0: return None


        widget_rect = self.rect()
        target_rect = self._get_target_rect(widget_rect)

        if not target_rect.contains(widget_pos.toPoint()) or target_rect.width() <= 0 or target_rect.height() <= 0: return None

        relative_x = widget_pos.x() - target_rect.left()
        relative_y = widget_pos.y() - target_rect.top()

        scale_x = original_size.width() / target_rect.width()
        scale_y = original_size.height() / target_rect.height()

        image_x = relative_x * scale_x
        image_y = relative_y * scale_y

        image_x = max(0, min(image_x, self.image.width() - 1))
        image_y = max(0, min(image_y, self.image.height() - 1))

        return QPointF(image_x, image_y)

    def mousePressEvent(self, event: QMouseEvent):
        image_pos = self._map_widget_to_image(event.position())
        if image_pos:
            self.is_drawing = True
            self.apply_brush(image_pos)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.is_drawing:
            image_pos = self._map_widget_to_image(event.position())
            if image_pos:
                self.apply_brush(image_pos)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.is_drawing = False

    def apply_brush(self, image_pos: QPointF):
        if not self.image or self.image.isNull(): return
        color = black if self.draw_value == 1 else alp
        painter = QPainter(self.image)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(color)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
        brush_radius = self.brush_size / 2.0
        painter.drawEllipse(image_pos, brush_radius, brush_radius)
        painter.end()
        self.update()

    def clear_grid(self):
        if self.image:
            self.image.fill(alp)
            self.update()

    def set_brush_size(self, size):
        self.brush_size = max(1, size)

    def toggle_eraser(self):
        self.draw_value = 0 if self.draw_value == 1 else 1

    def get_mask(self):
        if not self.image or self.image.isNull(): return None
        mask = np.zeros((self.image.height(), self.image.width()), dtype=np.uint8)
        img_format = self.image.format() # Get format once

        # Use constBits() for read-only access, slightly safer
        ptr = self.image.constBits()
        # Important: Ensure the size is correct based on format BITS per pixel, not bytes sometimes
        bytes_per_pixel = self.image.depth() // 8
        expected_size = self.image.width() * self.image.height() * bytes_per_pixel
        ptr.setsize(expected_size) # Set size based on image properties

        try:
            arr = np.array(ptr, copy=False).reshape(self.image.height(), self.image.width(), bytes_per_pixel)

            # Check alpha channel based on format
            alpha_index = -1
            if img_format in (QImage.Format.Format_ARGB32_Premultiplied, QImage.Format.Format_ARGB32):
                alpha_index = 3 # Assuming BGRA byte order from Qt on many platforms
            elif img_format == QImage.Format.Format_RGBA8888:
                 alpha_index = 3 # Assuming RGBA
            # Add other formats if needed, e.g., Grayscale8 might use value > 0

            if alpha_index != -1:
                painted_mask = arr[:, :, alpha_index] > 0
                mask[painted_mask] = 1
            else: # If format doesn't have a clear alpha channel or not handled above
                 print(f"Using fallback pixel iteration for mask (Format: {img_format})")
                 for y in range(self.image.height()):
                     for x in range(self.image.width()):
                         if QColor(self.image.pixel(x, y)).alpha() > 0:
                             mask[y, x] = 1
        except Exception as e:
             print(f"Error processing image buffer for mask: {e}")
             print("Falling back to pixel iteration for mask.")
             for y in range(self.image.height()):
                 for x in range(self.image.width()):
                     if QColor(self.image.pixel(x, y)).alpha() > 0:
                          mask[y, x] = 1
        return mask