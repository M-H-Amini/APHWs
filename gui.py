import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox
import APHW as mh

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("gui.ui", self)
        self.listButton.clicked.connect(self.listButtonClicked)
        self.studentList.clicked.connect(self.studentChanged)    
        self.filesList.clicked.connect(self.openCode)

    def listButtonClicked(self):
        students = mh.getStudentNames('aphw')
        self.studentList.clear()
        self.studentList.addItems(students)    
    
    def openCode(self):
        path = os.path.join('aphw', self.studentList.currentItem().text(),
                            self.filesList.currentItem().text())
        try:
            with open(path, 'r') as file:
                code = file.read()
            self.codeEdit.setText(code)
        except:
            print('Error: msg')
            QMessageBox.information(self, 'Cannot open file!', "I couldn't open it!", QMessageBox.Ok)

    def studentChanged(self):
        item = self.studentList.currentItem().text()
        path = os.path.join('aphw', item)
        files = os.listdir(path)
        self.filesList.clear()
        self.filesList.addItems(files)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()