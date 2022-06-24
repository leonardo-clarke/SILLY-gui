import sys
import os

import numpy as np
import pandas as pd

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QTextEdit, QMainWindow, QPushButton, QGridLayout, QWidget, QToolBar, QFileDialog
from PyQt6.QtGui import QAction, QIcon

import matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from astropy.io import fits

import line_fitting_functions as lff

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

        layout = QGridLayout()
        
        self.filename = ''
        self.df = pd.DataFrame()
        self.x0 = None
        self.x1 = None
        self.release = False
        self.fit_number = 0

        self.canv = mplCanvas()
        layout.addWidget(self.canv, 0, 0)
        layout.addWidget(NavigationToolbar(self.canv, self), 1, 0)

        self.output_text = QTextEdit()
        layout.addWidget(self.output_text, 0, 1)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.setWindowTitle('silly-GUI')
        self.setGeometry(200, 200, 1250, 650)

        self.add_toolbar()


    def add_toolbar(self):

        """ method to add a toolbar 

        Returns
        -------
        adds functional toolbar with toggle drag and add file feature

        """

        toolbar = QToolBar()
        self.addToolBar(toolbar)

        upload_file = QPushButton('upload file', self)
        upload_file.clicked[bool].connect(self.getfile)
        toolbar.addWidget(upload_file)

        button = QPushButton('select region', self)
        toolbar.addWidget(button)
        button.clicked[bool].connect(self.selectrange)

        fit = QPushButton('fit', self)
        toolbar.addWidget(fit)
        fit.clicked[bool].connect(self.update_for_fit)

        fit = QPushButton('clear line fits', self)
        toolbar.addWidget(fit)
        fit.clicked[bool].connect(self.clear_line_fits)

    def selectrange(self):
    
        self.cid_press = self.canv.mpl_connect('button_press_event', self.on_press)
        self.cid_release = self.canv.mpl_connect('button_release_event', self.on_release)

    def on_press(self, event):

        print('press')
        self.x0 = event.xdata
        print(self.x0)

    def on_release(self, event):

        print('release')
        self.x1 = event.xdata
        self.release = True
        
        if self.release == True:
            self.canv.mpl_disconnect(self.cid_press)
            self.canv.mpl_disconnect(self.cid_release)

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
            wavelengths, spectrum, err_spec = lff.read_fits_spectrum(self.filename, fits.getheader(self.filename, ext=1))
            df_dictionary = {'':np.arange(len(wavelengths)), 'wavelength':wavelengths, 'flux':spectrum, 'error':err_spec}
            self.df = pd.DataFrame(df_dictionary)
            self.update()

    def update(self, previous_ax_limits=False):

        """ method to update plot based on user selected file

        Returns
        -------
        updates canvas with new data

        """
        xlim = self.canv.axes.get_xlim(); ylim = self.canv.axes.get_ylim()
        
        self.canv.axes.cla()
        self.canv.axes.set_ylabel('flux density')
        self.df.plot(x = self.df.columns[1], y = self.df.columns[2], ax = self.canv.axes)
        if previous_ax_limits == True:
            print(xlim, ylim)
            self.canv.axes.set_xlim(xlim); self.canv.axes.set_ylim(ylim)
        self.canv.draw()
    
    def update_for_fit(self):
        print(self.x0)
        print(self.x1)
        if self.x0 == None:
            print('no values selected!')
            self.output_text.append('no values selected!')
        else:
            print('wow!')
            self.fit_number += 1
            params, covariance, wavelengths, spectrum = lff.fit_emission_line_to_gaussian(self.x0, self.x1, self.filename)
            self.canv.axes.plot(wavelengths, lff.gaussian(wavelengths, params), label='fit {}'.format(self.fit_number))
            self.canv.axes.legend()
            self.canv.draw()
            self.update_fit_list(params, covariance)

    def clear_line_fits(self):
        self.update(previous_ax_limits=True)
        self.fit_number = 0
        self.output_text.clear()

    def update_fit_list(self, params, covariance):
        self.output_text.append('- fit {0}: flux:{1}, sig:{2}, mu:{3}, c:{4}'.format(self.fit_number,
                                                            params[0],
                                                            params[1],
                                                            params[2],
                                                            params[3]))
        self.output_text.append('- fit {0}: xmin: {1}, xmax: {2}'.format(self.fit_number, 
                                                            self.x0,
                                                            self.x1))
        self.output_text.append('******************')

if (__name__ == '__main__'):
    application = QApplication([])
    mainWindow = ApplicationWindow()
    mainWindow.show()
    application.exec()