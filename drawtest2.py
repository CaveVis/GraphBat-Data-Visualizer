from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSpinBox, QHBoxLayout, QLabel
from PySide6.QtGui import QPainter, QColor, QMouseEvent, QImage, QPixmap
from PySide6.QtCore import Qt, QRect
import numpy as np

alp = QColor.fromRgbF(0.0,0.0,0.0,0.0)
black = QColor.fromRgbF(0.0,0.0,0.0,1.0)

class PaintGrid(QWidget):
    def __init__(self, brush_size=5, grid_size=1000, background_path=None):
        super().__init__()
        self.grid_size = grid_size
        self.brush_size = brush_size
        self.is_drawing = False
        self.draw_value = 1

        # Load the background image and determine size
        self.background = None
        if background_path:
            self.background = QPixmap(background_path)
            self.img_width = self.background.width()
            self.img_height = self.background.height()

            self.cell_size = self.background.width() / self.grid_size
            
            max_size = 800  #  adjust if needed
            if self.img_width > max_size or self.img_height > max_size:
                scale_factor = max_size / max(self.img_width, self.img_height)
                self.img_width = int(self.img_width * scale_factor)
                self.img_height = int(self.img_height * scale_factor)
                self.background = self.background.scaled(self.img_width, self.img_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        else:
            # Default size if no image is provided
            self.img_width, self.img_height = 800, 800

        self.setFixedSize(self.img_width, self.img_height)  # Set canvas size to match image
        self.image = QImage(self.img_width, self.img_height, QImage.Format_RGBA64)
        self.image.fill(QColor(0, 0, 0, 0))  # Transparent background

    def paintEvent(self, event):
        painter = QPainter(self)


        if self.background:
            painter.drawPixmap(0, 0, self.background)

        # Draw the painting layer on top
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
            color = black if self.draw_value == 1 else alp

            painter = QPainter(self.image)
            painter.setPen(color)
            painter.setBrush(color)
            painter.setCompositionMode(QPainter.CompositionMode_Source)

            brush_size_px = self.brush_size * self.cell_size

            top_left_x = int((col * self.cell_size) - (brush_size_px / 2))
            top_left_y = int((row * self.cell_size) - (brush_size_px / 2))

            painter.drawRect(top_left_x, top_left_y, brush_size_px, brush_size_px)
            self.update(QRect(top_left_x, top_left_y, brush_size_px, brush_size_px))  


    def clear_grid(self):
        self.image.fill(alp)
        self.update()

    def set_brush_size(self, size):
        self.brush_size = size

    def toggle_eraser(self):
        self.draw_value = 0 if self.draw_value == 1 else 1

    def set_background_image(self, image):
        self.bg_image = image
        self.update()

    def get_mask(self):
        mask = np.zeros((self.grid_size, self.grid_size), dtype=int)

        # Map grid size to image size
        cell_width = self.image.width() / self.grid_size
        cell_height = self.image.height() / self.grid_size

        for x in range(self.grid_size):
            for y in range(self.grid_size):
                # Convert grid coordinates to image pixel coordinates
                px = int(x * cell_width)
                py = int(y * cell_height)

                # Get pixel color
                pixel_color = QColor.fromRgba(self.image.pixel(px, py))

                # Check if black or transparent
                if pixel_color.alpha() > 0 and pixel_color == black:  
                    mask[y, x] = 1
                else: 
                    mask[y, x] = 0

        return mask.tolist()
    
class MainApp(QWidget):
    def __init__(self, brush_size=5, background_path="Howards_Waterfall_Cave_Map-1.png"):
        super().__init__()
        self.setWindowTitle("Paint Grid with Adaptive Canvas")
        self.layout = QVBoxLayout()
        self.background = QPixmap(background_path)
        controls_layout = QHBoxLayout()

        self.grid_size_input = QSpinBox()
        self.grid_size_input.setRange(10, 10000)
        self.grid_size_input.setValue(1000)
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


        self.grid_widget = PaintGrid(brush_size, 100, background_path)
        self.layout.addWidget(self.grid_widget)
        self.setLayout(self.layout)

    def create_grid(self):
        self.grid_size = self.grid_size_input.value()
        self.brush_size = self.brush_size_input.value()

        background_path = "Howards_Waterfall_Cave_Map-1.png"  

        self.layout.removeWidget(self.grid_widget)
        self.grid_widget.deleteLater()

        # Create new grid with the same background image
        self.grid_widget = PaintGrid(self.brush_size, self.grid_size, background_path)

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
        with open("output_list.txt", 'w') as file:
            for item in mask:
                file.write(str(item) + '\n')
            print("Done writing file")

if __name__ == "__main__":
    app = QApplication([])
    window = MainApp()
    window.show()
    app.exec()
