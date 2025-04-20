# This Python file uses the following encoding: utf-8
import sys
import json
import shutil
#from PyQt5 import QtWidgets
from PySide6 import QtSvg
from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import (QApplication, QMainWindow, QSizeGrip, QFileDialog, QWidget,
                                QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QComboBox, QListWidget, QAbstractItemView, QListWidgetItem,
                                QLineEdit, QPushButton, QDialogButtonBox, QMessageBox, QDialog, QTableWidget,QHeaderView, QTableWidgetItem)
from mainwindow import Ui_mainwindow
import pandas as pd
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as Navi
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import os
import traceback
import datetime
import mplcursors
import src.data_processing.data_processor as data_processor
from src.data_processing.data_processor import AnomalyDialog, ColumnSelectionDialog, DataProcessor
import src.project_management.project_manager as project_manager
from src.project_management.project_manager import ProjectManager
#Canvas class
class MatplotlibCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None,width=5, height = 5, dpi = 120):
        f = Figure(figsize = (width,height),dpi = dpi)
        self.axes= f.add_subplot(111)
        super(MatplotlibCanvas,self).__init__(f)
        f.tight_layout(pad=3)

class MainWindow(QMainWindow):
    def __init__(self, /):
        QMainWindow.__init__(self)
        self.ui = Ui_mainwindow()
        self.ui.setupUi(self)

        ##############################
        ### Set up session variables
        ##############################
        self.canv = MatplotlibCanvas(self)
        self.df = pd.DataFrame()  # Initialize empty DataFrame
        self.sensor_states = {}

        # Create DataProcessor instance
        self.data_processor = data_processor.DataProcessor(parent=self)

        ### Load existing user preferences ###
        self.app_settings = QSettings("GraphBat", "userPrefs")
        #Theme
        self.switchStylesheet(self.app_settings.value("theme", "style_brown.qss"))
        self.ui.appTheme_combobox.setCurrentIndex(self.app_settings.value("theme_index", 0))
        #Fullscreen mode
        is_fullscreen = self.app_settings.value("is_fullscreen", True)
        if is_fullscreen:
            self.ui.maximize_button.clicked.connect(lambda: self.toggleMaximized())
            self.ui.fullscreen_checkbox.setChecked(True)
        else:
            self.ui.fullscreen_checkbox.setChecked(False)
        #Font
        is_dyslexic = self.app_settings.value("is_dyslexic", False)
        if is_dyslexic:
            QApplication.instance().setFont(QFont("Comic Sans MS"))
            self.ui.dyslexicfont_checkbox.setChecked(True)
        else:
            QApplication.instance().setFont(QFont("Verdana"))
            self.ui.dyslexicfont_checkbox.setChecked(False)
        print(f"User preferences are saved at {self.app_settings.fileName()}")

        #################################

        #Taskbar setup
        self.taskbar_width = 300
        self.ui.project_taskbar_toolbox.setItemIcon(self.ui.project_taskbar_toolbox.currentIndex(), QIcon("images/icons/bat_flying.svg"))
        self.ui.toolbox_graphlist.setItemIcon(self.ui.toolbox_graphlist.currentIndex(), QIcon("images/icons/bat_flying.svg"))

        #Hide default title bar
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(":/images/logos/Logo V2.svg"))
        self.setWindowTitle("GraphBat")

        #Size grip
        QSizeGrip(self.ui.size_grip)

        #### Top taskbar buttons ###########################
        #Close button
        self.ui.exit_button.clicked.connect(lambda: self.close())
        #Minimize button
        self.ui.minimize_button.clicked.connect(lambda: self.showMinimized())
        #Maximize button
        self.ui.maximize_button.clicked.connect(lambda: self.toggleMaximized())
        #Settings button
        self.ui.settings_button_top.clicked.connect(lambda: self.ui.main_body_stack.setCurrentWidget(self.ui.settings_page))
        #Home button
        self.ui.home_button.clicked.connect(lambda: self.returnHome())
        ###################################################

        ###########

        #### Homescreen taskbar buttons ############################
        #About button
        self.ui.about_button_side.clicked.connect(lambda: self.ui.main_body_stack.setCurrentWidget(self.ui.about_page))
        #Settings button
        self.ui.settings_button_side.clicked.connect(lambda: self.ui.main_body_stack.setCurrentWidget(self.ui.settings_page))
        #Create project button
        self.ui.create_button_side.clicked.connect(lambda: self.ui.main_body_stack.setCurrentWidget(self.ui.create_project_page))
        #Load project button
        self.ui.load_button_side.clicked.connect(lambda: self.ui.main_body_stack.setCurrentWidget(self.ui.load_page))

        ###Project taskbar ##################
        self.ui.project_taskbar_toolbox.currentChanged.connect(lambda: self.updateToolboxIcons(self.ui.project_taskbar_toolbox, self.ui.project_taskbar_toolbox.currentIndex()))
        self.ui.toolbox_graphlist.currentChanged.connect(lambda: self.updateToolboxIcons(self.ui.toolbox_graphlist, self.ui.toolbox_graphlist.currentIndex()))

        #Close taskbar
        self.ui.close_button.clicked.connect(lambda: self.toggleSidebar())

        #######################################

        ### Homescreen primary buttons
        #Create button
        self.ui.create_button_main.clicked.connect(lambda: self.ui.main_body_stack.setCurrentWidget(self.ui.create_project_page))
        #Load button
        self.ui.load_button_main.clicked.connect(lambda: self.ui.main_body_stack.setCurrentWidget(self.ui.load_page))

        #### Create project page buttons #####################
        #Cancel button
        self.ui.cancel_create_button.clicked.connect(lambda: self.ui.main_body_stack.setCurrentWidget(self.ui.home_page))

        self.ui.create_add_data_button.clicked.connect(self.data_processor.getFileCSV)
        self.ui.create_add_map_button.clicked.connect(self.data_processor.getFileImage)
        #Create button (demo code)
        self.ui.confirm_create_button.clicked.connect(lambda: self.createNewProject())

        ########################
        ### Project page buttons

        self.ui.button_linegraph.clicked.connect(lambda: self.display_canvas_in_frame("Line Graph"))
        self.ui.dropdown_bargraph.activated.connect(self.update_bar_agg_method)
        self.ui.button_histogram.clicked.connect(lambda: self.display_canvas_in_frame("Histogram"))
        self.ui.button_boxplot.clicked.connect(lambda: self.display_canvas_in_frame("Box Plot"))
        self.ui.button_cavemap.clicked.connect(lambda: self.display_canvas_in_frame("Cave Map"))

        #########################
        #### Load project page buttons
        self.ui.load_back_button.clicked.connect(lambda: self.ui.main_body_stack.setCurrentWidget(self.ui.home_page))

        #########################

        ### Settings page buttons ##############
        self.ui.appTheme_combobox.currentIndexChanged.connect(self.updateAppTheme)
        self.ui.fullscreen_checkbox.stateChanged.connect(self.setFullscreenMode)
        self.ui.dyslexicfont_checkbox.stateChanged.connect(self.setDyslexicFont)

        #######################


        def moveWindow(e):
            if not self.isMaximized():
                if e.buttons() == Qt.MouseButton.LeftButton:
                    self.move(self.pos() + e.globalPosition().toPoint() - self.clickPosition)
                    self.clickPosition = e.globalPosition().toPoint()
                    e.accept()

        self.ui.header.mouseMoveEvent = moveWindow

        self.show()

    def get_plot_data(self):
        self.df, self.sensor_states = self.data_processor.readData()

    def update_bar_agg_method(self):
        """Update aggregation method based on dropdown selection"""
        text = self.ui.dropdown_bargraph.currentText()
        print(text)
        match text:
            case "Bar Graph - Mean":
                self.agg_method = "mean"
            case "Bar Graph - Median":
                self.agg_method = "median"
            case "Bar Graph - Minimum":
                self.agg_method = "min"
            case "Bar Graph - Maximum":
                self.agg_method = "max"
            case "Bar Graph - Count":
                self.agg_method = "count"
            case _:  # Default case
                self.agg_method = "mean"
        self.display_canvas_in_frame("Bar Graph")  # Redraw the bar graph

    def display_canvas_in_frame(self, graph_type):
        plt.clf()
        # Clear previous widgets in the layout
        while self.ui.verticalLayout_55.count():
            child = self.ui.verticalLayout_55.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Create a new canvas and navigation toolbar
        self.canv = MatplotlibCanvas(self, width=8, height=4, dpi=100)
        toolbar = Navi(self.canv, self)  # Add navigation toolbar


        # Check if DataFrame exists and isn't empty
        if not hasattr(self, 'df') or self.df.empty:
            self.get_plot_data()

        project_name = ProjectManager.get_project()
        base_data_dir = os.path.join("Projects", project_name, "datafiles")
        premerge_data_dir = os.path.join(base_data_dir, "processed_data")
        merged_data_dir = os.path.join(base_data_dir, "processed_data")
        
        #Clear the axes
        self.canv.axes.cla()
        
        if not self.df.empty:
            try:
                # Process anomaly dialogs using sensor_states
                for sensor_col in list(self.sensor_states.keys()):
                    state = self.sensor_states[sensor_col]
                    
                    # Skip if already processed
                    if state['status'] in ('cleaned', 'ignored', 'viewed'):
                        continue
                    
                    # Only show dialog if we have anomalies
                    if not state['anomalies'].empty:
                        dialog = AnomalyDialog(self, {
                            'sensor_name': sensor_col.replace("Temperature_", ""),
                            'count': len(state['anomalies']),
                            'values': state['anomalies'],
                            'global_lower_bound': state['bounds']['lower'],
                            'global_upper_bound': state['bounds']['upper'],
                            'total_points': len(state['original_data'])
                        })
                        
                        result = dialog.exec()

                        if result == QDialog.Accepted:
                            if dialog.result == "remove":
                                # Create cleaned version
                                cleaned_data = state['original_data'].copy()
                                cleaned_data.loc[state['anomalies'].index] = None
                                cleaned_data = cleaned_data.ffill().bfill()
                                
                                # Update state in sensor_states
                                self.sensor_states[sensor_col].update({
                                    'status': 'cleaned',
                                    'processed_data': cleaned_data
                                })    
                            elif dialog.result == "ignore":
                                self.sensor_states[sensor_col]['status'] = 'ignored'
                                
                            elif dialog.result == "view":
                                self.sensor_states[sensor_col]['status'] = 'viewed'

                     # Save individual processed sensor data
                    if 'processed_data' in state:
                        sensor_name = sensor_col
                        processed_filename = f"processed_{sensor_name}.csv"
                        processed_filepath = os.path.join(premerge_data_dir, processed_filename)
                        state['processed_data'].to_csv(processed_filepath)

                # Rebuild main dataframe after any changes
                dfs = []
                for sensor_col, state in self.sensor_states.items():
                    dfs.append(state['processed_data'])
                
                self.df = pd.concat(dfs, axis=1) if dfs else pd.DataFrame()
                #Make sure that no rows exist without data
                self.df = self.df.sort_index().dropna(axis=0)

                #Rename columns to Sensor 1, Sensor 2, etc.
                self.df.columns = [f"Sensor {i+1}" for i in range(self.df.shape[1])]

                # Save merged dataframe
                if not self.df.empty:
                    processed_merged_filename = "processed_merged_data.csv"
                    processed_merged_filepath = os.path.join(merged_data_dir, processed_merged_filename)
                    self.df.to_csv(processed_merged_filepath)     

                if graph_type == "Line Graph":
                    #First plot all clean_data points regardless of anomaly status
                    for c in self.df.columns:
                        if not self.df[c].empty:
                            lines = self.canv.axes.plot(self.df.index, self.df[c], label = c)
                            mplcursors.cursor(lines)  # or just mplcursors.cursor()


                    # Modified anomaly plotting:
                    for sensor_col, state in self.sensor_states.items():
                        if state['status'] == 'viewed' and not state['anomalies'].empty:
                            outliers = self.sensor_states[sensor_col]['anomalies']
                            if not outliers.empty:
                                try:
                                    if not outliers.empty:
                                        self.canv.axes.scatter(
                                            outliers.index, 
                                            outliers.values, 
                                            color='red', 
                                            s=5, 
                                            label=f"{sensor_col.replace('Temperature_', '')} outliers",
                                            zorder=3
                                        )
                                except Exception as e:
                                    print(f"Error plotting outliers: {e}")

                    # Configure plot with larger fonts
                    plt.rcParams.update({'font.size': 10})  # Set base font size
                    self.canv.axes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y-%m-%d'))
                    self.canv.axes.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator())
                    # Rotate and adjust x-axis labels with larger font
                    plt.setp(self.canv.axes.get_xticklabels(), rotation=45, ha='right', fontsize=10)
                    plt.setp(self.canv.axes.get_yticklabels(), fontsize=10)
                    legend = self.canv.axes.legend()
                    legend.set_draggable(True)
                    self.canv.axes.set_xlabel('Date-Time', fontsize=18)
                    self.canv.axes.set_ylabel('Measured Temperature(°C)', fontsize=18)
                    self.canv.axes.set_title('Temperature in Cave Over Time', fontsize=22, pad=20)

                elif graph_type == "Bar Graph":
                    try:
                        # For bar graphs, resample the data to a suitable frequency
                        # First ensure we have a proper datetime index
                        if not isinstance(self.df.index, pd.DatetimeIndex):
                            self.df.index = pd.to_datetime(self.df.index)

                        # Determine appropriate frequency based on date range
                        date_range = (self.df.index.max() - self.df.index.min()).total_seconds()
                        
                        if date_range > 60*60*24*30:  # More than a month
                            freq = 'W'  # Weekly
                            freq_label = 'Weekly'
                        elif date_range > 60*60*24*7:  # More than a week
                            freq = 'D'  # Daily
                            freq_label = 'Daily'
                        elif date_range > 60*60*24:  # More than a day
                            freq = '6H'  # 6-hourly
                            freq_label = '6-Hourly'
                        else:
                            freq = 'H'  # Hourly
                            freq_label = 'Hourly'

                        if not hasattr(self, 'agg_method') or self.agg_method is None:
                            self.agg_method = "mean" #Default aggregation method
                        
                        # Apply aggregation based on selected method
                        if self.agg_method == "mean":
                            agg_df = self.df.resample(freq).mean()
                        elif self.agg_method == "Median":
                            agg_df = self.df.resample(freq).median()
                        elif self.agg_method == "min":
                            agg_df = self.df.resample(freq).min()
                        elif self.agg_method == "max":
                            agg_df = self.df.resample(freq).max()
                        elif self.agg_method == "sum":
                            agg_df = self.df.resample(freq).sum()
                        elif self.agg_method == "count":
                            agg_df = self.df.resample(freq).count()
                        else:
                            # Default to mean
                            agg_df = self.df.resample(freq).mean()
                        # Calculate bar width based on number of columns
                        num_cols = len(agg_df.columns)
                        width = 0.8 / num_cols if num_cols > 0 else 0.8
                        
                        # Convert datetime index to numerical values for plotting
                        dates_num = matplotlib.dates.date2num(agg_df.index)
                        
                        # Plot each column as a separate bar series
                        for i, col in enumerate(agg_df.columns):
                            # Calculate position for this set of bars
                            pos = dates_num + (i * width)
                            self.canv.axes.bar(pos, agg_df[col], width=width, label=col)    
                        # Configure plot
                        self.canv.axes.set_xlabel('Time Period')
                        self.canv.axes.set_ylabel(f'{self.agg_method.capitalize()} Temperature (°C)')
                        self.canv.axes.set_title(f'{freq_label} {self.agg_method.capitalize()} Temperature')
                        
                        # Format x-axis as dates
                        self.canv.axes.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%Y-%m-%d'))
                        self.canv.axes.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator())
                        plt.setp(self.canv.axes.get_xticklabels(), rotation=45, ha='right')
                        
                        # Add legend
                        if num_cols > 0:
                            legend = self.canv.axes.legend()
                            legend.set_draggable(True)
                    except Exception as e:
                        print(f"Error in bar graph plotting: {e}")
                        raise

                elif graph_type == "Histogram":
                    try:
                        # We'll create a histogram for each column with transparency
                        bins = 20  # Number of bins
                        
                        for col in self.df.columns:
                            # Remove NaN values for histogram
                            clean_data = self.df[col].dropna()
                            
                            # Only create histogram if we have clean_data
                            if len(clean_data) > 0:
                                self.canv.axes.hist(clean_data, bins, alpha=0.7, label=col)
                                #mplcursors.cursor(hist)

                        # Configure plot
                        self.canv.axes.set_xlabel('Temperature (°C)')
                        self.canv.axes.set_ylabel('Frequency')
                        self.canv.axes.set_title('Temperature Distribution')
                        legend = self.canv.axes.legend()
                        legend.set_draggable(True)
                    except Exception as e:
                        print(f"Error in histogram plotting: {e}")
                        raise
                elif graph_type == "Box Plot":
                    try:
                        # For box plots, we need to prepare the clean_data differently
                        # We'll create a list of clean_data for each column
                        clean_data = []
                        labels = []
                        for col in self.df.columns:
                            # Only add column if it has non-NaN values
                            if not self.df[col].isna().all():
                                clean_data.append(self.df[col].dropna())
                                labels.append(col)
                        
                        # Create box plot
                        if clean_data:
                            self.canv.axes.boxplot(clean_data, tick_labels=labels, manage_ticks=True, patch_artist=True)
                            # Configure plot
                            self.canv.axes.set_xlabel('Sensors')
                            self.canv.axes.set_ylabel('Temperature (°C)')
                            self.canv.axes.set_title('Temperature Distribution by Sensor')
                            self.canv.axes.grid(True, linestyle='--', alpha=0.7)
                            # Rotate x-axis labels to prevent crowding
                            plt.setp(self.canv.axes.get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')
                    except Exception as e:
                        print(f"Error in box plot plotting: {e}")
                        raise

                self.canv.draw()
                self.canv.figure.tight_layout()
            except Exception as e:
                print("Plotting error:", e)
                traceback.print_exc()

        # Add both to the layout
        #VerticalLayout 
        self.ui.verticalLayout_55.addWidget(toolbar)
        self.ui.verticalLayout_55.addWidget(self.canv)

    def setDyslexicFont(self, is_dyslexic):
        self.app_settings.setValue("is_dyslexic", is_dyslexic)

    def setFullscreenMode(self, state):
        self.app_settings.setValue("is_fullscreen", state)

    def updateAppTheme(self, index):
        match index:
            case 0:
                self.switchStylesheet("style_brown.qss")
            case 1:
                self.switchStylesheet("style_black.qss")
            case 2:
                self.switchStylesheet("style_white.qss")

        self.app_settings.setValue("theme_index", index)

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPosition().toPoint()

    def toggleMaximized(self):
        if self.isMaximized():
            self.showNormal()
            self.ui.maximize_button.setIcon(QIcon("images/icons/maximize-2.svg"))
        else:
            self.showMaximized()
            self.ui.maximize_button.setIcon(QIcon("images/icons/minimize-2.svg"))

    def toggleSidebar(self):
        current_width = self.ui.taskbar_body_container.width()
        if current_width > 0:
            self.taskbar_width = current_width
            self.ui.taskbar_body_container.setFixedWidth(0)
        else:
            self.ui.taskbar_body_container.setFixedWidth(self.taskbar_width)

    def switchActiveTaskbar(self):
        if self.ui.main_body_stack.currentIndex() == 4:
            self.ui.taskbar_body_container.setCurrentIndex(1)   #project taskbar
        else:
            self.ui.taskbar_body_container.setCurrentIndex(0)   #homepage taskbar

    def createNewProject(self):
        maxTitleLen = 50
        maxDescLen = 500
        project_name = self.ui.textEdit.toPlainText().strip()
        project_description = self.ui.plainTextEdit.toPlainText().strip()

        # Error checking for project name
        if not project_name:
            self.showErrorMessage("Project name is empty")
            return
        if len(project_name) > maxTitleLen:
            self.showErrorMessage(f"Project name cannot exceed {maxTitleLen} chars")
            return
        # Validate description length
        if len(project_description) > maxDescLen:
            self.showErrorMessage(f"Project description cannot exceed {maxDescLen} characters")
            return

        # Create a dictionary for project data
        project_data = {"project_name": project_name,
                        "project_description": project_description,
                        "created_at": datetime.datetime.now().isoformat(),
                        "last_modified": datetime.datetime.now().isoformat()
                        }

        # Get the root directory of your project (Cave-Data-App)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Construct the path to the Projects directory
        projects_dir = os.path.join(project_root, "Projects")

        # Create directory to the main project folder
        project_folder = os.path.join(projects_dir, project_name)

        if os.path.exists(project_folder):
            self.showErrorMessage(f"A project named '{project_name}' exists, try a diffrent name")
            return

        project_manager.ProjectManager.set_project(project_name)
        # Define the JSON file path
        json_file_path = os.path.join(project_folder, "project_info.json")
        # Write to JSON file
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, indent=4)  # indent=4 for pretty formatting

        #Create subfolders under datafiles in project 
        data_subfolders = ['raw_data', 'preprocessed_data','processed_data', 'images', 'videos']
        for folder in data_subfolders:
            folder_path = os.path.join(project_folder, 'datafiles', folder)
            os.makedirs(folder_path, exist_ok=True)
            print(f"Created directory: {folder_path}")

        # Save unmerged csv files to datafiles/raw_data
        if not hasattr(self, 'filenames') or not self.filenames:
            print("No files to save")
        raw_data_path = os.path.join("Projects", project_name, "datafiles", "raw_data")
        os.makedirs(raw_data_path, exist_ok=True)

        for file_path in self.data_processor.filenames:
            try:
                # Get the base filename
                filename = os.path.basename(file_path)

                # Create destination path
                dest_path = os.path.join(raw_data_path, filename)

                # Copy the original file
                shutil.copy2(file_path, dest_path)
                print(f"Saved raw file: {dest_path}")

            except Exception as e:
                print(f"Error saving {file_path}: {str(e)}")
                traceback.print_exc()

        self.ui.main_body_stack.setCurrentWidget(self.ui.project_homepage)
        self.switchActiveTaskbar()

        try:
            os.makedirs(project_folder)
            print(f"Directory '{project_folder}' created successfully.")
        except FileExistsError:
            print(f"Directory '{project_folder}' already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{project_folder}'.")
        except Exception as e:
            print(f"An error occurred: {e}")

        #Error Message
    def showErrorMessage(self, message):
        QMessageBox.warning(self, "Error", message)

    def showSuccessMessage(self, message):
        QMessageBox.information(self, "Success", message)

    def returnHome(self):
        self.ui.main_body_stack.setCurrentWidget(self.ui.home_page)
        self.switchActiveTaskbar()

    def updateToolboxIcons(self, toolbox, index):
        for i in range(toolbox.count()):
            if i == index:
                toolbox.setItemIcon(i, QIcon("images/icons/bat_flying.svg"))  # Set active icon
            else:
                toolbox.setItemIcon(i, QIcon("images/icons/bat_hanging.svg"))  # Set inactive icon

    def switchStylesheet(self, file_path):
        try:
            with open(file_path, 'r') as file:
                stylesheet = file.read()
            self.setStyleSheet(stylesheet)
            self.app_settings.setValue("theme", file_path)
        except FileNotFoundError:
            print("Stylesheet not found at path " + file_path)
        except Exception as e:
            print(f"An error occurred: {e}")
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    sys.exit(app.exec())
