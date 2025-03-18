# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

#####
#A lot of the code is hardcoded just for testing sake, but I'll change it
#####

from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
from PyQt5.QtWidgets import QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as Navi
from matplotlib.figure import Figure
import seaborn as sns
import pandas as pd
import sip # can be installed : pip install sip
import os
import json
import shutil
#Canvas class
class MatplotlibCanvas(FigureCanvasQTAgg):
    def __init__(self,parent=None,width=5, height = 5, dpi = 120):
        f = Figure(figsize = (width,height),dpi = dpi)
        self.axes= f.add_subplot(111)
        super(MatplotlibCanvas,self).__init__(f)
        f.tight_layout()



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_CSV = QtWidgets.QAction(MainWindow)
        self.actionOpen_CSV.setObjectName("actionOpen_CSV")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionOpen_CSV)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.createProB = QtWidgets.QPushButton(self.centralwidget)
        self.createProB.setObjectName("createProB")
        self.createProB.setText("Create Project")
        self.horizontalLayout.addWidget(self.createProB)

        self.saveProB = QtWidgets.QPushButton(self.centralwidget)
        self.saveProB.setObjectName("saveProB")
        self.saveProB.setText("Save Project")
        self.horizontalLayout.addWidget(self.saveProB)

        self.loadProB = QtWidgets.QPushButton(self.centralwidget)
        self.loadProB.setObjectName("loadProB")
        self.loadProB.setText("Load Project")
        self.horizontalLayout.addWidget(self.loadProB)






        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



        #Setting up file name var, canvas, dataframe and toolbar

        self.filenames =''
        self.canv = MatplotlibCanvas(self)
        self.df = pd.DataFrame()
        self.toolbar = Navi(self.canv,self.centralwidget)
        self.horizontalLayout.addWidget(self.toolbar)

        self.themes = ['bmh','classic','dark_background','seaborn','fast','ggplot','grayscale']

        #Start of button codes
        self.pushButton.clicked.connect(self.getFile)
        self.comboBox.currentIndexChanged['QString'].connect(self.update)
        self.createProB.clicked.connect(self.createP)
        self.saveProB.clicked.connect(self.saveP)
        self.loadProB.clicked.connect(self.loadP)


    def createP(self):
        f =QFileDialog.getExistingDirectory(None,"Select Project Folder")
        if f:
            self.pFold =f
            self.pData ={
                "pf":self.pFold, "files":[]}
        self.dataF = os.path.join(self.pFold,"data")
        os.makedirs(self.dataF,exist_ok =True)
        print(f"Project has been made: {self.pFold}")

    def saveP(self):
        if not hasattr(self,"pFold") or not self.pFold:
            print("There isn't a project folder to select")
            return
        self.dataF = os.path.join(self.pFold,"data")
        os.makedirs(self.dataF,exist_ok =True)

        localF = []
        for f in self.filenames:
            try:
                projPath = os.path.join(self.dataF, os.path.basename(f))
                shutil.copy2(f,projPath)
                localF.append(os.path.basename(f))
                print(f"Copied {f} to {projPath}")
            except Exception as e:
                print(f"Error copying file {f}: {e}")


        self.pData["files"] =localF
        pf = os.path.join(self.pFold,"proj.json")
        with open(pf,"w") as i:
            json.dump(self.pData,i,indent = 4)

        print(f"Project saved to {pf}")

    def loadP(self):
        file,_ = QFileDialog.getOpenFileName(filter = "Project Files (*.json)")

        if not file:
            print("No Project Selected")
            return

        try:
            with open(file,"r") as i:
                self.pData = json.load(i)

            self.pFold =self.pData.get("pf","")
            self.dataF = os.path.join(self.pFold,"data")
            os.makedirs(self.dataF, exist_ok=True)
            self.filenames = [os.path.join(self.dataF, f) for f in self.pData.get("files", [])]

            print(f"Loaded project: {file}")
            print(f"Project Folder: {self.pFold}")
            print(f"Files in project: {self.filenames}")

            if not self.filenames:
                print("No files found")

            self.readData()
            self.update(self.themes[0])

        except Exception as e:
            print(f"Error loading in project: {e}")



    def update(self,v):
        print("V from CB: ", v)
        plt.clf()
        plt.style.use(v)
        try:
            self.horizontalLayout.removeWidget(self.toolbar)
            self.verticalLayout.removeWidget(self.canv)

            sip.delete(self.toolbar)
            sip.delete(self.canv)
            self.toolbar = None
            self.canv = None
            self.verticalLayout.removeItem(self.spacerItem1)
        except Exception as e:
            print(e)
            pass
        self.canv = MatplotlibCanvas(self)
        self.toolbar = Navi(self.canv,self.centralwidget)
        self.horizontalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canv)

        self.canv.axes.cla()
        a = self.df.plot(ax = self.canv.axes)
        legend = a.legend()
        legend.set_draggable(True)
        a.set_xlabel('X axis')
        a.set_ylabel('Y axis')
        a.set_title('Title')
        self.canv.draw()


    def getFile(self):
        #Will get file address of csv file and read it
        files,_ = QFileDialog.getOpenFileNames(filter="CSV Files (*.csv)")
        if files:
            self.filenames = files
            print("Files :", self.filenames)
            self.readData()
        else:
            print("No files selected.")

    def readData(self):
        #Function to read csv data
        dfs = []

        for file in self.filenames:
            try:
                df = pd.read_csv(file,
                              encoding = 'utf-8',
                              usecols=['Date-Time (EST)', 'Temperature   (°C)']
                              )
                df.rename(columns={"Date-Time (EST)": "Datetime", "Temperature   (°C)": "Temperature"}, inplace=True)
                df["Datetime"] = pd.to_datetime(df["Datetime"], format="%m/%d/%Y %H:%M:%S", errors="coerce")
                df.dropna(subset=["Datetime"], inplace=True)
                dfs.append(df)
            except Exception as e:
                print("Error in {file}: {e}")

        if dfs:
            self.df = pd.concat(dfs).sort_values(by= "Datetime")
            self.df.set_index("Datetime", inplace=True)
            self.update(self.themes[0])
        else:
            print("Data not valid")



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Select Theme"))
        self.pushButton.setText(_translate("MainWindow", "Open"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen_CSV.setText(_translate("MainWindow", "Open CSV"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
