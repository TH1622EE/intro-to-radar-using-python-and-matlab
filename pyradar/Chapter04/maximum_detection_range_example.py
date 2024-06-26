"""
Project: RadarBook
File: maximum_detection_range_example.py
Created by: Lee A. Harrison
On: 6/30/2018
Created with: PyCharm

Copyright (C) 2019 Artech House (artech@artechhouse.com)
This file is part of Introduction to Radar Using Python and MATLAB
and can not be copied and/or distributed without the express permission of Artech House.
"""
import sys
from Chapter04.ui.MaximumDetectionRange_ui import Ui_MainWindow
from Libs.radar_range import radar_range
from numpy import linspace
from PyQt5.QtWidgets import QApplication, QMainWindow
from matplotlib.backends.qt_compat import QtCore
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class MaximumDetectionRange(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        super(self.__class__, self).__init__(parent)

        self.setupUi(self)

        # Connect to the input boxes, when the user presses enter the form updates
        self.snr_start.returnPressed.connect(self._update_canvas)
        self.snr_end.returnPressed.connect(self._update_canvas)
        self.system_temperature.returnPressed.connect(self._update_canvas)
        self.bandwidth.returnPressed.connect(self._update_canvas)
        self.noise_figure.returnPressed.connect(self._update_canvas)
        self.losses.returnPressed.connect(self._update_canvas)
        self.peak_power.returnPressed.connect(self._update_canvas)
        self.antenna_gain.returnPressed.connect(self._update_canvas)
        self.frequency.returnPressed.connect(self._update_canvas)
        self.target_rcs.returnPressed.connect(self._update_canvas)

        # Set up a figure for the plotting canvas
        fig = Figure() 
        self.axes1 = fig.add_subplot(111)
        self.my_canvas = FigureCanvas(fig)

        # Add the canvas to the vertical layout
        self.verticalLayout.addWidget(self.my_canvas)
        self.addToolBar(QtCore.Qt.TopToolBarArea, NavigationToolbar(self.my_canvas, self))

        # Update the canvas for the first display
        self._update_canvas()

    def _update_canvas(self):
        """
        Update the figure when the user changes an input value.
        :return:
        """
        # Get the signal to noise ratio from the form
        snr_start = float(self.snr_start.text())
        snr_end = float(self.snr_end.text())

        # Set up the signal to noise ratio array
        signal_to_noise = linspace(snr_start, snr_end, 2000)

        # Convert the noise figure to noise factor
        noise_figure = float(self.noise_figure.text())
        noise_factor = 10.0 ** (noise_figure / 10.0)

        # Convert the losses, antenna gain and target rcs to linear units
        losses = 10.0 ** (float(self.losses.text()) / 10.0)
        antenna_gain = 10.0 ** (float(self.antenna_gain.text()) / 10.0)
        target_rcs = 10.0 ** (float(self.target_rcs.text()) / 10.0)

        # Set up the input args
        kwargs = {'signal_to_noise': 10.0 ** (signal_to_noise / 10.0),
                  'system_temperature': float(self.system_temperature.text()),
                  'bandwidth': float(self.bandwidth.text()),
                  'noise_factor': noise_factor,
                  'losses': losses,
                  'peak_power': float(self.peak_power.text()),
                  'antenna_gain': antenna_gain,
                  'frequency': float(self.frequency.text()),
                  'target_rcs': target_rcs}

        # Calculate the maximum detection range
        maximum_range = radar_range.maximum_range(**kwargs)

        # Clear the axes for the updated plot
        self.axes1.clear()

        # Display the results
        self.axes1.plot(signal_to_noise, maximum_range / 1.e3, '')

        # Set the plot title and labels
        self.axes1.set_title('Maximum Detection Range', size=14)
        self.axes1.set_xlabel('Signal to Noise Ratio (dB)', size=12)
        self.axes1.set_ylabel('Maximum Detection Range (km)', size=12)

        # Set the tick label size
        self.axes1.tick_params(labelsize=12)

        # Turn on the grid
        self.axes1.grid(linestyle=':', linewidth=0.5)

        # Update the canvas
        self.my_canvas.draw()


def start(parent):
    form = MaximumDetectionRange(parent)  # Set the form
    form.show()                     # Show the form


def main():
    app = QApplication(sys.argv)    # A new instance of QApplication
    form = MaximumDetectionRange()  # Set the form
    form.show()                     # Show the form
    app.exec_()                     # Execute the app


if __name__ == '__main__':
    main()
