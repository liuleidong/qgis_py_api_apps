import sys
from PyQt5.QtWidgets import *

from qgis.core import *
from qgis.gui import *

from MainWindow import Ui_MainWindow


class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.mapCanvas = QgsMapCanvas(self)
        self.layout = QGridLayout()
        self.layout.addWidget(self.mapCanvas)
        self.centralWidget().setLayout(self.layout)


def main():
    a = QApplication(sys.argv)
    wm = MainWindow()
    wm.show()
    sys.exit(a.exec_())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
