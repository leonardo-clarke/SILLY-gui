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

class mplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(mplCanvas, self).__init__(fig)

class ApplicationWindow(QMainWindow):
    
    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.setWindowTitle('silly-GUI')
        self.setGeometry(200, 200, 350, 350)
        
        self.filename = ''
        self.df = pd.DataFrame()
        self.wave_range = []
        
        self.canv = mplCanvas()
        layout.addWidget(self.canv)

        self.add_toolbar()

    def add_toolbar(self):

        toolbar = QToolBar()
        self.addToolBar(toolbar)

        upload_file = QAction('upload file', self)
        upload_file.triggered.connect(self.getfile)
        toolbar.addAction(upload_file)

        toggle_drag = QAction('toggle', self)
        toggle_drag.triggered.connect(self.selectrange)
        toolbar.addAction(toggle_drag)


    def selectrange(self):
        
        return


    def getfile(self):

        self.filename = QFileDialog.getOpenFileName(filter = "csv (*.csv)")[0]
        print('File :', self.filename)
        self.getdata()
        
    def getdata(self):

        self.df = pd.read_csv(self.filename, header=0)
        print(self.df)
        self.update() 
    
    def update(self):
        
        self.canv.axes.cla()
        self.df.plot(x = self.df.columns[1], y = self.df.columns[2], ax = self.canv.axes)
        self.canv.draw()
        #sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

if (__name__ == '__main__'):
    application = QApplication([])
    mainWindow = ApplicationWindow()
    mainWindow.show()
    application.exec()