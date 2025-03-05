# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

#####
#This does not work with the temp csv files yet
#Only with files that have columns of the same data type (int,float, etc)
#I'll fix it in a bit but I'm just putting this in the git so everyone can use a test with it
#####

from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtWidgets import QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as Navi
from matplotlib.figure import Figure
import seaborn as sns
import pandas as pd
import sip # can be installed : pip install sip

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

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



        #Setting up file name var, canvas, dataframe and toolbar

        self.filename =''
        self.canv = MatplotlibCanvas(self)
        self.df = []
        self.toolbar = Navi(self.canv,self.centralwidget)
        self.horizontalLayout.addWidget(self.toolbar)

        self.themes = ['bmh','classic','dark_background','seaborn','fast','ggplot','grayscale']

        #Start of button codes
        self.pushButton.clicked.connect(self.getFile)
        self.comboBox.currentIndexChanged['QString'].connect(self.update)


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
            self.VerticalLayout.removeItem(self.spacerItem1)
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
        self.filename = QFileDialog.getOpenFileName(filter = "csv (*.csv)")[0]
        print("File :", self.filename)
        self.readData()

    def readData(self):
        #Function to read csv data
        self.df = pd.read_csv(self.filename,encoding = 'utf-8').fillna(0)
        self.update(self.themes[0])



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
