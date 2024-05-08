from PyQt5.QtWidgets import QMainWindow
from ui.MainWindow import Ui_MainWindow

from qgis.core import Qgis


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.label.setText(Qgis.version())