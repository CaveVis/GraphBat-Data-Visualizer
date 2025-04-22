from PySide6.QtWidgets import (QWidget, QDialog, QPushButton, QVBoxLayout,
                               QHBoxLayout, QLabel, QLineEdit, QApplication) 
from PySide6.QtGui import (QPainter, QColor, QMouseEvent, QImage, QPixmap,
                           QIntValidator)
from PySide6.QtCore import Qt, QRect, QSize, QPoint, Signal 

import numpy as np
import sys 

# Define colors outside class for clarity
COLOR_TRANSPARENT = QColor.fromRgbF(0.0, 0.0, 0.0, 0.0)
COLOR_DRAW = QColor.fromRgbF(1.0, 0.0, 0.0, 0.5) # Semi-transparent red

# Dedicated Drawing Canvas Widget
class DrawingCanvas(QWidget):
    def __init__(self, background_pixmap=None, parent=None):
        super().__init__(parent)
        self.parent_dialog = parent # Reference to the main dialog

        self.background_pixmap = background_pixmap if background_pixmap else QPixmap()
        self.scaled_pixmap = self.background_pixmap # Initially same size
        self.drawing_image = QImage(self.background_pixmap.size(), QImage.Format_ARGB32)
        self.drawing_image.fill(COLOR_TRANSPARENT)

        self._image_rect = QRect()
        self.is_drawing = False

        # Ensure the canvas can receive mouse events
        self.setMouseTracking(True)
        # Set a minimum size hint based on the image
        if not self.background_pixmap.isNull():
             self.setMinimumSize(self.background_pixmap.size() / 2) # Example minimum size


    def resizeEvent(self, event):
        if not self.background_pixmap.isNull():
            # Scale pixmap to fit canvas size while maintaining aspect ratio
            self.scaled_pixmap = self.background_pixmap.scaled(
                self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )

            # Center the scaled pixmap within the canvas widget
            x = (self.width() - self.scaled_pixmap.width()) // 2
            y = (self.height() - self.scaled_pixmap.height()) // 2
            self._image_rect = QRect(x, y, self.scaled_pixmap.width(), self.scaled_pixmap.height())
        else:
             self._image_rect = self.rect() # Fill whole area if no background

        self.update() # Trigger repaint
        super().resizeEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw background
        if not self.scaled_pixmap.isNull():
            painter.drawPixmap(self._image_rect.topLeft(), self.scaled_pixmap)

        # Draw the user's drawing on top, scaled to the current display rect
        painter.drawImage(self._image_rect, self.drawing_image)

        painter.end()

    def mousePressEvent(self, event: QMouseEvent):
        # Start drawing only if left button is pressed within the image area
        if event.button() == Qt.LeftButton and self._image_rect.contains(event.pos()):
            self.is_drawing = True
            self._draw_at(event.pos()) # Draw first point immediately
            event.accept() # Indicate event was handled
        else:
            event.ignore() # Pass event up if not handled


    def mouseMoveEvent(self, event: QMouseEvent):
        # Continue drawing if mouse is moving while button is pressed and within image area
        if self.is_drawing and self._image_rect.contains(event.pos()):
            self._draw_at(event.pos())
            event.accept()
        else:
             event.ignore()


    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.is_drawing:
            self.is_drawing = False
            event.accept()
        else:
            event.ignore()


    def _draw_at(self, widget_pos: QPoint):
        # Check if parent dialog exists and has the required attributes
        if not self.parent_dialog or not hasattr(self.parent_dialog, 'brush_size') or not hasattr(self.parent_dialog, 'draw_value'):
             print("Error: Cannot access parent dialog properties.")
             return
        # Ensure we don't divide by zero if the rect is empty
        if self._image_rect.width() == 0 or self._image_rect.height() == 0:
            return

        # Calculate position relative to the top-left corner of the image rect
        relative_x = widget_pos.x() - self._image_rect.x()
        relative_y = widget_pos.y() - self._image_rect.y()

        # Scale the relative position to the original image dimensions
        original_x = (relative_x * self.background_pixmap.width()) / self._image_rect.width()
        original_y = (relative_y * self.background_pixmap.height()) / self._image_rect.height()


        painter = QPainter(self.drawing_image)
        painter.setRenderHint(QPainter.Antialiasing)

        # Use CompositionMode_Source to replace pixels (for both drawing and erasing)
        painter.setCompositionMode(QPainter.CompositionMode_Source)

        color = COLOR_DRAW if self.parent_dialog.draw_value == 1 else COLOR_TRANSPARENT
        painter.setBrush(color)
        painter.setPen(Qt.NoPen) # No outline for the brush stroke

        # Draw ellipse centered at the calculated original image coordinates
        # QPointF allows for sub-pixel precision if needed, though drawEllipse takes ints
        draw_point = QPoint(int(original_x), int(original_y))
        brush_radius = self.parent_dialog.brush_size # Use diameter for drawEllipse width/height
        painter.drawEllipse(draw_point, brush_radius, brush_radius)

        painter.end()
        self.update() # Trigger a repaint of the canvas widget


    def clear_drawing(self):
        if self.drawing_image:
            self.drawing_image.fill(COLOR_TRANSPARENT)
            self.update()

# Main Dialog Window 
class PaintGrid(QDialog):
    mask_exported = Signal(np.ndarray) # Signal to emit the mask

    def __init__(self, brush_size=10, background_path=None, parent=None): # Increased default brush size
        super().__init__(parent)
        self.setWindowTitle("Drawing Tool")

        self.brush_size = brush_size
        self.draw_value = 1 # 1 for drawing, 0 for erasing
        self.output_mask = None # To store the final mask

        try:
            background_pixmap = QPixmap(background_path) if background_path else QPixmap()
            if background_pixmap.isNull() and background_path:
                print(f"Warning: Could not load background image from: {background_path}")
        except Exception as e:
             print(f"Error loading background image: {e}")
             background_pixmap = QPixmap() # Use empty pixmap if loading fails


        #Main Layout (Vertical)
        self.main_layout = QVBoxLayout(self)

        # Drawing Canvas
        self.canvas = DrawingCanvas(background_pixmap, parent=self)
        self.main_layout.addWidget(self.canvas, 1) # Add canvas, allow it to stretch (stretch factor 1)

        #Control Buttons Layout (Horizontal) 
        self.controls_layout = QHBoxLayout()

        # Brush Size
        self.brush_size_label = QLabel(f"Brush Size: {self.brush_size}")
        self.controls_layout.addWidget(self.brush_size_label)
        self.brush_size_input = QLineEdit(str(self.brush_size))
        self.brush_size_input.setValidator(QIntValidator(1, 100))
        self.brush_size_input.setFixedWidth(40) # Make input field smaller
        self.brush_size_input.textChanged.connect(self._update_brush_size)
        self.controls_layout.addWidget(self.brush_size_input)
        self.controls_layout.addSpacing(20) # Add space

        # Eraser Toggle
        self.eraser_button = QPushButton("Eraser (OFF)")
        self.eraser_button.setCheckable(True) # Make it act like a toggle
        self.eraser_button.clicked.connect(self.toggle_eraser)
        self.controls_layout.addWidget(self.eraser_button)

        # Clear Button
        self.clear_button = QPushButton("Clear Drawing")
        self.clear_button.clicked.connect(self.clear_canvas)
        self.controls_layout.addWidget(self.clear_button)

        # Export Button
        self.export_button = QPushButton("Export Mask & Close")
        self.export_button.clicked.connect(self.get_mask)
        self.controls_layout.addWidget(self.export_button)

        # Add controls layout to the main layout
        self.main_layout.addLayout(self.controls_layout)


        # Set Initial Dialog Size 
        if not background_pixmap.isNull():
             # Set size based on image + padding for controls
             img_w = background_pixmap.width()
             img_h = background_pixmap.height()
             # Make initial size reasonable, e.g., max 800x600 display for image part
             display_w = min(img_w, 800)
             display_h = min(img_h, 600)
             padding_h = 80 # Approximate height needed for controls + margins
             self.resize(max(display_w, 400), display_h + padding_h) # Ensure minimum width
        else:
             self.resize(600, 450) # Default size if no image

    def _update_brush_size(self, text):
        try:
            size = int(text)
            if size < 1:
                size = 1
            elif size > 10000:
                 size = 10000 # Clamp to max if validator somehow fails
            self.brush_size = size
            self.brush_size_label.setText(f"Brush Size: {self.brush_size}")
        except ValueError:
             # Handle case where input is temporarily empty or invalid
             self.brush_size_label.setText("Brush Size: -")


    def toggle_eraser(self, checked):
        if checked:
            self.draw_value = 0 # Erase mode
            self.eraser_button.setText("Eraser (ON)")
        else:
            self.draw_value = 1 # Draw mode
            self.eraser_button.setText("Eraser (OFF)")

    def clear_canvas(self):
        self.canvas.clear_drawing()

    def get_mask(self) -> np.ndarray | None:
        """Generates the mask from the drawing_image."""
        target_image = self.canvas.drawing_image
        if not target_image or target_image.isNull():
            print("Error: Drawing image is invalid.")
            return None

        
        original_format = target_image.format()
        if original_format != QImage.Format_ARGB32:
             # Keep a reference to the converted image if conversion happens
             target_image = target_image.convertToFormat(QImage.Format_ARGB32)
             if target_image.isNull():
                 print(f"Error: Failed to convert image from {original_format} to ARGB32.")
                 return None


        height = target_image.height()
        width = target_image.width()
        mask = np.zeros((height, width), dtype=np.uint8)

    
        try:
             bytes_per_pixel = target_image.depth() // 8
             if bytes_per_pixel != 4: # Expecting 4 bytes for ARGB32
                 raise ValueError(f"Unexpected bytes per pixel: {bytes_per_pixel} for format {target_image.format()}")

             expected_size = width * height * bytes_per_pixel

             # Get the memory view for the image buffer
             ptr = target_image.constBits() # Returns a memoryview in PySide6


             actual_size = len(ptr)
             if actual_size < expected_size:
                  raise ValueError(f"Buffer size mismatch. Expected {expected_size}, got {actual_size}")



             # Create numpy array view from the buffer (no data copy)
             # Pass the memoryview directly to frombuffer
             # If the buffer is larger than needed (e.g., due to byte alignment),
             # slice the numpy array *after* creation based on expected size.
             arr_flat = np.frombuffer(ptr, dtype=np.uint8)

             # Check if flat array size matches expected size before reshaping
             if arr_flat.size < expected_size:
                 raise ValueError(f"Numpy array size {arr_flat.size} is smaller than expected {expected_size} after frombuffer.")

             # Take only the expected part of the buffer and reshape
             arr = arr_flat[:expected_size].reshape((height, width, bytes_per_pixel))

             # Alpha channel is the last one in ARGB32 (index 3)
             alpha_channel = arr[:, :, 3]
             mask[alpha_channel > 0] = 1 # Set mask to 1 where alpha > 0

            
             self.accept()
             mask = np.flipud(mask) 
             self.output=mask
             np.save("my_array.npy", mask)   ################### This needs to go to project files 
             return mask

        except Exception as e:
             print(f"Error processing image buffer for mask: {e}")
             print("Falling back to slower pixel-by-pixel iteration for mask.")
             #iterate pixel by pixel (slower)
             for y in range(height):
                 for x in range(width):
                     pixel_color = QColor(target_image.pixel(x, y))
                     if pixel_color.alpha() > 0:
                         mask[y, x] = 1


             self.accept()
             mask = np.flipud(mask) 
             self.output = mask
             np.save("my_array.npy", mask)   ################### This needs to go to project files 
             return mask

