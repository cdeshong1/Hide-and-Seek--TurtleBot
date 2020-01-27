#! /usr/bin/python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Turtle.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!



from PyQt5 import QtCore, QtGui, QtWidgets
from subprocess import call
import time
import roslib; roslib.load_manifest('rviz_python_tutorial')
from python_qt_binding.QtGui import *
from python_qt_binding.QtCore import *
import rviz

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 1000)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50,20, 1110, 950))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.StartButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.StartButton.sizePolicy().hasHeightForWidth())
        self.StartButton.setSizePolicy(sizePolicy)
        self.StartButton.setObjectName("StartButton")
        self.horizontalLayout.addWidget(self.StartButton)
        self.StopButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.StopButton.sizePolicy().hasHeightForWidth())
        self.StopButton.setSizePolicy(sizePolicy)
        self.StopButton.setObjectName("StopButton")
        self.horizontalLayout.addWidget(self.StopButton)
        self.LaunchButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.LaunchButton.setObjectName("LaunchButton")
	self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
	self.verticalLayout.addWidget(self.label)
        font = QtGui.QFont()
        font.setFamily("Ubuntu Mono")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setText("Time")
        self.label.setObjectName("label")
####################################################################################################
	self.frame = rviz.VisualizationFrame()
	self.frame.setSplashPath("")
	self.frame.initialize()
	reader = rviz.YamlConfigReader()
        config = rviz.Config()
        reader.readFile(config, "navigation.rviz")
        self.frame.load(config)
	self.frame.setMenuBar( None )
        self.frame.setStatusBar( None )
        self.frame.setHideButtonVisibility( False )
	self.frame.setFullScreen( True )	

        ## frame.getManager() returns the VisualizationManager
        ## instance, which is a very central class.  It has pointers
        ## to other manager objects and is generally required to make
        ## any changes in an rviz instance.
        self.manager = self.frame.getManager()
	self.verticalLayout.addWidget(self.frame)
	self.verticalLayout.addWidget(self.LaunchButton)
	self.verticalLayout.addLayout(self.horizontalLayout)
####################################################################################################
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #Calling appropriate function based on the button clicked
        self.LaunchButton.clicked.connect(self.launched)
        self.StartButton.clicked.connect(self.started)
        self.StopButton.clicked.connect(self.stopped)

        #Timer stuff
        self.timer = QtCore.QTimer
        #self.timer.timeout.connect(self.countdown)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.StartButton.setText(_translate("MainWindow", "START"))
        self.StopButton.setText(_translate("MainWindow", "STOP"))
        self.LaunchButton.setText(_translate("MainWindow", "LAUNCH"))

###################################################################################################
    def launched(self):
        global launched
        if(launched == 0):
            launched += 1
            call(['gnome-terminal', '-e', "sshpass -p 'turtlebot' ssh -t turtlebot@10.191.22.32 roslaunch my_robot_name_2dnav turtlebot_configuration.launch"])
	    time.sleep(10)
	    call(['gnome-terminal', '-e', "sshpass -p 'turtlebot' ssh -t turtlebot@10.191.22.32 roslaunch my_robot_name_2dnav move_base.launch"])
	    time.sleep(5)
####################################################################################################

            
    #Method called when the start button is clicked
    def started(self):
        self.timer.start(1000)
        self.label.setText(str(timeLeft))

    #Method called when the stop button is clicked
    def stopped(self):
        global flag
        flag = 0
	

#Global variables
timeLeft = 10
running = 0
launched = 0

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


