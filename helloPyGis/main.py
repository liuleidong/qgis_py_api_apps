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
        self.label = QLabel(Qgis.releaseName(), self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.centralwidget.setLayout(self.layout)


def main():
    a = QApplication(sys.argv)
    wm = MainWindow()
    wm.show()
    sys.exit(a.exec_())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
