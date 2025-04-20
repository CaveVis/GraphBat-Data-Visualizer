import os
import json
import shutil
import datetime
import traceback
from PySide6.QtWidgets import QMessageBox

class ProjectManager:
    _instance = None
    current_project = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def set_project(cls, project_name):
        cls.current_project = project_name
    
    @classmethod
    def get_project(cls):
        return cls.current_project
    
    @classmethod
    def create_new_project(cls, parent, project_name, project_description, data_processor):
        """Create a new project with validation and folder structure"""
        max_title_len = 50
        max_desc_len = 500
        
        # Error checking for project name
        if not project_name:
            cls.show_error_message(parent, "Project name is empty")
            return False
        if len(project_name) > max_title_len:
            cls.show_error_message(parent, f"Project name cannot exceed {max_title_len} chars")
            return False
        # Validate description length
        if len(project_description) > max_desc_len:
            cls.show_error_message(parent, f"Project description cannot exceed {max_desc_len} characters")
            return False

        # Create project directory structure
        project_folder = os.path.join("Projects", project_name)
        if os.path.exists(project_folder):
            cls.show_error_message(parent, f"A project named '{project_name}' exists, try a different name")
            return False

        try:
            # Create project info
            project_data = {
                "project_name": project_name,
                "project_description": project_description,
                "created_at": datetime.datetime.now().isoformat(),
                "last_modified": datetime.datetime.now().isoformat()
            }

            # Create directories
            os.makedirs(project_folder)
            data_subfolders = ['raw_data', 'preprocessed_data', 'processed_data', 'images', 'videos']
            for folder in data_subfolders:
                folder_path = os.path.join(project_folder, 'datafiles', folder)
                os.makedirs(folder_path, exist_ok=True)

            # Save project info
            json_file_path = os.path.join(project_folder, "project_info.json")
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, indent=4)

            # Save raw data files if they exist
            if hasattr(data_processor, 'filenames') and data_processor.filenames:
                raw_data_path = os.path.join(project_folder, "datafiles", "raw_data")
                for file_path in data_processor.filenames:
                    try:
                        filename = os.path.basename(file_path)
                        dest_path = os.path.join(raw_data_path, filename)
                        shutil.copy2(file_path, dest_path)
                    except Exception as e:
                        print(f"Error saving {file_path}: {str(e)}")
                        traceback.print_exc()

            cls.set_project(project_name)
            return True
            
        except Exception as e:
            cls.show_error_message(parent, f"An error occurred while creating project: {str(e)}")
            return False

    @classmethod
    def get_project_info(cls, project_name):
        """Get project information from its JSON file"""
        project_folder = os.path.join("Projects", project_name)
        json_file = os.path.join(project_folder, "project_info.json")
        
        if not os.path.exists(json_file):
            return None
            
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading project info: {e}")
            return None

    @staticmethod
    def show_error_message(parent, message):
        QMessageBox.warning(parent, "Error", message)

    @staticmethod
    def show_success_message(parent, message):
        QMessageBox.information(parent, "Success", message)