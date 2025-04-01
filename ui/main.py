# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtCore import Qt, QSettings
from PyQt5.QtWidgets import QMainWindow, QApplication
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QSizeGrip
from mainwindow import Ui_mainwindow


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
