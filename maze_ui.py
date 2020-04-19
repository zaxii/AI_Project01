# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'maze.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.maze_window = QtWidgets.QLabel(self.centralwidget)
        self.maze_window.setGeometry(QtCore.QRect(50, 50, 500, 500))
        self.maze_window.setText("")
        self.maze_window.setObjectName("maze_window")

        self.startBtn = QtWidgets.QPushButton(self.centralwidget)
        self.startBtn.setGeometry(QtCore.QRect(660, 500, 100, 50))
        self.startBtn.setObjectName("startBtn")

        self.Mode = QtWidgets.QPushButton(self.centralwidget)
        self.Mode.setGeometry(QtCore.QRect(660, 420, 100, 50))
        self.Mode.setObjectName("Mode")

        self.iterationBtn = QtWidgets.QPushButton(self.centralwidget)
        self.iterationBtn.setGeometry(QtCore.QRect(660, 340, 100, 50))
        self.iterationBtn.setObjectName("resetButton")

        self.resetBtn = QtWidgets.QPushButton(self.centralwidget)
        self.resetBtn.setGeometry(QtCore.QRect(660, 260, 100, 50))
        self.resetBtn.setObjectName("resetButton")

        self.stepMsg = QtWidgets.QLabel(self.centralwidget)
        self.stepMsg.setGeometry(QtCore.QRect(660, 80, 100, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.stepMsg.setFont(font)
        self.stepMsg.setAlignment(QtCore.Qt.AlignCenter)
        self.stepMsg.setObjectName("stepMsg")
        self.step = QtWidgets.QLabel(self.centralwidget)
        self.step.setGeometry(QtCore.QRect(660, 150, 100, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.step.setFont(font)
        self.step.setAlignment(QtCore.Qt.AlignCenter)
        self.step.setObjectName("step")

        self.iterationMsg = QtWidgets.QLabel(self.centralwidget)
        self.iterationMsg.setGeometry(QtCore.QRect(660, 220, 100, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.iterationMsg.setFont(font)
        self.iterationMsg.setAlignment(QtCore.Qt.AlignCenter)
        self.iterationMsg.setObjectName("iterationMsg")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.startBtn.setText(_translate("MainWindow", "START"))
        self.iterationBtn.setText(_translate("MainWindow", "LEARN"))
        self.Mode.setText(_translate("MainWindow", "QLearning"))
        self.resetBtn.setText(_translate("MainWindow", "RESET"))
        self.stepMsg.setText(_translate("MainWindow", "当前步数"))
        self.step.setText(_translate("MainWindow", "0"))
        self.iterationMsg.setText(_translate("MainWindow", "N = 0"))
