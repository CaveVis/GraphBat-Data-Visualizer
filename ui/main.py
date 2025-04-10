# This Python file uses the following encoding: utf-8
import sys
from PyQt5 import QtWidgets
from PySide6.QtCore import Qt, QSettings
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QSizeGrip, QFileDialog
from mainwindow import Ui_mainwindow
import pandas as pd
import os
import traceback


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

        #Initialize data processor
        #self.data_processor = DataProcessor()

        self.ui.pushButton_5.clicked.connect(self.handleFileSelection)
        self.ui.pushButton_6.clicked.connect(self.handleImageSelection)
        #Create button (demo code)
        self.ui.confirm_create_button.clicked.connect(lambda: self.createNewProject())

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

    def handleImageSelection(self):
         #Will get file address of img file and read it
        file,_ = QFileDialog.getOpenFileName(filter = "Images (*.png *.xpm *.jpg)")
        if file:
            self.imgfile = file
            print("Files :", self.imgfile)
        else:
            print("No files selected.")

    def handleFileSelection(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select CSV Files", "", "CSV Files (*.csv)")
        if files:
            self.ui.filenames = files
            print("Files:", self.ui.filenames)
            self.readFileCSV(files)

    def readFileCSV(self, file_paths):
        dfs = []
        for file in file_paths:
            try:
                df = pd.read_csv(file)
                if 'datetime' in df.columns:
                    df['datetime'] = pd.to_datetime(df['datetime'])
                    df.set_index('datetime', inplace=True)
                dfs.append(df)
            except Exception as e:
                print(f"Error reading {file}: {e}")

        if dfs:
            self.df = pd.concat(dfs, axis=1)
            self.df.sort_index(inplace=True)
            print("DataFrame created successfully.")
    
    def readData(self):
    
        """
        Takes csv file(s) and returns a dataframe with index as datetime and datatype as columns.
        
        """

        #First pass: Read and preprocess all files
        merged_dfs = []
        for file in self.filenames:
            try:
                # Get column selections for this file
                if file not in self.column_selection:
                    print(f"No column selections for {file}, skipping file")
                    continue

                select = self.column_selection[file]
                index_col = select['index']
                data_col = select['data']
                rename = select['renames']

                sensor_name = os.path.basename(file).split('.')[0]

                # Skip if this sensor has already been processed this session
                # if temp_col_name in self.cleaned_anomaly_columns or temp_col_name in self.ignored_anomaly_columns:
                #   continue

                try:
                    # reads the csv files, only the selected columns, and saves it into a dataframe
                    cols = [index_col] + data_col
                    single_df = pd.read_csv(
                        file, encoding='utf-8',
                        usecols=cols
                    )
                except ValueError as e:
                    print(f"Missing required columns in {file}: {e}")
                    continue

                # Validate data content
                if single_df.empty:
                    print(f"No data in {file}")
                    continue

                try:
                    # formats the date time column so that it is readable by matplotlib
                    single_df[index_col] = pd.to_datetime(single_df[index_col],
                                                          errors="coerce")
                    # Drop rows with invalid dates
                    single_df = single_df.dropna(subset=[index_col])
                except Exception as e:
                    print(f"Can't convert {index_col} to datetime: {e}")
                    continue

                # Set index
                single_df = single_df.set_index(index_col)

                # Save rename choices
                rename_dict = {}
                for col in data_col:
                    if col in rename:
                        new_name = f"{rename[col]}_{sensor_name}"
                    else:
                        new_name = f"{col}_{sensor_name}"
                    rename_dict[col] = new_name

                single_df = single_df.rename(columns=rename_dict)
                # if the index is datetime
                if isinstance(single_df.index, pd.DatetimeIndex):
                    # Calculate time differences to detect sampling rate
                    time_diffs = single_df.index.to_series().diff()
                    sampling_interval = '2min'

                    if not time_diffs.empty:
                        # Get the most common time difference (mode) to determine sampling rate
                        sampling_interval = time_diffs.mode().iloc[0] if not time_diffs.empty else pd.Timedelta(0)
                        print(f"Detected sampling interval: {sampling_interval}")
                    else:
                        print("Warning: Could not determine sampling interval for input data")

                    # Resample to consistent interval (e.g. 2 minutes)
                    single_df = single_df.resample(sampling_interval).mean().interpolate(method='linear')

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
            
            self.updateStatistics()
            self.update(self.themes[0])
        
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
