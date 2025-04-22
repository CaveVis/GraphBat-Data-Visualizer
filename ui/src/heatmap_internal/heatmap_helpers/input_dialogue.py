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
class InputDialogue(QDialog):
    def __init__(self, parent=None, dataframe=None):
        super(InputDialogue, self).__init__(parent)
        self.setWindowTitle("Heatmap Input")
        self.resize(600, 400)
        
        # Main layout
        self.layout = QFormLayout(self)
        self.dataframe = dataframe
        self.background_path = None
        # Create widgets
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

        self.layout.addRow("Colormap Scale (Standard Deviations from mean):", self.sdev_button)
        self.layout.addRow("Start Index:", self.index_start)
        self.layout.addRow("End Index:", self.index_end)
        self.layout.addRow("Skip Every N Rows:", self.index_skip)
        self.layout.addRow("Distance Mode:", self.set_mode)
        self.layout.addRow(self.sensor_button)
        self.layout.addRow(self.set_mask_button)
        self.layout.addRow(self.submit_button, self.cancel_button)                      
        self.sensor_positions = {}
    def set_sensor(self):
        self.background_path, _ = QFileDialog.getOpenFileName(self, "Select Background Image", "", "Images (*.png *.jpg)")
        if not self.background_path:
            return

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

            draw_win = PaintGrid(background_path=self.background_path)  # set this earlier
            draw_win.exec()
            self.mask = draw_win.get_mask()
        else:
            mask_path, _ = QFileDialog.getOpenFileName(self, "Select Mask File", "", "NPY Files (*.npy)")
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
        "mask": getattr(self, "mask", None)
    }
        


class SensorPicker(QDialog):
    def __init__(self, background_path, sensor_names, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Sensor Locations")
        self.sensor_names = sensor_names
        self.current_index = 0
        self.sensor_positions = {}

        self.image_label = QLabel()
        self.pixmap = QPixmap(background_path)
        self.title_label = QLabel(f"Click on the image to set {self.sensor_names[0]}'s position")

        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addWidget(self.image_label)

    def get_click(self, event):
        print(f"Mouse click at {event.pos()}, current_index: {self.current_index}")
        if self.current_index >= len(self.sensor_names):
            return

        x = event.pos().x()
        y = event.pos().y()
        sensor = self.sensor_names[self.current_index]
        self.sensor_positions[sensor] = (x, y)
        print(f"Set {sensor} to {(x, y)}")

        self.current_index += 1  # Move to next sensor

        # Update title or close
        if self.current_index == len(self.sensor_names):
            self.close()
        else:
            next_sensor = self.sensor_names[self.current_index]
            self.title_label.setText(f"Click on the image to set {next_sensor}'s position")
    def showEvent(self, event):
        super().showEvent(event)
        self.image_label.setPixmap(self.pixmap)
        self.image_label.mousePressEvent = self.get_click

    def get_positions(self):
        return self.sensor_positions
    
class NewHeatMap(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Heatmap Option")

        # Main question
        question_label = QLabel("Load the pre-existing heatmap?")

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