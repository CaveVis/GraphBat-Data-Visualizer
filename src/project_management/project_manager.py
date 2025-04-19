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