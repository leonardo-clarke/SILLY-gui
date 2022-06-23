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

from astropy.io import fits

import line_fitting_functions

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
        self.wave_range = []
        
        self.canv = mplCanvas()
        layout.addWidget(self.canv)

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
        toggle_drag.triggered.connect(self.selectrange)
        toolbar.addAction(toggle_drag)


    def selectrange(self):
        
        return


    def getfile(self):
        
        """ method to open file

        Returns
        -------
        updates self.filename

        """

        self.filename = QFileDialog.getOpenFileName(filter = "CSV (*.csv);; FITS (*.fits)")[0]
        print('File :', self.filename)
        self.getdata()
        
    def getdata(self):

        """ method to read file data

        Returns
        -------
        updates self.df to add data according to what's in self.filename

        """

        if self.filename[-4:] == '.csv':
            self.df = pd.read_csv(self.filename, header=0)
            print(self.df)
            self.update()
        elif self.filename[-5:] == '.fits':
            wavelengths, spectrum, err_spec = line_fitting_functions.read_fits_spectrum(self.filename, fits.getheader(self.filename, ext=1))
            df_dictionary = {'':np.arange(len(wavelengths)), 'wavelength':wavelengths, 'flux':spectrum, 'error':err_spec}
            self.df = pd.DataFrame(df_dictionary)
            print(self.df)
            self.update()

    def update(self):

        """ method to update plot based on user selected file

        Returns
        -------
        updates canvas with new data

        """
        
        self.canv.axes.cla()
        self.canv.axes.set_ylabel('flux density')
        self.df.plot(x = self.df.columns[1], y = self.df.columns[2], ax = self.canv.axes)
        self.canv.draw()
        #sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

if (__name__ == '__main__'):
    application = QApplication([])
    mainWindow = ApplicationWindow()
    mainWindow.show()
    application.exec()