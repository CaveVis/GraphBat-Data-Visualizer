# This Python file uses the following encoding: utf-8
import sys
import os
import traceback
import mplcursors
import pandas as pd
import matplotlib
from PySide6 import QtSvg
from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import (QApplication, QMainWindow, QSizeGrip, QFileDialog, QWidget,
                                QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QComboBox, QListWidget, QAbstractItemView, QListWidgetItem,
                                QLineEdit, QPushButton, QPlainTextEdit, QSizePolicy, QDateTimeEdit, QFrame, QDialogButtonBox, QMessageBox, QDialog)
from mainwindow import Ui_mainwindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as Navi
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import src.data_processing.data_processor as data_processor
from src.data_processing.data_processor import AnomalyDialog
from src.project_management.project_manager import ProjectManager
from src.draw_tool import PaintGrid
from src.draw_tool import PaintGrid
from src.heatmap_internal.heatmap_helpers.Heatmap_Widget import Heatmap_Widget
from src.heatmap_internal.heatmap_helpers.heatmap_utils import dist_linear, dijkstras, get_sdev_from_dataframe, load_cave_map
from src.heatmap_internal.heatmap_helpers.input_dialogue import * 
#Canvas class
class MatplotlibCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None,width=5, height = 5, dpi = 120):
        f = Figure(figsize = (width,height),dpi = dpi)
        self.axes= f.add_subplot(111)
        super(MatplotlibCanvas,self).__init__(f)
        f.tight_layout(pad=3)

class CustomNavigationToolbar(Navi):
    def __init__(self, canvas, parent=None):
        super().__init__(canvas, parent)
        self.canvas = canvas
        self.parent = parent  # Reference to MainWindow

        clock_action = self.addAction(self._icon("clock"), "Set time range", self.adjust_time_range)
        # Get the list of actions in the toolbar
        actions = self.actions()

        # Remove the action we just added (from the end)
        self.removeAction(clock_action)

        # Re-insert it at the desired position (e.g., after the 5th standard button)
        target_index = min(5, len(actions)-1)  # Make sure we don't go out of bounds
        self.insertAction(actions[target_index], clock_action)
        
    def _icon(self, name):
        """Modified icon loader that checks for custom icons"""
        if name == "clock":
            # Load your custom clock icon
            return QIcon("ui/images/icons/clock.png")
        return super()._icon(name)
    
    def adjust_time_range(self):
        """Open a dialog to adjust the time range of the graph"""
        if not hasattr(self.parent, 'df') or self.parent.df.empty:
            QMessageBox.warning(self.parent, "No Data", "No data available to adjust time range")
            return
            
        # Get current axes and limits
        ax = self.canvas.figure.axes[0]
        current_xlim = ax.get_xlim()
        
        # Convert matplotlib dates to datetime
        min_date = matplotlib.dates.num2date(current_xlim[0])
        max_date = matplotlib.dates.num2date(current_xlim[1])
        
        # Create a dialog for time range selection
        dialog = QDialog(self.parent)
        dialog.setWindowTitle("Adjust Time Range")
        layout = QVBoxLayout()
        
        # Min date selector
        min_layout = QHBoxLayout()
        min_layout.addWidget(QLabel("Start Date:"))
        min_date_edit = QDateTimeEdit(min_date)
        min_date_edit.setCalendarPopup(True)
        min_date_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        min_layout.addWidget(min_date_edit)
        layout.addLayout(min_layout)
        
        # Max date selector
        max_layout = QHBoxLayout()
        max_layout.addWidget(QLabel("End Date:"))
        max_date_edit = QDateTimeEdit(max_date)
        max_date_edit.setCalendarPopup(True)
        max_date_edit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        max_layout.addWidget(max_date_edit)
        layout.addLayout(max_layout)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        
        if dialog.exec() == QDialog.Accepted:
            try:
                # Get new dates from the dialog
                new_min = min_date_edit.dateTime().toPython()
                new_max = max_date_edit.dateTime().toPython()
                
                # Convert to matplotlib dates
                new_min_num = matplotlib.dates.date2num(new_min)
                new_max_num = matplotlib.dates.date2num(new_max)
                
                # Set new limits
                ax.set_xlim(new_min_num, new_max_num)
                self.canvas.draw()
                
            except Exception as e:
                QMessageBox.warning(self.parent, "Error", f"Failed to adjust time range: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self, /):
        QMainWindow.__init__(self)
        self.ui = Ui_mainwindow()
        self.ui.setupUi(self)

        ##############################
        ### Set up session variables
        ##############################
        self.navigation_stack = []
        self.canv = MatplotlibCanvas(self)
        self.df = pd.DataFrame()  # Initialize empty DataFrame
        self.sensor_states = {}
        self.cave_map_background_path = None

        # Create DataProcessor instance
        self.data_processor = data_processor.DataProcessor(parent=self)

        #Set up fonts for project labels
        self.font = QFont()
        self.font.setFamilies([u"Verdana"])
        self.font.setPointSize(15)
        self.font.setBold(True)

        self.font2 = QFont()
        self.font2.setFamilies([u"Verdana"])
        self.font2.setPointSize(12)
        self.font2.setBold(True)

        self.font5 = QFont()
        self.font5.setFamilies([u"Verdana"])
        self.font5.setPointSize(11)
        self.font5.setItalic(True)

        self.font3 = QFont()
        self.font3.setFamilies([u"Verdana"])
        self.font3.setPointSize(8)

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
        self.ui.settings_button_top.clicked.connect(lambda: self.navigate_to(self.ui.settings_page))
        #Home button
        self.ui.home_button.clicked.connect(lambda: self.returnHome())
        ###################################################

        ###########

        #### Homescreen taskbar buttons ############################
        #About button
        self.ui.about_button_side.clicked.connect(lambda: self.navigate_to(self.ui.about_page))
        #Settings button
        self.ui.settings_button_side.clicked.connect(lambda: self.navigate_to(self.ui.settings_page))
        #Create project button
        self.ui.create_button_side.clicked.connect(lambda: self.navigate_to(self.ui.create_project_page))
        #Load project button
        self.ui.load_button_side.clicked.connect(lambda: self.navigate_to(self.ui.load_page))

        ###Project taskbar ##################
        self.ui.project_taskbar_toolbox.currentChanged.connect(lambda: self.updateToolboxIcons(self.ui.project_taskbar_toolbox, self.ui.project_taskbar_toolbox.currentIndex()))
        self.ui.toolbox_graphlist.currentChanged.connect(lambda: self.updateToolboxIcons(self.ui.toolbox_graphlist, self.ui.toolbox_graphlist.currentIndex()))

        #Close taskbar
        self.ui.close_button.clicked.connect(lambda: self.toggleSidebar())

        #######################################

        ### Homescreen primary buttons
        #Create button
        self.ui.create_button_main.clicked.connect(lambda: self.navigate_to(self.ui.create_project_page))
        #Load button
        self.ui.load_button_main.clicked.connect(lambda: [self.navigate_to(self.ui.load_page),
                                                        self.load_projects_list()
                                                        ])

        #### Create project page buttons #####################
        #Cancel button
        self.ui.cancel_create_button.clicked.connect(lambda:self.go_back())

        self.ui.create_add_data_button.clicked.connect(self.data_processor.getFileCSV)
        self.ui.create_add_map_button.clicked.connect(self.data_processor.getFileImage)
        #Create project button
        self.ui.confirm_create_button.clicked.connect(lambda: self.handle_project_creation())

        ########################
        ### Project page buttons

        self.ui.button_linegraph.clicked.connect(lambda: self.display_canvas_in_frame("Line Graph"))
        self.ui.dropdown_bargraph.activated.connect(self.update_bar_agg_method)
        self.ui.button_histogram.clicked.connect(lambda: self.display_canvas_in_frame("Histogram"))
        self.ui.button_boxplot.clicked.connect(lambda: self.display_canvas_in_frame("Box Plot"))
        self.ui.button_cavemap.clicked.connect(lambda: self.display_canvas_in_frame("Cave Map"))

        ########################
        ### Taskbar buttons on left-hand side

        self.ui.pushButton_13.clicked.connect(lambda: self.handle_project_edit())
        self.ui.pushButton_14.clicked.connect(lambda: [self.navigate_to(self.ui.load_page),
                                                        self.load_projects_list()
                                                        ])
        self.ui.pushButton_15.clicked.connect(lambda: self.navigate_to(self.ui.create_project_page))
        self.ui.pushButton_11.clicked.connect(lambda: self.navigate_to(self.ui.settings_page))

        #########################
        #### Load project page buttons
        self.ui.load_button_side.clicked.connect(lambda: [self.navigate_to(self.ui.load_page),
                                                        self.load_projects_list()
                                                        ])
        self.ui.load_back_button.clicked.connect(lambda: self.go_back())

        self.ui.pushButton_12.clicked.connect(lambda: self.navigate_to(self.ui.about_page))

        #########################
        ### Settings page buttons 
        self.ui.appTheme_combobox.currentIndexChanged.connect(self.updateAppTheme)
        self.ui.fullscreen_checkbox.stateChanged.connect(self.setFullscreenMode)
        self.ui.dyslexicfont_checkbox.stateChanged.connect(self.setDyslexicFont)
        self.ui.pushButton_2.clicked.connect(lambda: self.go_back())

        

        #######################
        ### About page buttons 
        self.ui.about_back_button.clicked.connect(self.go_back)
        ##########################


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

    def display_canvas_in_frame(self, graph_type=None, project_name=None):
        plt.clf()
        # Clear previous widgets in the layout
        while self.ui.verticalLayout_55.count():
            child = self.ui.verticalLayout_55.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Create a new canvas and navigation toolbar
        self.canv = MatplotlibCanvas(self, width=8, height=4, dpi=100)
        toolbar = CustomNavigationToolbar(self.canv, self)  # Add navigation toolbar

        # Check if DataFrame exists and isn't empty
        if not hasattr(self, 'df') or self.df.empty:
            self.get_plot_data()

        # Check if a project is loaded or a project name is provided
        if project_name is None:
            project_name = ProjectManager.get_project()
        
        if project_name is None:
            QMessageBox.warning(
                self,
                "No Project Loaded",
                "Please load a project before plotting data."
            )
            return
        #project_name = ProjectManager.get_project()

        base_data_dir = os.path.join("Projects", project_name, "datafiles")
        premerge_data_dir = os.path.join(base_data_dir, "processed_data")
        merged_data_dir = os.path.join(base_data_dir,"processed_data", "merged_dataset")
        
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

                #Filters based on time range set
                if hasattr(self, 'start_t') and hasattr(self, 'end_t'):
                    filtered_df = self.df[(self.df.index >= self.start_t) & (self.df.index <= self.end_t)]
                else:
                    filtered_df = self.df.copy()

                if graph_type == "Line Graph":
                    #First plot all clean_data points regardless of anomaly status
                    for c in filtered_df.columns:
                        if not filtered_df[c].empty:
                            lines = self.canv.axes.plot(filtered_df.index, filtered_df[c], label = c)
                            mplcursors.cursor(lines)


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

                    # Determine the range of values for the x-axis
                    x_min = filtered_df.index.min()
                    x_max = filtered_df.index.max()
                    x_range = x_max - x_min

                    # Set custom x-axis tick marks
                    x_ticks = [x_min + pd.Timedelta(seconds=i * (x_range.total_seconds() / 9)) for i in range(10)]
                    x_ticks = [tick.round('S') for tick in x_ticks]  # Round to nearest second



                    # Determine the range of values for each column
                    y_min = filtered_df.min().min()
                    y_max = filtered_df.max().max()
                    y_range = y_max - y_min
                    # Set custom y-axis tick marks
                    y_ticks = [y_min + i * (y_range / 9) for i in range(10)]
                    y_ticks[-1] = y_max  # Ensure the last tick is y_max

                    y_ticks = [round(tick * 2) / 2 for tick in y_ticks]  # Round to nearest 0.5

                    #self.canv.axes.set_xticks(x_ticks)
                    #self.canv.axes.set_xlim(x_min, x_max)
                    #self.canv.axes.set_yticks(y_ticks)
                    #self.canv.axes.set_ylim(y_min, y_max)

                    self.canv.axes.tick_params(axis='x', rotation=45, labelsize=10)
                    self.canv.axes.tick_params(axis='y', labelsize=10)

                    # Rotate and adjust x-axis labels with larger font
                    plt.rcParams.update({'font.size': 10})  # Set base font size
                    plt.setp(self.canv.axes.get_xticklabels(), rotation=45, ha='right', fontsize=10)
                    plt.setp(self.canv.axes.get_yticklabels(), fontsize=10)
                    legend = self.canv.axes.legend()
                    legend.set_draggable(True)
                    self.canv.axes.set_xlabel('Date-Time', fontsize=16)
                    self.canv.axes.set_ylabel('Measured Temperature(°C)', fontsize=16)
                    self.canv.axes.set_title('Temperature in Cave Over Time', fontsize=18, pad=20)

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
                elif graph_type == "Cave Map":
                    try:
                        self.heatmap_widget = Heatmap_Widget()
                            # If not already stored, ask the user

                        if project_name is None:
                            project_name = ProjectManager.get_project()
        
                        if project_name is None:
                            QMessageBox.warning(
                                self,
                                "No Project Loaded",
                                "Please load a project before plotting data."
                            )
                            return

                            
                        if self.heatmap_widget.alpha == None:
                            inputheatmap = InputDialogue(dataframe=self.df)
                            return_code = inputheatmap.exec()
                            if return_code == QDialog.Accepted:
                                input = inputheatmap.output

                            else:
                                print("Dialog Rejected or Closed.")
                                user_input_data = None 
                            sensor_positions = input["sensor_positions"]
                            sensor_names = self.df.columns.to_list()
                            mask_ = input["mask"]
                            dist_lin = {sensor: dist_linear(sensor_positions[sensor], mask_) for sensor in sensor_positions}
                            dist_dijk = {sensor: dijkstras(sensor_positions[sensor], mask_) for sensor in sensor_positions}
                            mode_select = input["mode"]
                            start = input["start"]
                            end = input["end"]
                            skip = input["skip"]
                            cave_map = input["cave_map"]
                            sensor_distances = dist_lin if mode_select == 0 else dist_dijk
                            std_dev, avg_val = get_sdev_from_dataframe(self.df)
                            sensor_x = [int(sensor_positions[s][0]) for s in sensor_names]
                            sensor_y = [int(sensor_positions[s][1]) for s in sensor_names]
                            self.heatmap_widget.plot_data(
                                dfs=self.df, 
                                timestamps=self.df.index.to_list()[start:end:skip],
                                sensor_x=sensor_x,  
                                sensor_y=sensor_y,  
                                cave_map_path=cave_map,   
                                mask_=mask_,                              
                                sensor_distances=sensor_distances,
                                sensor_names=self.df.columns.to_list(),
                                s_dev=std_dev,
                                avg=avg_val,
                                sdev_steps=2,
                                alpha=1,
                                c_map_name='jet'
                            )
                            self.heatmap_widget.canvas.draw()
                        else: 
                            dialog = NewHeatMap()
                            if dialog.exec() == QDialog.rejected:
                                inputheatmap = InputDialogue(dataframe=self.df)
                                return_code = inputheatmap.exec()
                                if return_code == QDialog.Accepted:
                                    input = inputheatmap.output
                                else:
                                    print("Dialog Rejected or Closed.")
                                    user_input_data = None 
                                sensor_positions = input["sensor_positions"]
                                sensor_names = self.df.columns.to_list()
                                mask_ = input["mask"]
                                dist_lin = {sensor: dist_linear(sensor_positions[sensor], mask_) for sensor in sensor_positions}
                                dist_dijk = {sensor: dijkstras(sensor_positions[sensor], mask_) for sensor in sensor_positions}
                                mode_select = input["mode"]
                                start = input["start"]
                                end = input["end"]
                                skip = input["skip"]
                                sensor_distances = dist_lin if mode_select == 0 else dist_dijk
                                std_dev, avg_val = get_sdev_from_dataframe(self.df)
                                sensor_x = [int(sensor_positions[s][0]) for s in sensor_names]
                                sensor_y = [int(sensor_positions[s][1]) for s in sensor_names]
                                self.heatmap_widget.plot_data(
                                    dfs=self.df, 
                                    timestamps=self.df.index.to_list()[start:end:skip],
                                    sensor_x=sensor_x,  
                                    sensor_y=sensor_y,  
                                    cave_map=load_cave_map(self.cave_map_background_path),   
                                    mask_=mask_,                              
                                    sensor_distances=sensor_distances,
                                    sensor_names=self.df.columns.to_list(),
                                    s_dev=std_dev,
                                    avg=avg_val,
                                    sdev_steps=2,
                                    alpha=1,
                                    c_map_name='jet'
                                )

                                self.heatmap_widget.canvas.draw()
                    except Exception as e:
                        print(f"Error displaying cave map: {e}")
                        raise
            except Exception as e:
                    print(f"Error plotting data: {e}")
                    raise
                
        if graph_type == "Cave Map":
            self.ui.verticalLayout_55.addWidget(self.heatmap_widget)  
        else: 
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

    def navigate_to(self, new_widget):
        """Centralized navigation function using QStackedWidget's built-in features"""
        current = self.ui.main_body_stack.currentWidget()
        if current != new_widget:
            self.navigation_stack.append(current)
            self.ui.main_body_stack.setCurrentWidget(new_widget)
            
            # Special handling for taskbar switching if needed
            if new_widget == self.ui.project_homepage:
                self.switchActiveTaskbar()

    def go_back(self):
        """Go back to the previous page using navigation stack"""
        if self.navigation_stack:
            previous_widget = self.navigation_stack.pop()
            self.ui.main_body_stack.setCurrentWidget(previous_widget)
            
            # Special handling for taskbar switching if needed
            if previous_widget == self.ui.project_homepage:
                self.switchActiveTaskbar()
        else:
            # If no history, go home
            self.returnHome()

    def handle_project_creation(self):
        project_name = self.ui.input_project_name.toPlainText().strip()
        project_description = self.ui.plainTextEdit.toPlainText().strip()
        
        success = ProjectManager.create_new_project(
            parent=self,
            project_name=project_name,
            project_description=project_description,
            data_processor=self.data_processor
        )
        
        if success:
            self.ui.label_74.setText(project_name)
            self.ui.label_76.setText(project_name)
            self.navigate_to(self.ui.project_homepage)
            self.switchActiveTaskbar()

    def clear_project_widgets_only(self):
        """Clear only project-related widgets from the layout"""
        for i in reversed(range(self.ui.verticalLayout_18.count())):
            widget = self.ui.verticalLayout_18.itemAt(i).widget()
            if widget and (widget.objectName().startswith("projectFrame_") 
                        or widget.objectName() == "noProjectsFrame"):
                widget.deleteLater()
                self.ui.verticalLayout_18.removeWidget(widget)

    def load_projects_list(self):
        """Load all projects and display them in styled frames like the example"""

        #First clear all existing project frames
        self.clear_project_widgets_only()
        projects = ProjectManager.get_all_projects()
    
        if not projects:
            # Create a "no projects" message frame style
            no_projects_frame = QFrame()
            no_projects_frame.setObjectName("noProjectsFrame")
            no_projects_frame.setFrameShape(QFrame.Shape.StyledPanel)
            no_projects_frame.setFrameShadow(QFrame.Shadow.Raised)
            
            layout = QHBoxLayout(no_projects_frame)
            layout.setContentsMargins(0, 0, 0, 0)
            
            label = QLabel("No user projects found")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFont(self.font2)
            layout.addWidget(label)
            
            self.ui.verticalLayout_18.addWidget(no_projects_frame)
            return
        
        for project in projects:
            # Create container frame (same style as self.example_loadfile_container_)
            project_frame = QFrame(self.ui.load_body)
            project_frame.setObjectName(f"projectFrame_{project['project_name']}")
            project_frame.setFrameShape(QFrame.Shape.StyledPanel)
            project_frame.setFrameShadow(QFrame.Shadow.Raised)

            # Main horizontal layout
            frame_layout = QHBoxLayout(project_frame)
            frame_layout.setSpacing(0)
            frame_layout.setContentsMargins(0, 0, 0, 0)
            
            # Left side - Project info (matches example_loadfile_info)
            info_frame = QFrame(project_frame)
            info_frame.setObjectName(f"infoFrame_{project['project_name']}")
            sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            info_frame.setSizePolicy(sizePolicy)
            info_frame.setFrameShape(QFrame.Shape.StyledPanel)
            info_frame.setFrameShadow(QFrame.Shadow.Raised)
            
            info_layout = QVBoxLayout(info_frame)
            info_layout.setObjectName(u"verticalLayout")
            info_layout.setSpacing(0)
            info_layout.setContentsMargins(0, 0, 0, 0)
            
            # Project name (like label_26)
            name_label = QLabel(project['project_name'])
            name_label.setObjectName(f"projectName_{project['project_name']}")
            name_label.setFont(self.font2)
            info_layout.addWidget(name_label)
            
            # Project files, number of saved data files and image files (like label_27)
            project_name = project['project_name']
            base_data_dir = os.path.join("Projects", project_name, "datafiles")
            data_dir = os.path.join(base_data_dir, "raw_data")
            viz_dir = os.path.join(base_data_dir, "images")
            data_lst = os.listdir(data_dir)
            print(data_lst)
            viz_lst = os.listdir(viz_dir)
            attached_file_count = len(data_lst)
            attached_viz_count = len(viz_lst)

            desc_label = QLabel(f"{attached_file_count} attached files, {attached_viz_count} saved graphs")
            desc_label.setObjectName(f"projectDesc_{project['project_name']}")
            desc_label.setWordWrap(True)
            info_layout.addWidget(desc_label)
            
            # Last modified date (like label_28)
            date_label = QLabel(f"Last accessed: {project['last_modified']}")
            date_label.setObjectName(f"projectDate_{project['project_name']}")
            date_label.setFont(self.font5)  
            info_layout.addWidget(date_label)
            
            frame_layout.addWidget(info_frame)
            
            # Right side - Buttons (matches example_loadfile_buttons)
            buttons_frame = QFrame()
            buttons_frame.setObjectName(f"buttonsFrame_{project['project_name']}")
            buttons_frame.setFrameShape(QFrame.Shape.StyledPanel)
            buttons_frame.setFrameShadow(QFrame.Shadow.Raised)
            
            buttons_layout = QVBoxLayout(buttons_frame)
            buttons_layout.setSpacing(6)
            buttons_layout.setContentsMargins(0, 0, 0, 0)
            
            # Load button (like pushButton_3)
            load_btn = QPushButton("Load")
            load_btn.setObjectName(f"loadBtn_{project['project_name']}")
            load_btn.clicked.connect(lambda _, p=project: self.handle_project_load(p))
            buttons_layout.addWidget(load_btn)
            
            # Edit button (like pushButton_4)
            edit_btn = QPushButton("Edit")
            edit_btn.setObjectName(f"editBtn_{project['project_name']}")
            edit_btn.clicked.connect(lambda _, p=project: self.handle_project_edit(p))
            buttons_layout.addWidget(edit_btn)
            
            # Delete button (like pushButton_7)
            delete_btn = QPushButton("Delete")
            delete_btn.setObjectName(f"deleteBtn_{project['project_name']}")
            delete_btn.clicked.connect(lambda _, p=project: self.handle_project_delete(p))
            buttons_layout.addWidget(delete_btn)
            
            frame_layout.addWidget(buttons_frame)
            
            # Add the completed project frame to the scroll area
            self.ui.verticalLayout_18.addWidget(project_frame)
        
        # Add stretch to push content up
        self.ui.verticalLayout_18.addStretch()

    def handle_project_load(self, project=None):
        """Handle project loading of data"""
        if not project:
            QMessageBox.warning(
                self,
                "No Project Selected",
                "Please load or select a file first"
            )
            return
        project_name = project['project_name']
        try:
            # Call readData with the project to load preprocessed data
            df, sensor_states = self.data_processor.readData(project=project)
            
            if df is None or sensor_states is None:
                raise Exception("Failed to load project data")
            
            # Store the loaded data
            self.df = df
            self.sensor_states = sensor_states
            
            #Set Project Name in Project's Taskbar
            self.ui.label_74.setText(project_name)
            #Set Project Name in Project's Header
            self.ui.label_76.setText(project_name)

            base_data_dir = os.path.join("Projects", project_name, "datafiles")
            data_dir = os.path.join(base_data_dir, "processed_data")
            viz_dir = os.path.join(base_data_dir, "images")
            data_lst = os.listdir(data_dir)
            viz_lst = os.listdir(viz_dir)
            #Set up QLabels in dataset_list in project taskbar
            for element in data_lst:
                label = QLabel(element)
                label.setFont(self.font3)
                label.setWordWrap(True)
                self.ui.verticalLayout_26.addWidget(label)

            #Set up QLabels in map_list in project taskbar
            for element in viz_lst:
                label = QLabel(element)
                label.setFont(self.font3)
                label.setWordWrap(True)

                self.ui.verticalLayout_35.addWidget(label)

            # Switch to the project home page
            ProjectManager.set_project(project_name)
            self.navigate_to(self.ui.project_homepage)
            self.switchActiveTaskbar()

            # Display a success message
            QMessageBox.information(
                self,
                "Success",
                f"Project '{project_name}' loaded successfully"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"An error occurred while loading the project: {str(e)}"
            )
            print(f"Error loading project: {str(e)}")
            traceback.print_exc()
                
    def handle_project_delete(self, project=None):
        """Handle project deletion with confirmation"""
        if not project:
            QMessageBox.warning(
                self,
                "No Project Selected",
                "Please load or select a file first"
            )
            return
        
        if ProjectManager.del_project(project['project_name']):
             # Successful deletion - update UI
            self.navigate_to(self.ui.home_page)
            self.switchActiveTaskbar()
            
            project_frame = self.findChild(QFrame, f"projectFrame_{project['project_name']}")
            if project_frame:
                project_frame.deleteLater()
                self.ui.verticalLayout_18.removeWidget(project_frame)
           
            # Show success message
            QMessageBox.information(
                self,
                "Success",
                f"Project '{project['project_name']}' was deleted successfully"
            ) 
            
    def handle_project_edit(self, project):
        """Open project editing dialog"""
        self.edit_project_dialog = QDialog(self)
        self.edit_project_dialog.setWindowTitle("Edit Project")
        
        layout = QVBoxLayout()
        
        # Name
        name_label = QLabel("Project Name:")
        self.edit_name_input = QLineEdit(project['project_name'])
        layout.addWidget(name_label)
        layout.addWidget(self.edit_name_input)
        
        # Description
        desc_label = QLabel("Description:")
        self.edit_desc_input = QPlainTextEdit(project['project_description'])
        layout.addWidget(desc_label)
        layout.addWidget(self.edit_desc_input)
        
        # File management
        file_btn = QPushButton("Add Data Files")
        file_btn.clicked.connect(self.data_processor.getFileCSV)
        layout.addWidget(file_btn)
        
        # Dialog buttons
        btn_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(self.edit_project_dialog.accept)
        btn_box.rejected.connect(self.edit_project_dialog.reject)
        layout.addWidget(btn_box)
        
        self.edit_project_dialog.setLayout(layout)
        
        if self.edit_project_dialog.exec() == QDialog.Accepted:
            success = ProjectManager.edit_project(
                parent=self,
                old_name=project['project_name'],
                new_name=self.edit_name_input.text().strip(),
                new_description=self.edit_desc_input.toPlainText().strip(),
                data_processor=self.data_processorpr
            )
            
            if success:
                self.load_projects_list()
                QMessageBox.information(self, "Success", "Project updated successfully")

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
