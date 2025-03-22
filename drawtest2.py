from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSpinBox, QHBoxLayout, QLabel, QFileDialog
from PySide6.QtGui import QPainter, QColor, QMouseEvent, QImage, QPixmap
from PySide6.QtCore import Qt, QRect
import numpy as np

alp = QColor.fromRgbF(0.0,0.0,0.0,0.0)
black = QColor.fromRgbF(0.0,0.0,0.0,1.0)
WINDOW_SIZE = 800
class PaintGrid(QWidget):
    def __init__(self, brush_size=5, grid_x=1000, grid_y = 1000, reso = 1000, background = None):
        super().__init__()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.brush_size = brush_size
        self.is_drawing = False
        self.draw_value = 1
        self.resoltion = reso
        self.cell_size = 1
        self.window_size = WINDOW_SIZE
        # Load the background image and determine size
        self.background = background
        if self.background:
            self.background = QPixmap(self.background)
            self.img_width = self.background.width()
            self.img_height = self.background.height()

            self.grid_x = self.img_width
            self.grid_y = self.img_height
            fix = grid_x / reso

            self.cell_size = self.grid_x / self.resoltion if self.resoltion else 1


            
            # Ensure image scales proportionally to a max size (optional)
              # You can adjust this if needed
            if self.img_width > WINDOW_SIZE or self.img_height > WINDOW_SIZE:
                scale_factor = WINDOW_SIZE / max(self.img_width, self.img_height)
                self.img_width = int(self.img_width * scale_factor)
                self.img_height = int(self.img_height * scale_factor)
                self.background = self.background.scaled(self.img_width, self.img_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        else:
            # Default size if no image is provided
            self.img_width, self.img_height = 800, 800

        if background:
            self.backg_image = QPixmap(background).scaled(self.window_size, self.window_size, Qt.KeepAspectRatioByExpanding)


        self.setFixedSize(self.img_width, self.img_height)  # Set canvas size to match image
        self.image = QImage(self.img_width, self.img_height, QImage.Format_RGBA64)
        self.image.fill(QColor(0, 0, 0, 0))  # Transparent background

    def paintEvent(self, event):
        painter = QPainter(self)

        # Draw background image first
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

        if 0 <= row < self.grid_y and 0 <= col < self.grid_x:
            color = black if self.draw_value == 1 else alp

            painter = QPainter(self.image)
            painter.setPen(color)
            painter.setBrush(color)
            painter.setCompositionMode(QPainter.CompositionMode_Source)

            brush_size_px = self.brush_size * self.cell_size

            top_left_x = int((col * self.cell_size) - (brush_size_px / 2))
            top_left_y = int((row * self.cell_size) - (brush_size_px / 2))

            painter.drawRect(top_left_x, top_left_y, brush_size_px, brush_size_px)
            self.update(QRect(top_left_x, top_left_y, brush_size_px, brush_size_px))  # Update only the affected area"


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
        mask = np.zeros((self.grid_y, self.grid_x), dtype=int)

        cell_width = self.image.width() / self.grid_x
        cell_height = self.image.height() / self.grid_y

        for x in range(self.grid_x):
            for y in range(self.grid_y):
                px = int(x * cell_width)
                py = int(y * cell_height)

                if px >= self.image.width() or py >= self.image.height():
                    continue

                pixel_color = QColor.fromRgba(self.image.pixel(px, py))

                # Flip the y-axis mapping
                flipped_y = self.grid_y - 1 - y  # Reverse row order

                if pixel_color.alpha() > 0 and pixel_color == black:
                    mask[flipped_y, x] = 1
                else:
                    mask[flipped_y, x] = 0

        return mask


class MainApp(QWidget):
    def __init__(self, brush_size=5, background = None):
        super().__init__()
        self.setWindowTitle("Paint Grid with Adaptive Canvas")
        self.layout = QVBoxLayout()
        self.background = background

        controls_layout = QHBoxLayout()

        self.generate_button1 = QPushButton("Select Image")
        self.generate_button1.clicked.connect(self.get_backimage)
        controls_layout.addWidget(self.generate_button1)


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

        # Pass background image path
        self.grid_widget = PaintGrid(brush_size, 100, background)
        self.layout.addWidget(self.grid_widget)
        self.setLayout(self.layout)

    def create_grid(self):
        self.brush_size = self.brush_size_input.value()

        # Remove and delete the existing widget
        self.layout.removeWidget(self.grid_widget)
        self.grid_widget.deleteLater()

        # Ensure the image is loaded correctly
        image = QImage(self.background)
        grid_x = image.width()
        grid_y = image.height()

        # Create a new grid with the updated background image and correct size
        self.grid_widget = PaintGrid(self.brush_size, grid_x, grid_y, reso=grid_x, background=self.background)

        self.layout.addWidget(self.grid_widget)


    def get_backimage(self):
        file, _ = QFileDialog.getOpenFileName(self, self.tr("Open File"), "", self.tr("Images (*.png *.jpg)"))
        if file:  # Ensure a file was selected
            self.background = file
            self.create_grid()



    def clear_grid(self):
        self.grid_widget.clear_grid()

    def set_brush_size(self):
        self.grid_widget.set_brush_size(self.brush_size_input.value())

    def toggle_eraser(self):
        self.grid_widget.toggle_eraser()

    def export_mask(self):
        mask = self.grid_widget.get_mask()
        print("Exported Mask:", mask)
        np.save('my_array.npy', mask)
if __name__ == "__main__":
    app = QApplication([])
    window = MainApp()
    window.show()
    app.exec()
