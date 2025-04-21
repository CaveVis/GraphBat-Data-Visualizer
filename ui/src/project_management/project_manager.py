import os
import json
import re
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
    def edit_project(cls, parent, old_name, new_name, new_description, data_processor):
        """Edit existing project metadata and data files"""
        # Validate new name
        if not new_name:
            cls.show_error_message(parent, "Project name cannot be empty")
            return False
        
        if new_name != old_name:
            if not re.match(r'^[a-zA-Z0-9_\-()]+$', new_name):
                cls.show_error_message(parent, "Invalid characters in project name")
                return False
            
            if len(new_name) > 40:
                cls.show_error_message(parent, "Project name too long (max 40 chars)")
                return False

        old_path = os.path.join("Projects", old_name)
        new_path = os.path.join("Projects", new_name)

        try:
            # Rename directory if name changed
            if new_name != old_name:
                if os.path.exists(new_path):
                    cls.show_error_message(parent, "Project name already exists")
                    return False
                shutil.move(old_path, new_path)

            # Update project info
            json_path = os.path.join(new_path, "project_info.json")
            with open(json_path, 'r+') as f:
                data = json.load(f)
                data['project_name'] = new_name
                data['project_description'] = new_description
                data['last_modified'] = datetime.datetime.now().isoformat()
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()

            # Update current project if it was edited
            if cls.current_project == old_name:
                cls.current_project = new_name

            # Process new data files
            raw_data_path = os.path.join(new_path, "datafiles", "raw_data")
            if hasattr(data_processor, 'filenames') and data_processor.filenames:
                for file_path in data_processor.filenames:
                    shutil.copy2(file_path, raw_data_path)

            return True
        except Exception as e:
            cls.show_error_message(parent, f"Error editing project: {str(e)}")
            return False
        
    @classmethod
    def del_project(cls, project_name=None):
        """Delete a project, with optional project_name parameter"""

        target_project = project_name if project_name is not None else cls.current_project
        if target_project is None:
            return False
        
        #current_project = cls.get_project()
        proj_dir = os.path.join("Projects", target_project)
        
        # First confirmation
        confirm1 = QMessageBox.question(
            None,
            "Confirm Deletion",
            f"Delete project '{target_project}' and all its files?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm1 == QMessageBox.No:
            return False
        # Second confirmation
        confirm2 = QMessageBox.question(
            None,
            "Final Warning",
            "This cannot be undone! All project data will be permanently lost.\n"
            "Are you absolutely sure?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm2 == QMessageBox.No:
            return False
    
        try:
            shutil.rmtree(proj_dir)
            if cls.current_project == target_project:
                cls.current_project = None  # Clear current if it was deleted
            return True
        except Exception as e:
            cls.show_error_message(None, f"Failed to delete project: {str(e)}")
            return False
        
    @classmethod
    def get_project(cls):
        return cls.current_project
    
    @classmethod
    def get_all_projects(cls):
        """Return a list of all existing projects with their metadata"""
        projects_dir = "Projects"
        projects = []
        
        if not os.path.exists(projects_dir):
            return projects
        
        for project_name in os.listdir(projects_dir):
            project_path = os.path.join(projects_dir, project_name)
            if os.path.isdir(project_path):
                # Get project info from JSON file
                project_info = cls.get_project_info(project_name)
                
                if project_info is None:
                    # Create basic info if JSON is missing
                    project_info = {
                        "project_name": project_name,
                        "project_description": "No description available",
                        "created_at": "Unknown",
                        "last_modified": "Unknown"
                    }
            
                # Add the project path and any additional metadata
                project_info["path"] = project_path
                projects.append(project_info)

        return projects
    
    @classmethod
    def create_new_project(cls, parent, project_name, project_description, data_processor):
        """Create a new project with validation and folder structure"""
        max_title_len = 40
        max_desc_len = 500
        
        # Error checking for project name
        if not project_name:
            cls.show_error_message(parent, "Project name is empty")
            return False
        if len(project_name) > max_title_len:
            cls.show_error_message(parent, f"Project name cannot exceed {max_title_len} chars")
            return False

        validChar = re.compile(r'^[a-zA-Z0-9_\-()]+$')
        if not validChar.match(project_name):
            # Find the invalid character
            for char in project_name:
                if not re.match(r'[a-zA-Z0-9_\-()]', char):
                    cls.show_error_message(parent, f"'{char}' is not allowed.")
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

            os.makedirs("Projects", exist_ok=True)
            hasData = hasattr(data_processor, 'filenames') and data_processor.filenames

            if not hasData:
                # Saving without CSV files attached
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Question)
                msg_box.setText("Project does not contain any CSV files (CSV files can be added later). Save new project?")
                msg_box.setWindowTitle("Confirm Save")
                msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                result = msg_box.exec()
                if result == QMessageBox.No:
                    return False
            elif hasData:
                # Saving with CSV files attached
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Question)
                msg_box.setText("You are about to save a project that has a dataset attached. Please confirm that you want to save. This action will update the dataset accordingly.")
                msg_box.setWindowTitle("Confirm Save")
                msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                result = msg_box.exec()
                if result == QMessageBox.No:
                    return False
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