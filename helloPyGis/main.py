import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from qgis.core import Qgis


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(400, 200, 800, 600)
        self.label = QLabel(Qgis.releaseName(),self)


def main():
    a = QApplication(sys.argv)
    wm = MainWindow()
    wm.show()
    sys.exit(a.exec_())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
