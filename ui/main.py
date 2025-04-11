# This Python file uses the following encoding: utf-8
import sys
from PyQt5 import QtWidgets
from PySide6.QtCore import Qt, QSettings
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QSizeGrip, QFileDialog, QWidget
from mainwindow import Ui_mainwindow
import pandas as pd
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as Navi
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import os
import traceback

#Canvas class
class MatplotlibCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None,width=5, height = 5, dpi = 120):
        f = Figure(figsize = (width,height),dpi = dpi)
        self.axes= f.add_subplot(111)
        super(MatplotlibCanvas,self).__init__(f)
        f.tight_layout(pad=3)

class ColumnSelectionDialog(QtWidgets.QDialog):
    def __init__(self, columns, parent=None):
        super(ColumnSelectionDialog, self).__init__(parent)
        self.setWindowTitle("Select Columns To Read")
        self.resize(400, 300)

        self.layout = QtWidgets.QVBoxLayout(self)

        # Test description directing user
        self.description = QtWidgets.QLabel("Select an index column from you inputted CSV files and a data column:")
        self.layout.addWidget(self.description)

        # Selection of index columns
        self.index_group = QtWidgets.QGroupBox("Index Column (column that will tie all columns together ex:date-time)")
        self.index_layout = QtWidgets.QVBoxLayout(self.index_group)
        self.index_combo = QtWidgets.QComboBox()
        self.index_combo.addItems(columns)
        self.index_layout.addWidget(self.index_combo)
        self.layout.addWidget(self.index_group)

        # Selection of data columns
        self.data_group = QtWidgets.QGroupBox("Data Columns")
        self.data_layout = QtWidgets.QVBoxLayout(self.data_group)

        # Widget for adding spefic columns columns
        self.data_list = QtWidgets.QListWidget()
        self.data_list.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        for column in columns:
            item = QtWidgets.QListWidgetItem(column)
            self.data_list.addItem(item)
        self.data_layout.addWidget(self.data_list)
        self.layout.addWidget(self.data_group)

        # Rename selected columns widgets
        self.rename_group = QtWidgets.QGroupBox("Rename Selected Data Column (Optional)")
        self.rename_layout = QtWidgets.QHBoxLayout(self.rename_group)
        self.rename_label = QtWidgets.QLabel("New Name:")
        self.rename_edit = QtWidgets.QLineEdit()
        self.rename_button = QtWidgets.QPushButton("Set Name")
        self.rename_layout.addWidget(self.rename_label)
        self.rename_layout.addWidget(self.rename_edit)
        self.rename_layout.addWidget(self.rename_button)
        self.layout.addWidget(self.rename_group)

        # Connect rename button
        self.rename_button.clicked.connect(self.rename_selected)

        # Buttons for column selection
        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        self.layout.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Initialize choices
        self.selected_index = ""
        self.selected_data = []
        self.column_rename = {}
    #Rename selected column
    def rename_selected(self):
        selected_item = self.data_list.selectedItems()
        if selected_item and self.rename_edit.text().strip():
            colum_n = selected_item[0].text()
            new_name = self.rename_edit.text().strip()
            self.column_rename[colum_n] = new_name

            # Update show new names
            selected_item[0].setText(f"{colum_n} → {new_name}")

            # Clear the edit
            self.rename_edit.clear()
    #Takes in user selection from index and data
    def accept(self):
        self.selected_index = self.index_combo.currentText()
        self.selected_data = [item.text().split(" → ")[0] for item in
                              [self.data_list.item(i) for i in range(self.data_list.count())
                               if self.data_list.item(i).isSelected()]]

        # Error checking
        if not self.selected_index:
            QtWidgets.QMessageBox.warning(self, "Selection Error", "Please select an index column")
            return

        if not self.selected_data:
            QtWidgets.QMessageBox.warning(self, "Selection Error", "Please select at least one data column")
            return

        super(ColumnSelectionDialog, self).accept()

class MainWindow(QMainWindow):
    def __init__(self, /):
        QMainWindow.__init__(self)
        self.ui = Ui_mainwindow()
        self.ui.setupUi(self)

        ##############################
        ### Set up session variables
        ##############################
        self.canv = MatplotlibCanvas(self)
        self.sensor_states = {}

        ### Load existing user preferences ###
        self.app_settings = QSettings("GraphBat", "userPrefs")
        #Theme
        self.switchStylesheet(self.app_settings.value("theme", "style_brown.qss"))
        self.ui.appTheme_combobox.setCurrentIndex(self.app_settings.value("theme_index", 0))
        #Fullscreen mode
        is_fullscreen = self.app_settings.value("is_fullscreen", True)
        if is_fullscreen:
            self.ui.maximize_button.clicked.connect(self.toggleMaximized())
            self.ui.fullscreen_checkbox.setChecked(True)
        else:
            self.ui.fullscreen_checkbox.setChecked(False)
        #Font
        is_dyslexic = self.app_settings.value("is_dyslexic", False)
        if is_dyslexic:
            print("read is dyslexic")
            QApplication.instance().setFont(QFont("Comic Sans MS"))
            self.ui.dyslexicfont_checkbox.setChecked(True)
        else:
            print("read is not dyslexic")
            QApplication.instance().setFont(QFont("Verdana"))
            self.ui.dyslexicfont_checkbox.setChecked(False)
        print(f"User preferences are saved at {self.app_settings.fileName()}")

        #################################

        #Taskbar setup
        self.taskbar_width = 300

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

        self.ui.pushButton_5.clicked.connect(self.getFileCSV)
        self.ui.pushButton_6.clicked.connect(self.handleImageSelection)
        #Create button (demo code)
        self.ui.confirm_create_button.clicked.connect(lambda: self.createNewProject())

        ########################
        ### Project page buttons

        self.ui.button_linegraph.clicked.connect(lambda: self.display_canvas_in_frame("Line Graph"))
        self.ui.button_bargraph.clicked.connect(lambda: self.display_canvas_in_frame("Bar Graph"))
        self.ui.button_histogram.clicked.connect(lambda: self.display_canvas_in_frame("Histogram"))
        self.ui.button_boxplot.clicked.connect(lambda: self.display_canvas_in_frame("Box Plot"))
        self.ui.button_cavemap.clicked.connect(lambda: self.display_canvas_in_frame("Cave Map"))

        #########################

        #########################
        ### Project toolbar graph buttons
        #Only implemented for bar graph buttons for now
        self.ui.pushButton_10.clicked.connect(lambda: self.set_agg_method("mean"))
        self.ui.pushButton_20.clicked.connect(lambda: self.set_agg_method("median"))
        self.ui.pushButton_8.clicked.connect(lambda: self.set_agg_method("min"))
        self.ui.pushButton_18.clicked.connect(lambda: self.set_agg_method("max"))
        self.ui.pushButton_16.clicked.connect(lambda: self.set_agg_method("sum"))
        self.ui.pushButton_9.clicked.connect(lambda: self.set_agg_method("count"))

        ##########################

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

    def set_agg_method(self, method):
        self.agg_method = method
        self.display_canvas_in_frame("Bar Graph")

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

        #Clear the axes
        self.canv.axes.cla()
        
        if not self.df.empty:
            try:
                if graph_type == "Line Graph":
                    for c in self.df.columns:
                        if not self.df[c].empty:
                            self.canv.axes.plot(self.df.index, self.df[c], label = c)

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
                        elif self.agg_method == "median":
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
                            self.canv.axes.boxplot(clean_data, labels=labels, patch_artist=True)
                            # Configure plot
                            self.canv.axes.set_xlabel('Sensor')
                            self.canv.axes.set_ylabel('Temperature (°C)')
                            self.canv.axes.set_title('Temperature Distribution by Sensor')
                            self.canv.axes.grid(True, linestyle='--', alpha=0.7)
                            
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

    def handleImageSelection(self):
         #Will get file address of img file and read it
        file,_ = QFileDialog.getOpenFileName(filter = "Images (*.png *.xpm *.jpg)")
        if file:
            self.imgfile = file
            print("Files :", self.imgfile)
        else:
            print("No files selected.")

    def getFileCSV(self):
         #Will get file address of csv file and read it
         files,_ = QFileDialog.getOpenFileNames(filter="CSV Files (*.csv)")
         if files:
             self.filenames = files
             print("Files :", self.filenames)
             self.readData()
         else:
             print("No files selected.")
    
    def readData(self):
    
        """
        Takes csv file(s) and returns a dataframe with index as datetime and datatype as columns.
        
        """

        #First pass: Read and preprocess all files
        for file in self.filenames:
            try:
                sensor_name = os.path.basename(file).split('.')[0]
                temp_col_name = f"Temperature_{sensor_name}"

                #Skip if already processed
                if temp_col_name in self.sensor_states:
                    continue

                try:
                    #reads the csv files, only the Date time and temperature column, and saves it into a dataframe
                    single_df = pd.read_csv(
                        file,encoding = 'utf-8',
                        usecols=['Date-Time (EST)', 'Temperature   (°C)']
                        )
                    
                except ValueError as e:
                    print(f"Missing required columns in {file}: {e}")
                    continue

                #Validate data content
                if single_df.empty:
                    print(f"No data in {file}")
                    continue
                
                #formats the date time column so that it is readable by matplotlib
                single_df["Date-Time (EST)"] = pd.to_datetime(single_df["Date-Time (EST)"], 
                                                             format="%m/%d/%Y %H:%M:%S", errors="coerce")
                # Drop rows with invalid dates
                single_df = single_df.dropna(subset=["Date-Time (EST)"])

                #Set datetime as index
                single_df = single_df.set_index("Date-Time (EST)")

                # Calculate time differences to detect sampling rate
                time_diffs = single_df.index.to_series().diff()

                if not time_diffs.empty:
                    # Get the most common time difference (mode) to determine sampling rate
                    sampling_interval = time_diffs.mode().iloc[0] if not time_diffs.empty else pd.Timedelta(0)
                    print(f"Detected sampling interval: {sampling_interval}")
                else:
                    print("Warning: Could not determine sampling interval for input data")
                    
                #Resample to consistent interval (e.g. 2 minutes)
                single_df = single_df.resample(sampling_interval).mean().interpolate(method='linear')   
                        
                # Rename temperature column to include sensor name
                single_df = single_df.rename(
                    columns={'Temperature   (°C)': temp_col_name}
                    )
                
                # Detect anomalies
                anomaly_info = self.detectAnomalies(single_df[temp_col_name])
                print(anomaly_info)
                # Store initial state
                self.sensor_states[temp_col_name] = {
                    'status': 'raw',
                    'original_data': single_df[[temp_col_name]].copy(),
                    'processed_data': single_df[[temp_col_name]].copy(),
                    'anomalies': anomaly_info['values'],
                    'bounds': {  
                        'lower': anomaly_info['global_lower_bound'],
                        'upper': anomaly_info['global_upper_bound']
                    }
                }

            except Exception as e:
                print(f"Error processing {file}: {str(e)}")
                traceback.print_exc()
                continue

        # Build main dataframe from sensor states
        dfs = []
        for sensor, state in self.sensor_states.items():
            dfs.append(state['processed_data'])
        
        self.df = pd.concat(dfs, axis=1) if dfs else pd.DataFrame()    

        if not self.df.empty:
            self.df.index = pd.to_datetime(self.df.index)
            self.df = self.df.sort_index().dropna(axis=0)
            
            # Write CSV
            os.makedirs('datafiles', exist_ok=True)
            file_path = os.path.join('datafiles', 'originalDF.csv')
            self.df.to_csv(file_path)

    def detectAnomalies(self, data):
        """
        Enhanced anomaly detection with better spike handling and duplicate management
        """
        clean_data = data.dropna()
        sensor_name = clean_data.name.replace("Temperature_", "") if hasattr(clean_data, 'name') else "Unknown"

        if clean_data.empty:
            return {
                "count": 0,
                "values": pd.Series(dtype=float),
                "global_lower_bound": None,
                "global_upper_bound": None,
                "total_points": 0,
                "sensor_name": sensor_name
            }

        # Calculate quartiles and IQR
        Q1 = clean_data.quantile(0.25, interpolation='midpoint')
        Q3 = clean_data.quantile(0.75, interpolation='midpoint')
        IQR = Q3 - Q1

        # Identify IQR outliers
        threshold = 1.5
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        iqr_outliers = clean_data[(clean_data < lower_bound) | (clean_data > upper_bound)]
        
        # Spike detection with adaptive threshold
        diff = clean_data.diff().abs()
        if not diff.empty:
            # Dynamic spike threshold based on rolling window
            rolling_std = diff.rolling(window=10, min_periods=1).std()
            spike_threshold = 3 * rolling_std  # 3 standard deviations
            spike_outliers = clean_data[diff > spike_threshold]
            
            # Combine outliers while preserving important cases
            combined_outliers = pd.concat([iqr_outliers, spike_outliers])
            
            # Smart de-duplication - keep all if they're significant spikes
            if not combined_outliers.empty:
                # Only remove duplicates that aren't significant spikes
                mask = (combined_outliers.index.duplicated(keep='first') & 
                    (diff.loc[combined_outliers.index] < 2 * rolling_std.loc[combined_outliers.index]))
                outliers = combined_outliers[~mask]
            else:
                outliers = combined_outliers
        else:
            outliers = iqr_outliers

        return {
            "count": len(outliers),
            "values": outliers.sort_values(),
            "global_lower_bound": lower_bound,
            "global_upper_bound": upper_bound,
            "total_points": len(clean_data),
            "sensor_name": sensor_name,
            "iqr_outliers": len(iqr_outliers),
            "spike_outliers": len(outliers) - len(iqr_outliers)
        }  
    
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
        self.ui.main_body_stack.setCurrentWidget(self.ui.project_homepage)
        self.switchActiveTaskbar()

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
