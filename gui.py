import sys
import os

import numpy as np
import pandas as pd

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QToolBar, QFileDialog
from PyQt6.QtGui import QAction, QIcon

import matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure

matplotlib.use('QtAgg')

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class ApplicationWindow(QMainWindow):
    
    def __init__(self):

        super().__init__()

        self.setWindowTitle('silly-GUI')
        self.setGeometry(200, 200, 350, 350)
        self.filename = ''
        self.df = pd.DataFrame()
        self.add_toolbar()

    def add_toolbar(self):

        toolbar = QToolBar()
        self.addToolBar(toolbar)
        button_action = QAction('upload file', self)
        #button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.getfile)
        toolbar.addAction(button_action)

    def getfile(self):

        self.filename = QFileDialog.getOpenFileName(filter = "csv (*.csv)")[0]
        print('File :', self.filename)
        self.getdata()
        
    def getdata(self):

        self.df = pd.read_csv(self.filename, header=0)
        print(self.df)
		#self.Update(self.themes[0]) 
    
    def update(self):
        
        return



        

    #     menuBar = self.menuBar()
    # def read_data(self):
    #     return
    
    # def menu(self):
    #     return
# lmin = 500
# lmax = 510
# a = 1
# mean = 505
# sigma = 1

# toy = toy_data.gaussian_noise(lmin, lmax, a, mean, sigma)
if (__name__ == '__main__'):
    application = QApplication([])
    mainWindow = ApplicationWindow()
    mainWindow.show()
    application.exec()