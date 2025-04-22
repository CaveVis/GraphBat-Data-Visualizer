# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QCheckBox, QComboBox,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QMainWindow, QMenuBar,
    QPlainTextEdit, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QStackedWidget, QTextEdit, QToolBox,
    QVBoxLayout, QWidget)
import icons_rc

class Ui_mainwindow(object):
    def setupUi(self, mainwindow):
        if not mainwindow.objectName():
            mainwindow.setObjectName(u"mainwindow")
        mainwindow.resize(960, 540)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mainwindow.sizePolicy().hasHeightForWidth())
        mainwindow.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(u":/logo/images/logos/Logo V2.ico", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        mainwindow.setWindowIcon(icon)
        mainwindow.setStyleSheet(u"*[style_ID=\"borderThick\"]\n"
"{\n"
"border: 2px solid #AD6300;\n"
"}\n"
"\n"
"*[style_ID=\"header\"]\n"
"{\n"
"background-color: #1A110A;\n"
"border: 1px solid #AD6300;\n"
"}\n"
"\n"
"*[style_ID=\"banner\"]\n"
"{\n"
"background-color: #493721;\n"
"border: none;\n"
"}\n"
"\n"
"*[style_ID=\"footer\"]\n"
"{\n"
"background-color: #1A110A;\n"
"border-top: 1px solid #AD6300;\n"
"}\n"
"\n"
"\n"
"*[style_ID=\"subtleText\"]\n"
"{\n"
"color: #AD6300\n"
"}\n"
"\n"
"*[style_ID=\"backgroundGraphic\"]\n"
"{\n"
"border-image: url(:/backgrounds/images/bgs/Cave Background Digital.png) stretch;\n"
"background-position: center;\n"
"}\n"
"\n"
"*[style_ID=\"backgroundDark\"]\n"
"{\n"
"background-color: #1A110A;\n"
"}\n"
"\n"
"*[style_ID=\"borderlessDark\"]\n"
"{\n"
"background-color: #1A110A;\n"
"border:none;\n"
"}\n"
"\n"
"*[style_ID=\"borderless\"]\n"
"{\n"
"border: none;\n"
"}\n"
"\n"
"*[style_ID=\"taskbarBgLight\"]\n"
"{\n"
"background-color: #252013;\n"
"border:none;\n"
"}\n"
"\n"
"*[style_ID=\"bigButton\"]\n"
"{\n"
"backgr"
                        "ound-color: rgba(26,17,10,255);\n"
"border-color: #000000 ;\n"
"color: #FFFFFF;\n"
"font-size: 30px;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"color: #FFFFFF;\n"
"text-align: left;\n"
"background-color: #4F3F30;\n"
"border: 1px solid #AD6300;\n"
"padding:3px 6px 3px 6px;\n"
"border-radius: 10px;\n"
"}\n"
"QPushButton:hover\n"
"{\n"
"background-color: #604C3A;\n"
"}\n"
"\n"
"*[style_ID=\"toolboxBackground\"]\n"
"{\n"
"background-color: #252013;\n"
"border-bottom: 1px solid #AD6300;\n"
"color: white;\n"
"}\n"
"\n"
"#taskbar_container\n"
"{\n"
"background-color: #252013;\n"
"border: 1px solid #AD6300;\n"
"}\n"
"\n"
"QToolBox:tab[style_ID=\"tbTabTier1\"]\n"
"{\n"
"background-color: #1A110A;\n"
"border-bottom: 1px solid #AD6300;\n"
"color: white;\n"
"}\n"
"\n"
"QToolBox:tab[style_ID=\"tbTabTier2\"]\n"
"{\n"
"background-color: #1A110A;\n"
"border-bottom: 1px solid #AD6300;\n"
"color: white;\n"
"}\n"
"\n"
"QLabel\n"
"{\n"
"color: #FFFFFF\n"
"}\n"
"\n"
"*[style_ID=\"logo\"]\n"
"{\n"
"border-image: url(:/logo/images/logos/L"
                        "ogo V1.svg);\n"
"border: none;\n"
"}\n"
"\n"
"QScrollBar:vertical, QScrollBar:horizontal\n"
"{\n"
"background: #493721;\n"
"}\n"
"QScrollBar:handle:vertical, QScrollBar:handle:horizontal\n"
"{\n"
"background: #AD6300;\n"
"border: 2px solid #493721;\n"
"}\n"
"QScrollBar:add-line:vertical, QScrollBar:sub-line:vertical, QScrollBar:add-line:horizontal, QScrollBar:sub-line:horizontal\n"
"{\n"
"background: #493721;\n"
"}\n"
"\n"
"\n"
"")
        self.centralwidget = QWidget(mainwindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setStyleSheet(u"")
        self.horizontalLayout_8 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.window_content = QFrame(self.centralwidget)
        self.window_content.setObjectName(u"window_content")
        sizePolicy.setHeightForWidth(self.window_content.sizePolicy().hasHeightForWidth())
        self.window_content.setSizePolicy(sizePolicy)
        self.window_content.setFrameShape(QFrame.Shape.StyledPanel)
        self.window_content.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_40 = QVBoxLayout(self.window_content)
        self.verticalLayout_40.setSpacing(0)
        self.verticalLayout_40.setObjectName(u"verticalLayout_40")
        self.verticalLayout_40.setContentsMargins(0, 0, 0, 0)
        self.header = QFrame(self.window_content)
        self.header.setObjectName(u"header")
        self.header.setMaximumSize(QSize(16777215, 50))
        self.header.setStyleSheet(u"")
        self.header.setFrameShape(QFrame.Shape.StyledPanel)
        self.header.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.header)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.logo_container = QFrame(self.header)
        self.logo_container.setObjectName(u"logo_container")
        self.logo_container.setStyleSheet(u"border: none")
        self.logo_container.setFrameShape(QFrame.Shape.StyledPanel)
        self.logo_container.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.logo_container)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.logo_container)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(32, 32))
        self.label_6.setMaximumSize(QSize(32, 32))
        self.label_6.setPixmap(QPixmap(u":/logo/images/logos/Logo V2.svg"))
        self.label_6.setScaledContents(True)

        self.horizontalLayout_12.addWidget(self.label_6)


        self.horizontalLayout_4.addWidget(self.logo_container, 0, Qt.AlignmentFlag.AlignLeft)

        self.frame_3 = QFrame(self.header)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.home_button = QPushButton(self.frame_3)
        self.home_button.setObjectName(u"home_button")
        self.home_button.setStyleSheet(u"border: none;\n"
"background-color: none;")
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/icons/home.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.home_button.setIcon(icon1)

        self.horizontalLayout_3.addWidget(self.home_button)

        self.settings_button_top = QPushButton(self.frame_3)
        self.settings_button_top.setObjectName(u"settings_button_top")
        self.settings_button_top.setStyleSheet(u"border: none;\n"
"background-color: none;")
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/icons/settings.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.settings_button_top.setIcon(icon2)

        self.horizontalLayout_3.addWidget(self.settings_button_top)

        self.minimize_button = QPushButton(self.frame_3)
        self.minimize_button.setObjectName(u"minimize_button")
        self.minimize_button.setStyleSheet(u"border: none;\n"
"background-color: none;")
        icon3 = QIcon()
        icon3.addFile(u":/icons/images/icons/minus.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.minimize_button.setIcon(icon3)

        self.horizontalLayout_3.addWidget(self.minimize_button)

        self.maximize_button = QPushButton(self.frame_3)
        self.maximize_button.setObjectName(u"maximize_button")
        self.maximize_button.setStyleSheet(u"border: none;\n"
"background-color: none;")
        icon4 = QIcon()
        icon4.addFile(u":/icons/images/icons/maximize-2.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.maximize_button.setIcon(icon4)

        self.horizontalLayout_3.addWidget(self.maximize_button)

        self.exit_button = QPushButton(self.frame_3)
        self.exit_button.setObjectName(u"exit_button")
        self.exit_button.setStyleSheet(u"border: none;\n"
"background-color: none;")
        icon5 = QIcon()
        icon5.addFile(u":/icons/images/icons/x.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.exit_button.setIcon(icon5)

        self.horizontalLayout_3.addWidget(self.exit_button)


        self.horizontalLayout_4.addWidget(self.frame_3, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignVCenter)


        self.verticalLayout_40.addWidget(self.header)

        self.main_body_container = QFrame(self.window_content)
        self.main_body_container.setObjectName(u"main_body_container")
        sizePolicy.setHeightForWidth(self.main_body_container.sizePolicy().hasHeightForWidth())
        self.main_body_container.setSizePolicy(sizePolicy)
        self.main_body_container.setStyleSheet(u"")
        self.main_body_container.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_body_container.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.main_body_container)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.taskbar_container = QFrame(self.main_body_container)
        self.taskbar_container.setObjectName(u"taskbar_container")
        sizePolicy.setHeightForWidth(self.taskbar_container.sizePolicy().hasHeightForWidth())
        self.taskbar_container.setSizePolicy(sizePolicy)
        self.taskbar_container.setMaximumSize(QSize(16777215, 16777215))
        self.taskbar_container.setFrameShape(QFrame.Shape.StyledPanel)
        self.taskbar_container.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.taskbar_container)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.taskbar_body_container = QStackedWidget(self.taskbar_container)
        self.taskbar_body_container.setObjectName(u"taskbar_body_container")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.taskbar_body_container.sizePolicy().hasHeightForWidth())
        self.taskbar_body_container.setSizePolicy(sizePolicy1)
        self.taskbar_body_container.setMinimumSize(QSize(200, 0))
        self.taskbar_body_container.setMaximumSize(QSize(400, 16777215))
        self.homepage_taskbar = QWidget()
        self.homepage_taskbar.setObjectName(u"homepage_taskbar")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.homepage_taskbar.sizePolicy().hasHeightForWidth())
        self.homepage_taskbar.setSizePolicy(sizePolicy2)
        self.homepage_taskbar.setMinimumSize(QSize(0, 0))
        self.verticalLayout_51 = QVBoxLayout(self.homepage_taskbar)
        self.verticalLayout_51.setObjectName(u"verticalLayout_51")
        self.frame_28 = QFrame(self.homepage_taskbar)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_28.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_66 = QVBoxLayout(self.frame_28)
        self.verticalLayout_66.setSpacing(10)
        self.verticalLayout_66.setObjectName(u"verticalLayout_66")
        self.verticalLayout_66.setContentsMargins(0, 0, 0, 0)
        self.label_32 = QLabel(self.frame_28)
        self.label_32.setObjectName(u"label_32")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_32.setFont(font)

        self.verticalLayout_66.addWidget(self.label_32)

        self.label_4 = QLabel(self.frame_28)
        self.label_4.setObjectName(u"label_4")
        font1 = QFont()
        font1.setPointSize(12)
        self.label_4.setFont(font1)
        self.label_4.setWordWrap(True)

        self.verticalLayout_66.addWidget(self.label_4)


        self.verticalLayout_51.addWidget(self.frame_28, 0, Qt.AlignmentFlag.AlignTop)

        self.frame_5 = QFrame(self.homepage_taskbar)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFont(font1)
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_5)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.create_button_side = QPushButton(self.frame_5)
        self.create_button_side.setObjectName(u"create_button_side")
        self.create_button_side.setFont(font1)
        self.create_button_side.setStyleSheet(u"")
        icon6 = QIcon()
        icon6.addFile(u":/icons/images/icons/file-plus.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.create_button_side.setIcon(icon6)
        self.create_button_side.setIconSize(QSize(32, 32))

        self.verticalLayout_4.addWidget(self.create_button_side)

        self.load_button_side = QPushButton(self.frame_5)
        self.load_button_side.setObjectName(u"load_button_side")
        self.load_button_side.setFont(font1)
        self.load_button_side.setStyleSheet(u"")
        icon7 = QIcon()
        icon7.addFile(u":/icons/images/icons/folder.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.load_button_side.setIcon(icon7)
        self.load_button_side.setIconSize(QSize(32, 32))

        self.verticalLayout_4.addWidget(self.load_button_side)

        self.settings_button_side = QPushButton(self.frame_5)
        self.settings_button_side.setObjectName(u"settings_button_side")
        self.settings_button_side.setFont(font1)
        self.settings_button_side.setStyleSheet(u"")
        self.settings_button_side.setIcon(icon2)
        self.settings_button_side.setIconSize(QSize(32, 32))

        self.verticalLayout_4.addWidget(self.settings_button_side)

        self.about_button_side = QPushButton(self.frame_5)
        self.about_button_side.setObjectName(u"about_button_side")
        self.about_button_side.setFont(font1)
        self.about_button_side.setStyleSheet(u"")
        icon8 = QIcon()
        icon8.addFile(u":/icons/images/icons/info.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.about_button_side.setIcon(icon8)
        self.about_button_side.setIconSize(QSize(32, 32))

        self.verticalLayout_4.addWidget(self.about_button_side)


        self.verticalLayout_51.addWidget(self.frame_5, 0, Qt.AlignmentFlag.AlignBottom)

        self.taskbar_body_container.addWidget(self.homepage_taskbar)
        self.project_taskbar = QWidget()
        self.project_taskbar.setObjectName(u"project_taskbar")
        sizePolicy2.setHeightForWidth(self.project_taskbar.sizePolicy().hasHeightForWidth())
        self.project_taskbar.setSizePolicy(sizePolicy2)
        self.verticalLayout_53 = QVBoxLayout(self.project_taskbar)
        self.verticalLayout_53.setSpacing(0)
        self.verticalLayout_53.setObjectName(u"verticalLayout_53")
        self.verticalLayout_53.setContentsMargins(0, 0, 0, 0)
        self.project_taskbar_container = QFrame(self.project_taskbar)
        self.project_taskbar_container.setObjectName(u"project_taskbar_container")
        self.project_taskbar_container.setFrameShape(QFrame.Shape.StyledPanel)
        self.project_taskbar_container.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_52 = QVBoxLayout(self.project_taskbar_container)
        self.verticalLayout_52.setSpacing(6)
        self.verticalLayout_52.setObjectName(u"verticalLayout_52")
        self.verticalLayout_52.setContentsMargins(0, 0, 0, 0)
        self.frame_19 = QFrame(self.project_taskbar_container)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_19.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_38 = QVBoxLayout(self.frame_19)
        self.verticalLayout_38.setSpacing(0)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.verticalLayout_38.setContentsMargins(6, 0, 0, 0)
        self.label_74 = QLabel(self.frame_19)
        self.label_74.setObjectName(u"label_74")
        font2 = QFont()
        font2.setPointSize(12)
        font2.setBold(True)
        self.label_74.setFont(font2)

        self.verticalLayout_38.addWidget(self.label_74)


        self.verticalLayout_52.addWidget(self.frame_19, 0, Qt.AlignmentFlag.AlignTop)

        self.frame_20 = QFrame(self.project_taskbar_container)
        self.frame_20.setObjectName(u"frame_20")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.frame_20.sizePolicy().hasHeightForWidth())
        self.frame_20.setSizePolicy(sizePolicy3)
        self.frame_20.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_20.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_39 = QVBoxLayout(self.frame_20)
        self.verticalLayout_39.setSpacing(0)
        self.verticalLayout_39.setObjectName(u"verticalLayout_39")
        self.verticalLayout_39.setContentsMargins(0, 0, 0, 0)
        self.project_taskbar_toolbox = QToolBox(self.frame_20)
        self.project_taskbar_toolbox.setObjectName(u"project_taskbar_toolbox")
        self.project_taskbar_toolbox.setStyleSheet(u"")
        self.toolbox_project = QWidget()
        self.toolbox_project.setObjectName(u"toolbox_project")
        self.toolbox_project.setGeometry(QRect(0, 0, 128, 84))
        self.verticalLayout_56 = QVBoxLayout(self.toolbox_project)
        self.verticalLayout_56.setObjectName(u"verticalLayout_56")
        self.verticalLayout_56.setContentsMargins(6, 0, 6, 0)
        self.toolbox_project_body = QFrame(self.toolbox_project)
        self.toolbox_project_body.setObjectName(u"toolbox_project_body")
        self.toolbox_project_body.setFrameShape(QFrame.Shape.StyledPanel)
        self.toolbox_project_body.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_23 = QVBoxLayout(self.toolbox_project_body)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.verticalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.pushButton_13 = QPushButton(self.toolbox_project_body)
        self.pushButton_13.setObjectName(u"pushButton_13")

        self.verticalLayout_23.addWidget(self.pushButton_13)

        self.pushButton_14 = QPushButton(self.toolbox_project_body)
        self.pushButton_14.setObjectName(u"pushButton_14")

        self.verticalLayout_23.addWidget(self.pushButton_14)

        self.pushButton_15 = QPushButton(self.toolbox_project_body)
        self.pushButton_15.setObjectName(u"pushButton_15")

        self.verticalLayout_23.addWidget(self.pushButton_15)


        self.verticalLayout_56.addWidget(self.toolbox_project_body, 0, Qt.AlignmentFlag.AlignTop)

        icon9 = QIcon()
        icon9.addFile(u":/icons/images/icons/bat_hanging.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.project_taskbar_toolbox.addItem(self.toolbox_project, icon9, u"Project")
        self.toolbox_graphs = QWidget()
        self.toolbox_graphs.setObjectName(u"toolbox_graphs")
        self.toolbox_graphs.setGeometry(QRect(0, 0, 84, 106))
        self.toolbox_graphs.setStyleSheet(u"")
        self.verticalLayout_58 = QVBoxLayout(self.toolbox_graphs)
        self.verticalLayout_58.setSpacing(0)
        self.verticalLayout_58.setObjectName(u"verticalLayout_58")
        self.verticalLayout_58.setContentsMargins(0, 0, 0, 0)
        self.frame_18 = QFrame(self.toolbox_graphs)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_37 = QVBoxLayout(self.frame_18)
        self.verticalLayout_37.setSpacing(0)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.verticalLayout_37.setContentsMargins(15, 0, 0, 0)
        self.toolbox_graphlist = QToolBox(self.frame_18)
        self.toolbox_graphlist.setObjectName(u"toolbox_graphlist")
        self.toolbox_graphlist.setStyleSheet(u"background: transparent")
        self.toolbox_datasets = QWidget()
        self.toolbox_datasets.setObjectName(u"toolbox_datasets")
        self.toolbox_datasets.setGeometry(QRect(0, 0, 69, 46))
        self.toolbox_datasets.setStyleSheet(u"background: transparent")
        self.verticalLayout_25 = QVBoxLayout(self.toolbox_datasets)
        self.verticalLayout_25.setSpacing(0)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.verticalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_2 = QScrollArea(self.toolbox_datasets)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setStyleSheet(u"background: transparent")
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 69, 46))
        self.scrollAreaWidgetContents_2.setStyleSheet(u"background: transparent")
        self.verticalLayout_27 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_27.setSpacing(0)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.verticalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.dataset_list = QFrame(self.scrollAreaWidgetContents_2)
        self.dataset_list.setObjectName(u"dataset_list")
        self.dataset_list.setStyleSheet(u"background: transparent")
        self.dataset_list.setFrameShape(QFrame.Shape.StyledPanel)
        self.dataset_list.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_26 = QVBoxLayout(self.dataset_list)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.verticalLayout_26.setContentsMargins(0, 0, 4, 0)

        self.verticalLayout_27.addWidget(self.dataset_list, 0, Qt.AlignmentFlag.AlignTop)

        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_25.addWidget(self.scrollArea_2)

        self.toolbox_graphlist.addItem(self.toolbox_datasets, icon9, u"Datasets")
        self.toolbox_maps = QWidget()
        self.toolbox_maps.setObjectName(u"toolbox_maps")
        self.toolbox_maps.setGeometry(QRect(0, 0, 86, 46))
        self.toolbox_maps.setStyleSheet(u"background: transparent")
        self.verticalLayout_36 = QVBoxLayout(self.toolbox_maps)
        self.verticalLayout_36.setSpacing(0)
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.verticalLayout_36.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_5 = QScrollArea(self.toolbox_maps)
        self.scrollArea_5.setObjectName(u"scrollArea_5")
        self.scrollArea_5.setStyleSheet(u"background: transparent")
        self.scrollArea_5.setWidgetResizable(True)
        self.scrollAreaWidgetContents_5 = QWidget()
        self.scrollAreaWidgetContents_5.setObjectName(u"scrollAreaWidgetContents_5")
        self.scrollAreaWidgetContents_5.setGeometry(QRect(0, 0, 86, 46))
        self.scrollAreaWidgetContents_5.setStyleSheet(u"background: transparent")
        self.verticalLayout_35 = QVBoxLayout(self.scrollAreaWidgetContents_5)
        self.verticalLayout_35.setSpacing(0)
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.verticalLayout_35.setContentsMargins(0, 0, 0, 0)
        self.map_list = QFrame(self.scrollAreaWidgetContents_5)
        self.map_list.setObjectName(u"map_list")
        self.map_list.setStyleSheet(u"background: transparent")
        self.map_list.setFrameShape(QFrame.Shape.StyledPanel)
        self.map_list.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_34 = QVBoxLayout(self.map_list)
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.verticalLayout_34.setContentsMargins(0, 0, 4, 0)

        self.verticalLayout_35.addWidget(self.map_list, 0, Qt.AlignmentFlag.AlignTop)

        self.scrollArea_5.setWidget(self.scrollAreaWidgetContents_5)

        self.verticalLayout_36.addWidget(self.scrollArea_5)

        self.toolbox_graphlist.addItem(self.toolbox_maps, icon9, u"Maps")

        self.verticalLayout_37.addWidget(self.toolbox_graphlist)


        self.verticalLayout_58.addWidget(self.frame_18)

        self.project_taskbar_toolbox.addItem(self.toolbox_graphs, icon9, u"Data")
        self.toolbox_other = QWidget()
        self.toolbox_other.setObjectName(u"toolbox_other")
        self.toolbox_other.setGeometry(QRect(0, 0, 132, 54))
        self.verticalLayout_57 = QVBoxLayout(self.toolbox_other)
        self.verticalLayout_57.setSpacing(0)
        self.verticalLayout_57.setObjectName(u"verticalLayout_57")
        self.verticalLayout_57.setContentsMargins(0, 0, 0, 0)
        self.toolbox_other_body = QFrame(self.toolbox_other)
        self.toolbox_other_body.setObjectName(u"toolbox_other_body")
        self.toolbox_other_body.setFrameShape(QFrame.Shape.StyledPanel)
        self.toolbox_other_body.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_22 = QVBoxLayout(self.toolbox_other_body)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(6, 0, 6, 0)
        self.pushButton_11 = QPushButton(self.toolbox_other_body)
        self.pushButton_11.setObjectName(u"pushButton_11")
        self.pushButton_11.setIcon(icon2)

        self.verticalLayout_22.addWidget(self.pushButton_11)

        self.pushButton_12 = QPushButton(self.toolbox_other_body)
        self.pushButton_12.setObjectName(u"pushButton_12")
        self.pushButton_12.setIcon(icon8)

        self.verticalLayout_22.addWidget(self.pushButton_12)


        self.verticalLayout_57.addWidget(self.toolbox_other_body, 0, Qt.AlignmentFlag.AlignTop)

        self.project_taskbar_toolbox.addItem(self.toolbox_other, icon9, u"Other")

        self.verticalLayout_39.addWidget(self.project_taskbar_toolbox, 0, Qt.AlignmentFlag.AlignTop)


        self.verticalLayout_52.addWidget(self.frame_20)


        self.verticalLayout_53.addWidget(self.project_taskbar_container)

        self.taskbar_body_container.addWidget(self.project_taskbar)

        self.horizontalLayout_13.addWidget(self.taskbar_body_container)

        self.close_button_container = QFrame(self.taskbar_container)
        self.close_button_container.setObjectName(u"close_button_container")
        self.close_button_container.setFrameShape(QFrame.Shape.StyledPanel)
        self.close_button_container.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.close_button_container)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.close_button = QPushButton(self.close_button_container)
        self.close_button.setObjectName(u"close_button")
        self.close_button.setMaximumSize(QSize(16, 16))
        self.close_button.setStyleSheet(u"border:none; background-color: none;")
        icon10 = QIcon()
        icon10.addFile(u":/icons/images/icons/menu.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.close_button.setIcon(icon10)

        self.horizontalLayout_14.addWidget(self.close_button, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)


        self.horizontalLayout_13.addWidget(self.close_button_container, 0, Qt.AlignmentFlag.AlignLeft)


        self.horizontalLayout.addWidget(self.taskbar_container, 0, Qt.AlignmentFlag.AlignLeft)

        self.main_body_content = QFrame(self.main_body_container)
        self.main_body_content.setObjectName(u"main_body_content")
        self.main_body_content.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_body_content.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_59 = QVBoxLayout(self.main_body_content)
        self.verticalLayout_59.setSpacing(0)
        self.verticalLayout_59.setObjectName(u"verticalLayout_59")
        self.verticalLayout_59.setContentsMargins(0, 0, 0, 0)
        self.main_body_stack = QStackedWidget(self.main_body_content)
        self.main_body_stack.setObjectName(u"main_body_stack")
        sizePolicy.setHeightForWidth(self.main_body_stack.sizePolicy().hasHeightForWidth())
        self.main_body_stack.setSizePolicy(sizePolicy)
        self.home_page = QWidget()
        self.home_page.setObjectName(u"home_page")
        sizePolicy.setHeightForWidth(self.home_page.sizePolicy().hasHeightForWidth())
        self.home_page.setSizePolicy(sizePolicy)
        self.horizontalLayout_10 = QHBoxLayout(self.home_page)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.main_body = QFrame(self.home_page)
        self.main_body.setObjectName(u"main_body")
        sizePolicy.setHeightForWidth(self.main_body.sizePolicy().hasHeightForWidth())
        self.main_body.setSizePolicy(sizePolicy)
        self.main_body.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_body.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.main_body)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.banner = QFrame(self.main_body)
        self.banner.setObjectName(u"banner")
        self.banner.setMaximumSize(QSize(16777215, 40))
        self.banner.setStyleSheet(u"border: none;\n"
"")
        self.banner.setFrameShape(QFrame.Shape.StyledPanel)
        self.banner.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.banner)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_3 = QLabel(self.banner)
        self.label_3.setObjectName(u"label_3")
        font3 = QFont()
        font3.setPointSize(15)
        self.label_3.setFont(font3)

        self.horizontalLayout_7.addWidget(self.label_3, 0, Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignVCenter)


        self.verticalLayout_2.addWidget(self.banner)

        self.main_content = QFrame(self.main_body)
        self.main_content.setObjectName(u"main_content")
        sizePolicy.setHeightForWidth(self.main_content.sizePolicy().hasHeightForWidth())
        self.main_content.setSizePolicy(sizePolicy)
        self.main_content.setStyleSheet(u"")
        self.main_content.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_content.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_2 = QGridLayout(self.main_content)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.create_button_main = QPushButton(self.main_content)
        self.create_button_main.setObjectName(u"create_button_main")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(1)
        sizePolicy4.setHeightForWidth(self.create_button_main.sizePolicy().hasHeightForWidth())
        self.create_button_main.setSizePolicy(sizePolicy4)
        self.create_button_main.setMinimumSize(QSize(100, 100))
        self.create_button_main.setMaximumSize(QSize(400, 400))
        self.create_button_main.setAutoFillBackground(False)
        self.create_button_main.setStyleSheet(u"text-align: center")
        self.create_button_main.setIcon(icon6)
        self.create_button_main.setIconSize(QSize(64, 64))
        self.create_button_main.setFlat(False)

        self.gridLayout_2.addWidget(self.create_button_main, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 80, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(80, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 1, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(80, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 1, 2, 1, 1)

        self.load_button_main = QPushButton(self.main_content)
        self.load_button_main.setObjectName(u"load_button_main")
        sizePolicy4.setHeightForWidth(self.load_button_main.sizePolicy().hasHeightForWidth())
        self.load_button_main.setSizePolicy(sizePolicy4)
        self.load_button_main.setMinimumSize(QSize(100, 100))
        self.load_button_main.setMaximumSize(QSize(400, 400))
        self.load_button_main.setStyleSheet(u"text-align: center")
        self.load_button_main.setIcon(icon7)
        self.load_button_main.setIconSize(QSize(64, 64))

        self.gridLayout_2.addWidget(self.load_button_main, 1, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(80, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 1, 4, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 80, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_2, 2, 2, 1, 1)


        self.verticalLayout_2.addWidget(self.main_content)


        self.horizontalLayout_10.addWidget(self.main_body)

        self.main_body_stack.addWidget(self.home_page)
        self.create_project_page = QWidget()
        self.create_project_page.setObjectName(u"create_project_page")
        self.verticalLayout_7 = QVBoxLayout(self.create_project_page)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.create_project_body_2 = QFrame(self.create_project_page)
        self.create_project_body_2.setObjectName(u"create_project_body_2")
        self.create_project_body_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.create_project_body_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.create_project_body_2)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.create_header = QFrame(self.create_project_body_2)
        self.create_header.setObjectName(u"create_header")
        self.create_header.setFrameShape(QFrame.Shape.StyledPanel)
        self.create_header.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.create_header)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(6, 4, 0, 4)
        self.label_7 = QLabel(self.create_header)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font)

        self.horizontalLayout_17.addWidget(self.label_7)


        self.verticalLayout_8.addWidget(self.create_header, 0, Qt.AlignmentFlag.AlignTop)

        self.create_body_scroll_area = QScrollArea(self.create_project_body_2)
        self.create_body_scroll_area.setObjectName(u"create_body_scroll_area")
        self.create_body_scroll_area.setStyleSheet(u"")
        self.create_body_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.create_body_scroll_area.setWidgetResizable(True)
        self.create_project_body = QWidget()
        self.create_project_body.setObjectName(u"create_project_body")
        self.create_project_body.setGeometry(QRect(0, 0, 259, 420))
        self.create_project_body.setStyleSheet(u"")
        self.verticalLayout_13 = QVBoxLayout(self.create_project_body)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(6, 0, 0, 0)
        self.frame_4 = QFrame(self.create_project_body)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_10 = QFrame(self.frame_4)
        self.frame_10.setObjectName(u"frame_10")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.frame_10.sizePolicy().hasHeightForWidth())
        self.frame_10.setSizePolicy(sizePolicy5)
        self.frame_10.setMinimumSize(QSize(0, 50))
        self.frame_10.setMaximumSize(QSize(16777215, 100))
        self.frame_10.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_10)
        self.verticalLayout_9.setSpacing(4)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.label_8 = QLabel(self.frame_10)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font1)

        self.verticalLayout_9.addWidget(self.label_8, 0, Qt.AlignmentFlag.AlignTop)

        self.input_project_name = QTextEdit(self.frame_10)
        self.input_project_name.setObjectName(u"input_project_name")
        self.input_project_name.setMaximumSize(QSize(400, 30))
        self.input_project_name.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.input_project_name.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.input_project_name.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)

        self.verticalLayout_9.addWidget(self.input_project_name, 0, Qt.AlignmentFlag.AlignTop)


        self.verticalLayout_5.addWidget(self.frame_10)

        self.frame_11 = QFrame(self.frame_4)
        self.frame_11.setObjectName(u"frame_11")
        sizePolicy5.setHeightForWidth(self.frame_11.sizePolicy().hasHeightForWidth())
        self.frame_11.setSizePolicy(sizePolicy5)
        self.frame_11.setMinimumSize(QSize(0, 100))
        self.frame_11.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame_11)
        self.verticalLayout_10.setSpacing(4)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.frame_11)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font1)

        self.verticalLayout_10.addWidget(self.label_9)

        self.frame_12 = QFrame(self.frame_11)
        self.frame_12.setObjectName(u"frame_12")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.frame_12.sizePolicy().hasHeightForWidth())
        self.frame_12.setSizePolicy(sizePolicy6)
        self.frame_12.setMinimumSize(QSize(0, 30))
        self.frame_12.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_19.setSpacing(4)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.create_add_data_button = QPushButton(self.frame_12)
        self.create_add_data_button.setObjectName(u"create_add_data_button")
        self.create_add_data_button.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_19.addWidget(self.create_add_data_button)

        self.label_10 = QLabel(self.frame_12)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_19.addWidget(self.label_10)


        self.verticalLayout_10.addWidget(self.frame_12)

        self.lineEdit = QLineEdit(self.frame_11)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMaximumSize(QSize(400, 30))

        self.verticalLayout_10.addWidget(self.lineEdit)


        self.verticalLayout_5.addWidget(self.frame_11)

        self.frame_14 = QFrame(self.frame_4)
        self.frame_14.setObjectName(u"frame_14")
        sizePolicy5.setHeightForWidth(self.frame_14.sizePolicy().hasHeightForWidth())
        self.frame_14.setSizePolicy(sizePolicy5)
        self.frame_14.setMinimumSize(QSize(0, 100))
        self.frame_14.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.frame_14)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.label_11 = QLabel(self.frame_14)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font1)

        self.verticalLayout_11.addWidget(self.label_11)

        self.frame_15 = QFrame(self.frame_14)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_20.setSpacing(4)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.create_add_map_button = QPushButton(self.frame_15)
        self.create_add_map_button.setObjectName(u"create_add_map_button")
        self.create_add_map_button.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_20.addWidget(self.create_add_map_button)

        self.label_12 = QLabel(self.frame_15)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_20.addWidget(self.label_12)


        self.verticalLayout_11.addWidget(self.frame_15)

        self.lineEdit_2 = QLineEdit(self.frame_14)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setMaximumSize(QSize(400, 30))

        self.verticalLayout_11.addWidget(self.lineEdit_2)


        self.verticalLayout_5.addWidget(self.frame_14)

        self.frame_16 = QFrame(self.frame_4)
        self.frame_16.setObjectName(u"frame_16")
        sizePolicy5.setHeightForWidth(self.frame_16.sizePolicy().hasHeightForWidth())
        self.frame_16.setSizePolicy(sizePolicy5)
        self.frame_16.setMinimumSize(QSize(0, 150))
        self.frame_16.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_16)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.label_13 = QLabel(self.frame_16)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFont(font1)

        self.verticalLayout_12.addWidget(self.label_13, 0, Qt.AlignmentFlag.AlignTop)

        self.plainTextEdit = QPlainTextEdit(self.frame_16)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setMaximumSize(QSize(600, 300))

        self.verticalLayout_12.addWidget(self.plainTextEdit, 0, Qt.AlignmentFlag.AlignTop)

        self.label_14 = QLabel(self.frame_16)
        self.label_14.setObjectName(u"label_14")

        self.verticalLayout_12.addWidget(self.label_14)


        self.verticalLayout_5.addWidget(self.frame_16)


        self.verticalLayout_13.addWidget(self.frame_4, 0, Qt.AlignmentFlag.AlignTop)

        self.create_body_scroll_area.setWidget(self.create_project_body)

        self.verticalLayout_8.addWidget(self.create_body_scroll_area)

        self.create_footer = QFrame(self.create_project_body_2)
        self.create_footer.setObjectName(u"create_footer")
        self.create_footer.setFrameShape(QFrame.Shape.StyledPanel)
        self.create_footer.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.create_footer)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(4, 4, 4, 4)
        self.cancel_create_button = QPushButton(self.create_footer)
        self.cancel_create_button.setObjectName(u"cancel_create_button")

        self.horizontalLayout_18.addWidget(self.cancel_create_button, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom)

        self.confirm_create_button = QPushButton(self.create_footer)
        self.confirm_create_button.setObjectName(u"confirm_create_button")

        self.horizontalLayout_18.addWidget(self.confirm_create_button, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignBottom)


        self.verticalLayout_8.addWidget(self.create_footer, 0, Qt.AlignmentFlag.AlignBottom)


        self.verticalLayout_7.addWidget(self.create_project_body_2)

        self.main_body_stack.addWidget(self.create_project_page)
        self.about_page = QWidget()
        self.about_page.setObjectName(u"about_page")
        self.horizontalLayout_15 = QHBoxLayout(self.about_page)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.about_container = QFrame(self.about_page)
        self.about_container.setObjectName(u"about_container")
        self.about_container.setFrameShape(QFrame.Shape.StyledPanel)
        self.about_container.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.about_container)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.label_15 = QLabel(self.about_container)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font)

        self.verticalLayout_14.addWidget(self.label_15, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.frame_7 = QFrame(self.about_container)
        self.frame_7.setObjectName(u"frame_7")
        sizePolicy.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy)
        self.frame_7.setStyleSheet(u"border: none")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.frame_7)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(6, 0, 0, 0)
        self.label = QLabel(self.frame_7)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label.setWordWrap(True)

        self.verticalLayout_15.addWidget(self.label)

        self.frame_8 = QFrame(self.frame_7)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.frame_9 = QFrame(self.frame_8)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.frame_9)
        self.verticalLayout_16.setSpacing(4)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.label_16 = QLabel(self.frame_9)
        self.label_16.setObjectName(u"label_16")
        font4 = QFont()
        font4.setBold(True)
        self.label_16.setFont(font4)

        self.verticalLayout_16.addWidget(self.label_16)

        self.label_17 = QLabel(self.frame_9)
        self.label_17.setObjectName(u"label_17")

        self.verticalLayout_16.addWidget(self.label_17)

        self.label_18 = QLabel(self.frame_9)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font4)

        self.verticalLayout_16.addWidget(self.label_18)

        self.label_19 = QLabel(self.frame_9)
        self.label_19.setObjectName(u"label_19")

        self.verticalLayout_16.addWidget(self.label_19)

        self.label_20 = QLabel(self.frame_9)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font4)

        self.verticalLayout_16.addWidget(self.label_20)

        self.label_21 = QLabel(self.frame_9)
        self.label_21.setObjectName(u"label_21")

        self.verticalLayout_16.addWidget(self.label_21)

        self.label_22 = QLabel(self.frame_9)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font4)

        self.verticalLayout_16.addWidget(self.label_22)

        self.label_23 = QLabel(self.frame_9)
        self.label_23.setObjectName(u"label_23")

        self.verticalLayout_16.addWidget(self.label_23)


        self.horizontalLayout_16.addWidget(self.frame_9)

        self.label_24 = QLabel(self.frame_8)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setMaximumSize(QSize(200, 200))
        self.label_24.setPixmap(QPixmap(u":/logo/images/logos/Logo V2.svg"))
        self.label_24.setScaledContents(True)

        self.horizontalLayout_16.addWidget(self.label_24)


        self.verticalLayout_15.addWidget(self.frame_8)


        self.verticalLayout_14.addWidget(self.frame_7)

        self.about_back_button = QPushButton(self.about_container)
        self.about_back_button.setObjectName(u"about_back_button")

        self.verticalLayout_14.addWidget(self.about_back_button, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom)


        self.horizontalLayout_15.addWidget(self.about_container)

        self.main_body_stack.addWidget(self.about_page)
        self.load_page = QWidget()
        self.load_page.setObjectName(u"load_page")
        self.horizontalLayout_21 = QHBoxLayout(self.load_page)
        self.horizontalLayout_21.setSpacing(0)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.load_page_body = QFrame(self.load_page)
        self.load_page_body.setObjectName(u"load_page_body")
        self.load_page_body.setStyleSheet(u"")
        self.load_page_body.setFrameShape(QFrame.Shape.StyledPanel)
        self.load_page_body.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_17 = QVBoxLayout(self.load_page_body)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.load_header = QFrame(self.load_page_body)
        self.load_header.setObjectName(u"load_header")
        self.load_header.setFrameShape(QFrame.Shape.StyledPanel)
        self.load_header.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_29 = QHBoxLayout(self.load_header)
        self.horizontalLayout_29.setSpacing(0)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalLayout_29.setContentsMargins(6, 0, 0, 6)
        self.label_25 = QLabel(self.load_header)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font)

        self.horizontalLayout_29.addWidget(self.label_25, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)


        self.verticalLayout_17.addWidget(self.load_header)

        self.load_scroll_area = QScrollArea(self.load_page_body)
        self.load_scroll_area.setObjectName(u"load_scroll_area")
        self.load_scroll_area.setStyleSheet(u"")
        self.load_scroll_area.setWidgetResizable(True)
        self.load_body = QWidget()
        self.load_body.setObjectName(u"load_body")
        self.load_body.setGeometry(QRect(0, 0, 738, 389))
        self.load_body.setStyleSheet(u"")
        self.verticalLayout_18 = QVBoxLayout(self.load_body)
        self.verticalLayout_18.setSpacing(15)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(6, 6, 0, -1)
        self.load_scroll_area.setWidget(self.load_body)

        self.verticalLayout_17.addWidget(self.load_scroll_area)

        self.load_footer = QFrame(self.load_page_body)
        self.load_footer.setObjectName(u"load_footer")
        self.load_footer.setFrameShape(QFrame.Shape.StyledPanel)
        self.load_footer.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_27 = QHBoxLayout(self.load_footer)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(6, 6, 0, 6)
        self.load_back_button = QPushButton(self.load_footer)
        self.load_back_button.setObjectName(u"load_back_button")

        self.horizontalLayout_27.addWidget(self.load_back_button, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom)


        self.verticalLayout_17.addWidget(self.load_footer)


        self.horizontalLayout_21.addWidget(self.load_page_body)

        self.main_body_stack.addWidget(self.load_page)
        self.project_homepage = QWidget()
        self.project_homepage.setObjectName(u"project_homepage")
        sizePolicy.setHeightForWidth(self.project_homepage.sizePolicy().hasHeightForWidth())
        self.project_homepage.setSizePolicy(sizePolicy)
        self.horizontalLayout_38 = QHBoxLayout(self.project_homepage)
        self.horizontalLayout_38.setSpacing(0)
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.horizontalLayout_38.setContentsMargins(0, 0, 0, 0)
        self.project_homepage_container = QFrame(self.project_homepage)
        self.project_homepage_container.setObjectName(u"project_homepage_container")
        self.project_homepage_container.setFrameShape(QFrame.Shape.StyledPanel)
        self.project_homepage_container.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_54 = QVBoxLayout(self.project_homepage_container)
        self.verticalLayout_54.setSpacing(0)
        self.verticalLayout_54.setObjectName(u"verticalLayout_54")
        self.verticalLayout_54.setContentsMargins(0, 0, 0, 0)
        self.project_homepage_header = QFrame(self.project_homepage_container)
        self.project_homepage_header.setObjectName(u"project_homepage_header")
        self.project_homepage_header.setFrameShape(QFrame.Shape.StyledPanel)
        self.project_homepage_header.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_39 = QHBoxLayout(self.project_homepage_header)
        self.horizontalLayout_39.setSpacing(0)
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.horizontalLayout_39.setContentsMargins(0, 0, 0, 0)
        self.frame_13 = QFrame(self.project_homepage_header)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_40 = QHBoxLayout(self.frame_13)
        self.horizontalLayout_40.setSpacing(0)
        self.horizontalLayout_40.setObjectName(u"horizontalLayout_40")
        self.horizontalLayout_40.setContentsMargins(4, 0, 0, 0)
        self.label_76 = QLabel(self.frame_13)
        self.label_76.setObjectName(u"label_76")
        font5 = QFont()
        font5.setPointSize(14)
        font5.setBold(True)
        self.label_76.setFont(font5)

        self.horizontalLayout_40.addWidget(self.label_76)


        self.horizontalLayout_39.addWidget(self.frame_13)

        self.frame_17 = QFrame(self.project_homepage_header)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_41 = QHBoxLayout(self.frame_17)
        self.horizontalLayout_41.setObjectName(u"horizontalLayout_41")
        self.dropdown_bargraph = QComboBox(self.frame_17)
        self.dropdown_bargraph.addItem("")
        self.dropdown_bargraph.addItem("")
        self.dropdown_bargraph.addItem("")
        self.dropdown_bargraph.addItem("")
        self.dropdown_bargraph.addItem("")
        self.dropdown_bargraph.setObjectName(u"dropdown_bargraph")
        self.dropdown_bargraph.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_41.addWidget(self.dropdown_bargraph)

        self.button_boxplot = QPushButton(self.frame_17)
        self.button_boxplot.setObjectName(u"button_boxplot")

        self.horizontalLayout_41.addWidget(self.button_boxplot)

        self.button_histogram = QPushButton(self.frame_17)
        self.button_histogram.setObjectName(u"button_histogram")

        self.horizontalLayout_41.addWidget(self.button_histogram)

        self.button_linegraph = QPushButton(self.frame_17)
        self.button_linegraph.setObjectName(u"button_linegraph")

        self.horizontalLayout_41.addWidget(self.button_linegraph)

        self.button_cavemap = QPushButton(self.frame_17)
        self.button_cavemap.setObjectName(u"button_cavemap")

        self.horizontalLayout_41.addWidget(self.button_cavemap)


        self.horizontalLayout_39.addWidget(self.frame_17)


        self.verticalLayout_54.addWidget(self.project_homepage_header)

        self.project_homepage_body = QFrame(self.project_homepage_container)
        self.project_homepage_body.setObjectName(u"project_homepage_body")
        sizePolicy.setHeightForWidth(self.project_homepage_body.sizePolicy().hasHeightForWidth())
        self.project_homepage_body.setSizePolicy(sizePolicy)
        self.project_homepage_body.setFrameShape(QFrame.Shape.StyledPanel)
        self.project_homepage_body.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_55 = QVBoxLayout(self.project_homepage_body)
        self.verticalLayout_55.setSpacing(0)
        self.verticalLayout_55.setObjectName(u"verticalLayout_55")
        self.verticalLayout_55.setContentsMargins(0, 0, 0, 0)
        self.project_stack = QStackedWidget(self.project_homepage_body)
        self.project_stack.setObjectName(u"project_stack")
        self.project_home_page = QWidget()
        self.project_home_page.setObjectName(u"project_home_page")
        self.horizontalLayout_23 = QHBoxLayout(self.project_home_page)
        self.horizontalLayout_23.setSpacing(0)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.label_75 = QLabel(self.project_home_page)
        self.label_75.setObjectName(u"label_75")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy7.setHorizontalStretch(1)
        sizePolicy7.setVerticalStretch(1)
        sizePolicy7.setHeightForWidth(self.label_75.sizePolicy().hasHeightForWidth())
        self.label_75.setSizePolicy(sizePolicy7)
        self.label_75.setMaximumSize(QSize(300, 300))
        self.label_75.setPixmap(QPixmap(u":/backgrounds/images/bgs/ExampleCaveMap.png"))
        self.label_75.setScaledContents(True)
        self.label_75.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_23.addWidget(self.label_75)

        self.project_stack.addWidget(self.project_home_page)
        self.graph_cavemap_page = QWidget()
        self.graph_cavemap_page.setObjectName(u"graph_cavemap_page")
        self.horizontalLayout_25 = QHBoxLayout(self.graph_cavemap_page)
        self.horizontalLayout_25.setSpacing(0)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.graph_cavemap_page_body = QFrame(self.graph_cavemap_page)
        self.graph_cavemap_page_body.setObjectName(u"graph_cavemap_page_body")
        self.graph_cavemap_page_body.setFrameShape(QFrame.Shape.StyledPanel)
        self.graph_cavemap_page_body.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_69 = QVBoxLayout(self.graph_cavemap_page_body)
        self.verticalLayout_69.setSpacing(0)
        self.verticalLayout_69.setObjectName(u"verticalLayout_69")
        self.verticalLayout_69.setContentsMargins(0, 0, 0, 0)
        self.label_35 = QLabel(self.graph_cavemap_page_body)
        self.label_35.setObjectName(u"label_35")

        self.verticalLayout_69.addWidget(self.label_35)


        self.horizontalLayout_25.addWidget(self.graph_cavemap_page_body)

        self.project_stack.addWidget(self.graph_cavemap_page)
        self.graph_line_page = QWidget()
        self.graph_line_page.setObjectName(u"graph_line_page")
        self.verticalLayout_73 = QVBoxLayout(self.graph_line_page)
        self.verticalLayout_73.setSpacing(0)
        self.verticalLayout_73.setObjectName(u"verticalLayout_73")
        self.verticalLayout_73.setContentsMargins(0, 0, 0, 0)
        self.graph_line_page_body = QFrame(self.graph_line_page)
        self.graph_line_page_body.setObjectName(u"graph_line_page_body")
        self.graph_line_page_body.setFrameShape(QFrame.Shape.StyledPanel)
        self.graph_line_page_body.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_72 = QVBoxLayout(self.graph_line_page_body)
        self.verticalLayout_72.setSpacing(0)
        self.verticalLayout_72.setObjectName(u"verticalLayout_72")
        self.verticalLayout_72.setContentsMargins(0, 0, 0, 0)
        self.label_37 = QLabel(self.graph_line_page_body)
        self.label_37.setObjectName(u"label_37")

        self.verticalLayout_72.addWidget(self.label_37)


        self.verticalLayout_73.addWidget(self.graph_line_page_body)

        self.project_stack.addWidget(self.graph_line_page)
        self.graph_bar_page = QWidget()
        self.graph_bar_page.setObjectName(u"graph_bar_page")
        self.horizontalLayout_26 = QHBoxLayout(self.graph_bar_page)
        self.horizontalLayout_26.setSpacing(0)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.graph_bar_page_body = QFrame(self.graph_bar_page)
        self.graph_bar_page_body.setObjectName(u"graph_bar_page_body")
        self.graph_bar_page_body.setFrameShape(QFrame.Shape.StyledPanel)
        self.graph_bar_page_body.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.graph_bar_page_body)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_33 = QLabel(self.graph_bar_page_body)
        self.label_33.setObjectName(u"label_33")

        self.verticalLayout.addWidget(self.label_33)


        self.horizontalLayout_26.addWidget(self.graph_bar_page_body)

        self.project_stack.addWidget(self.graph_bar_page)
        self.graph_histogram_page = QWidget()
        self.graph_histogram_page.setObjectName(u"graph_histogram_page")
        self.verticalLayout_71 = QVBoxLayout(self.graph_histogram_page)
        self.verticalLayout_71.setSpacing(0)
        self.verticalLayout_71.setObjectName(u"verticalLayout_71")
        self.verticalLayout_71.setContentsMargins(0, 0, 0, 0)
        self.graph_histogram_page_body = QFrame(self.graph_histogram_page)
        self.graph_histogram_page_body.setObjectName(u"graph_histogram_page_body")
        self.graph_histogram_page_body.setFrameShape(QFrame.Shape.StyledPanel)
        self.graph_histogram_page_body.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_70 = QVBoxLayout(self.graph_histogram_page_body)
        self.verticalLayout_70.setObjectName(u"verticalLayout_70")
        self.verticalLayout_70.setContentsMargins(0, 0, 0, 0)
        self.label_36 = QLabel(self.graph_histogram_page_body)
        self.label_36.setObjectName(u"label_36")

        self.verticalLayout_70.addWidget(self.label_36)


        self.verticalLayout_71.addWidget(self.graph_histogram_page_body)

        self.project_stack.addWidget(self.graph_histogram_page)
        self.graph_boxplot_page = QWidget()
        self.graph_boxplot_page.setObjectName(u"graph_boxplot_page")
        self.verticalLayout_68 = QVBoxLayout(self.graph_boxplot_page)
        self.verticalLayout_68.setSpacing(0)
        self.verticalLayout_68.setObjectName(u"verticalLayout_68")
        self.verticalLayout_68.setContentsMargins(0, 0, 0, 0)
        self.graph_boxplot_page_body = QFrame(self.graph_boxplot_page)
        self.graph_boxplot_page_body.setObjectName(u"graph_boxplot_page_body")
        self.graph_boxplot_page_body.setFrameShape(QFrame.Shape.StyledPanel)
        self.graph_boxplot_page_body.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_67 = QVBoxLayout(self.graph_boxplot_page_body)
        self.verticalLayout_67.setSpacing(0)
        self.verticalLayout_67.setObjectName(u"verticalLayout_67")
        self.verticalLayout_67.setContentsMargins(0, 0, 0, 0)
        self.label_34 = QLabel(self.graph_boxplot_page_body)
        self.label_34.setObjectName(u"label_34")

        self.verticalLayout_67.addWidget(self.label_34)


        self.verticalLayout_68.addWidget(self.graph_boxplot_page_body)

        self.project_stack.addWidget(self.graph_boxplot_page)
        self.graph_multi_page = QWidget()
        self.graph_multi_page.setObjectName(u"graph_multi_page")
        self.horizontalLayout_24 = QHBoxLayout(self.graph_multi_page)
        self.horizontalLayout_24.setSpacing(0)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(0, 0, 0, 0)
        self.graph_multi_page_body = QFrame(self.graph_multi_page)
        self.graph_multi_page_body.setObjectName(u"graph_multi_page_body")
        self.graph_multi_page_body.setFrameShape(QFrame.Shape.StyledPanel)
        self.graph_multi_page_body.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.graph_multi_page_body)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label_30 = QLabel(self.graph_multi_page_body)
        self.label_30.setObjectName(u"label_30")

        self.gridLayout.addWidget(self.label_30, 1, 2, 1, 1)

        self.label_31 = QLabel(self.graph_multi_page_body)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout.addWidget(self.label_31, 2, 1, 1, 1)

        self.label_29 = QLabel(self.graph_multi_page_body)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout.addWidget(self.label_29, 1, 1, 1, 1)


        self.horizontalLayout_24.addWidget(self.graph_multi_page_body)

        self.project_stack.addWidget(self.graph_multi_page)

        self.verticalLayout_55.addWidget(self.project_stack)


        self.verticalLayout_54.addWidget(self.project_homepage_body)


        self.horizontalLayout_38.addWidget(self.project_homepage_container)

        self.main_body_stack.addWidget(self.project_homepage)
        self.settings_page = QWidget()
        self.settings_page.setObjectName(u"settings_page")
        sizePolicy.setHeightForWidth(self.settings_page.sizePolicy().hasHeightForWidth())
        self.settings_page.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QVBoxLayout(self.settings_page)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.settings_body = QFrame(self.settings_page)
        self.settings_body.setObjectName(u"settings_body")
        sizePolicy.setHeightForWidth(self.settings_body.sizePolicy().hasHeightForWidth())
        self.settings_body.setSizePolicy(sizePolicy)
        self.settings_body.setFrameShape(QFrame.Shape.StyledPanel)
        self.settings_body.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.settings_body)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.settings_header = QFrame(self.settings_body)
        self.settings_header.setObjectName(u"settings_header")
        self.settings_header.setFrameShape(QFrame.Shape.StyledPanel)
        self.settings_header.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_31 = QHBoxLayout(self.settings_header)
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.label_2 = QLabel(self.settings_header)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font5)

        self.horizontalLayout_31.addWidget(self.label_2, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)


        self.verticalLayout_3.addWidget(self.settings_header, 0, Qt.AlignmentFlag.AlignTop)

        self.frame_21 = QFrame(self.settings_body)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_21.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_60 = QVBoxLayout(self.frame_21)
        self.verticalLayout_60.setSpacing(0)
        self.verticalLayout_60.setObjectName(u"verticalLayout_60")
        self.verticalLayout_60.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_6 = QScrollArea(self.frame_21)
        self.scrollArea_6.setObjectName(u"scrollArea_6")
        self.scrollArea_6.setWidgetResizable(True)
        self.scrollAreaWidgetContents_6 = QWidget()
        self.scrollAreaWidgetContents_6.setObjectName(u"scrollAreaWidgetContents_6")
        self.scrollAreaWidgetContents_6.setGeometry(QRect(0, 0, 260, 152))
        self.verticalLayout_62 = QVBoxLayout(self.scrollAreaWidgetContents_6)
        self.verticalLayout_62.setObjectName(u"verticalLayout_62")
        self.verticalLayout_62.setContentsMargins(6, 0, 0, 0)
        self.frame_25 = QFrame(self.scrollAreaWidgetContents_6)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_25.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_63 = QVBoxLayout(self.frame_25)
        self.verticalLayout_63.setObjectName(u"verticalLayout_63")
        self.verticalLayout_63.setContentsMargins(0, 0, 0, 0)
        self.frame_22 = QFrame(self.frame_25)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setFont(font1)
        self.frame_22.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_22.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_61 = QVBoxLayout(self.frame_22)
        self.verticalLayout_61.setObjectName(u"verticalLayout_61")
        self.verticalLayout_61.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.frame_22)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)

        self.verticalLayout_61.addWidget(self.label_5, 0, Qt.AlignmentFlag.AlignTop)

        self.appTheme_combobox = QComboBox(self.frame_22)
        self.appTheme_combobox.addItem("")
        self.appTheme_combobox.addItem("")
        self.appTheme_combobox.addItem("")
        self.appTheme_combobox.setObjectName(u"appTheme_combobox")
        self.appTheme_combobox.setMaximumSize(QSize(200, 16777215))

        self.verticalLayout_61.addWidget(self.appTheme_combobox)


        self.verticalLayout_63.addWidget(self.frame_22)

        self.frame_26 = QFrame(self.frame_25)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_26.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_65 = QVBoxLayout(self.frame_26)
        self.verticalLayout_65.setObjectName(u"verticalLayout_65")
        self.dyslexicfont_checkbox = QCheckBox(self.frame_26)
        self.dyslexicfont_checkbox.setObjectName(u"dyslexicfont_checkbox")

        self.verticalLayout_65.addWidget(self.dyslexicfont_checkbox)


        self.verticalLayout_63.addWidget(self.frame_26)

        self.frame_24 = QFrame(self.frame_25)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_24.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_64 = QVBoxLayout(self.frame_24)
        self.verticalLayout_64.setObjectName(u"verticalLayout_64")
        self.fullscreen_checkbox = QCheckBox(self.frame_24)
        self.fullscreen_checkbox.setObjectName(u"fullscreen_checkbox")
        self.fullscreen_checkbox.setChecked(True)

        self.verticalLayout_64.addWidget(self.fullscreen_checkbox)


        self.verticalLayout_63.addWidget(self.frame_24)


        self.verticalLayout_62.addWidget(self.frame_25, 0, Qt.AlignmentFlag.AlignTop)

        self.scrollArea_6.setWidget(self.scrollAreaWidgetContents_6)

        self.verticalLayout_60.addWidget(self.scrollArea_6)


        self.verticalLayout_3.addWidget(self.frame_21)

        self.settings_footer = QFrame(self.settings_body)
        self.settings_footer.setObjectName(u"settings_footer")
        self.settings_footer.setFrameShape(QFrame.Shape.StyledPanel)
        self.settings_footer.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_32 = QHBoxLayout(self.settings_footer)
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.pushButton_2 = QPushButton(self.settings_footer)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_32.addWidget(self.pushButton_2, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom)

        self.pushButton = QPushButton(self.settings_footer)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_32.addWidget(self.pushButton, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignBottom)


        self.verticalLayout_3.addWidget(self.settings_footer, 0, Qt.AlignmentFlag.AlignBottom)


        self.verticalLayout_6.addWidget(self.settings_body)

        self.main_body_stack.addWidget(self.settings_page)

        self.verticalLayout_59.addWidget(self.main_body_stack)

        self.footer = QFrame(self.main_body_content)
        self.footer.setObjectName(u"footer")
        self.footer.setMaximumSize(QSize(16777215, 20))
        self.footer.setStyleSheet(u"border: none;\n"
"")
        self.footer.setFrameShape(QFrame.Shape.StyledPanel)
        self.footer.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.footer)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 2)
        self.frame = QFrame(self.footer)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.version_label = QLabel(self.frame)
        self.version_label.setObjectName(u"version_label")
        self.version_label.setStyleSheet(u"")

        self.horizontalLayout_5.addWidget(self.version_label)


        self.horizontalLayout_2.addWidget(self.frame, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom)

        self.frame_27 = QFrame(self.footer)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_27.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_27)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.frame_27)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_11.addWidget(self.frame_2, 0, Qt.AlignmentFlag.AlignRight)

        self.size_grip_container = QFrame(self.frame_27)
        self.size_grip_container.setObjectName(u"size_grip_container")
        self.size_grip_container.setMinimumSize(QSize(15, 15))
        self.size_grip_container.setMaximumSize(QSize(15, 15))
        self.size_grip_container.setFrameShape(QFrame.Shape.StyledPanel)
        self.size_grip_container.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_30 = QHBoxLayout(self.size_grip_container)
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.size_grip = QWidget(self.size_grip_container)
        self.size_grip.setObjectName(u"size_grip")
        self.size_grip.setMinimumSize(QSize(20, 20))
        self.size_grip.setMaximumSize(QSize(20, 20))

        self.horizontalLayout_30.addWidget(self.size_grip, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignBottom)


        self.horizontalLayout_11.addWidget(self.size_grip_container, 0, Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignBottom)


        self.horizontalLayout_2.addWidget(self.frame_27, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout_59.addWidget(self.footer)


        self.horizontalLayout.addWidget(self.main_body_content)


        self.verticalLayout_40.addWidget(self.main_body_container)


        self.horizontalLayout_8.addWidget(self.window_content)

        mainwindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(mainwindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 960, 21))
        mainwindow.setMenuBar(self.menubar)

        self.retranslateUi(mainwindow)

        self.project_taskbar_toolbox.setCurrentIndex(1)
        self.toolbox_graphlist.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(mainwindow)
    # setupUi

    def retranslateUi(self, mainwindow):
        mainwindow.setWindowTitle(QCoreApplication.translate("mainwindow", u"GraphBat", None))
        mainwindow.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderThick", None))
        self.centralwidget.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderThick", None))
        self.window_content.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderThick", None))
        self.header.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"header", None))
        self.label_6.setText("")
        self.home_button.setText("")
        self.settings_button_top.setText("")
        self.minimize_button.setText("")
        self.maximize_button.setText("")
        self.maximize_button.setProperty(u"style_ID", "")
        self.exit_button.setText("")
        self.main_body_container.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderless", None))
        self.taskbar_body_container.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderless", None))
        self.label_32.setText(QCoreApplication.translate("mainwindow", u"GraphBat", None))
        self.label_4.setText(QCoreApplication.translate("mainwindow", u"Create or load a project to get started.", None))
        self.create_button_side.setText(QCoreApplication.translate("mainwindow", u"Create Project", None))
        self.load_button_side.setText(QCoreApplication.translate("mainwindow", u"Load Project", None))
        self.settings_button_side.setText(QCoreApplication.translate("mainwindow", u"App Settings", None))
        self.about_button_side.setText(QCoreApplication.translate("mainwindow", u"About This App", None))
        self.label_74.setText(QCoreApplication.translate("mainwindow", u"Project Name", None))
        self.frame_20.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"taskbarBgLight", None))
        self.project_taskbar_toolbox.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"tbTabTier1", None))
        self.toolbox_project.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"taskbarBgLight", None))
        self.toolbox_project_body.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"taskbarBgLight", None))
        self.pushButton_13.setText(QCoreApplication.translate("mainwindow", u"Modify Project", None))
        self.pushButton_14.setText(QCoreApplication.translate("mainwindow", u"Load Project", None))
        self.pushButton_15.setText(QCoreApplication.translate("mainwindow", u"Create New Project", None))
        self.project_taskbar_toolbox.setItemText(self.project_taskbar_toolbox.indexOf(self.toolbox_project), QCoreApplication.translate("mainwindow", u"Project", None))
        self.toolbox_graphs.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderlessDark", None))
        self.frame_18.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"taskbarBgLight", None))
        self.toolbox_graphlist.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"tbTabTier2", None))
        self.toolbox_datasets.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"tbTabTier2", None))
        self.scrollArea_2.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderless", None))
        self.dataset_list.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"taskbarBgLight", None))
        self.toolbox_graphlist.setItemText(self.toolbox_graphlist.indexOf(self.toolbox_datasets), QCoreApplication.translate("mainwindow", u"Datasets", None))
        self.toolbox_maps.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"tbTabTier2", None))
        self.scrollArea_5.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderless", None))
        self.scrollAreaWidgetContents_5.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderless", None))
        self.map_list.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"taskbarBgLight", None))
        self.toolbox_graphlist.setItemText(self.toolbox_graphlist.indexOf(self.toolbox_maps), QCoreApplication.translate("mainwindow", u"Maps", None))
        self.project_taskbar_toolbox.setItemText(self.project_taskbar_toolbox.indexOf(self.toolbox_graphs), QCoreApplication.translate("mainwindow", u"Data", None))
        self.toolbox_other.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"taskbarBgLight", None))
        self.toolbox_other_body.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"taskbarBgLight", None))
        self.pushButton_11.setText(QCoreApplication.translate("mainwindow", u"Settings", None))
        self.pushButton_12.setText(QCoreApplication.translate("mainwindow", u"About GraphBat", None))
        self.project_taskbar_toolbox.setItemText(self.project_taskbar_toolbox.indexOf(self.toolbox_other), QCoreApplication.translate("mainwindow", u"Other", None))
        self.close_button_container.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderlessDark", None))
        self.close_button.setText("")
        self.close_button.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"iconButton", None))
        self.main_body_content.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderless", None))
        self.main_body_stack.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderless", None))
        self.main_body.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderless", None))
        self.banner.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"banner", None))
        self.label_3.setText(QCoreApplication.translate("mainwindow", u"Welcome!", None))
        self.main_content.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"backgroundGraphic", None))
        self.create_button_main.setText(QCoreApplication.translate("mainwindow", u"New\n"
"Project", None))
        self.create_button_main.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"bigButton", None))
        self.load_button_main.setText(QCoreApplication.translate("mainwindow", u"Load\n"
"Project", None))
        self.load_button_main.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"bigButton", None))
        self.create_project_body_2.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderless", None))
        self.create_header.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"banner", None))
        self.label_7.setText(QCoreApplication.translate("mainwindow", u"New Project", None))
        self.create_body_scroll_area.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderless", None))
        self.create_project_body.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderlessDark", None))
        self.label_8.setText(QCoreApplication.translate("mainwindow", u"Project Name", None))
        self.label_9.setText(QCoreApplication.translate("mainwindow", u"Add Data Files (optional)", None))
        self.create_add_data_button.setText(QCoreApplication.translate("mainwindow", u"Add file...", None))
        self.label_10.setText(QCoreApplication.translate("mainwindow", u"in .CSV format only", None))
        self.label_11.setText(QCoreApplication.translate("mainwindow", u"Add Cave Map (optional)", None))
        self.create_add_map_button.setText(QCoreApplication.translate("mainwindow", u"Add file...", None))
        self.label_12.setText(QCoreApplication.translate("mainwindow", u"in .JPG, .JPEG, .PNG, or .GIF format", None))
        self.label_13.setText(QCoreApplication.translate("mainwindow", u"Project Description (optional)", None))
        self.label_14.setText(QCoreApplication.translate("mainwindow", u"Max 2000 characters", None))
        self.create_footer.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"banner", None))
        self.cancel_create_button.setText(QCoreApplication.translate("mainwindow", u"Cancel", None))
        self.confirm_create_button.setText(QCoreApplication.translate("mainwindow", u"Create", None))
        self.about_container.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"backgroundDark", None))
        self.label_15.setText(QCoreApplication.translate("mainwindow", u"About GraphBat", None))
        self.label.setText(QCoreApplication.translate("mainwindow", u"GraphBat was created as a student project for Spring 2025's Computer Science Capstone Project class at Kennesaw State University under the supervision of Dr. Sharon Perry. It is an open source application free for noncommercial use. ", None))
        self.label_16.setText(QCoreApplication.translate("mainwindow", u"Hayden Harper", None))
        self.label_17.setText(QCoreApplication.translate("mainwindow", u"Project Lead, Back-End Developer (Cave Map Visualizer)", None))
        self.label_18.setText(QCoreApplication.translate("mainwindow", u"Nathan Karg", None))
        self.label_19.setText(QCoreApplication.translate("mainwindow", u"Back-End Developer (Graphs and Other Visualizations)", None))
        self.label_20.setText(QCoreApplication.translate("mainwindow", u"Abdalla Ugas", None))
        self.label_21.setText(QCoreApplication.translate("mainwindow", u"Back-End Developer (Data Import and Export)", None))
        self.label_22.setText(QCoreApplication.translate("mainwindow", u"Caroline Roberson", None))
        self.label_23.setText(QCoreApplication.translate("mainwindow", u"Front-End Developer, UX Designer", None))
        self.label_24.setText("")
        self.about_back_button.setText(QCoreApplication.translate("mainwindow", u"Back", None))
        self.load_page_body.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"banner", None))
        self.label_25.setText(QCoreApplication.translate("mainwindow", u"Load Project", None))
        self.load_scroll_area.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderless", None))
        self.load_body.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderlessDark", None))
        self.load_back_button.setText(QCoreApplication.translate("mainwindow", u"Back", None))
        self.project_homepage.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderless", None))
        self.project_homepage_container.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderless", None))
        self.project_homepage_header.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderlessDark", None))
        self.label_76.setText(QCoreApplication.translate("mainwindow", u"Project Name", None))
        self.dropdown_bargraph.setItemText(0, QCoreApplication.translate("mainwindow", u"Bar Graph - Mean", None))
        self.dropdown_bargraph.setItemText(1, QCoreApplication.translate("mainwindow", u"Bar Graph - Median", None))
        self.dropdown_bargraph.setItemText(2, QCoreApplication.translate("mainwindow", u"Bar Graph - Minimum", None))
        self.dropdown_bargraph.setItemText(3, QCoreApplication.translate("mainwindow", u"Bar Graph - Maximum", None))
        self.dropdown_bargraph.setItemText(4, QCoreApplication.translate("mainwindow", u"Bar Graph - Count", None))

        self.button_boxplot.setText(QCoreApplication.translate("mainwindow", u"Box Plot", None))
        self.button_histogram.setText(QCoreApplication.translate("mainwindow", u"Histogram", None))
        self.button_linegraph.setText(QCoreApplication.translate("mainwindow", u"Line Graph", None))
        self.button_cavemap.setText(QCoreApplication.translate("mainwindow", u"Heat Map", None))
        self.project_homepage_body.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderless", None))
        self.project_home_page.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"backgroundGraphic", None))
        self.label_75.setText("")
        self.label_35.setText(QCoreApplication.translate("mainwindow", u"TextLabel", None))
        self.label_37.setText(QCoreApplication.translate("mainwindow", u"TextLabel", None))
        self.label_33.setText(QCoreApplication.translate("mainwindow", u"TextLabel", None))
        self.label_36.setText(QCoreApplication.translate("mainwindow", u"TextLabel", None))
        self.label_34.setText(QCoreApplication.translate("mainwindow", u"TextLabel", None))
        self.label_30.setText(QCoreApplication.translate("mainwindow", u"graph 2", None))
        self.label_31.setText(QCoreApplication.translate("mainwindow", u"graph 3", None))
        self.label_29.setText(QCoreApplication.translate("mainwindow", u"graph 1", None))
        self.settings_body.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"backgroundDark", None))
        self.settings_header.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"banner", None))
        self.label_2.setText(QCoreApplication.translate("mainwindow", u"Application Settings", None))
        self.scrollArea_6.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderlessDark", None))
        self.scrollAreaWidgetContents_6.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"borderlessDark", None))
        self.label_5.setText(QCoreApplication.translate("mainwindow", u"App Theme", None))
        self.appTheme_combobox.setItemText(0, QCoreApplication.translate("mainwindow", u"Default", None))
        self.appTheme_combobox.setItemText(1, QCoreApplication.translate("mainwindow", u"Dark", None))
        self.appTheme_combobox.setItemText(2, QCoreApplication.translate("mainwindow", u"Light", None))

        self.dyslexicfont_checkbox.setText(QCoreApplication.translate("mainwindow", u"Dyslexic-Friendly Font (requires restart)", None))
        self.fullscreen_checkbox.setText(QCoreApplication.translate("mainwindow", u"Start in fullscreen mode", None))
        self.settings_footer.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"banner", None))
        self.pushButton_2.setText(QCoreApplication.translate("mainwindow", u"Cancel", None))
        self.pushButton.setText(QCoreApplication.translate("mainwindow", u"Save", None))
        self.footer.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"footer", None))
        self.version_label.setText(QCoreApplication.translate("mainwindow", u"Version 1.0.0 (April 2025)", None))
        self.version_label.setProperty(u"style_ID", QCoreApplication.translate("mainwindow", u"subtleText", None))
    # retranslateUi

