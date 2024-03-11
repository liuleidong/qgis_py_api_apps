import sys
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from qgis.core import *
from qgis.gui import *

from MainWindow import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.gsMapCanvas = QgsMapCanvas(self)
        self.gsBridge = QgsLayerTreeMapCanvasBridge(QgsProject.instance().layerTreeRoot(), self.gsMapCanvas)
        # 如何建立信号槽的连接
        # self.gsBridge.canvasLayersChanged.connect(self.gsMapCanvas,QgsMapCanvas.setLayers())
        self.layout = QGridLayout()
        self.layout.addWidget(self.gsMapCanvas)
        self.centralWidget().setLayout(self.layout)
        self.actionload_project.triggered.connect(self.load_layer)
        # self.init_layer_tree()
        self.gsLayerTreeView = QgsLayerTreeView()
        self.gsLayerTreeModel = QgsLayerTreeModel(QgsProject.instance().layerTreeRoot())
        self.gsLayerTreeModel.setFlag(QgsLayerTreeModel.AllowNodeReorder)
        self.gsLayerTreeModel.setFlag(QgsLayerTreeModel.AllowNodeRename)
        self.gsLayerTreeModel.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)
        self.gsLayerTreeModel.setFlag(QgsLayerTreeModel.ShowLegendAsTree)
        self.gsLayerTreeModel.setFlag(QgsLayerTreeModel.UseEmbeddedWidgets)
        self.gsLayerTreeModel.setFlag(QgsLayerTreeModel.UseTextFormatting)
        self.gsLayerTreeModel.setAutoCollapseLegendNodes(10)
        self.gsLayerTreeView.setModel(self.gsLayerTreeModel)
        self.gsDockWidget = QgsDockWidget()
        self.gsDockWidget.setWindowTitle(r'layer tree')
        tempLayout = QVBoxLayout()
        tempLayout.addWidget(self.gsLayerTreeView)
        self.gsDockWidget.setLayout(tempLayout)
        self.addDockWidget(Qt.LeftDockWidgetArea,self.gsDockWidget)


    def load_layer(self):
        path_to_airports_layer = os.getcwd() + r'\..\python_cookbook\airports.shp'
        # The format is:
        # vlayer = QgsVectorLayer(data_source, layer_name, provider_name)
        vlayer = QgsVectorLayer(path_to_airports_layer, "Airports layer", "ogr")
        if not vlayer.isValid():
            print("Layer failed to load!")
        else:
            QgsProject.instance().addMapLayer(vlayer)


def main():
    QgsApplication.setPrefixPath('C:/OSGeo4W/apps/qgis-ltr-dev',True)
    qgs = QgsApplication([], True)
    qgs.initQgis()

    wm = MainWindow()
    wm.show()
    e = qgs.exec_()
    qgs.exitQgis()
    sys.exit(e)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
