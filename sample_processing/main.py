import platform

from PyQt5.QtCore import Qt
from qgis.core import QgsApplication
from qgis.analysis import QgsNativeAlgorithms
from processing.core.Processing import Processing
from processing.algs.qgis import QgisAlgorithmProvider

from mymainwindow import MainWindow

if __name__ == '__main__':
    qgis_installation = ""
    sys = platform.system()
    if sys == "Windows":
        qgis_installation = r"C:/OSGeo4W/apps/qgis-ltr-dev"
    elif sys == "Linux":
        qgis_installation = r"/home/t/dev/cpp/apps/qgis"

    QgsApplication.setPrefixPath(qgis_installation, True)
    QgsApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QgsApplication([], True)
    app.initQgis()
    # app.processingRegistry().addProvider(QgsNativeAlgorithms())
    # app.processingRegistry().addProvider(QgisAlgorithmProvider())
    Processing.initialize()
    # app.processingRegistry().addProvider()
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()
    app.exitQgis()
