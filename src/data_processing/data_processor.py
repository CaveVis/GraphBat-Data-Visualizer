import os
import shutil
import datetime
import pandas as pd
import traceback
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import (QApplication, QMainWindow, QSizeGrip, QFileDialog, QWidget,
                                QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QComboBox, QListWidget, QAbstractItemView, QListWidgetItem,
                                QLineEdit, QPushButton, QDialogButtonBox, QMessageBox, QDialog, QTableWidget,QHeaderView, QTableWidgetItem)

from src.project_management.project_manager import ProjectManager

class ColumnSelectionDialog(QDialog):
    def __init__(self, columns, parent=None):
        super(ColumnSelectionDialog, self).__init__(parent)
        self.setWindowTitle("Select Columns To Read")
        self.resize(400, 300)

        self.layout = QVBoxLayout(self)

        # Test description directing user
        self.description = QLabel("Select an index column from you inputted CSV files and a data column:")
        self.layout.addWidget(self.description)

        # Selection of index columns
        self.index_group = QGroupBox("Index Column (column that will tie all columns together ex:date-time)")
        self.index_layout = QVBoxLayout(self.index_group)
        self.index_combo = QComboBox()
        self.index_combo.addItems(columns)
        self.index_layout.addWidget(self.index_combo)
        self.layout.addWidget(self.index_group)

        # Selection of data columns
        self.data_group = QGroupBox("Data Columns")
        self.data_layout = QVBoxLayout(self.data_group)

        # Widget for adding spefic columns columns
        self.data_list = QListWidget()
        self.data_list.setSelectionMode(QAbstractItemView.MultiSelection)
        for column in columns:
            item = QListWidgetItem(column)
            self.data_list.addItem(item)
        self.data_layout.addWidget(self.data_list)
        self.layout.addWidget(self.data_group)

        # Rename selected columns widgets
        self.rename_group = QGroupBox("Rename Selected Data Column (Optional)")
        self.rename_layout = QHBoxLayout(self.rename_group)
        self.rename_label = QLabel("New Name:")
        self.rename_edit = QLineEdit()
        self.rename_button = QPushButton("Set Name")
        self.rename_layout.addWidget(self.rename_label)
        self.rename_layout.addWidget(self.rename_edit)
        self.rename_layout.addWidget(self.rename_button)
        self.layout.addWidget(self.rename_group)

        # Connect rename button
        self.rename_button.clicked.connect(self.rename_selected)

        # Buttons for column selection
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
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
            QMessageBox.warning(self, "Selection Error", "Please select an index column")
            return

        if not self.selected_data:
            QMessageBox.warning(self, "Selection Error", "Please select at least one data column")
            return

        super(ColumnSelectionDialog, self).accept()

class AnomalyDialog(QDialog):
    def __init__(self, parent=None, anomaly_info=None):
        super(AnomalyDialog, self).__init__(parent)
        self.setWindowTitle("Anomaly Detection")
        self.resize(600, 400)
        
        # Main layout
        self.layout = QVBoxLayout(self)
        
        #Detailed information label
        sensor_name = anomaly_info.get('sensor_name', 'Unknown')
        count = anomaly_info.get('count', 0)
        lower_bound = anomaly_info.get('global_lower_bound', 'N/A')
        upper_bound = anomaly_info.get('global_upper_bound', 'N/A')
        total_points = anomaly_info.get('total_points', 0)
        percent_anomalies = (count / total_points * 100) if total_points > 0 else 0
        
        info_text = (
            f"<h3>Anomalies Detected in {sensor_name} Sensor</h3>"
            f"<p>Total Anomalies: {count} </p>"
            f"<p>Total Anomalies: {count} out of {total_points} data points ({percent_anomalies:.2f}%)</p>"
            f"<p>Anomaly Thresholds:</p>"
            f"<ul>"
            f"<li>Lower Bound: {lower_bound:.2f}</li>"
            f"<li>Upper Bound: {upper_bound:.2f}</li>"
            f"</ul>"
            "<p>Choose how to handle these anomalies:</p>"
        )

        self.info_label = QLabel(info_text)
        self.info_label.setWordWrap(True)
        self.layout.addWidget(self.info_label)
        
        # Create table to display anomalies
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Timestamp", "Value"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.layout.addWidget(self.table)
        
        # Fill table with anomaly clean_data
        outliers = anomaly_info.get('values', pd.Series())

        #Ensure outliers index is datetime
        if len(outliers) > 0:
            self.table.setRowCount(len(outliers))
            
            #Process each outlier
            for i, (timestamp, value) in enumerate(outliers.items()):
                    #Handle timestamp formatting
                    if isinstance(timestamp, (pd.Timestamp, datetime.datetime)):
                        time_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        #Try to convert to datetime if not already
                        try:
                            timestamp = pd.to_datetime(timestamp)
                            time_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                        except:
                            #If all else fails, use string representation
                            time_str = str(timestamp)

                    #Create and add table items
                    time_item = QTableWidgetItem(time_str)
                    value_item = QTableWidgetItem(f"{value:.2f}")
                    self.table.setItem(i, 0, time_item)
                    self.table.setItem(i, 1, value_item)
        else:
            self.table.setRowCount(0)

        
        # Button group
        self.button_box = QHBoxLayout()
        
        # Create options
        self.remove_button = QPushButton("Remove Outliers")
        self.ignore_button = QPushButton("Ignore Outliers")
        self.view_button = QPushButton("View Outliers")
        
        self.button_box.addWidget(self.remove_button)
        self.button_box.addWidget(self.ignore_button)
        self.button_box.addWidget(self.view_button)
        self.layout.addLayout(self.button_box)
        
        # Connect buttons to actions
        self.remove_button.clicked.connect(self.accept_remove)
        self.ignore_button.clicked.connect(self.accept_ignore)
        self.view_button.clicked.connect(self.accept_view)
        
        # Result attribute to track user's choice
        self.result = "cancel"
        
    def accept_remove(self):
        self.result = "remove"
        self.accept()
        
    def accept_ignore(self):
        self.result = "ignore"
        self.accept()
    
    def accept_view(self):
        self.result = "view"
        self.accept()

class DataProcessor:
    def __init__(self, parent=None):
        # Store parent widget reference
        self.parent = parent
        self.sensor_states = {}
        self.filenames = []
        self.c_column_selection = {}
        self.rename_dict = {}
        self.df = pd.DataFrame()

    def getFileCSV(self):
        #Will get file address of csv file and read it
        files,_ = QFileDialog.getOpenFileNames(filter="CSV Files (*.csv)")
        if files:
            self.filenames = files
            print("Files :", self.filenames)

            #if not files are selected
            if not self.filenames:
                print("No valid files selected.")
                return
            
            try:
                #Only asks for columns on first file and used for all files
                f_file = self.filenames[0]
                sample_df =pd.read_csv(f_file, nrows=0, encoding='utf-8')
                column = sample_df.columns.tolist()

                #Dialog box shows up to select columns once
                dial = ColumnSelectionDialog(column)
                if dial.exec_() == QDialog.Accepted:
                    if not hasattr(self, 'c_column_selection'):
                        self.c_column_selection = {}

                    self.c_column_selection = {
                        'index': dial.selected_index,
                        'data': dial.selected_data,
                        'renames': dial.column_rename
                    }
                    #self.readData()
                else:
                    # If a user cancels selection, remove that file
                    print("Column selection cancelled.")

            except Exception as e:
                print(f"Error reading columns from {f_file}: {e}")
                traceback.print_exc()

        else:
            print("No files selected.")

        return self.filenames
    
    def getFileImage(self):
         #Will get file address of img file and read it
        file,_ = QFileDialog.getOpenFileName(filter = "Images (*.png *.xpm *.jpg)")
        if file:
            self.imgfile = file
            print("Files :", self.imgfile)
        else:
            print("No files selected.")

    def readData(self, project=None):
    
        """
        Takes csv file(s) and returns a dataframe with index as datetime and datatype as columns.
        
        """
        if project:
            # Project mode - load preprocessed data
            project_name = project['project_name']
            base_data_dir = os.path.join("Projects", project_name, "datafiles", "preprocessed_data")
            merged_filepath = os.path.join(base_data_dir, "preprocessed_merged_data.csv")
            
            try:
                # Load the merged dataframe
                self.df = pd.read_csv(merged_filepath, index_col=0, parse_dates=True)
                
                # Reconstruct sensor_states from individual preprocessed files
                self.sensor_states = {}
                for file in os.listdir(base_data_dir):
                    if file.startswith("preprocessed_") and file != "preprocessed_merged_data.csv":
                        sensor_name = file.split('_')[1].split('.')[0]
                        filepath = os.path.join(base_data_dir, file)
                        single_df = pd.read_csv(filepath, index_col=0, parse_dates=True)
                        
                        for col in single_df.columns:
                            # Recreate sensor state for each column
                            anomaly_info = self.detectAnomalies(single_df[col])
                            self.sensor_states[col] = {
                                'status': 'raw',
                                'original_data': single_df[[col]].copy(),
                                'processed_data': single_df[[col]].copy(),
                                'anomalies': anomaly_info['values'],
                                'bounds': {
                                    'lower': anomaly_info['global_lower_bound'],
                                    'upper': anomaly_info['global_upper_bound']
                                }
                            }
                return self.df, self.sensor_states 
                     
            except Exception as e:
                print(f"Error loading preprocessed data: {str(e)}")
                traceback.print_exc()
                return None, None
            
        #Normal mode - no project, reading raw files
        if not hasattr(self, 'c_column_selection') or not self.c_column_selection:
            print("No columns selected. Please select columns")
            return
        
        index_col = self.c_column_selection['index']
        data_cols = self.c_column_selection['data']
        renames = self.c_column_selection.get('renames', {})

        project_name = ProjectManager.get_project()
        base_data_dir = os.path.join("Projects", project_name, "datafiles")
        premerge_data_dir = os.path.join(base_data_dir, "preprocessed_data")
        merged_data_dir = os.path.join(base_data_dir, "preprocessed_data")

        #First pass: Read and preprocess all files
        merged_dfs = []
        for file in self.filenames:
            try:
                sensor_name = os.path.basename(file).split('.')[0]
                try:
                    # reads the csv files and only the columns the user selected and puts it into a dataframe
                    cols = [index_col] + data_cols
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
                for col in data_cols:
                    if col in renames:
                        new_name = f"{renames[col]}_{sensor_name}"
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
                        sampling_interval = time_diffs.mode().iloc[0] if not time_diffs.empty else pd.Timedelta(minutes=2)
                        #print(f"Detected sampling interval: {sampling_interval}")
                    else:
                        print("Warning: Could not determine sampling interval for input data")

                    # Resample to consistent interval (e.g. 2 minutes)
                    single_df = single_df.resample(sampling_interval).mean().interpolate(method='linear')

                # Save the preprocessed single file before merging
                raw_filename = f"preprocessed_{sensor_name}.csv"
                raw_filepath = os.path.join(premerge_data_dir, raw_filename)
                single_df.to_csv(raw_filepath)
                print(f"Saved preprocessed file: {raw_filepath}")

                # Process each column for anomalies and store in sensor states
                for col in single_df.columns:
                    try:
                        # Detect anomalies
                        anomaly_info = self.detectAnomalies(single_df[col])

                    # Store initial state
                        self.sensor_states[col] = {
                            'status': 'raw',
                            'original_data': single_df[[col]].copy(),
                            'processed_data': single_df[[col]].copy(),
                            'anomalies': anomaly_info['values'],
                            'bounds': {
                                'lower': anomaly_info['global_lower_bound'],
                                'upper': anomaly_info['global_upper_bound']
                            }
                    }
                    except Exception as e:
                        print(f"Warning: Error detecting anomalies the following columns: {col}: {str(e)}")
                        traceback.print_exc()
                        # Continue processing other columns
                        continue

                merged_dfs.append(single_df)

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
        
            # Save the merged dataframe
            raw_merged_filename = "preprocessed_merged_data.csv"
            raw_merged_filepath = os.path.join(merged_data_dir, raw_merged_filename)
            self.df.to_csv(raw_merged_filepath)
            print(f"Saved merged data: {raw_merged_filepath}")

        return self.df, self.sensor_states

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