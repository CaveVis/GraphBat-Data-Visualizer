from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSpinBox, QHBoxLayout, QLabel
from PySide6.QtGui import QPainter, QColor, QMouseEvent, QImage
from PySide6.QtCore import Qt, QRect
import numpy as np


##
##
## Not complete and kinda buggy right now
##
##
class PaintGrid(QWidget):
    window_size = 1000
    def __init__(self, brush_size = 5, grid_size=100):
        super().__init__()
        self.grid_size = grid_size
        self.cell_size = self.window_size / self.grid_size
        self.fixed_size = 1000
        self.setFixedSize(self.window_size, self.window_size)
        self.is_drawing = False
        self.draw_value = 1
        self.brush_size = brush_size
        self.image = QImage(self.width(), self.height(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)

    def mousePressEvent(self, event: QMouseEvent):
        self.is_drawing = True
        self.apply_brush(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.is_drawing:
            self.apply_brush(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.is_drawing = False
    
    def apply_brush(self, event):
        col = int(event.position().x()) // self.cell_size
        row = int(event.position().y()) // self.cell_size

        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            color = QColor(0, 0, 0) if self.draw_value == 1 else QColor(255, 255, 255)
            painter = QPainter(self.image)
            painter.setPen(color)
            painter.setBrush(color)

            brush_size_px = self.brush_size * self.cell_size

            top_left_x = int((col * self.cell_size) - (brush_size_px / 2))
            top_left_y = int((row * self.cell_size) - (brush_size_px / 2))

            painter.drawRect(top_left_x, top_left_y, brush_size_px, brush_size_px)
            self.update(QRect(top_left_x, top_left_y, brush_size_px, brush_size_px))  # Update only the affected area"


    def clear_grid(self):
        self.image.fill(Qt.white)
        self.update()

    def set_brush_size(self, size):
        self.brush_size = size

    def toggle_eraser(self):
        self.draw_value = 0 if self.draw_value == 1 else 1

    def get_mask(self):
        mask = np.zeros((self.grid_size, self.grid_size), dtype=int)
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                pixel_color = QColor(self.image.pixel(x * self.cell_size, y * self.cell_size))
                mask[y, x] = 1 if pixel_color == QColor(0, 0, 0) else 0
        return mask.tolist()


class MainApp(QWidget):
    def __init__(self, brush_size=5):
        super().__init__()
        self.setWindowTitle("Paint Grid Mask")
        self.layout = QVBoxLayout()

        controls_layout = QHBoxLayout()

        self.grid_size_input = QSpinBox()
        self.grid_size_input.setRange(10, 10000)  
        self.grid_size_input.setValue(100)
        
        controls_layout.addWidget(self.grid_size_input)

        self.generate_button = QPushButton("Generate Grid")
        self.generate_button.clicked.connect(self.create_grid)
        controls_layout.addWidget(self.generate_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_grid)
        controls_layout.addWidget(self.clear_button)

        
        self.brush_size_input = QSpinBox()
        self.brush_size_input.setRange(1, 1000)
        self.brush_size_input.setValue(5)
        self.brush_size_input.valueChanged.connect(self.set_brush_size)
        controls_layout.addWidget(QLabel("Brush Size:"))
        controls_layout.addWidget(self.brush_size_input)

        self.eraser_button = QPushButton("Eraser")
        self.eraser_button.clicked.connect(self.toggle_eraser)
        controls_layout.addWidget(self.eraser_button)

        self.layout.addLayout(controls_layout)

        self.export_button = QPushButton("Export Mask")
        self.export_button.clicked.connect(self.export_mask)
        self.layout.addWidget(self.export_button)

        self.grid_widget = PaintGrid()
        self.layout.addWidget(self.grid_widget)
        self.setLayout(self.layout)

    def create_grid(self):
        self.grid_size = self.grid_size_input.value()
        self.brush_size = self.brush_size_input.value()
        self.layout.removeWidget(self.grid_widget)
        self.grid_widget.deleteLater()
        self.grid_widget = PaintGrid(self.brush_size, self.grid_size)
        self.layout.addWidget(self.grid_widget)

    def clear_grid(self):
        self.grid_widget.clear_grid()

    def set_brush_size(self):
        self.grid_widget.set_brush_size(self.brush_size_input.value())

    def toggle_eraser(self):
        self.grid_widget.toggle_eraser()

    def export_mask(self):
        mask = self.grid_widget.get_mask()
        print("Exported Mask:", mask)


if __name__ == "__main__":
    app = QApplication([])
    window = MainApp()
    window.show()
    app.exec()
