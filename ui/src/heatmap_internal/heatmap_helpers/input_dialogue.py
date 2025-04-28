import os
import shutil
import datetime
import pandas as pd
import numpy as np
import traceback
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import (QApplication, QMainWindow, QSizeGrip, QFileDialog, QWidget,
                                QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QComboBox, QListWidget, QAbstractItemView, QListWidgetItem,
                                QLineEdit, QPushButton, QDialogButtonBox, QMessageBox, QDialog, QTableWidget,QHeaderView, QTableWidgetItem, QFormLayout)
from PySide6.QtGui import QIntValidator, QPixmap
from PySide6.QtCore import Qt, QSize
from src.project_management.project_manager import ProjectManager 
import glob

class InputDialogue(QDialog):
    def __init__(self, parent=None, dataframe=None):
        
        self.proj_name = ProjectManager.get_project()
        super(InputDialogue, self).__init__(parent)
        self.setWindowTitle("Heatmap Input")
        self.resize(600, 400)
        


        self.project_name = ProjectManager.get_project()
        
        if self.project_name is None:
            QMessageBox.warning(
                self,
                "No Project Loaded",
                "Please load a project before plotting data."
            )
            return
   

        base_data_dir = os.path.join("Projects", self.project_name, "datafiles")
        self.image_data_dir = os.path.join(base_data_dir, "images")                                           ### create new folder in Proj Man for this 

        
        # Main layout
        self.layout = QFormLayout(self)
        self.dataframe = dataframe

        # Create widgets

        
        self.image_combo = QComboBox()
        self.populate_image_combo()
        self.image_combo.currentIndexChanged.connect(self.update_background_path)
        self.sensor_button = QPushButton("Set Sensor Locations", clicked = self.set_sensor)
        self.set_mask_button = QPushButton("Select Mask", clicked = self.set_mask)
        self.sdev_button = QComboBox()
        self.sdev_button.addItems(["1", "2", "3", "4", "5"])

        self.index_start = QLineEdit()
        self.index_start.setValidator(QIntValidator(1, 100000000))

        self.index_end = QLineEdit()
        self.index_end.setValidator(QIntValidator(1, 100000000))

        self.index_skip = QLineEdit()
        self.index_skip.setValidator(QIntValidator(1, 100000000))

        self.set_mode = QComboBox()
        self.set_mode.addItems(["Linear", "Dijkstra's"])

        self.cancel_button = QPushButton("Cancel", clicked = self.cancel)
        self.submit_button = QPushButton("Submit", clicked = self.submit)    

        self.layout.addRow("Select Image:", self.image_combo)
        self.layout.addRow("Colormap Scale (Standard Deviations from mean):", self.sdev_button)
        self.layout.addRow("Start Index:", self.index_start)
        self.layout.addRow("End Index:", self.index_end)
        self.layout.addRow("Skip Every N Rows:", self.index_skip)
        self.layout.addRow("Distance Mode:", self.set_mode)
        self.layout.addRow(self.sensor_button)
        self.layout.addRow(self.set_mask_button)
        self.layout.addRow(self.submit_button, self.cancel_button)                      
        self.sensor_positions = {}


    def populate_image_combo(self):
        if not os.path.exists(self.image_data_dir):
            return
        
        # Find all image files
        image_extensions = ['*.png', '*.jpg', '*.jpeg']
        files = []
        for ext in image_extensions:
            files.extend(glob.glob(os.path.join(self.image_data_dir, ext)))

        files.sort()  # Optional: alphabetically sort

        # Store full paths inside the combo's "userData"
        for file in files:
            filename = os.path.basename(file)
            self.image_combo.addItem(filename, userData=file)
        
        # Default selection
        if files:
            self.background_path = files[0]

    def update_background_path(self, index):
        if index >= 0:
            self.background_path = self.image_combo.itemData(index)

    def set_sensor(self):
        sensor_names = self.dataframe.columns  # skip index/timestamp
        picker = SensorPicker(self.background_path, sensor_names, self)
        picker.exec()
        

        self.sensor_positions = picker.get_positions()

  

        print()

    def set_mask(self):
        choice = QMessageBox.question(self, "Mask Input",
            "Would you like to draw a new mask?\nSelect 'No' to load one from file.",
            QMessageBox.Yes | QMessageBox.No)

        if choice == QMessageBox.Yes:
            # Launch draw tool as a window
            from src.draw_tool import PaintGrid  

            draw_win = PaintGrid(background_path=self.background_path) 
            draw_win.exec()
            self.mask = draw_win.get_mask()
        else:
            mask_path, _ = QFileDialog.getOpenFileName(self, "Select Mask File", self.image_data_dir, "NPY Files (*.npy)")
            if mask_path:
                self.mask = np.load(mask_path)

    def cancel(self):
        self.reject()
        print()
    def submit(self):
         self.accept()  
         self.output = {
        "sensor_positions": self.sensor_positions,
        "sdev": int(self.sdev_button.currentText()),
        "start": int(self.index_start.text()),
        "end": int(self.index_end.text()),
        "skip": int(self.index_skip.text()),
        "mode": self.set_mode.currentText(),
        "mask": getattr(self, "mask", None),
        "cave_map" : os.path.join(self.image_data_dir, self.image_combo.currentText())
    }
        

class SensorPicker(QDialog):
    def __init__(self, background_path, sensor_names, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Sensor Locations")
        self.sensor_names = sensor_names
        self.current_index = 0
        self.sensor_positions = {}

        self.image_label = QLabel()
        self.original_pixmap = QPixmap(background_path)

        # Set a fixed size for the dialog
        self.setFixedSize(800, 600)
        self.scale_pixmap()

        self.title_label = QLabel(f"Click on the image to set {self.sensor_names[0]}'s position")

        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addWidget(self.image_label)

        # Connect mouse press event handler
        self.image_label.mousePressEvent = self.get_click

    def scale_pixmap(self):
        """Scales the pixmap to fit the dialog while keeping its aspect ratio."""
        max_size = QSize(780, 500)  # Leave some room for margins and title
        scaled_pixmap = self.original_pixmap.scaled(
            max_size, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setFixedSize(scaled_pixmap.size())

    def get_click(self, event):
        print(f"Mouse click at {event.pos()}, current_index: {self.current_index}")
        if self.current_index >= len(self.sensor_names):
            return

        # Get click coordinates on the scaled image
        x = event.pos().x()
        y = event.pos().y()

        # Calculate the ratio of scaled image to original
        scaled_pixmap = self.image_label.pixmap()
        scale_x = self.original_pixmap.width() / scaled_pixmap.width()
        scale_y = self.original_pixmap.height() / scaled_pixmap.height()

        # Scale the coordinates up to original image resolution
        x_original = int(x * scale_x)
        y_original = int(y * scale_y)

        # Flip Y-axis to make (0, 0) at the bottom-left
        y_flipped = self.original_pixmap.height() - y_original

        # Save sensor position with flipped Y
        sensor = self.sensor_names[self.current_index]
        self.sensor_positions[sensor] = (x_original, y_flipped)
        print(f"Set {sensor} to {(x_original, y_flipped)}")

        # Move to next sensor
        self.current_index += 1  

        # Update title or close
        if self.current_index == len(self.sensor_names):
            self.close()
        else:
            next_sensor = self.sensor_names[self.current_index]
            self.title_label.setText(f"Click on the image to set {next_sensor}'s position")


    def get_positions(self):
        return self.sensor_positions

    
class NewHeatMap(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Heatmap Option")

        # Main question
        question_label = QLabel("Load the pre-existing heatmap?")                    #### currently not functional

        yes_button = QPushButton("Yes")
        no_button = QPushButton("No")

        yes_button.clicked.connect(self.accept)  # Return QDialog.Accepted
        no_button.clicked.connect(self.reject)   # Return QDialog.Rejected

        # Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(question_label)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
