import sys

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListView, QFileSystemModel, QApplication, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import log_viewer


class Widget(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.LOG_PATH = QDir.currentPath() + '/LOGS/board/'

        hlay = QHBoxLayout(self)
        self.listview = QListView()
        self.listview.setFixedWidth(350)
        hlay.addWidget(self.listview)

        self.figure = plt.figure()
        self.figure, (self.ax0, self.ax1) = plt.subplots(nrows=2, sharex=True)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.label = QLabel()
        self.label.setFixedHeight(25)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.label)
        hlay.addLayout(layout)

        self.dirModel = QFileSystemModel()
        self.dirModel.setRootPath(QDir.rootPath())
        self.dirModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)

        self.fileModel = QFileSystemModel()
        self.fileModel.setFilter(QDir.NoDotAndDotDot | QDir.Files)

        self.listview.setModel(self.fileModel)
        self.listview.setRootIndex(self.fileModel.setRootPath(self.LOG_PATH))
        self.listview.selectionModel().selectionChanged.connect(self.log_changed)
        self.listview.adjustSize()

    def log_changed(self, selected, deselected):
        index = self.listview.currentIndex()
        log_name = index.data(Qt.DisplayRole)

        self.figure.clear()
        self.label.setVisible(False)

        times, alts, throttles, pitches, cfg_line = log_viewer.parse_log(filename=self.LOG_PATH + log_name)

        if len(times) == 0:
            self.label.setText('Empty log!')
            self.label.setVisible(True)
            return

        self.ax0 = self.figure.add_subplot(2, 1, 1)
        self.ax1 = self.figure.add_subplot(2, 1, 2, sharex=self.ax0)
        mtimes = mdates.date2num(times)
        self.ax0.plot(mtimes, throttles, '-g')
        self.ax0.legend(['Throttle'])
        self.ax0.set_ylim(988, 2012)
        self.ax0.set_ylim(988, 1700)
        self.ax0.text(0.1, 1.2, cfg_line, fontsize=14, transform=self.ax0.transAxes, va='top')

        self.ax1.plot(mtimes, alts, ':b')
        self.ax1.legend(['Altitude'])
        self.ax1.set_ylim(-0.5, 30)

        # self.ax[2].plot(mtimes, pitches, ':c')
        # self.ax[2].legend(['Pitch'])

        sec_loc = mdates.SecondLocator(interval=1)
        sec_formatter = mdates.DateFormatter('%H:%M:%S.%f')

        self.ax0.xaxis.set_major_locator(sec_loc)
        self.ax0.xaxis.set_major_formatter(sec_formatter)
        self.ax1.xaxis.set_major_locator(sec_loc)
        self.ax1.xaxis.set_major_formatter(sec_formatter)
        # self.ax[2].xaxis.set_major_locator(sec_loc)
        # self.ax[2].xaxis.set_major_formatter(sec_formatter)
        plt.gcf().autofmt_xdate(rotation=90)

        # plt.text(cfg_line,  fontdict=font)
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
