import sys
import os

import numpy as np
import pandas as pd

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QToolBar, QFileDialog
from PyQt6.QtGui import QAction, QIcon

import matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

matplotlib.use('QtAgg')

class mplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(mplCanvas, self).__init__(fig)

class ApplicationWindow(QMainWindow):

    """ Handles main GUI window and inherits from PyQt6.QtQidgets.QMainWindow

    Attributes
    ----------
    setLayout : QVBoxLayout object
        initalize layout of GUI.
    setCentralWidget : QWidget object
        initalize widget object.
    setGeometry: inherited from QMainWindow
        set size of GUI window
    setWindowTile: inherited from QMainWindow
        set name of GUI window
    
    filename: str
        user inputted file, default is empty string
    df: pandas DataFrame
        data from user inputed file, default is empty dataframe
    wave_range: list
        user selected wavelength range, default is empty list
    """
    
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
        self.x0 = None
        self.x1 = None
        
        self.canv = mplCanvas()
        layout.addWidget(self.canv)
        layout.addWidget(NavigationToolbar(self.canv, self))

        self.add_toolbar()

    def add_toolbar(self):

        """ method to add a toolbar 

        Returns
        -------
        adds functional toolbar with toggle drag and add file feature

        """

        toolbar = QToolBar()
        self.addToolBar(toolbar)

        upload_file = QAction('upload file', self)
        upload_file.triggered.connect(self.getfile)
        toolbar.addAction(upload_file)

        toggle_drag = QAction('toggle', self)
        self.toggled = False
        toggle_drag.triggered.connect(self.selectrange)
        toolbar.addAction(toggle_drag)


    def selectrange(self):
        
        self.canv.mpl_connect('button_press_event', self.on_press)
        self.canv.mpl_connect('button_release_event', self.on_release)
        self.update_for_fit()


    def on_press(self, event):
        print('press')
        self.x0 = event.xdata
        print(self.x0)

    def on_release(self, event):
        print('release')
        self.x1 = event.xdata
        print(self.x1)
        #self.rect.set_width(self.x1 - self.x0)
        #self.rect.set_height(self.y1 - self.y0)
        #self.rect.set_xy((self.x0, self.y0))
        #self.canv.axes.figure.canvas.draw()

    def getfile(self):
        
        """ method to open file

        Returns
        -------
        updates self.filename

        """

        self.filename = QFileDialog.getOpenFileName(filter = "csv (*.csv)")[0]
        print('File :', self.filename)
        self.getdata()
        
    def getdata(self):

        """ method to read file data

        Returns
        -------
        updates self.df to add data according to what's in self.filename

        """

        self.df = pd.read_csv(self.filename, header=0)
        print(self.df)
        self.update() 
    
    def update(self):

        """ method to update plot based on user selected file

        Returns
        -------
        updates canvas with new data

        """
        
        self.canv.axes.cla()
        self.df.plot(x = self.df.columns[1], y = self.df.columns[2], ax = self.canv.axes)
        self.canv.draw()
    
    def update_for_fit(self):

        self.canv.axes.cla()
        

if (__name__ == '__main__'):
    application = QApplication([])
    mainWindow = ApplicationWindow()
    mainWindow.show()
    application.exec()