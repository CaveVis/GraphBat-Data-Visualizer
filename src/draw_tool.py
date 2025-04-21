from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtGui import QPainter, QColor, QMouseEvent, QImage, QPixmap
from PySide6.QtCore import Qt, QRect, QSize, QPoint, QPointF 

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as Navi
alp = QColor.fromRgbF(0.0, 0.0, 0.0, 0.0)
red = QColor.fromRgbF(1.0, 0.0, 0.0, 0.5)

class PaintGrid(QWidget):
    def __init__(self, brush_size=5, background=None, parent=None):
        fig = FigureCanvasQTAgg()
        super().__init__(fig)
        self.setParent(parent)

        self.background_pixmap = QPixmap(background) if background else None
        self.scaled_pixmap = None
        self.brush_size = brush_size
        self.is_drawing = False
        self.draw_value = 1

        self.drawing_image = QImage(self.background_pixmap.size(), QImage.Format_ARGB32)
        self.drawing_image.fill(Qt.transparent)

        self._image_rect = QRect()

    def resizeEvent(self, event):
        if self.background_pixmap:
            # Maintain aspect ratio
            self.scaled_pixmap = self.background_pixmap.scaled(
                self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )

            # Center the image
            x = (self.width() - self.scaled_pixmap.width()) // 2
            y = (self.height() - self.scaled_pixmap.height()) // 2
            self._image_rect = QRect(x, y, self.scaled_pixmap.width(), self.scaled_pixmap.height())
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.scaled_pixmap:
            painter.drawPixmap(self._image_rect, self.scaled_pixmap)
        # Draw on top
        painter.drawImage(self._image_rect, self.drawing_image)
        painter.end()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self._image_rect.contains(event.pos()):
            self.is_drawing = True
            self._draw_at(event.pos())

    def mouseMoveEvent(self, event):
        if self.is_drawing and self._image_rect.contains(event.pos()):
            self._draw_at(event.pos())

    def mouseReleaseEvent(self, event):
        self.is_drawing = False

    def _draw_at(self, pos):
        # Convert widget pos to image-relative pos
        x = (pos.x() - self._image_rect.x()) * self.background_pixmap.width() / self._image_rect.width()
        y = (pos.y() - self._image_rect.y()) * self.background_pixmap.height() / self._image_rect.height()

        painter = QPainter(self.drawing_image)
        # Set composition mode to Source to *overwrite* pixels instead of blending
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        color = red if self.draw_value == 1 else Qt.transparent
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        painter.drawEllipse(QPoint(int(x), int(y)), self.brush_size, self.brush_size)
        painter.end()
        self.update()


    def clear_grid(self):
        if self.drawing_image:
            self.drawing_image.fill(Qt.transparent)
            self.update()


    def set_brush_size(self, size):
        self.brush_size = max(1, size)

    def toggle_eraser(self):
        self.draw_value = 0 if self.draw_value == 1 else 1

    def get_mask(self):
      
        if not self.drawing_image or self.drawing_image.isNull():
            return None

        mask = np.zeros((self.drawing_image.height(), self.drawing_image.width()), dtype=np.uint8)
        img_format = self.drawing_image.format()

        ptr = self.drawing_image.constBits()
        bytes_per_pixel = self.drawing_image.depth() // 8
        expected_size = self.drawing_image.width() * self.drawing_image.height() * bytes_per_pixel
        ptr.setsize(expected_size)

        try:
            arr = np.array(ptr, copy=False).reshape(self.drawing_image.height(), self.drawing_image.width(), bytes_per_pixel)

            alpha_index = -1
            if img_format in (QImage.Format.Format_ARGB32_Premultiplied, QImage.Format.Format_ARGB32):
                alpha_index = 3  # BGRA
            elif img_format == QImage.Format.Format_RGBA8888:
                alpha_index = 3  # RGBA

            if alpha_index != -1:
                painted_mask = arr[:, :, alpha_index] > 0
                mask[painted_mask] = 1
            else:
                print(f"Using fallback pixel iteration for mask (Format: {img_format})")
                for y in range(self.drawing_image.height()):
                    for x in range(self.drawing_image.width()):
                        if QColor(self.drawing_image.pixel(x, y)).alpha() > 0:
                            mask[y, x] = 1
        except Exception as e:
            print(f"Error processing image buffer for mask: {e}")
            print("Falling back to pixel iteration for mask.")
            for y in range(self.drawing_image.height()):
                for x in range(self.drawing_image.width()):
                    if QColor(self.drawing_image.pixel(x, y)).alpha() > 0:
                        mask[y, x] = 1

        return mask
