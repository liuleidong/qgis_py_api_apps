import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from qgis.core import Qgis


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(400, 200, 800, 600)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        self.releaseName_label = QLabel(Qgis.releaseName(), self)
        self.devVersion_label = QLabel(Qgis.devVersion(), self)
        self.geosVersion_label = QLabel(Qgis.geosVersion(), self)
        self.version_label = QLabel(Qgis.version(),self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.releaseName_label)
        self.layout.addWidget(self.devVersion_label)
        self.layout.addWidget(self.geosVersion_label)
        self.layout.addWidget(self.version_label)
        self.centralwidget.setLayout(self.layout)


def main():
    a = QApplication(sys.argv)
    wm = MainWindow()
    wm.show()
    sys.exit(a.exec_())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
